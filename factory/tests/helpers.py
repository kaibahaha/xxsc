"""Test helpers (not production code)."""

from __future__ import annotations


def make_event(event_id: str = "EV-0001", **overrides):
    event = {
        "schema_version": "1.0",
        "event_id": event_id,
        "project_id": "AGL-SHADOW-001",
        "task_id": "TASK-1",
        "producer": "WORKBUDDY_01",
        "target_agents": ["CHATGPT_01"],
        "kind": "FACT_PUBLISHED",
        "source": "github",
        "observed_at": "2026-10-25T15:00:00Z",
        "summary": "adapter written",
        "raw_ref": "kaibahaha/xxsc@exp/test:factory/agl/storage/github.py",
        "spec_hash": "b" * 64,
        "run_id": "RUN-TEST-1",
    }
    event.update(overrides)
    return event
