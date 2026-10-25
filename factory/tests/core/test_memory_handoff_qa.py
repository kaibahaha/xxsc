from dataclasses import replace
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import pytest
from factory.agl.context import build_context
from factory.agl.controller import Controller
from factory.agl.handoff import resume
from factory.agl.memory import knowledge
from factory.agl.schemas import ArtifactEvidence, Handoff, MemoryNote
from conftest import COMMIT, SPEC, authenticator, proposal, reconcile, token
from test_controller_leases import move


def note(i, kind="FACT", **kw):
    values = dict(note_id=f"N{i}", type=kind, task_id="T", agent_id="agent-0", provider_id="chatgpt",
        run_id="run-0", spec_hash=SPEC, commit_sha=COMMIT, summary=f"finding-{i}", evidence_refs=(f"log://{i}",), test_id="test-core")
    values.update(kw)
    return MemoryNote(**values)


def test_typed_knowledge_exact_fail_scope_and_cold_history(core):
    c, clock, _ = core
    c.put_note(token(), "patch", note(0, "PATCH_SUMMARY", summary="passed"))
    c.put_note(token(), "other-patch", note(1, "PATCH_SUMMARY", commit_sha="c" * 40))
    c.put_note(token(), "failure", note(2, "FAIL"))
    c.put_note(token(), "claim-note", note(3, "CLAIM", expires_at=clock() + 1))
    for i in range(4, 40): c.put_note(token(), f"note-{i}", note(i))
    clock.value += 2
    result = knowledge(c.snapshot(), "T", SPEC, COMMIT, now=clock(), hot_limit=3)
    assert len(result["hot"]) == 3 and len(result["cold_note_ids"]) == 40
    assert all(n["type"] != "CLAIM" for n in result["warm"])
    all_hot = knowledge(c.snapshot(), "T", SPEC, COMMIT, now=clock(), hot_limit=100)["hot"]
    assert next(n for n in all_hot if n["note_id"] == "N0")["candidate_status"] == "RECHECK_REQUIRED"
    other = knowledge(c.snapshot(), "T", SPEC, "c" * 40, now=clock(), hot_limit=100)["hot"]
    assert next(n for n in other if n["note_id"] == "N1")["candidate_status"] == "PROPOSED"
    assert c.snapshot()["tasks"]["T"]["status"] == "READY"


def test_handoff_cold_start_and_expired_authority(core):
    c, clock, registry = core
    grant = c.claim(token(), "claim", proposal(ttl_seconds=3600))["lease"]
    handoff = Handoff(handoff_id="H1", task_id="T", agent_id="agent-0", provider_id="chatgpt", run_id="run-0",
        spec_hash=SPEC, attempt_id=grant["attempt_id"], fencing_epoch=grant["fencing_epoch"], commit_sha=COMMIT,
        decision_log=("keep original evidence",), open_issues=("test pending",), next_action="run tests", evidence_refs=("log://handoff",))
    assert c.save_handoff(token(), "handoff", handoff)["status"] == "STORED"
    fresh = Controller(c.backend, registry, authenticator, clock=clock)
    assert resume(fresh.snapshot(), "agent-0", "T", now=clock())["action"] == "CONTINUE"
    clock.value += 7200
    ctx = build_context(fresh.snapshot(), "agent-0", "T", now=clock())
    assert ctx["HOT"]["continuation"] == "READ_ONLY_RECLAIM_REQUIRED"
    assert ctx["WARM"]["handoff"]["next_action"] == "run tests"
    assert c.save_handoff(token(), "late-history", replace(handoff, handoff_id="H2", next_action="reclaim"))["status"] == "STORED"
    assert c.snapshot()["tasks"]["T"]["status"] == "READY"


def prepare_qa(c):
    grant = c.claim(token(), "claim", proposal())["lease"]
    assert move(c, grant, "RUNNING")["status"] == "ACCEPTED"
    assert move(c, grant, "SUBMITTED", commit_sha=COMMIT)["status"] == "ACCEPTED"
    assert move(c, grant, "QA_PENDING")["status"] == "ACCEPTED"
    return grant


