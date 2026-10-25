"""Solution for P04: reconcile vector-clocked versions per key."""


def _is_nonnegative_int(value):
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _strictly_dominates(left_clock, right_clock):
    nodes = set(left_clock) | set(right_clock)
    strictly_greater = False
    for node in nodes:
        left = left_clock.get(node, 0)
        right = right_clock.get(node, 0)
        if left < right:
            return False
        if left > right:
            strictly_greater = True
    return strictly_greater


def reconcile_versions(events: list[dict]) -> list[dict]:
    """Return deterministic winners and causal-conflict metadata per key."""
    if not isinstance(events, list):
        raise ValueError("events must be a list")

    required = {"event_id", "key", "clock", "value", "timestamp"}
    by_event_id = {}
    by_key = {}

    for event in events:
        if not isinstance(event, dict) or not required.issubset(event):
            raise ValueError("each event must contain all required fields")
        event_id = event["event_id"]
        key = event["key"]
        clock = event["clock"]
        value = event["value"]
        timestamp = event["timestamp"]
        if not isinstance(event_id, str) or not event_id:
            raise ValueError("event_id must be a non-empty string")
        if not isinstance(key, str) or not key:
            raise ValueError("key must be a non-empty string")
        if not isinstance(clock, dict):
            raise ValueError("clock must be a dict")
        for node, counter in clock.items():
            if not isinstance(node, str) or not node:
                raise ValueError("clock node names must be non-empty strings")
            if not _is_nonnegative_int(counter):
                raise ValueError("clock counters must be non-negative integers")
        if value is not None and not isinstance(value, str):
            raise ValueError("value must be a string or None")
        if not _is_nonnegative_int(timestamp):
            raise ValueError("timestamp must be a non-negative integer")

        previous = by_event_id.get(event_id)
        if previous is not None:
            if previous != event:
                raise ValueError("conflicting events share an event_id")
            continue
        by_event_id[event_id] = event
        by_key.setdefault(key, []).append(event)

    result = []
    for key in sorted(by_key):
        versions = by_key[key]
        superseded = set()
        for candidate in versions:
            for other in versions:
                if candidate is other:
                    continue
                if _strictly_dominates(other["clock"], candidate["clock"]):
                    superseded.add(candidate["event_id"])
                    break

        maxima = [
            event for event in versions if event["event_id"] not in superseded
        ]
        winner = max(maxima, key=lambda event: (event["timestamp"], event["event_id"]))
        conflict_ids = (
            sorted(event["event_id"] for event in maxima) if len(maxima) > 1 else []
        )
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
