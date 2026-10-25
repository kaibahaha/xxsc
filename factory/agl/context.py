"""Small HOT/WARM context plus expandable immutable COLD indices."""
from .events import pending_deliveries
from .handoff import resume
from .memory import knowledge


def build_context(state, agent_id, task_id, *, now, hot_limit=16):
    continuation = resume(state, agent_id, task_id, now=now)
    task = continuation["task"]
    notes = knowledge(state, task_id, task["spec_hash"], task["candidate_commit"], now=now, hot_limit=hot_limit) if task else {}
    return {"HOT": {"authority": task, "continuation": continuation["action"], "notes": notes.get("hot", [])},
            "WARM": {"handoff": continuation["handoff"], "notes": notes.get("warm", []),
                     "pending": pending_deliveries(state, agent_id)},
            "COLD": {"note_ids": notes.get("cold_note_ids", []),
                     "event_ids": list(state["events"]), "cursor_index": state["cursors"]}}
