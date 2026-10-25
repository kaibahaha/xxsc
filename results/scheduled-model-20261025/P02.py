"""Solution for P02: replay unordered versioned order events."""


def _is_nonnegative_int(value):
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def replay(events: list[dict]) -> dict:
    """Validate, deduplicate, and replay order events by revision.

    Runs in O(n log n) time and uses O(n) auxiliary space.
    """
    if not isinstance(events, list):
        raise ValueError("events must be a list")

    required = {"event_id", "order_id", "revision", "kind"}
    by_event_id = {}
    by_order = {}
    revisions = set()

    for event in events:
        if not isinstance(event, dict) or not required.issubset(event):
            raise ValueError("each event must contain all required fields")

        event_id = event["event_id"]
        order_id = event["order_id"]
        revision = event["revision"]
        kind = event["kind"]
        if not isinstance(event_id, str) or not event_id:
            raise ValueError("event_id must be a non-empty string")
        if not isinstance(order_id, str) or not order_id:
            raise ValueError("order_id must be a non-empty string")
        if not _is_nonnegative_int(revision):
            raise ValueError("revision must be a non-negative integer")
        if kind not in ("SET", "DELETE"):
            raise ValueError("kind must be SET or DELETE")
        if kind == "SET":
            if "amount" not in event or not _is_nonnegative_int(event["amount"]):
                raise ValueError("SET events need a non-negative integer amount")
        elif "amount" in event:
            raise ValueError("DELETE events must not contain amount")

        previous = by_event_id.get(event_id)
        if previous is not None:
            if previous != event:
                raise ValueError("conflicting events share an event_id")
            continue
        by_event_id[event_id] = event

        version_key = (order_id, revision)
        if version_key in revisions:
            raise ValueError("an order revision has multiple event_ids")
        revisions.add(version_key)
        by_order.setdefault(order_id, []).append(event)

    active = []
    deleted = []
    total_amount = 0
    for order_id in sorted(by_order):
        ordered_events = sorted(by_order[order_id], key=lambda item: item["revision"])
        final = ordered_events[-1]
        if final["kind"] == "SET":
            amount = final["amount"]
            active.append(
                {"order_id": order_id, "amount": amount,
                 "revision": final["revision"]}
            )
            total_amount += amount
        else:
            deleted.append({"order_id": order_id, "revision": final["revision"]})

    return {"active": active, "deleted": deleted, "total_amount": total_amount}
