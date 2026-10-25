"""P04 - 向量时钟并发冲突与确定性裁决.

SCHED-CODE-20261025-BLIND-T5-R2
Deliverable: results/scheduled-model-20261025/P04.py
Entrypoint : reconcile_versions(events) -> list[dict]

仅使用 Python 3.11 标准库。
"""

from __future__ import annotations

_REQUIRED_FIELDS = ("event_id", "key", "clock", "value", "timestamp")


def _is_real_int(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _is_non_empty_str(value) -> bool:
    return isinstance(value, str) and value != ""


def _dominates(clock_x, clock_y) -> bool:
    """True iff x strictly causally dominates y.

    Every node count of x must be >= that of y (missing nodes count as 0) and
    at least one node must be strictly greater.  Equal clocks therefore never
    dominate each other.  ``timestamp`` plays no role here.
    """
    strictly_greater = False
    for node in set(clock_x) | set(clock_y):
        left = clock_x.get(node, 0)
        right = clock_y.get(node, 0)
        if left < right:
            return False
        if left > right:
            strictly_greater = True
    return strictly_greater


def reconcile_versions(events):
    """Reconcile vector-clock versioned writes, per key.

    Pipeline
    --------
    1. Validate the container and every event.
    2. Global idempotent dedup on ``event_id`` (identical payload collapses,
       any difference raises ``ValueError``).
    3. Per key, do the pairwise domination scan: a version is *superseded* if
       some other version strictly causally dominates it; the rest form the
       *maxima* set.
    4. If maxima holds more than one version we have a conflict; the winner is
       picked deterministically by ``(timestamp, event_id)`` descending.
       ``conflict_ids`` is empty when the maximum is unique.

    Complexity: per key O(m^2 * k) pairwise comparisons (m versions, k nodes),
    plus O(n log n) for sorting; space O(n + total clock entries).
    Input is never mutated.
    """
    if not isinstance(events, list):
        raise ValueError("events must be a list")

    # ---- validate + idempotent dedup -------------------------------------
    canonical: dict = {}
    for index, event in enumerate(events):
        if not isinstance(event, dict):
            raise ValueError("events[%d] must be a dict" % index)
        for field in _REQUIRED_FIELDS:
            if field not in event:
                raise ValueError("events[%d] is missing required field %r" % (index, field))

        event_id = event["event_id"]
        key = event["key"]
        clock = event["clock"]
        value = event["value"]
        timestamp = event["timestamp"]

        if not _is_non_empty_str(event_id):
            raise ValueError("events[%d].event_id must be a non-empty string" % index)
        if not _is_non_empty_str(key):
            raise ValueError("events[%d].key must be a non-empty string" % index)

        if not isinstance(clock, dict):
            raise ValueError("events[%d].clock must be a dict" % index)
        for node, count in clock.items():
            if not _is_non_empty_str(node):
                raise ValueError("events[%d].clock keys must be non-empty strings" % index)
            if not _is_real_int(count) or count < 0:
                raise ValueError(
                    "events[%d].clock[%r] must be a non-negative integer (bool rejected)"
                    % (index, node)
                )

        if value is not None and not isinstance(value, str):
            raise ValueError("events[%d].value must be a string or None" % index)

        if not _is_real_int(timestamp) or timestamp < 0:
            raise ValueError(
                "events[%d].timestamp must be a non-negative integer (bool rejected)" % index
            )

        signature = (key, tuple(sorted(clock.items())), value, timestamp)
        previous = canonical.get(event_id)
        if previous is None:
            canonical[event_id] = signature
        elif previous != signature:
            raise ValueError("conflicting payload for duplicate event_id %r" % (event_id,))

    # ---- group by key ------------------------------------------------------
    by_key: dict = {}
    for event_id, (key, clock_items, value, timestamp) in canonical.items():
        by_key.setdefault(key, []).append(
            {"event_id": event_id, "clock": dict(clock_items), "value": value,
             "timestamp": timestamp}
        )

    result = []
    for key in sorted(by_key):
        versions = by_key[key]

        superseded = []
        maxima = []
        for candidate in versions:
            dominated = False
            for other in versions:
                if other is candidate:
                    continue
                if _dominates(other["clock"], candidate["clock"]):
                    dominated = True
                    break
            if dominated:
                superseded.append(candidate["event_id"])
            else:
                maxima.append(candidate)

        # Deterministic winner: (timestamp, event_id) descending.
        winner = max(maxima, key=lambda item: (item["timestamp"], item["event_id"]))

        conflict_ids = []
        if len(maxima) > 1:
            conflict_ids = sorted(item["event_id"] for item in maxima)

        result.append(
            {
                "key": key,
                "winner_id": winner["event_id"],
                "value": winner["value"],
                "conflict_ids": conflict_ids,
                "superseded_ids": sorted(superseded),
            }
        )

    return result


if __name__ == "__main__":  # pragma: no cover - manual smoke check
    sample = [
        {"event_id": "u1", "key": "k", "clock": {"A": 1}, "value": "a", "timestamp": 10},
        {"event_id": "u2", "key": "k", "clock": {"B": 1}, "value": "b", "timestamp": 11},
        {"event_id": "u3", "key": "k", "clock": {"A": 2}, "value": "c", "timestamp": 9},
        {"event_id": "u4", "key": "z", "clock": {"A": 1, "B": 1}, "value": None, "timestamp": 3},
    ]
    print(reconcile_versions(sample))
