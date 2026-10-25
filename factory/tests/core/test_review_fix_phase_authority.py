"""P1-01 regressions: elapsed wall time cannot revoke accepted business facts."""
from copy import deepcopy
import pytest
from factory.agl.controller import Controller
from factory.agl.leases import SQLiteLeaseBackend
from factory.agl.replay import rebuild
from factory.agl.schemas import StateTransition
from conftest import COMMIT, SPEC, agent, authenticator, proposal, reconcile, token
from test_controller_leases import move
from test_memory_handoff_qa import evidence, prepare_qa


def stage_claim(c, actor, key):
    task = c.snapshot()["tasks"]["T"]
    return c.claim(token(actor), key, proposal(actor, version=task["version"],
        attempt_id=key, commit_sha=task["candidate_commit"], ttl_seconds=300))


def raw_move(c, grant, target, actor, key, **kw):
    task = c.snapshot()["tasks"]["T"]
    values = dict(task_id="T", agent_id=f"agent-{actor}", provider_id=agent(actor).provider_id,
        run_id=f"run-{actor}", spec_hash=SPEC, attempt_id=grant["attempt_id"],
        fencing_epoch=grant["fencing_epoch"], expected_version=task["version"],
        to_state=target, commit_sha=COMMIT, evidence_refs=("phase://evidence",))
    values.update(kw)
    return c.transition(token(actor), key, StateTransition(**values))


def test_p101_submitted_candidate_survives_hour_and_qa_takeover(core, tmp_path):
    c, clock, _ = core
    prepare_qa(c)
    clock.value += 3601
    c.recover(token(), "one-hour")
    task = c.snapshot()["tasks"]["T"]
    assert task["status"] == "QA_PENDING"
    assert task["candidate_commit"] == COMMIT
    grant = stage_claim(c, 1, "B-qa")
    assert grant["status"] == "GRANTED"
    e, c.evidence_verifier = evidence(tmp_path)
    assert raw_move(c, grant["lease"], "QA_GREEN", 1, "B-result", evidence=e.to_dict())["status"] == "ACCEPTED"


def test_p101_qa_green_survives_two_hours_and_review_takeover(core, tmp_path):
    c, clock, _ = core
    grant = prepare_qa(c)
    e, c.evidence_verifier = evidence(tmp_path)
    assert move(c, grant, "QA_GREEN", actor=1, evidence=e.to_dict())["status"] == "ACCEPTED"
    expected = deepcopy(c.snapshot()["tasks"]["T"]["qa_evidence"])
    clock.value += 7200
    c.recover(token(), "two-hours")
    task = c.snapshot()["tasks"]["T"]
    assert task["status"] == "QA_GREEN"
    assert task["qa_evidence"] == expected
    review = stage_claim(c, 2, "C-review")
    assert review["status"] == "GRANTED"
    assert raw_move(c, review["lease"], "REVIEW_APPROVED", 2, "review-result")["status"] == "ACCEPTED"


def test_p101_expired_original_epoch_rejected_without_losing_candidate(core):
    c, clock, _ = core
    original = prepare_qa(c)
    clock.value += 3601
    result = raw_move(c, original, "QA_GREEN", 0, "late-original")
    assert result["error_code"] == "LATE_STALE_ATTEMPT"
    task = c.snapshot()["tasks"]["T"]
    assert task["status"] == "QA_PENDING" and task["candidate_commit"] == COMMIT


def test_p101_restart_replay_and_author_offline_preserve_qa(core, tmp_path):
    c, clock, registry = core
    grant = prepare_qa(c)
    e, c.evidence_verifier = evidence(tmp_path)
    assert move(c, grant, "QA_GREEN", actor=1, evidence=e.to_dict())["status"] == "ACCEPTED"
    clock.value += 7200
    c.update_health(token(2), "author-offline", "agent-0", health="OFFLINE", admission_status="DRAINING")
    fresh = Controller(c.backend, registry, authenticator, clock=clock)
    state = fresh.snapshot()
    assert state == rebuild(c.backend.records())
    assert state["tasks"]["T"]["status"] == "QA_GREEN"
    assert state["tasks"]["T"]["qa_evidence"] == e.to_dict()
    restored = SQLiteLeaseBackend.restore(tmp_path / "replayed.sqlite", c.backend.records(),
        expected_head_hash=c.backend.records()[-1]["record_hash"])
    assert restored.snapshot() == state


