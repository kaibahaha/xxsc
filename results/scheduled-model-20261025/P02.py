"""P02 - 乱序订单事件的幂等重放.

SCHED-CODE-20261025-BLIND-T5-R2
Deliverable: results/scheduled-model-20261025/P02.py
Entrypoint : replay(events) -> dict

仅使用 Python 3.11 标准库。
"""

from __future__ import annotations

_SET = "SET"
_DELETE = "DELETE"
_REQUIRED_FIELDS = ("event_id", "order_id", "revision", "kind")


def _is_real_int(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _is_non_empty_str(value) -> bool:
    return isinstance(value, str) and value != ""


def replay(events):
    """Idempotently replay out-of-order order events.

    Pipeline
    --------
    1. Validate the container and every event (types, required fields, the
       ``amount`` presence rule per ``kind``).
    2. Global idempotent dedup on ``event_id``: identical payloads collapse,
       any difference raises ``ValueError``.
    3. Per ``(order_id, revision)`` there may be at most one distinct
       ``event_id``; two different ids on the same revision raise
       ``ValueError`` regardless of payload.
    4. Replay each order by ascending revision: ``SET`` activates with the
       amount, ``DELETE`` removes and leaves a tombstone.  A higher revision
       always wins, so a deleted order can be resurrected by a later ``SET``.

    Returns ``{"active": [...], "deleted": [...], "total_amount": int}`` with
    both lists sorted by ``order_id``.

    Complexity: O(n log n) time, O(n) extra space.  Input is never mutated.
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
        order_id = event["order_id"]
        revision = event["revision"]
        kind = event["kind"]

        if not _is_non_empty_str(event_id):
            raise ValueError("events[%d].event_id must be a non-empty string" % index)
        if not _is_non_empty_str(order_id):
            raise ValueError("events[%d].order_id must be a non-empty string" % index)
        if not _is_real_int(revision) or revision < 0:
            raise ValueError(
                "events[%d].revision must be a non-negative integer (bool rejected)" % index
            )
        if kind not in (_SET, _DELETE):
            raise ValueError("events[%d].kind must be 'SET' or 'DELETE'" % index)

        if kind == _SET:
            if "amount" not in event:
                raise ValueError("events[%d] with kind='SET' must carry 'amount'" % index)
            amount = event["amount"]
            if not _is_real_int(amount) or amount < 0:
                raise ValueError(
                    "events[%d].amount must be a non-negative integer (bool rejected)" % index
                )
        else:
            if "amount" in event:
                raise ValueError("events[%d] with kind='DELETE' must not carry 'amount'" % index)
            amount = None

        signature = (order_id, revision, kind, amount)
        previous = canonical.get(event_id)
        if previous is None:
            canonical[event_id] = signature
        elif previous != signature:
            raise ValueError("conflicting payload for duplicate event_id %r" % (event_id,))

    # ---- one distinct event_id per (order_id, revision) -------------------
    revision_owner: dict = {}
    for event_id, (order_id, revision, _kind, _amount) in canonical.items():
        slot = (order_id, revision)
        owner = revision_owner.get(slot)
        if owner is None:
            revision_owner[slot] = event_id
        elif owner != event_id:
            raise ValueError(
                "conflicting events %r and %r for order %r revision %d"
                % (owner, event_id, order_id, revision)
            )

    # ---- group by order, replay by ascending revision ---------------------
    by_order: dict = {}
    for event_id, (order_id, revision, kind, amount) in canonical.items():
        by_order.setdefault(order_id, []).append((revision, event_id, kind, amount))

    active: dict = {}
    deleted: dict = {}

    for order_id in by_order:
        # (order_id, revision) is unique after the check above, so sorting by
        # (revision, event_id) is fully deterministic.
        for revision, _event_id, kind, amount in sorted(by_order[order_id]):
            if kind == _SET:
                active[order_id] = (amount, revision)
                deleted.pop(order_id, None)
            else:
                active.pop(order_id, None)
                deleted[order_id] = revision

    active_list = [
        {"order_id": order_id, "amount": active[order_id][0], "revision": active[order_id][1]}
        for order_id in sorted(active)
    ]
    deleted_list = [
        {"order_id": order_id, "revision": deleted[order_id]}
        for order_id in sorted(deleted)
    ]
    total_amount = sum(entry["amount"] for entry in active_list)

    return {"active": active_list, "deleted": deleted_list, "total_amount": total_amount}


if __name__ == "__main__":  # pragma: no cover - manual smoke check
    sample = [
        {"event_id": "e1", "order_id": "o1", "revision": 1, "kind": "SET", "amount": 50},
        {"event_id": "e2", "order_id": "o1", "revision": 3, "kind": "DELETE"},
        {"event_id": "e3", "order_id": "o1", "revision": 2, "kind": "SET", "amount": 70},
        {"event_id": "e4", "order_id": "o2", "revision": 1, "kind": "SET", "amount": 20},
        {"event_id": "e4", "order_id": "o2", "revision": 1, "kind": "SET", "amount": 20},
    ]
    print(replay(sample))
