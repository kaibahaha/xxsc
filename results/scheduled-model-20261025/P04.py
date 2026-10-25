"""Reconcile causally ordered and concurrent vector-clock versions."""


def reconcile_versions(events: list[dict]) -> list[dict]:
    """Find maximal causal versions per key, then choose a deterministic winner.

    For each key with m versions and at most k clock nodes, O(m^2*k)
    comparison time; O(n) auxiliary storage apart from clock contents.
    """
    if type(events) is not list:
        raise ValueError("events must be a list")

    seen = {}
    grouped = {}
    for event in events:
        required = ("event_id", "key", "clock", "value", "timestamp")
        if type(event) is not dict or any(field not in event for field in required):
            raise ValueError("invalid event structure")
        event_id, key = event["event_id"], event["key"]
        clock, value, timestamp = event["clock"], event["value"], event["timestamp"]
        if (type(event_id) is not str or not event_id or
                type(key) is not str or not key or type(clock) is not dict or
                not (type(value) is str or value is None) or
                type(timestamp) is not int or timestamp < 0):
            raise ValueError("invalid event fields")
        if any(type(node) is not str or not node or
               type(counter) is not int or counter < 0
               for node, counter in clock.items()):
            raise ValueError("invalid vector clock")
        if event_id in seen:
            if seen[event_id] != event:
                raise ValueError("conflicting global event_id")
            continue
        seen[event_id] = event
        grouped.setdefault(key, []).append(event)

    def dominates(left: dict, right: dict) -> bool:
        """True only if left >= right at all nodes and > at least one."""
        greater = False
        for node in left.keys() | right.keys():
            a = left.get(node, 0)
            b = right.get(node, 0)
            if a < b:
                return False
            if a > b:
                greater = True
        return greater

    results = []
    for key in sorted(grouped):
        versions = grouped[key]
        maximal = []
        superseded = []
        for i, candidate in enumerate(versions):
            if any(i != j and dominates(other["clock"], candidate["clock"])
                   for j, other in enumerate(versions)):
                superseded.append(candidate["event_id"])
            else:
                maximal.append(candidate)
        winner = max(maximal, key=lambda e: (e["timestamp"], e["event_id"]))
        results.append({
            "key": key,
            "winner_id": winner["event_id"],
            "value": winner["value"],
            "conflict_ids": sorted(e["event_id"] for e in maximal)
                            if len(maximal) > 1 else [],
            "superseded_ids": sorted(superseded),
        })
    return results
