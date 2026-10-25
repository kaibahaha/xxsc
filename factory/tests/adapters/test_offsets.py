"""Scheduling offsets: per-provider sub-pool, never 60/N across a mixed pool."""

from __future__ import annotations

import pytest

from agl.adapters.registry_view import RegistryView
from agl.errors import AglError
from agl.poll import PollPlanner, compute_offsets
from agl.support.poolgen import build_pool


@pytest.mark.parametrize(
    "k,expected",
    [
        (1, [0]),
        (2, [0, 30]),
        (3, [0, 20, 40]),
        (4, [0, 15, 30, 45]),
        (5, [0, 12, 24, 36, 48]),
        (6, [0, 10, 20, 30, 40, 50]),
    ],
)
def test_documented_offset_table(k, expected):
    assert compute_offsets(k) == expected


def test_non_divisor_is_quantized_not_rejected():
    offsets = compute_offsets(7)
    assert offsets[0] == 0
    assert len(offsets) == len(set(offsets)) == 7
    assert all(0 <= o < 60 for o in offsets)
    assert offsets == sorted(offsets)


def test_slot_count_above_cadence_rejected():
    with pytest.raises(AglError):
        compute_offsets(61)


def test_zero_slots_rejected():
    with pytest.raises(AglError):
        compute_offsets(0)


def test_offsets_are_per_provider_not_global():
    """N=10 mixed: ChatGPT keeps 60-minute K-slot table, WorkBuddy keeps its own."""
    cfg = build_pool(10, mix={"chatgpt": 4, "workbuddy": 4, "codex": 2},
                     admission="ADMITTED_ACTIVE", ref="exp/test")
    registry = RegistryView.from_config(cfg)
    planner = PollPlanner(registry, None, None, run_id="RUN-PLAN")  # type: ignore[arg-type]
    slots = planner.plan()
    by_provider = {}
    for slot in slots:
        by_provider.setdefault(slot.provider_id, []).append(slot)

    chat = by_provider["chatgpt"]
    assert [s.offset_minutes for s in chat] == [0, 15, 30, 45]
    assert all(s.cadence_minutes == 60 for s in chat)

    wb = by_provider["workbuddy"]
    assert all(s.cadence_minutes == 20 for s in wb)
    assert [s.offset_minutes for s in wb] == [0, 5, 10, 15]

    # the global N (10) must not appear as a divisor anywhere
    assert all(s.offset_minutes != 10 for s in chat)


def test_manifest_is_a_proposal_not_a_schedule():
    cfg = build_pool(6, mix={"chatgpt": 3, "workbuddy": 2, "codex": 1},
                     admission="ADMITTED_ACTIVE", ref="exp/test")
    planner = PollPlanner(RegistryView.from_config(cfg), None, None, run_id="RUN-PLAN")  # type: ignore[arg-type]
    manifest = planner.schedule_manifest()
    assert manifest["verified"] is False
    assert manifest["approval_required"] is True
    assert manifest["creates_real_schedule"] is False
    assert set(manifest["providers"]) == {"chatgpt", "workbuddy", "codex"}
    assert manifest["global_pool_size"] == 6


def test_unknown_cadence_yields_native_unverified_slots():
    cfg = build_pool(2, mix={"codex": 2}, admission="ADMITTED_ACTIVE", ref="exp/test")
    planner = PollPlanner(RegistryView.from_config(cfg), None, None, run_id="RUN-PLAN")  # type: ignore[arg-type]
    slots = planner.plan()
    assert all(s.source == "NATIVE_UNVERIFIED" for s in slots)
    assert all(s.offset_minutes is None for s in slots)