def test_no_runner_no_qa_green(core):
    c, _, _ = core
    grant = prepare_qa(c)
    assert move(c, grant, "QA_GREEN", actor=1)["error_code"] == "BLOCKED_EXECUTOR"
    assert move(c, grant, "QA_GREEN", actor=0, command="self-qa")["error_code"] == "INDEPENDENCE_REQUIRED"
    assert c.snapshot()["tasks"]["T"]["status"] == "QA_PENDING"


def evidence(tmp_path):
    # Actual local subprocess, with captured stdout/stderr. Provider identities are simulations.
    proc = subprocess.run([sys.executable, "-c", "assert 2 + 2 == 4; print('1 assertion passed')"], capture_output=True)
    out, err = tmp_path / "stdout.txt", tmp_path / "stderr.txt"
    out.write_bytes(proc.stdout)
    err.write_bytes(proc.stderr)
    e = ArtifactEvidence(evidence_id="LOCAL-RUNTIME-1", task_id="T", spec_hash=SPEC, commit_sha=COMMIT,
        runner_agent_id="agent-1", environment_id="pytest-local-subprocess", command="python -c assertion",
        exit_code=proc.returncode, stdout_sha256=hashlib.sha256(proc.stdout).hexdigest(),
        stderr_sha256=hashlib.sha256(proc.stderr).hexdigest(), evidence_refs=(str(out), str(err)), test_summary="1 real assertion")
    attested = e.to_dict()
    def verifier(candidate):
        return (candidate.to_dict() == attested and hashlib.sha256(out.read_bytes()).hexdigest() == candidate.stdout_sha256
                and hashlib.sha256(err.read_bytes()).hexdigest() == candidate.stderr_sha256)
    return e, verifier


@pytest.mark.parametrize("invalid", ["wrong-sha", "failed", "hash-corrupt", "wrong-runner", "no-verifier"])
def test_qa_requires_exact_verified_runtime(core, tmp_path, invalid):
    c, _, _ = core
    grant = prepare_qa(c)
    e, verify = evidence(tmp_path)
    c.evidence_verifier = verify
    if invalid == "wrong-sha": e = replace(e, commit_sha="c" * 40)
    if invalid == "failed": e = replace(e, exit_code=1)
    if invalid == "hash-corrupt": Path(e.evidence_refs[0]).write_text("forged")
    if invalid == "wrong-runner": e = replace(e, runner_agent_id="agent-2")
    if invalid == "no-verifier": c.evidence_verifier = None
    assert move(c, grant, "QA_GREEN", actor=1, evidence=e.to_dict())["status"] == "REJECTED"
    assert c.snapshot()["tasks"]["T"]["status"] == "QA_PENDING"


def test_runtime_evidence_gate_and_approval_chain(core, tmp_path):
    c, _, _ = core
    grant = prepare_qa(c)
    e, verify = evidence(tmp_path)
    c.evidence_verifier = verify
    # This tests the simulated state machine. It is not independent QA of this delivery.
    assert move(c, grant, "QA_GREEN", actor=1, evidence=e.to_dict())["status"] == "ACCEPTED"
    assert move(c, grant, "DONE", actor=2, command="premature-done")["error_code"] == "ILLEGAL_TRANSITION"
    for target in ("REVIEW_APPROVED", "INTEGRATION_VERIFIED", "DONE"):
        assert move(c, grant, target, actor=2)["status"] == "ACCEPTED"
    assert c.snapshot()["tasks"]["T"]["lease"] is None
    assert c.snapshot()["tasks"]["T"]["status"] == "DONE"


def test_new_fail_blocks_only_same_candidate_acceptance(core, tmp_path):
    c, _, _ = core
    grant = prepare_qa(c)
    e, verify = evidence(tmp_path)
    c.evidence_verifier = verify
    assert move(c, grant, "QA_GREEN", actor=1, evidence=e.to_dict())["status"] == "ACCEPTED"
    assert c.put_note(token(), "other-fail", note(1, "FAIL", commit_sha="c" * 40))["status"] == "STORED"
    assert move(c, grant, "REVIEW_APPROVED", actor=2)["status"] == "ACCEPTED"
    assert c.put_note(token(), "matching-fail", note(2, "FAIL"))["status"] == "STORED"
    assert move(c, grant, "INTEGRATION_VERIFIED", actor=2)["error_code"] == "CANDIDATE_RECHECK_REQUIRED"