@pytest.mark.parametrize("phase,actor", [("SUBMITTED", 0), ("QA_PENDING", 1), ("QA_GREEN", 2),
                                         ("REVIEW_APPROVED", 2), ("INTEGRATION_VERIFIED", 2)])
def test_phase_lease_expiry_preserves_each_confirmed_phase(core, tmp_path, phase, actor):
    c, clock, _ = core
    if phase == "SUBMITTED":
        grant = c.claim(token(), "execute", proposal())["lease"]
        move(c, grant, "RUNNING")
        move(c, grant, "SUBMITTED", commit_sha=COMMIT)
    else:
        grant = prepare_qa(c)
        if phase != "QA_PENDING":
            e, c.evidence_verifier = evidence(tmp_path)
            move(c, grant, "QA_GREEN", actor=1, evidence=e.to_dict())
            if phase in {"REVIEW_APPROVED", "INTEGRATION_VERIFIED"}:
                move(c, grant, "REVIEW_APPROVED", actor=2)
            if phase == "INTEGRATION_VERIFIED":
                move(c, grant, "INTEGRATION_VERIFIED", actor=2)
    confirmed = c.snapshot()["tasks"]["T"]
    assert confirmed["status"] == phase and confirmed["lease"] is None
    result = stage_claim(c, actor, "phase-grant")
    assert result["status"] == "GRANTED"
    old = result["lease"]
    clock.value += 3601
    c.recover(token(), "phase-expired")
    current = c.snapshot()["tasks"]["T"]
    for field in ("status", "candidate_commit", "qa_evidence", "author"):
        assert current[field] == confirmed[field]
    assert current["lease"] is None and current["fencing_epoch"] > old["fencing_epoch"]
    assert stage_claim(c, actor, "new-phase-grant")["status"] == "GRANTED"
    target = {"SUBMITTED": "QA_PENDING", "QA_PENDING": "QA_GREEN", "QA_GREEN": "REVIEW_APPROVED",
              "REVIEW_APPROVED": "INTEGRATION_VERIFIED", "INTEGRATION_VERIFIED": "DONE"}[phase]
    assert raw_move(c, old, target, actor, "old-phase-result")["error_code"] == "LATE_STALE_ATTEMPT"


def test_stage_token_is_owned_and_candidate_bound(core):
    c, _, _ = core
    prepare_qa(c)
    task = c.snapshot()["tasks"]["T"]
    wrong = proposal(1, version=task["version"], commit_sha="c" * 40)
    assert c.claim(token(1), "wrong-candidate", wrong)["error_code"] == "STALE_COMMIT"
    grant = stage_claim(c, 1, "qa-owner")["lease"]
    assert raw_move(c, grant, "QA_GREEN", 2, "borrowed-token")["error_code"] == "LEASE_OWNER_REQUIRED"
    assert raw_move(c, grant, "QA_GREEN", 1, "changed-commit", commit_sha="c" * 40)["error_code"] == "STALE_COMMIT"
    assert c.snapshot()["tasks"]["T"]["status"] == "QA_PENDING"


