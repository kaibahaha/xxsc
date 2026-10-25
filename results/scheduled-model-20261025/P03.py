"""Deterministic wave scheduling for a capacity-constrained DAG."""

from collections import deque


def schedule(jobs: list[dict], completed: list[str], capacity: int) -> dict:
    """Validate all jobs, reject cycles, then greedily schedule ready jobs by wave.

    With V jobs and E dependencies: O(V(V+E) + V^2 log V) worst-case
    time using per-wave scans and sorts; O(V+E) auxiliary space.
    """
    if (type(jobs) is not list or type(completed) is not list or
            type(capacity) is not int or capacity <= 0):
        raise ValueError("invalid jobs, completed, or capacity")

    indexed = {}
    for job in jobs:
        if type(job) is not dict or any(
                field not in job for field in ("id", "depends", "cost", "priority")):
            raise ValueError("invalid job structure")
        job_id = job["id"]
        deps = job["depends"]
        cost, priority = job["cost"], job["priority"]
        if (type(job_id) is not str or not job_id or job_id in indexed or
                type(deps) is not list or
                type(cost) is not int or not 1 <= cost <= capacity or
                type(priority) is not int):
            raise ValueError("invalid job fields or duplicate id")
        if any(type(d) is not str or not d for d in deps) or len(set(deps)) != len(deps):
            raise ValueError("invalid or duplicate dependency")
        indexed[job_id] = job

    for job in jobs:
        if any(dep not in indexed for dep in job["depends"]):
            raise ValueError("dependency refers to an unknown job")

    if any(type(x) is not str or not x for x in completed):
        raise ValueError("invalid completed job id")
    if len(set(completed)) != len(completed) or any(x not in indexed for x in completed):
        raise ValueError("unknown or repeated completed job id")

    # Check the *whole* dependency graph, including precompleted jobs.
    indegree = {job_id: len(job["depends"]) for job_id, job in indexed.items()}
    successors = {job_id: [] for job_id in indexed}
    for job in jobs:
        for dep in job["depends"]:
            successors[dep].append(job["id"])
    ready = deque(job_id for job_id, degree in indegree.items() if degree == 0)
    visited = 0
    while ready:
        job_id = ready.popleft()
        visited += 1
        for nxt in successors[job_id]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                ready.append(nxt)
    if visited != len(indexed):
        raise ValueError("cyclic dependency graph")

    done = set(completed)
    waves = []
    while len(done) < len(indexed):
        candidates = [job for job in jobs
                      if job["id"] not in done and
                      all(dep in done for dep in job["depends"])]
        candidates.sort(key=lambda job: (-job["priority"], job["id"]))
        chosen = []
        load = 0
        for job in candidates:
            if load + job["cost"] <= capacity:
                chosen.append(job["id"])
                load += job["cost"]
        if not chosen:
            raise ValueError("unable to schedule any remaining job")
        waves.append({"job_ids": chosen, "load": load})
        done.update(chosen)  # Unlocks successors only in the *next* wave.
    return {"waves": waves, "total_waves": len(waves)}
