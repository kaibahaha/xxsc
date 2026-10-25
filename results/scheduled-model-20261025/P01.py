"""Merge deduplicated half-open event windows by tenant."""


def merge_windows(events: list[dict], gap: int) -> list[dict]:
    """Return deterministic merged windows; reject malformed or conflicting events.

    Time: O(n log n); auxiliary space: O(n).
    """
    if type(events) is not list or type(gap) is not int or gap < 0:
        raise ValueError("events must be a list and gap a nonnegative integer")

    seen = {}
    grouped = {}
    required = ("event_id", "tenant", "start", "end")
    for event in events:
        if type(event) is not dict or any(k not in event for k in required):
            raise ValueError("invalid event structure")
        event_id, tenant = event["event_id"], event["tenant"]
        start, end = event["start"], event["end"]
        if (type(event_id) is not str or not event_id or
                type(tenant) is not str or not tenant or
                type(start) is not int or type(end) is not int or start >= end):
            raise ValueError("invalid event fields")
        if event_id in seen:
            if seen[event_id] != event:
                raise ValueError("conflicting event_id")
            continue
        seen[event_id] = event
        grouped.setdefault(tenant, []).append((start, end, event_id))

    output = []
    for tenant in sorted(grouped):
        windows = sorted(grouped[tenant])
        current_start = current_end = count = None
        for start, end, _event_id in windows:
            if current_start is None:
                current_start, current_end, count = start, end, 1
            elif start <= current_end + gap:
                current_end = max(current_end, end)
                count += 1
            else:
                output.append({"tenant": tenant, "start": current_start,
                               "end": current_end, "count": count})
                current_start, current_end, count = start, end, 1
        if current_start is not None:
            output.append({"tenant": tenant, "start": current_start,
                           "end": current_end, "count": count})
    return output
