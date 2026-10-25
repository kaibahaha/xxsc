"""End-to-end integration over a real bare repository.

Flow: publish event -> per-target immutable delivery -> agent reads with cursor
-> ACK -> cursor advances -> replay is a no-op. Also covers fail-closed cases
(draining agent, missing board, read-only provider).
"""

from __future__ import annotations

import json

import pytest

from agl.adapters.registry_view import RegistryView
from agl.poll import PollPlanner
from agl.storage.ledger import normalize_event
from agl.support.poolgen import build_pool
from helpers import make_event

ROOT = "factory/projects/AGL-SHADOW-001"


def _planner(registry, storage, ledger, run_id="RUN-INT-1"):
    return PollPlanner(registry, storage, ledger, run_id=run_id, runner_available=False)


@pytest.mark.real_git
def test_event_delivery_ack_and_cursor_roundtrip(ledger, storage):
    event = normalize_event(make_event(target_agents=["CHATGPT_01", "WORKBUDDY_01"], summary="roundtrip"))
    for target in event["target_agents"]:
        assert ledger.put_event(event, target).status == "CREATED"

    # consumer 1 reads and acknowledges
    from agl.adapters.github_mailbox import AdapterContext
    from agl.adapters.providers import build_adapter

    cfg = build_pool(2, mix={"chatgpt": 1, "workbuddy": 1}, admission="ADMITTED_ACTIVE", ref="exp/test", runtime_root=ROOT)
    registry = RegistryView.from_config(cfg)
    rec = next(a for a in registry.enabled_agents() if a.provider_id == "workbuddy")
    adapter = build_adapter(rec, AdapterContext(storage, ledger, ROOT, "RUN-INT-1"))

    first = adapter.read(cursor=None)
    assert first.board_known is True
    assert [e["event_id"] for e in first.events] == ["EV-0001"]
    assert first.cursor_out == "2026-10-25T15:00:00Z"

    ledger.put_receipt(rec.agent_id, "EV-0001", result="DELIVERY_ACK",
                       evidence_ref="03_events/20261025/EV-0001/WORKBUDDY_01.json")
    ledger.advance_cursor(rec.agent_id, first.cursor_out)

    second = adapter.read(cursor=ledger.get_cursor(rec.agent_id)["cursor"])
    assert second.events == []  # nothing new after the cursor
    assert ledger.get_cursor(rec.agent_id)["cursor"] == "2026-10-25T15:00:00Z"


@pytest.mark.real_git
def test_ack_lost_then_replayed_is_idempotent(ledger, storage):
    event = normalize_event(make_event())
    ledger.put_event(event, "CHATGPT_01")
    first = ledger.put_receipt("CHATGPT_01", "EV-0001", result="DELIVERY_ACK",
                               evidence_ref="03_events/20261025/EV-0001/CHATGPT_01.json")
    # simulate "ACK write lost, agent retries the whole step"
    again = ledger.put_receipt("CHATGPT_01", "EV-0001", result="DELIVERY_ACK",
                               evidence_ref="03_events/20261025/EV-0001/CHATGPT_01.json")
    assert first.status == "CREATED"
    assert again.status == "IDEMPOTENT_REPLAY"
    assert ledger.read_receipt("CHATGPT_01", "EV-0001")["result"] == "DELIVERY_ACK"


@pytest.mark.real_git
def test_duplicate_event_delivery_does_not_duplicate_business_event(ledger, storage):
    event = normalize_event(make_event())
    ledger.put_event(event, "CHATGPT_01")
    ledger.put_event(event, "CHATGPT_01")
    date = "20261025"
    assert ledger.list_event_ids(date) == ["EV-0001"]
    assert len(list(ledger.iter_events())) == 1