def test_phase_claim_requires_admission_role_and_read_permission(core):
    from dataclasses import replace
    c, _, _ = core
    prepare_qa(c)
    # Test uses explicit authorized edits; every permission change also revokes old authority.
    for key, changes, expected in [
        ("no-role", {"allowed_actions": ()}, "ACTION_DENIED"),
        ("no-read", {"allowed_reads": ()}, "READ_PATH_DENIED"),
        ("offline", {"health": "OFFLINE", "admission_status": "DRAINING"}, "ACTION_DENIED"),
    ]:
        record = replace(agent(1), **changes)
        assert c.apply_registry(token(), key, [record], expected_version=c.registry_version())["status"] == "REGISTRY_UPDATED"
        if key == "no-read":
            # A separate task-level read restriction is required for this assertion.
            # Controlled fixture injection models an authorized imported task scope.
            c.backend.transact("test-read-scope", {"kind": "TEST_SCOPE"}, c.clock(),
                lambda s: (s["tasks"]["T"].update(read_paths=["factory/candidate"]) or {"status": "FIXTURE"}))
        assert stage_claim(c, 1, key + "-claim")["error_code"] == expected


def test_reader_without_developer_write_scope_can_get_qa_authority(core):
    from dataclasses import replace
    c, _, _ = core
    prepare_qa(c)
    reader = replace(agent(1), capabilities=("test",), allowed_writes=(), allowed_actions=("qa",))
    c.apply_registry(token(), "read-only-runner", [reader], expected_version=c.registry_version())
    grant = stage_claim(c, 1, "reader-qa")["lease"]
    assert raw_move(c, grant, "SUBMITTED", 1, "cannot-develop")["error_code"] == "ILLEGAL_TRANSITION"


def test_legacy_waiting_lease_recovery_does_not_erase_evidence(core, tmp_path):
    c, _, _ = core
    original = prepare_qa(c)
    e, c.evidence_verifier = evidence(tmp_path)
    move(c, original, "QA_GREEN", actor=1, evidence=e.to_dict())
    def legacy_layout(state):
        task = state["tasks"]["T"]
        task["lease"] = dict(original, expires_at=c.clock() + 100)
        task.pop("lease_phase", None)
        return {"status": "LEGACY_FIXTURE"}
    c.backend.transact("legacy-layout", {"kind": "LEGACY_LAYOUT_FIXTURE"}, c.clock(), legacy_layout)
    # Retire pre-fix developer authority immediately, even before its deadline.
    c.recover(token(), "legacy-upgrade")
    task = c.snapshot()["tasks"]["T"]
    assert task["status"] == "QA_GREEN" and task["qa_evidence"] == e.to_dict() and task["lease"] is None
    assert stage_claim(c, 2, "review-after-upgrade")["status"] == "GRANTED"


def test_one_hundred_concurrent_phase_claims_have_one_authority(core):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier
    c, _, _ = core
    prepare_qa(c)
    version = c.snapshot()["tasks"]["T"]["version"]
    barrier = Barrier(100)
    def race(i):
        actor = 1 + i % 2
        request = proposal(actor, version=version, commit_sha=COMMIT, attempt_id=f"qa-race-{i}")
        barrier.wait(timeout=30)
        return c.claim(token(actor), f"qa-race-{i}", request)
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(race, range(100)))
    assert sum(r["status"] == "GRANTED" for r in results) == 1
    assert c.snapshot()["tasks"]["T"]["status"] == "QA_PENDING"


def test_replaying_accepted_command_cannot_roll_back_later_review(core, tmp_path):
    c, clock, _ = core
    prepare_qa(c)
    e, c.evidence_verifier = evidence(tmp_path)
    qa = stage_claim(c, 1, "qa-stage")["lease"]
    accepted = raw_move(c, qa, "QA_GREEN", 1, "qa-result", evidence=e.to_dict())
    record = c.backend.records()[-1]
    clock.value += 7200
    c.recover(token(), "later-hour")
    review = stage_claim(c, 2, "review-stage")["lease"]
    assert raw_move(c, review, "REVIEW_APPROVED", 2, "review-result")["status"] == "ACCEPTED"
    before, records = c.snapshot(), c.backend.records()
    # Retrying a prior committed request yields its historical receipt, without reapplying it.
    replay = c.transition(token(1), "qa-result", StateTransition.from_dict(record["request"]["payload"]))
    assert replay == accepted
    assert c.snapshot() == before and c.backend.records() == records
    assert c.snapshot()["tasks"]["T"]["status"] == "REVIEW_APPROVED"
