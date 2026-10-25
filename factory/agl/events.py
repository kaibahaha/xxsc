"""Read-only event delivery view. Processing receipts survive missing transport ACKs."""
from copy import deepcopy
from .schemas import digest


def pending_deliveries(state: dict, agent_id: str):
    out = []
    for entry in state["events"].values():
        event = entry["event"]
        if agent_id not in event["target_agents"]:
            continue
        key = digest([event["event_id"], agent_id])
        if key in state["acks"]:
            continue
        out.append({"event": deepcopy(event), "sha256": entry["sha256"],
                    "idempotency_key": key,
                    "action": "ACK_ONLY" if key in state["effects"] else "PROCESS",
                    "processing_receipt": deepcopy(state["effects"].get(key))})
    return out
