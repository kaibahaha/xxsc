"""State transition policy and dependency checks."""
from .schemas import require

TRANSITIONS = {
    "CLAIMED": {"RUNNING"}, "RUNNING": {"SUBMITTED", "BLOCKED", "FAILED"},
    "SUBMITTED": {"QA_PENDING"}, "QA_PENDING": {"QA_GREEN", "FAILED"},
    "QA_GREEN": {"REVIEW_APPROVED"}, "REVIEW_APPROVED": {"INTEGRATION_VERIFIED"},
    "INTEGRATION_VERIFIED": {"DONE"}, "BLOCKED": {"READY"}, "FAILED": {"READY"},
    "READY": set(), "DONE": set(),
}
GATE_ACTIONS = {"QA_GREEN": "qa", "REVIEW_APPROVED": "review", "INTEGRATION_VERIFIED": "integrate", "DONE": "accept"}


def validate_dag(tasks):
    visiting, visited = set(), set()
    def visit(task_id):
        require(task_id in tasks, "MISSING_DEPENDENCY")
        require(task_id not in visiting, "DAG_CYCLE")
        if task_id in visited:
            return
        visiting.add(task_id)
        for dependency in tasks[task_id]["dependencies"]:
            visit(dependency)
        visiting.remove(task_id)
        visited.add(task_id)
    for task_id in tasks:
        visit(task_id)


def dependencies_done(task, tasks):
    return all(tasks[d]["status"] == "DONE" for d in task["dependencies"])


def fence(task, attempt_id, epoch, now):
    lease = task.get("lease")
    require(lease is not None and lease["attempt_id"] == attempt_id
            and lease["fencing_epoch"] == epoch and lease["expires_at"] > now, "LATE_STALE_ATTEMPT")
    return lease


def invalidate(task):
    task["fencing_epoch"] += 1
    task["version"] += 1
    task["lease"] = None
    if task["status"] != "DONE":
        task["status"] = "READY"
        task["candidate_commit"] = None
        task["author"] = None
        task["qa_evidence"] = None


def expire_tasks(state, now):
    for task in state["tasks"].values():
        if task.get("lease") and task["lease"]["expires_at"] <= now:
            invalidate(task)
