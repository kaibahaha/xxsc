from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from threading import Barrier
import multiprocessing
import pytest
from factory.agl.controller import Controller
from factory.agl.leases import SQLiteLeaseBackend
from factory.agl.registry import AgentRegistry
from factory.agl.schemas import CoreError, LeaseGrant, ProviderSession, StateTransition, TaskSpec
from conftest import Clock, SPEC, COMMIT, agent, authenticator, proposal, reconcile, spec, token


def move(c, grant, target, *, actor=0, command=None, **kw):
    task = c.snapshot()["tasks"][grant["task_id"]]
    values = dict(task_id=task["task_id"], agent_id=f"agent-{actor}", provider_id=agent(actor).provider_id,
        run_id=f"run-{actor}", spec_hash=SPEC, attempt_id=grant["attempt_id"], fencing_epoch=grant["fencing_epoch"],
        expected_version=task["version"], to_state=target, commit_sha=task["candidate_commit"], evidence_refs=("verified-ref",))
    values.update(kw)
    return c.transition(token(actor), command or target, StateTransition(**values))


def test_100_concurrent_cross_provider_claims(core):
    c, clock, registry = core
    barrier = Barrier(100)
    def race(i):
        barrier.wait(timeout=30)
        return c.claim(token(i % 3), f"race-{i}", proposal(i % 3, attempt_id=f"race-attempt-{i}"))
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(race, range(100)))
    assert sum(r["status"] == "GRANTED" for r in results) == 1
    assert len([t for t in c.snapshot()["tasks"].values() if t["lease"]]) == 1
    assert len([r for r in c.backend.records() if r["request"]["kind"] == "CLAIM"]) == 100
    assert {r["request"]["actor"]["provider_id"] for r in c.backend.records() if r["request"]["kind"] == "CLAIM"} == {"chatgpt", "workbuddy", "codex"}


def process_race(args):
    path, i = args
    c = Controller(SQLiteLeaseBackend(path), AgentRegistry([agent(j) for j in range(3)], simulation=True), authenticator, clock=Clock())
    reconcile(c, f"process-board-{i}")
    return c.claim(token(i % 3), f"process-{i}", proposal(i % 3, attempt_id=f"proc-attempt-{i}"))


def test_independent_process_connections(core):
    c, _, _ = core
    with multiprocessing.get_context("fork").Pool(12) as pool:
        results = pool.map(process_race, [(c.backend.path, i) for i in range(24)])
    assert sum(r["status"] == "GRANTED" for r in results) == 1


def test_expiry_fencing_and_late_result(core):
    c, clock, _ = core
    old = c.claim(token(), "old", proposal(ttl_seconds=10))["lease"]
    assert move(c, old, "RUNNING")["status"] == "ACCEPTED"
    clock.value += 10
    rejected = move(c, old, "SUBMITTED", commit_sha=COMMIT)
    assert rejected["error_code"] == "LATE_STALE_ATTEMPT"
    task = c.snapshot()["tasks"]["T"]
    assert task["status"] == "READY" and task["candidate_commit"] is None
    new = c.claim(token(1), "new", proposal(1, version=task["version"]))["lease"]
    assert new["fencing_epoch"] > old["fencing_epoch"]
    before = c.snapshot()["tasks"]["T"]
    assert move(c, old, "RUNNING", command="late-again")["error_code"] == "LATE_STALE_ATTEMPT"
    assert c.snapshot()["tasks"]["T"] == before
    assert move(c, new, "RUNNING", actor=1, command="new-run")["status"] == "ACCEPTED"
    assert move(c, new, "SUBMITTED", actor=1, command="new-result", commit_sha=COMMIT)["status"] == "ACCEPTED"


def test_retried_old_grant_not_reported_valid(core):
    c, clock, _ = core
    request = proposal(ttl_seconds=1)
    assert c.claim(token(), "same", request)["status"] == "GRANTED"
    clock.value += 1
    assert c.claim(token(), "same", request)["error_code"] == "LATE_STALE_ATTEMPT"


def test_claim_retry_collision(core):
    c, _, _ = core
    p = proposal()
    assert c.claim(token(), "idem", p)["lease"] == c.claim(token(), "idem", p)["lease"]
    with pytest.raises(CoreError, match="COMMAND_ID_COLLISION"): c.claim(token(), "idem", replace(p, run_id="different"))


def test_unknown_board_and_fresh_instance(core):
    c, clock, registry = core
    fresh = Controller(c.backend, registry, authenticator, clock=clock)
    assert fresh.board()["board_status"] == "UNKNOWN"
    assert fresh.claim(token(), "not-ready", proposal())["error_code"] == "BOARD_UNKNOWN"
    assert reconcile(fresh, "fresh-board")["status"] == "RECONCILED"
    assert fresh.mark_board_unknown(token(), "git-read-failed", "READ_TIMEOUT")["status"] == "BOARD_UNKNOWN"
    assert fresh.claim(token(), "blocked", proposal())["error_code"] == "BOARD_UNKNOWN"
    assert reconcile(fresh, "after-readback")["status"] == "RECONCILED"
    assert fresh.claim(token(), "can-claim", proposal())["status"] == "GRANTED"


