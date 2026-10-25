"""Typed immutable history with scoped FAIL projection and bounded hot summaries."""
from copy import deepcopy
from .schemas import require


def knowledge(state: dict, task_id: str, spec_hash: str, commit_sha: str | None,
              *, now: float, hot_limit: int = 16):
    require(type(hot_limit) is int and hot_limit >= 0, "INVALID_HOT_LIMIT")
    history = [n for n in state["notes"].values() if n["task_id"] == task_id and n["spec_hash"] == spec_hash]
    active = [n for n in history if n["type"] != "CLAIM" or n["expires_at"] > now]
    failures = {(n["commit_sha"], n["test_id"]) for n in history if n["type"] == "FAIL"}
    visible, seen = [], set()
    for note in active:
        key = (note["type"], note["task_id"], note["spec_hash"], note["commit_sha"],
               note["test_id"], note["summary"], tuple(note["evidence_refs"]))
        if key in seen:
            continue
        seen.add(key)
        item = deepcopy(note)
        item["candidate_status"] = ("RECHECK_REQUIRED" if note["type"] == "PATCH_SUMMARY"
            and (note["commit_sha"], note["test_id"]) in failures else "PROPOSED")
        if note["commit_sha"] is None or note["commit_sha"] == commit_sha:
            visible.append(item)
    return {"hot": visible[-hot_limit:] if hot_limit else [],
            "warm": [n for n in visible if n["type"] in {"FAIL", "CLAIM"}],
            "cold_note_ids": [n["note_id"] for n in history]}
