"""Cold-start continuation is computed from authority, never from chat history."""
from copy import deepcopy


def resume(state: dict, agent_id: str, task_id: str, *, now: float):
    task = state["tasks"].get(task_id)
    handoffs = [h for h in state["handoffs"].values() if h["agent_id"] == agent_id and h["task_id"] == task_id]
    latest = handoffs[-1] if handoffs else None
    lease = task.get("lease") if task else None
    valid = bool(task and latest and lease and lease["agent_id"] == agent_id
                 and lease["expires_at"] > now and latest["spec_hash"] == task["spec_hash"]
                 and latest["attempt_id"] == lease["attempt_id"]
                 and latest["fencing_epoch"] == lease["fencing_epoch"]
                 and task["status"] != "DONE")
    return {"action": "CONTINUE" if valid else "READ_ONLY_RECLAIM_REQUIRED",
            "handoff": deepcopy(latest), "task": deepcopy(task)}
