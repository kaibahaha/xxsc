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
