"""Pure journal reducer. No network, clock, callbacks or inference in replay."""
from copy import deepcopy
from .schemas import digest, require

COLLECTIONS = ("agents", "tasks", "events", "effects", "acks", "cursors", "notes", "handoffs", "meta")


def empty_state():
    return {name: {} for name in COLLECTIONS}


def changes_between(before, after):
    out = []
    for collection in COLLECTIONS:
        require(set(before[collection]) <= set(after[collection]), "HISTORY_DELETION")
        for key, value in after[collection].items():
            if key not in before[collection] or before[collection][key] != value:
                out.append([collection, key, deepcopy(value)])
    return out


def rebuild(records):
    state = empty_state()
    previous = "0" * 64
    for expected, row in enumerate(records, 1):
        require(row["seq"] == expected and row["previous_hash"] == previous, "AUDIT_CHAIN_BROKEN")
        content = {k: v for k, v in row.items() if k != "record_hash"}
        require(digest(content) == row["record_hash"], "AUDIT_HASH_MISMATCH")
        for collection, key, value in row["changes"]:
            require(collection in COLLECTIONS, "INVALID_JOURNAL_COLLECTION")
            state[collection][key] = deepcopy(value)
        previous = row["record_hash"]
    return state


def board_projection(state: dict) -> dict:
    return {"schema_version": "2.0", "board_status": state["meta"].get("board", "UNKNOWN"),
            "tasks": [deepcopy(state["tasks"][k]) for k in sorted(state["tasks"])],
            "cursors": deepcopy(state["cursors"]),
            "event_ids": list(state["events"]), "note_ids": list(state["notes"])}
