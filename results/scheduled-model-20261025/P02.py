"""Replay unordered, globally idempotent order events by revision."""


def replay(events: list[dict]) -> dict:
    """Return active/deleted orders and active total. O(n log n) time, O(n) space."""
    if type(events) is not list:
        raise ValueError("events must be a list")

    seen = {}
    by_order = {}
    for event in events:
        if type(event) is not dict or any(
                key not in event for key in ("event_id", "order_id", "revision", "kind")):
            raise ValueError("invalid event structure")
        event_id, order_id = event["event_id"], event["order_id"]
        revision, kind = event["revision"], event["kind"]
        if (type(event_id) is not str or not event_id or
                type(order_id) is not str or not order_id or
                type(revision) is not int or revision < 0 or
                type(kind) is not str or kind not in ("SET", "DELETE")):
            raise ValueError("invalid event fields")
        if kind == "SET":
            if ("amount" not in event or type(event["amount"]) is not int or
                    event["amount"] < 0):
                raise ValueError("SET requires nonnegative integer amount")
        elif "amount" in event:
            raise ValueError("DELETE must not have amount")

        if event_id in seen:
            if seen[event_id] != event:
                raise ValueError("conflicting event_id")
            continue
        seen[event_id] = event
        revisions = by_order.setdefault(order_id, {})
        if revision in revisions:
            raise ValueError("multiple distinct events at same order revision")
        revisions[revision] = event

    active = []
    deleted = []
    total_amount = 0
    for order_id in sorted(by_order):
        revisions = by_order[order_id]
        # Replay in ascending revision order. The last event determines state.
        for revision in sorted(revisions):
            latest = revisions[revision]
        if latest["kind"] == "SET":
            amount = latest["amount"]
            active.append({"order_id": order_id, "amount": amount,
                           "revision": latest["revision"]})
            total_amount += amount
        else:
            deleted.append({"order_id": order_id, "revision": latest["revision"]})
    return {"active": active, "deleted": deleted, "total_amount": total_amount}
