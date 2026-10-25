"""P1-02 regressions: configuration reload is not a second bootstrap."""
from copy import deepcopy
from factory.agl.controller import Controller
from factory.agl.leases import SQLiteLeaseBackend
from factory.agl.registry import AgentRegistry
from factory.agl.schemas import Handoff
from conftest import Clock, SPEC, agent, authenticator, proposal, reconcile, spec, token
from test_events_recovery import ack, event, process


def pool(n, **kw):
    return AgentRegistry([agent(i) for i in range(n)], simulation=True, **kw)


def seed(c):
    assert c.add_tasks(token(), "seed-task", [spec()])["status"] == "CREATED"
    assert reconcile(c, "seed-board")["status"] == "RECONCILED"
    grant = c.claim(token(), "seed-claim", proposal())["lease"]
    e = event(targets=("agent-1",))
    assert c.publish(token(), "seed-event", e)["status"] == "PUBLISHED"
    process(c, e, key="seed-process")
    assert ack(c, e, key="seed-ack")["status"] == "ACK_RECORDED"
    h = Handoff(handoff_id="seed-H", task_id="T", agent_id="agent-0", provider_id=agent(0).provider_id,
        run_id="seed-run", spec_hash=SPEC, attempt_id=grant["attempt_id"], fencing_epoch=grant["fencing_epoch"],
        commit_sha=None, decision_log=("keep history",), open_issues=(), next_action="continue", evidence_refs=("seed://evidence",))
    assert c.save_handoff(token(), "seed-handoff", h)["status"] == "STORED"


def test_p102_two_to_six_new_config_restart_preserves_all_history(tmp_path):
    clock = Clock()
    c = Controller(SQLiteLeaseBackend(tmp_path / "2to6.sqlite"), pool(2), authenticator, clock=clock)
    seed(c)
    for i in range(2, 6):
        assert c.register_agent(token(), f"join-{i}", agent(i))["status"] == "REGISTERED"
    before, records = deepcopy(c.snapshot()), c.backend.records()
    fresh = Controller(c.backend, pool(6), authenticator, clock=clock)
    assert fresh.snapshot() == before
    assert fresh.backend.records() == records
    assert len(fresh.snapshot()["agents"]) == 6
    assert len(before["tasks"]) == len(before["events"]) == len(before["acks"]) == len(before["handoffs"]) == 1


def test_p102_six_to_ten_new_config_restart_preserves_all_history(tmp_path):
    clock = Clock()
    c = Controller(SQLiteLeaseBackend(tmp_path / "6to10.sqlite"), pool(6), authenticator, clock=clock)
    seed(c)
    for i in range(6, 10):
        assert c.register_agent(token(), f"join-{i}", agent(i))["status"] == "REGISTERED"
    before, records = deepcopy(c.snapshot()), c.backend.records()
    fresh = Controller(c.backend, pool(10), authenticator, clock=clock)
    assert fresh.snapshot() == before
    assert fresh.backend.records() == records
    assert len(fresh.snapshot()["agents"]) == 10


def test_versioned_bulk_growth_two_six_ten_and_idempotency(tmp_path):
    c = Controller(SQLiteLeaseBackend(tmp_path / "bulk.sqlite"), pool(2), authenticator, clock=Clock())
    seed(c)
    for n, expected in [(6, 1), (10, 2)]:
        records_before = c.backend.records()
        result = c.apply_registry(token(), f"config-{n}", [agent(i) for i in range(n)], expected_version=expected)
        assert result == {"status": "REGISTRY_UPDATED", "registry_version": expected + 1}
        snapshot = deepcopy(c.snapshot())
        replay = c.apply_registry(token(), f"config-{n}", [agent(i) for i in range(n)], expected_version=expected)
        assert replay == result and c.snapshot() == snapshot
        before_restart = c.backend.records()
        c = Controller(c.backend, pool(n), authenticator, clock=c.clock)
        assert c.snapshot() == snapshot and c.backend.records() == before_restart
        assert c.backend.records()[:len(records_before)] == records_before
    assert len(c.snapshot()["agents"]) == 10
    assert c.apply_registry(token(), "stale-config", [agent(10)], expected_version=1)["error_code"] == "REGISTRY_VERSION_CONFLICT"
    assert "agent-10" not in c.snapshot()["agents"]


def test_startup_config_does_not_authorize_or_overwrite(tmp_path):
    c = Controller(SQLiteLeaseBackend(tmp_path / "intent.sqlite"), pool(2), authenticator, clock=Clock())
    before, records = c.snapshot(), c.backend.records()
    fresh = Controller(c.backend, pool(10), authenticator, clock=c.clock)
    assert fresh.snapshot() == before and fresh.backend.records() == records
    assert fresh.claim(token(9), "not-admitted-from-config", proposal(9))["error_code"] == "UNKNOWN_AGENT"


def test_duplicate_identity_disable_restore_are_versioned_and_audited(tmp_path):
    from dataclasses import replace
    c = Controller(SQLiteLeaseBackend(tmp_path / "lifecycle.sqlite"), pool(6), authenticator, clock=Clock())
    seed(c)
    assert c.register_agent(token(), "duplicate", agent(1))["status"] == "DUPLICATE"
    assert len(c.snapshot()["agents"]) == 6 and c.registry_version() == 1
    disabled = replace(agent(1), desired_enabled=False, admission_status="UNAVAILABLE", health="OFFLINE")
    assert c.apply_registry(token(), "disable", [disabled], expected_version=1)["registry_version"] == 2
    c.add_tasks(token(), "other-task", [spec("OTHER")])
    assert c.claim(token(1), "disabled-claim", proposal(1, task_id="OTHER"))["error_code"] == "AGENT_NOT_ADMITTED"
    assert c.apply_registry(token(), "bad-restore-version", [agent(1)], expected_version=1)["error_code"] == "REGISTRY_VERSION_CONFLICT"
    assert c.apply_registry(token(), "restore", [agent(1)], expected_version=2)["registry_version"] == 3
    assert c.claim(token(1), "restored-claim", proposal(1, task_id="OTHER"))["status"] == "GRANTED"
    for key in ("events", "acks", "handoffs"):
        assert len(c.snapshot()[key]) == 1
    assert len(c.snapshot()["agents"]) == 6
    edits = [r for r in c.backend.records() if r["request"]["kind"] == "APPLY_REGISTRY"]
    assert [r["result"]["status"] for r in edits] == ["REGISTRY_UPDATED", "REJECTED", "REGISTRY_UPDATED"]


