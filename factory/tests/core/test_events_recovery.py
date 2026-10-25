from copy import deepcopy
from dataclasses import replace
import json
import random
import sqlite3
import pytest
from factory.agl.audit import audit, relay_eligibility
from factory.agl.controller import Controller
from factory.agl.events import pending_deliveries
from factory.agl.leases import SQLiteLeaseBackend
from factory.agl.replay import board_projection, rebuild
from factory.agl.schemas import Ack, CoreError, Event, digest
from conftest import SPEC, authenticator, proposal, reconcile, token


def event(i="E", targets=("agent-1", "agent-2"), **kw):
    values = dict(event_id=i, producer="agent-0", provider_id="chatgpt", target_agents=targets,
        task_id="T", kind="FACT_PUBLISHED", summary="observed fact", observed_at="2026-10-25T00:00:00Z",
        raw_ref="repo@commit:outbox/fact", run_id="run-0", spec_hash=SPEC)
    values.update(kw)
    return Event(**values)


def ack(c, e, i=1, key="ack"):
    return c.ack(token(i), key, Ack(event_id=e.event_id, agent_id=f"agent-{i}", provider_id=("chatgpt", "workbuddy", "codex")[i % 3],
        run_id=f"run-{i}", event_sha256=digest(e), evidence_refs=("sink://" + e.event_id,)))


def process(c, e, i=1, key="process"):
    return c.record_processing(token(i), key, e.event_id, "sink://" + e.event_id)


def test_duplicate_event_and_collision(core):
    c, _, _ = core
    e = event()
    assert c.publish(token(), "publish", e)["status"] == "PUBLISHED"
    assert c.publish(token(), "duplicate", e)["status"] == "DUPLICATE"
    assert c.publish(token(), "collision", replace(e, summary="changed"))["error_code"] == "EVENT_ID_COLLISION"
    assert len(c.snapshot()["events"]) == 1
    assert c.snapshot()["tasks"]["T"]["status"] == "READY"


def test_ack_loss_restart_ack_only(core):
    c, clock, registry = core
    e = event()
    c.publish(token(), "publish", e)
    assert process(c, e)["status"] == "PROCESSED"
    # Crash after durable sink receipt, before transport ACK. No external callback is re-executed.
    fresh = Controller(c.backend, registry, authenticator, clock=clock)
    delivery = pending_deliveries(fresh.snapshot(), "agent-1")
    assert [d["action"] for d in delivery] == ["ACK_ONLY"]
    assert process(fresh, e, key="process-after-crash")["status"] == "ALREADY_PROCESSED"
    assert len(fresh.snapshot()["effects"]) == 1
    assert ack(fresh, e)["status"] == "ACK_RECORDED"
    assert ack(fresh, e, key="duplicate-ack")["status"] == "DUPLICATE_ACK"
    assert pending_deliveries(fresh.snapshot(), "agent-1") == []
    assert pending_deliveries(fresh.snapshot(), "agent-2")[0]["action"] == "PROCESS"
    assert fresh.snapshot()["tasks"]["T"]["status"] == "READY"


def test_out_of_order_ack_does_not_skip_gaps(core):
    c, _, _ = core
    first, second = event("E1"), event("E2")
    for e in (first, second): c.publish(token(), e.event_id, e)
    assert ack(c, second, key="unverified")["error_code"] == "ACK_UNVERIFIED"
    process(c, second, key="p2")
    assert ack(c, second, key="ack2")["cursor"] == 0
    process(c, first, key="p1")
    assert ack(c, first, key="ack1")["cursor"] == 2
    assert len(c.snapshot()["cursors"]) == 1
    process(c, second, i=2, key="other-p")
    assert ack(c, second, i=2, key="other-a")["cursor"] == 0


def test_ack_scope_and_digest(core):
    c, _, _ = core
    e = event(targets=("agent-1",))
    c.publish(token(), "e", e)
    assert process(c, e, i=2)["error_code"] == "TARGET_DENIED"
    a = Ack(event_id="E", agent_id="agent-1", provider_id="workbuddy", run_id="run", event_sha256="f" * 64, evidence_refs=("sink://E",))
    assert c.ack(token(1), "bad-hash", a)["error_code"] == "ACK_HASH_MISMATCH"
    assert c.ack(token(2), "spoof", a)["error_code"] == "AUTH_SCOPE_MISMATCH"


@pytest.mark.parametrize("point", ["before_append", "after_append", "after_commit"])
def test_injected_write_failure_and_reconciliation(core, point):
    c, clock, registry = core
    def fault(at):
        if at == point: raise OSError("injected storage failure")
    c.backend.fault = fault
    result = c.claim(token(), "uncertain-claim", proposal())
    assert result["status"] == "UNKNOWN_WRITE"
    c.backend.fault = lambda _: None
    observed = c.backend.reconcile(result["command_id"], result["reconcile_request"])
    assert observed["status"] == ("COMMITTED" if point == "after_commit" else "NOT_FOUND")
    fresh = Controller(c.backend, registry, authenticator, clock=clock)
    assert reconcile(fresh, "fresh")["status"] == "RECONCILED"
    retry = fresh.claim(token(), "uncertain-claim", proposal())
    assert retry["status"] == "GRANTED"
    assert len([r for r in fresh.backend.records() if r["request"]["kind"] == "CLAIM"]) == 1


def test_read_failure_is_unknown_not_empty(core):
    c, _, _ = core
    c.backend.fault = lambda p: (_ for _ in ()).throw(OSError("read failed")) if p == "before_read" else None
    with pytest.raises(OSError): c.board()
    result = c.claim(token(), "during-read-failure", proposal())
    assert result["status"] == "UNKNOWN_WRITE"
    c.backend.fault = lambda _: None
    assert c.board()["board_status"] == "UNKNOWN"
    assert c.claim(token(), "after-read-failure", proposal())["error_code"] == "BOARD_UNKNOWN"