def test_clock_regression_fails_closed(core):
    c, clock, _ = core
    clock.value -= 1
    assert c.claim(token(), "backwards", proposal())["error_code"] == "CLOCK_REGRESSION"
    assert c.snapshot()["tasks"]["T"]["lease"] is None


@pytest.mark.parametrize("change,error", [({"desired_enabled": False}, "AGENT_NOT_ADMITTED"),
    ({"admission_status": "PENDING_PROBE"}, "AGENT_NOT_ADMITTED"), ({"health": "OFFLINE"}, "AGENT_NOT_ADMITTED"),
    ({"capabilities": ()}, "CAPABILITY_DENIED"), ({"allowed_writes": ("elsewhere",)}, "PATH_DENIED")])
def test_admission_and_permissions(tmp_path, change, error):
    clock = Clock()
    members = [replace(agent(0), **change), agent(1), agent(2)]
    c = Controller(SQLiteLeaseBackend(tmp_path / "x.db"), AgentRegistry(members, simulation=True), authenticator, clock=clock)
    assert c.add_tasks(token(1), "tasks", [spec()])["status"] == "CREATED"
    assert c.reconcile_board(token(1), "board", c.board_digest())["status"] == "RECONCILED"
    assert c.claim(token(), "denied", proposal())["error_code"] == error


def test_string_identity_is_not_authentication(core):
    c, _, _ = core
    for credential in ["agent-0", "", ProviderSession(agent_id="agent-0", provider_id="chatgpt", principal="principal-0", account_scope="account-0")]:
        with pytest.raises(CoreError, match="AUTHENTICATION_FAILED"): c.claim(credential, "bad", proposal())
    assert c.claim(token(1), "spoof", proposal())["error_code"] == "AUTH_SCOPE_MISMATCH"
    c.authenticate = lambda _: ProviderSession(agent_id="agent-0", provider_id="workbuddy", principal="principal-0", account_scope="account-0")
    assert c.claim("forged", "wrong-provider", proposal())["error_code"] == "AUTH_SCOPE_MISMATCH"


def test_dag_batch_is_atomic(core):
    c, _, _ = core
    result = c.add_tasks(token(), "cycle", [spec("A", dependencies=("B",)), spec("B", dependencies=("A",))])
    assert result["error_code"] == "DAG_CYCLE"
    assert set(c.snapshot()["tasks"]) == {"T"}
    assert c.add_tasks(token(), "missing", [spec("X", dependencies=("missing",))])["error_code"] == "MISSING_DEPENDENCY"
    assert c.add_tasks(token(), "dep", [spec("D", dependencies=("T",))])["status"] == "CREATED"
    assert c.claim(token(), "dependent", proposal(task_id="D"))["error_code"] == "DEPENDENCY_NOT_DONE"


def test_queue_priority_age_and_wip(core):
    c, clock, _ = core
    assert c.add_tasks(token(), "high", [spec("H", priority=5)])["status"] == "CREATED"
    assert [t["task_id"] for t in c.ready_tasks(token())] == ["H", "T"]
    clock.value += 3600
    c.add_tasks(token(), "new", [spec("NEW", priority=10)])
    assert c.ready_tasks(token())[0]["task_id"] == "H"
    assert c.claim(token(), "primary", proposal())["status"] == "GRANTED"
    assert c.claim(token(), "second", proposal(task_id="H"))["error_code"] == "WIP_LIMIT"


def test_provider_offline_revokes_and_transfers(core):
    c, _, _ = core
    old = c.claim(token(), "first", proposal())["lease"]
    assert c.update_health(token(1), "offline", "agent-0", health="OFFLINE", admission_status="DRAINING")["status"] == "UPDATED"
    task = c.snapshot()["tasks"]["T"]
    assert task["lease"] is None and task["fencing_epoch"] > old["fencing_epoch"]
    assert c.claim(token(1), "takeover", proposal(1, version=task["version"]))["status"] == "GRANTED"
    assert move(c, old, "RUNNING")["error_code"] == "LATE_STALE_ATTEMPT"


def test_renew_and_non_owner(core):
    c, clock, _ = core
    grant = c.claim(token(), "claim", proposal(ttl_seconds=10))["lease"]
    clock.value += 5
    assert c.renew(token(1), "steal", LeaseGrant.from_dict(grant))["error_code"] == "AUTH_SCOPE_MISMATCH"
    result = c.renew(token(), "renew", LeaseGrant.from_dict(grant), 20)
    assert result["lease"]["expires_at"] == clock.value + 20
    clock.value += 20
    assert c.renew(token(), "expired-renew", LeaseGrant.from_dict(grant))["error_code"] == "LATE_STALE_ATTEMPT"