def test_provider_quotas_and_failed_edits_preserve_history(tmp_path):
    policies = [{"provider_id": p, "account_scope": f"account-{i}", "capacity_verified": True, "capacity": capacity}
                for i, (p, capacity) in enumerate([("chatgpt", 1), ("workbuddy", 4), ("codex", 4)])]
    c = Controller(SQLiteLeaseBackend(tmp_path / "quotas.sqlite"), pool(2, quotas=policies), authenticator, clock=Clock())
    seed(c)
    assert c.apply_registry(token(), "other-providers", [agent(2), agent(4), agent(7)], expected_version=1)["status"] == "REGISTRY_UPDATED"
    before = deepcopy(c.snapshot())
    assert c.apply_registry(token(), "chatgpt-full", [agent(3)], expected_version=2)["error_code"] == "PROVIDER_QUOTA_EXCEEDED"
    assert c.snapshot() == before
    lowered = deepcopy(policies)
    lowered[1]["capacity"] = 1
    assert c.apply_registry(token(), "quota-reduction", [], expected_version=2, quotas=lowered)["error_code"] == "PROVIDER_QUOTA_EXCEEDED"
    assert c.snapshot() == before


def test_registry_edit_requires_authority_and_cannot_rebind_principal(tmp_path):
    from dataclasses import replace
    members = [agent(0), replace(agent(1), allowed_actions=())]
    c = Controller(SQLiteLeaseBackend(tmp_path / "auth.sqlite"), AgentRegistry(members, simulation=True), authenticator, clock=Clock())
    assert c.apply_registry(token(1), "not-admin", [agent(2)], expected_version=1)["error_code"] == "ACTION_DENIED"
    assert c.apply_registry(token(), "principal-rebind", [replace(agent(1), credential_principal="forged")], expected_version=1)["error_code"] == "IDENTITY_CHANGE_REQUIRES_NEW_AGENT"
    assert len(c.snapshot()["agents"]) == 2 and c.registry_version() == 1


def test_registry_edit_cas_concurrency(tmp_path):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier
    c = Controller(SQLiteLeaseBackend(tmp_path / "cas.sqlite"), pool(2), authenticator, clock=Clock())
    barrier = Barrier(2)
    def edit(i):
        barrier.wait()
        return c.apply_registry(token(), f"race-{i}", [agent(i)], expected_version=1)
    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(edit, [2, 3]))
    assert sum(r["status"] == "REGISTRY_UPDATED" for r in results) == 1
    assert sum(r.get("error_code") == "REGISTRY_VERSION_CONFLICT" for r in results) == 1
    assert len(c.snapshot()["agents"]) == 3 and c.registry_version() == 2


def test_restart_cannot_change_persisted_simulation_mode(tmp_path):
    import pytest
    from factory.agl.schemas import CoreError
    c = Controller(SQLiteLeaseBackend(tmp_path / "mode.sqlite"), pool(2), authenticator, clock=Clock())
    before = c.backend.records()
    with pytest.raises(CoreError, match="SIMULATION_MODE_MISMATCH"):
        Controller(c.backend, AgentRegistry([agent(0), agent(1)], simulation=False), authenticator, clock=c.clock)
    assert c.backend.records() == before


def test_noop_registration_keeps_version_and_rejects_duplicate_ids(tmp_path):
    c = Controller(SQLiteLeaseBackend(tmp_path / "noop.sqlite"), pool(2), authenticator, clock=Clock())
    assert c.apply_registry(token(), "same-registry", [agent(0), agent(1)], expected_version=1) == {
        "status": "REGISTRY_UNCHANGED", "registry_version": 1}
    assert c.apply_registry(token(), "duplicate-ids", [agent(2), agent(2)], expected_version=1)["error_code"] == "DUPLICATE_AGENT"
    assert c.registry_version() == 1 and len(c.snapshot()["agents"]) == 2


def test_disable_restore_never_resurrects_a_previous_lease(tmp_path):
    from dataclasses import replace
    from test_controller_leases import move
    c = Controller(SQLiteLeaseBackend(tmp_path / "fence.sqlite"), pool(3), authenticator, clock=Clock())
    seed(c)
    c.add_tasks(token(), "second-task", [spec("SECOND")])
    old = c.claim(token(1), "second-claim", proposal(1, task_id="SECOND"))["lease"]
    disabled = replace(agent(1), desired_enabled=False, admission_status="UNAVAILABLE", health="OFFLINE")
    c.apply_registry(token(), "disable-owner", [disabled], expected_version=1)
    c.apply_registry(token(), "restore-owner", [agent(1)], expected_version=2)
    task = c.snapshot()["tasks"]["SECOND"]
    fresh = c.claim(token(1), "reclaim", proposal(1, task_id="SECOND", version=task["version"]))["lease"]
    assert fresh["fencing_epoch"] > old["fencing_epoch"]
    assert move(c, old, "RUNNING", actor=1, command="late-old-owner")["error_code"] == "LATE_STALE_ATTEMPT"