def test_replay_restart_and_immutable_audit(core):
    c, clock, registry = core
    for i in range(20):
        e = event(f"E{i}")
        c.publish(token(), f"event-{i}", e)
        if i % 2:
            process(c, e, key=f"process-{i}")
            ack(c, e, key=f"ack-{i}")
    records = c.backend.records()
    assert rebuild(records) == c.snapshot()
    fresh = Controller(c.backend, registry, authenticator, clock=clock)
    assert board_projection(fresh.snapshot()) == board_projection(c.snapshot())
    result = audit(records, now=clock())
    assert result["record_count"] == len(records)
    assert len(result["delivery_gaps"]["agent-2"]) == 20
    broken = deepcopy(records)
    broken[3]["result"] = {"status": "forged"}
    with pytest.raises(CoreError, match="AUDIT_HASH_MISMATCH"): rebuild(broken)
    with c.backend.connect() as db:
        for sql in ("UPDATE journal SET record='{}' WHERE seq=1", "DELETE FROM journal WHERE seq=1"):
            with pytest.raises(sqlite3.IntegrityError, match="immutable audit"): db.execute(sql)


def test_random_crash_schedule_converges(core):
    c, _, _ = core
    rng = random.Random(20261025)
    for i in range(30):
        e = event(f"R{i}")
        point = rng.choice(["after_append", "after_commit", "none"])
        def fault(at):
            if at == point: raise OSError("crash")
        c.backend.fault = fault
        result = c.publish(token(), f"random-{i}", e)
        c.backend.fault = lambda _: None
        if result["status"] == "UNKNOWN_WRITE":
            proof = c.backend.reconcile(result["command_id"], result["reconcile_request"])
            if proof["status"] == "NOT_FOUND": c.publish(token(), f"random-{i}", e)
    assert len(c.snapshot()["events"]) == 30
    assert rebuild(c.backend.records()) == c.snapshot()


def test_orphan_recovery_and_relay_grace(core):
    c, clock, _ = core
    c.claim(token(), "claim", proposal(ttl_seconds=1))
    clock.value += 7200
    assert audit(c.backend.records(), now=clock())["expired_orphans"] == ["T"]
    assert c.recover(token(), "recover")["status"] == "RECOVERED"
    assert c.snapshot()["tasks"]["T"]["status"] == "READY"
    common = dict(source_verified=True, source_ready_at=1, native_attempt_at=None,
        native_outcome=None, grace_until=10, target_missing_verified=True)
    assert not relay_eligibility(**common, now=9)["eligible"]
    result = relay_eligibility(**common, now=10)
    assert result["eligible"] and result["native_outcome"] == "UNKNOWN"


def crash_worker(path, point):
    import os
    from conftest import Clock, agent
    from factory.agl.registry import AgentRegistry
    backend = SQLiteLeaseBackend(path)
    c = Controller(backend, AgentRegistry([agent(i) for i in range(3)], simulation=True), authenticator, clock=Clock())
    reconcile(c, "worker-readback")
    backend.fault = lambda p: os._exit(73) if p == point else None
    c.claim(token(), "crash-claim", proposal())


@pytest.mark.parametrize("point,committed", [("after_append", False), ("after_commit", True)])
def test_real_process_exit_atomicity(core, point, committed):
    import multiprocessing
    c, _, _ = core
    worker = multiprocessing.get_context("fork").Process(target=crash_worker, args=(c.backend.path, point))
    worker.start()
    worker.join(timeout=20)
    assert not worker.is_alive() and worker.exitcode == 73
    task = c.snapshot()["tasks"]["T"]
    assert (task["lease"] is not None) is committed
    assert rebuild(c.backend.records()) == c.snapshot()


def test_causation_blocks_ack_and_rolls_back(core):
    c, _, _ = core
    cause = event("cause")
    later = event("later", causation_id="cause")
    c.publish(token(), "cause", cause)
    c.publish(token(), "later", later)
    process(c, later, key="later-process")
    assert ack(c, later, key="too-early")["error_code"] == "CAUSATION_NOT_ACKED"
    assert not c.snapshot()["acks"]
    process(c, cause, key="cause-process")
    ack(c, cause, key="cause-ack")
    assert ack(c, later, key="later-ack")["cursor"] == 2


def test_git_journal_export_restore_new_database(core, tmp_path):
    c, clock, registry = core
    c.publish(token(), "publish", event())
    process(c, event())
    # JSON bytes are the future Git Adapter boundary; this test is local, no Git API simulated as real.
    exported = json.loads(json.dumps(c.backend.records()))
    restored = SQLiteLeaseBackend.restore(tmp_path / "restored.sqlite", exported, expected_head_hash=exported[-1]["record_hash"])
    fresh = Controller(restored, registry, authenticator, clock=clock)
    assert fresh.snapshot() == c.snapshot()
    assert pending_deliveries(fresh.snapshot(), "agent-1")[0]["action"] == "ACK_ONLY"
    assert fresh.claim(token(), "needs-reconcile", proposal())["error_code"] == "BOARD_UNKNOWN"
    with pytest.raises(CoreError, match="RESTORE_HEAD_MISMATCH"):
        SQLiteLeaseBackend.restore(tmp_path / "bad-head.sqlite", exported, expected_head_hash="0" * 64)
    with pytest.raises(CoreError, match="RESTORE_REQUIRES_EMPTY_DATABASE"):
        SQLiteLeaseBackend.restore(tmp_path / "restored.sqlite", exported, expected_head_hash=exported[-1]["record_hash"])