@pytest.mark.real_git
def test_draining_agent_cannot_claim(ledger, storage):
    cfg = build_pool(2, mix={"workbuddy": 2}, admission="ADMITTED_ACTIVE", ref="exp/test", runtime_root=ROOT)
    cfg["agents"][0]["admission_status"] = "DRAINING"
    registry = RegistryView.from_config(cfg)
    outcome = _planner(registry, storage, ledger).poll_once(cfg["agents"][0]["agent_id"], allow_write=True)
    assert outcome.status == "REFUSED"
    assert outcome.ok is False
    assert "ADMISSION_DRAINING" in " ".join(outcome.notes)


@pytest.mark.real_git
def test_pending_probe_agent_cannot_claim(ledger, storage):
    cfg = build_pool(2, mix={"workbuddy": 2}, admission="PENDING_PROBE", ref="exp/test", runtime_root=ROOT)
    registry = RegistryView.from_config(cfg)
    outcome = _planner(registry, storage, ledger).poll_once(cfg["agents"][0]["agent_id"])
    assert outcome.status == "REFUSED"


@pytest.mark.real_git
def test_missing_board_fails_closed(bare_remote, tmp_path):
    """Project without 08_projections/BOARD.md must yield BOARD_UNKNOWN, not 'no work'."""
    import subprocess

    from agl.storage.github import GitHubStorage
    from agl.storage.ledger import EventLedger
    from agl.storage.transports import LocalGitTransport

    bare = tmp_path / "empty.git"
    subprocess.run(["git", "init", "--bare", "-q", str(bare)], check=True)
    seed = tmp_path / "s"
    subprocess.run(["git", "init", "-q", str(seed)], check=True)
    subprocess.run(["git", "-C", str(seed), "config", "user.email", "a@b.c"], check=True)
    subprocess.run(["git", "-C", str(seed), "config", "user.name", "a"], check=True)
    (seed / "README.md").write_text("x\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(seed), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(seed), "commit", "-qm", "init"], check=True)
    subprocess.run(["git", "-C", str(seed), "branch", "-M", "exp/test"], check=True)
    subprocess.run(["git", "-C", str(seed), "remote", "add", "origin", str(bare)], check=True)
    subprocess.run(["git", "-C", str(seed), "push", "-q", "origin", "exp/test"], check=True)

    storage = GitHubStorage(LocalGitTransport(bare), "kaibahaha/xxsc", "exp/test")
    ledger = EventLedger(storage, ROOT)
    cfg = build_pool(2, mix={"workbuddy": 2}, admission="ADMITTED_ACTIVE", ref="exp/test", runtime_root=ROOT)
    outcome = _planner(RegistryView.from_config(cfg), storage, ledger).poll_once(cfg["agents"][0]["agent_id"])
    assert outcome.status == "BOARD_UNKNOWN"
    assert outcome.ok is False


@pytest.mark.real_git
def test_poll_dry_run_writes_nothing(ledger, storage, bare_remote):
    import subprocess

    before = subprocess.run(["git", "rev-parse", "refs/heads/exp/test"],
                            cwd=str(bare_remote), capture_output=True, text=True).stdout.strip()
    cfg = build_pool(2, mix={"workbuddy": 2}, admission="ADMITTED_ACTIVE", ref="exp/test", runtime_root=ROOT)
    outcome = _planner(RegistryView.from_config(cfg), storage, ledger).poll_once(cfg["agents"][0]["agent_id"])
    after = subprocess.run(["git", "rev-parse", "refs/heads/exp/test"],
                           cwd=str(bare_remote), capture_output=True, text=True).stdout.strip()
    assert outcome.status == "DRY_RUN"
    assert before == after


@pytest.mark.real_git
def test_poll_apply_writes_claim_and_run_record(ledger, storage):
    cfg = build_pool(2, mix={"workbuddy": 2}, admission="ADMITTED_ACTIVE", ref="exp/test", runtime_root=ROOT)
    agent_id = cfg["agents"][0]["agent_id"]
    outcome = _planner(RegistryView.from_config(cfg), storage, ledger).poll_once(agent_id, allow_write=True)
    assert outcome.status == "CLAIM_PROPOSED"
    assert outcome.task_id == "TASK-1"          # TASK-2 depends on TASK-1
    assert outcome.controller_state == "CONTROLLER_UNAVAILABLE"

    claim = storage.read_file(outcome.claim_path)
    assert claim.exists
    payload = json.loads(claim.text)
    assert payload["kind"] == "CLAIM_PROPOSED"
    assert payload["run_id"] == "RUN-INT-1"

    run = storage.read_file(f"{ROOT}/09_runs/{agent_id}/RUN-INT-1.md")
    assert run.exists
    assert "planned_at" in run.text and "actual_at" in run.text


@pytest.mark.real_git
def test_poll_is_idempotent_for_same_run_id(ledger, storage):
    cfg = build_pool(2, mix={"workbuddy": 2}, admission="ADMITTED_ACTIVE", ref="exp/test", runtime_root=ROOT)
    registry = RegistryView.from_config(cfg)
    agent_id = cfg["agents"][0]["agent_id"]
    first = _planner(registry, storage, ledger).poll_once(agent_id, allow_write=True)
    second = _planner(registry, storage, ledger).poll_once(agent_id, allow_write=True)
    assert first.claim_path == second.claim_path
    assert first.event_id == second.event_id


@pytest.mark.real_git
def test_poll_resumes_open_handoff(ledger, storage):
    cfg = build_pool(2, mix={"workbuddy": 2}, admission="ADMITTED_ACTIVE", ref="exp/test", runtime_root=ROOT)
    agent_id = cfg["agents"][0]["agent_id"]
    from agl.storage.github import canonical_json_bytes

    storage.write_immutable(
        f"{ROOT}/09_runs/{agent_id}/HANDOFF.json",
        canonical_json_bytes({"task_id": "TASK-1", "status": "OPEN", "next_action": "finish tests"}),
        idempotency_key="handoff-1",
    )
    outcome = _planner(RegistryView.from_config(cfg), storage, ledger).poll_once(agent_id)
    assert outcome.status == "RESUME_TASK"
    assert outcome.task_id == "TASK-1"


@pytest.mark.real_git
def test_chatgpt_agent_cannot_write_claim(ledger, storage):
    """A read-only provider proposes but cannot commit; status must say so."""
    cfg = build_pool(2, mix={"chatgpt": 2}, admission="ADMITTED_ACTIVE", ref="exp/test", runtime_root=ROOT)
    agent_id = cfg["agents"][0]["agent_id"]
    outcome = _planner(RegistryView.from_config(cfg), storage, ledger).poll_once(agent_id, allow_write=True)
    assert outcome.status == "CLAIM_PENDING_WRITE"
    assert outcome.claim_path is None
    assert outcome.task_id == "TASK-3"  # only review-capable task matches ChatGPT
    assert "no write credential" in " ".join(outcome.notes)


@pytest.mark.real_git
def test_n6_mixed_pool_polls_per_provider(ledger, storage):
    cfg = build_pool(6, mix={"chatgpt": 3, "workbuddy": 2, "codex": 1},
                     admission="ADMITTED_ACTIVE", ref="exp/test", runtime_root=ROOT)
    registry = RegistryView.from_config(cfg)
    statuses = {}
    for rec in registry.enabled_agents():
        outcome = _planner(registry, storage, ledger, run_id=f"RUN-{rec.agent_id}").poll_once(
            rec.agent_id, allow_write=True
        )
        statuses[rec.provider_id] = statuses.get(rec.provider_id, []) + [outcome.status]
    assert statuses["chatgpt"] == ["CLAIM_PENDING_WRITE"] * 3
    assert statuses["workbuddy"] == ["CLAIM_PROPOSED"] * 2
    assert statuses["codex"] == ["CLAIM_PROPOSED"]

    # each claim lives in its own outbox directory
    outbox_dirs = storage.list_files(f"{ROOT}/05_outbox")
    assert set(outbox_dirs) == {a.agent_id for a in registry.enabled_agents() if a.provider_id != "chatgpt"}