def test_illegal_transition_audited(core):
    c, _, _ = core
    grant = c.claim(token(), "claim", proposal())["lease"]
    assert move(c, grant, "DONE")["error_code"] == "ILLEGAL_TRANSITION"
    assert c.backend.records()[-1]["result"]["error_code"] == "ILLEGAL_TRANSITION"


def test_mock_is_not_production_authority(tmp_path):
    c = Controller(SQLiteLeaseBackend(tmp_path / "prod.db"), AgentRegistry([agent(0), agent(1)]), authenticator, clock=Clock())
    assert c.add_tasks(token(), "no-mock-admin", [spec()])["error_code"] == "ACTION_DENIED"


def test_registration_is_durable_and_identity_bound(core):
    c, clock, registry = core
    assert c.register_agent(token(), "join", agent(20))["status"] == "REGISTERED"
    fresh = Controller(c.backend, registry, authenticator, clock=clock)
    assert "agent-20" in fresh.snapshot()["agents"]
    assert reconcile(fresh, "after-join")["status"] == "RECONCILED"
    assert fresh.claim(token(20), "custom-provider", proposal(20))["status"] == "GRANTED"


def test_version_spec_scope_and_lease_owner(core):
    c, _, _ = core
    assert c.claim(token(), "bad-version", proposal(version=2))["error_code"] == "VERSION_CONFLICT"
    assert c.claim(token(), "bad-spec", proposal(spec_hash="c" * 64))["error_code"] == "SPEC_MISMATCH"
    grant = c.claim(token(), "grant", proposal())["lease"]
    assert move(c, grant, "RUNNING", actor=1)["error_code"] == "LEASE_OWNER_REQUIRED"
    assert c.add_tasks(token(), "restricted", [spec("restricted", allowed_agents=("agent-1",))])["status"] == "CREATED"
    assert c.claim(token(), "not-allowed", proposal(task_id="restricted"))["error_code"] == "TASK_AGENT_DENIED"


def test_board_compare_and_swap_conflict(core):
    c, _, _ = core
    old_digest = c.board_digest()
    c.add_tasks(token(), "new", [spec("NEW")])
    assert c.reconcile_board(token(), "stale-board", old_digest)["error_code"] == "BOARD_CONFLICT"


@pytest.mark.parametrize("ttl", [0, -1, float("inf"), float("nan"), 3601])
def test_invalid_lease_duration(ttl):
    with pytest.raises(CoreError, match="INVALID_TTL"): proposal(ttl_seconds=ttl)


def test_dynamic_registration_preserves_provider_quota(tmp_path):
    quota = {"provider_id": "chatgpt", "account_scope": "account-0", "capacity_verified": True, "capacity": 1}
    registry = AgentRegistry([agent(0), agent(1)], simulation=True, quotas=[quota])
    c = Controller(SQLiteLeaseBackend(tmp_path / "quota.sqlite"), registry, authenticator, clock=Clock())
    assert c.register_agent(token(), "over-quota", agent(3))["error_code"] == "PROVIDER_QUOTA_EXCEEDED"
    assert "agent-3" not in c.snapshot()["agents"]
    assert c.register_agent(token(), "other-provider", agent(2))["status"] == "REGISTERED"


def test_expired_renewal_retry_is_not_current_authority(core):
    c, clock, _ = core
    grant = c.claim(token(), "claim", proposal(ttl_seconds=1))["lease"]
    assert c.renew(token(), "same-renew", LeaseGrant.from_dict(grant), 2)["status"] == "RENEWED"
    clock.value += 2
    assert c.renew(token(), "same-renew", LeaseGrant.from_dict(grant), 2)["error_code"] == "LATE_STALE_ATTEMPT"


def test_task_read_scope_is_enforced(core):
    c, _, _ = core
    assert c.add_tasks(token(), "sensitive", [spec("sensitive", read_paths=("private/other",))])["status"] == "CREATED"
    assert c.claim(token(), "cannot-read", proposal(task_id="sensitive"))["error_code"] == "READ_PATH_DENIED"


def test_cached_grant_cannot_bypass_clock_fence(core):
    c, clock, _ = core
    p = proposal()
    assert c.claim(token(), "cached", p)["status"] == "GRANTED"
    clock.value -= 1
    assert c.claim(token(), "cached", p)["error_code"] == "CLOCK_REGRESSION"


def test_missing_idempotency_key_rejected(core):
    c, _, _ = core
    with pytest.raises(CoreError, match="MISSING_IDEMPOTENCY_KEY"):
        c.claim(token(), "", proposal())
