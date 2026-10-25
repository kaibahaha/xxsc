"""Immutable event ledger: per-(event_id,target) idempotency, collision, ACK, cursor."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from agl.errors import AglError, ErrorCode
from agl.storage.ledger import EventLedger
from agl.storage.ledger import event_digest, normalize_event

from helpers import make_event


def head(bare: Path, ref: str = "exp/test") -> str:
    return subprocess.run(["git", "rev-parse", f"refs/heads/{ref}"], cwd=str(bare),
                          capture_output=True, text=True).stdout.strip()


@pytest.mark.real_git
def test_event_written_with_manifest(ledger, storage):
    event = normalize_event(make_event())
    write = ledger.put_event(event, "CHATGPT_01")
    assert write.status == "CREATED"
    assert write.path.endswith("03_events/20261025/EV-0001/CHATGPT_01.json")
    manifest = ledger.read_manifest("20261025", "EV-0001")
    assert manifest["payload_sha256"] == event["payload_sha256"]
    stored = ledger.read_event("20261025", "EV-0001", "CHATGPT_01")
    assert event_digest(stored) == manifest["payload_sha256"]


@pytest.mark.real_git
def test_same_event_same_payload_is_idempotent(ledger, bare_remote):
    event = normalize_event(make_event())
    ledger.put_event(event, "CHATGPT_01")
    before = head(bare_remote)
    again = ledger.put_event(event, "CHATGPT_01")
    assert again.status == "IDEMPOTENT_REPLAY"
    assert again.dedupe is True
    assert head(bare_remote) == before


@pytest.mark.real_git
def test_same_event_id_different_payload_is_collision(ledger, bare_remote):
    first = normalize_event(make_event(summary="first"))
    ledger.put_event(first, "CHATGPT_01")
    before = head(bare_remote)

    second = normalize_event(make_event(summary="second"))
    with pytest.raises(AglError) as exc:
        ledger.put_event(second, "CHATGPT_01")
    assert exc.value.code is ErrorCode.COLLISION
    assert "EVENT_ID_COLLISION" in exc.value.message
    assert exc.value.detail["existing_sha256"] != exc.value.detail["incoming_sha256"]
    assert head(bare_remote) == before


@pytest.mark.real_git
def test_collision_blocks_every_target_not_just_the_one(ledger):
    event = normalize_event(make_event(target_agents=["CHATGPT_01", "WORKBUDDY_01"], summary="v1"))
    ledger.put_event(event, "CHATGPT_01")
    tampered = normalize_event(make_event(target_agents=["CHATGPT_01", "WORKBUDDY_01"], summary="v2"))
    with pytest.raises(AglError) as exc:
        ledger.put_event(tampered, "WORKBUDDY_01")
    assert exc.value.code is ErrorCode.COLLISION


@pytest.mark.real_git
def test_multi_target_creates_one_file_per_target(ledger):
    event = normalize_event(make_event(target_agents=["CHATGPT_01", "WORKBUDDY_01", "CODEX_01"]))
    for target in event["target_agents"]:
        assert ledger.put_event(event, target).status == "CREATED"
    date = "20261025"
    assert ledger.read_event(date, "EV-0001", "CHATGPT_01") is not None
    assert ledger.read_event(date, "EV-0001", "WORKBUDDY_01") is not None
    assert ledger.read_event(date, "EV-0001", "CODEX_01") is not None
    assert len(ledger.list_event_ids(date)) == 1  # one event dir, three deliveries


@pytest.mark.real_git
def test_target_must_be_in_target_agents(ledger):
    with pytest.raises(AglError):
        ledger.put_event(make_event(), "UNKNOWN_AGENT")


@pytest.mark.real_git
def test_receipt_idempotent_and_conflict(ledger):
    first = ledger.put_receipt("CHATGPT_01", "EV-0001", result="DELIVERY_ACK",
                               evidence_ref="03_events/20261025/EV-0001/CHATGPT_01.json")
    assert first.status == "CREATED"
    again = ledger.put_receipt("CHATGPT_01", "EV-0001", result="DELIVERY_ACK",
                               evidence_ref="03_events/20261025/EV-0001/CHATGPT_01.json")
    assert again.status == "IDEMPOTENT_REPLAY"
    with pytest.raises(AglError) as exc:
        ledger.put_receipt("CHATGPT_01", "EV-0001", result="FAILED",
                           evidence_ref="something-else")
    assert exc.value.code is ErrorCode.CONFLICT


@pytest.mark.real_git
def test_cursor_is_monotonic(ledger):
    assert ledger.get_cursor("CHATGPT_01")["cursor"] is None
    ledger.advance_cursor("CHATGPT_01", "2026-10-25T10:00:00Z")
    result = ledger.advance_cursor("CHATGPT_01", "2026-10-25T09:00:00Z")
    assert result["status"] == "MONOTONIC_NOOP"
    assert ledger.get_cursor("CHATGPT_01")["cursor"] == "2026-10-25T10:00:00Z"
    ledger.advance_cursor("CHATGPT_01", "2026-10-25T11:00:00Z")
    assert ledger.get_cursor("CHATGPT_01")["cursor"] == "2026-10-25T11:00:00Z"


@pytest.mark.real_git
def test_cursor_cas_survives_concurrent_writers(bare_remote, ledger):
    from agl.storage.github import GitHubStorage
    from agl.storage.transports import LocalGitTransport

    other = EventLedger(
        GitHubStorage(LocalGitTransport(bare_remote), "kaibahaha/xxsc", "exp/test",
                      allowed_prefixes=("factory",)),
        "factory/projects/AGL-SHADOW-001",
    )
    ledger.advance_cursor("CODEX_01", "2026-10-25T10:00:00Z")
    other.advance_cursor("CODEX_01", "2026-10-25T12:00:00Z")
    assert ledger.get_cursor("CODEX_01")["cursor"] == "2026-10-25T12:00:00Z"
    result = other.advance_cursor("CODEX_01", "2026-10-25T11:00:00Z")
    assert result["status"] == "MONOTONIC_NOOP"


@pytest.mark.real_git
def test_outbox_publish_is_scoped_to_agent(ledger):
    write = ledger.publish_outbox("WORKBUDDY_01", "RUN-1", make_event())
    assert write.path == "factory/projects/AGL-SHADOW-001/05_outbox/WORKBUDDY_01/RUN-1/EV-0001.json"
    assert write.status == "CREATED"


@pytest.mark.real_git
def test_iter_events_filters_by_task(ledger):
    ledger.put_event(normalize_event(make_event("EV-A", task_id="TASK-1")), "CHATGPT_01")
    ledger.put_event(normalize_event(make_event("EV-B", task_id="TASK-2")), "CHATGPT_01")
    only_task2 = list(ledger.iter_events(task_id="TASK-2"))
    assert [key for key, _ in only_task2] == ["20261025/EV-B"]


def test_event_digest_ignores_self_field():
    event = make_event()
    without = dict(event)
    with_self = dict(event, payload_sha256="0" * 64)
    assert event_digest(without) == event_digest(with_self)
