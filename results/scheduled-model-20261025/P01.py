"""P01 - 半开时间窗合并与幂等去重.

SCHED-CODE-20261025-BLIND-T5-R2
Deliverable: results/scheduled-model-20261025/P01.py
Entrypoint : merge_windows(events, gap) -> list[dict]

仅使用 Python 3.11 标准库。
"""

from __future__ import annotations

_REQUIRED_FIELDS = ("event_id", "tenant", "start", "end")


def _is_real_int(value) -> bool:
    """True only for genuine ints; bool is explicitly rejected."""
    return isinstance(value, int) and not isinstance(value, bool)


def _is_non_empty_str(value) -> bool:
    return isinstance(value, str) and value != ""


def merge_windows(events, gap):
    """Merge half-open [start, end) windows per tenant with an idempotent dedup.

    Steps
    -----
    1. Validate ``gap`` and the ``events`` container.
    2. Validate every event, then perform a global idempotent dedup on
       ``event_id``.  Identical duplicates collapse; the same id with any
       differing field raises ``ValueError``.
    3. Group the surviving events by tenant, sort each group by
       ``(start, end, event_id)`` and sweep once, merging a window when
       ``next.start <= current.end + gap`` (touching windows merge).
    4. Emit ``{"tenant", "start", "end", "count"}`` records sorted by
       ``(tenant, start, end)``.

    Complexity: O(n log n) time (dominated by sorting), O(n) extra space
    excluding the output.

    The input objects are never mutated.
    """
    if not isinstance(events, list):
        raise ValueError("events must be a list")
    if not _is_real_int(gap) or gap < 0:
        raise ValueError("gap must be a non-negative integer")

    # ---- validate + idempotent dedup -------------------------------------
    canonical: dict = {}
    for index, event in enumerate(events):
        if not isinstance(event, dict):
            raise ValueError("events[%d] must be a dict" % index)
        for field in _REQUIRED_FIELDS:
            if field not in event:
                raise ValueError("events[%d] is missing required field %r" % (index, field))

        event_id = event["event_id"]
        tenant = event["tenant"]
        start = event["start"]
        end = event["end"]

        if not _is_non_empty_str(event_id):
            raise ValueError("events[%d].event_id must be a non-empty string" % index)
        if not _is_non_empty_str(tenant):
            raise ValueError("events[%d].tenant must be a non-empty string" % index)
        if not _is_real_int(start):
            raise ValueError("events[%d].start must be an integer (bool rejected)" % index)
        if not _is_real_int(end):
            raise ValueError("events[%d].end must be an integer (bool rejected)" % index)
        if start >= end:
            raise ValueError("events[%d] must satisfy start < end" % index)

        signature = (tenant, start, end)
        previous = canonical.get(event_id)
        if previous is None:
            canonical[event_id] = signature
        elif previous != signature:
            raise ValueError("conflicting payload for duplicate event_id %r" % (event_id,))

    # ---- group by tenant --------------------------------------------------
    by_tenant: dict = {}
    for event_id, (tenant, start, end) in canonical.items():
        by_tenant.setdefault(tenant, []).append((start, end, event_id))

    result = []
    for tenant in sorted(by_tenant):
        windows = sorted(by_tenant[tenant], key=lambda item: (item[0], item[1], item[2]))

        cur_start = None
        cur_end = None
        cur_ids = set()

        for start, end, event_id in windows:
            if cur_start is None:
                cur_start, cur_end, cur_ids = start, end, {event_id}
                continue
            if start <= cur_end + gap:
                if end > cur_end:
                    cur_end = end
                cur_ids.add(event_id)
            else:
                result.append(
                    {
                        "tenant": tenant,
                        "start": cur_start,
                        "end": cur_end,
                        "count": len(cur_ids),
                    }
                )
                cur_start, cur_end, cur_ids = start, end, {event_id}

        if cur_start is not None:
            result.append(
                {
                    "tenant": tenant,
                    "start": cur_start,
                    "end": cur_end,
                    "count": len(cur_ids),
                }
            )

    # Tenants are emitted in sorted order and windows inside a tenant have
    # strictly increasing start, so the whole list is already ordered by
    # (tenant, start, end).
    return result


if __name__ == "__main__":  # pragma: no cover - manual smoke check
    sample = [
        {"event_id": "e1", "tenant": "x", "start": 0, "end": 5},
        {"event_id": "e2", "tenant": "x", "start": 7, "end": 9},
        {"event_id": "e3", "tenant": "x", "start": 9, "end": 10},
        {"event_id": "e4", "tenant": "y", "start": 1, "end": 3},
        {"event_id": "e2", "tenant": "x", "start": 7, "end": 9},
    ]
    print(merge_windows(sample, 2))
