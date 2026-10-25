"""Solution for P01: merge half-open event windows by tenant."""


def _is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def merge_windows(events: list[dict], gap: int) -> list[dict]:
    """Deduplicate events globally, then merge nearby windows per tenant.

    Runs in O(n log n) time and uses O(n) auxiliary space.
    """
    if not isinstance(events, list):
        raise ValueError("events must be a list")
    if not _is_int(gap) or gap < 0:
        raise ValueError("gap must be a non-negative integer")

    required = {"event_id", "tenant", "start", "end"}
    by_event_id = {}
    unique_events = []

    for event in events:
        if not isinstance(event, dict) or not required.issubset(event):
            raise ValueError("each event must contain all required fields")

        event_id = event["event_id"]
        tenant = event["tenant"]
        start = event["start"]
        end = event["end"]
        if not isinstance(event_id, str) or not event_id:
            raise ValueError("event_id must be a non-empty string")
        if not isinstance(tenant, str) or not tenant:
            raise ValueError("tenant must be a non-empty string")
        if not _is_int(start) or not _is_int(end) or start >= end:
            raise ValueError("start and end must be integers with start < end")

        previous = by_event_id.get(event_id)
        if previous is not None:
            if previous != event:
                raise ValueError("conflicting events share an event_id")
            continue
        by_event_id[event_id] = event
        unique_events.append((tenant, start, end, event_id))

    grouped = {}
    for tenant, start, end, event_id in unique_events:
        grouped.setdefault(tenant, []).append((start, end, event_id))

    result = []
    for tenant, windows in grouped.items():
        windows.sort()
        current_start = current_end = None
        count = 0
        for start, end, _event_id in windows:
            if current_start is None:
                current_start, current_end, count = start, end, 1
            elif start <= current_end + gap:
                current_end = max(current_end, end)
                count += 1
            else:
                result.append(
                    {"tenant": tenant, "start": current_start,
                     "end": current_end, "count": count}
                )
                current_start, current_end, count = start, end, 1
        if current_start is not None:
            result.append(
                {"tenant": tenant, "start": current_start,
                 "end": current_end, "count": count}
            )

    result.sort(key=lambda item: (item["tenant"], item["start"], item["end"]))
    return result
