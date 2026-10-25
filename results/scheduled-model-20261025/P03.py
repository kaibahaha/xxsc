"""Solution for P03: deterministic capacity-constrained wave scheduling."""


def _is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def schedule(jobs: list[dict], completed: list[str], capacity: int) -> dict:
    """Validate the full DAG and schedule unfinished jobs in greedy waves."""
    if not _is_int(capacity) or capacity <= 0:
        raise ValueError("capacity must be a positive integer")
    if not isinstance(jobs, list):
        raise ValueError("jobs must be a list")
    if not isinstance(completed, list):
        raise ValueError("completed must be a list")

    required = {"id", "depends", "cost", "priority"}
    job_by_id = {}
    for job in jobs:
        if not isinstance(job, dict) or not required.issubset(job):
            raise ValueError("each job must contain all required fields")
        job_id = job["id"]
        depends = job["depends"]
        cost = job["cost"]
        priority = job["priority"]
        if not isinstance(job_id, str) or not job_id:
            raise ValueError("job id must be a non-empty string")
        if job_id in job_by_id:
            raise ValueError("job ids must be unique")
        if not isinstance(depends, list):
            raise ValueError("depends must be a list")
        seen_dependencies = set()
        for dependency in depends:
            if not isinstance(dependency, str) or not dependency:
                raise ValueError("dependency ids must be non-empty strings")
            if dependency in seen_dependencies:
                raise ValueError("dependencies must not contain duplicates")
            seen_dependencies.add(dependency)
        if not _is_int(cost) or not 1 <= cost <= capacity:
            raise ValueError("cost must be an integer from 1 through capacity")
        if not _is_int(priority):
            raise ValueError("priority must be an integer")
        job_by_id[job_id] = job

    all_ids = set(job_by_id)
    for job_id, job in job_by_id.items():
        for dependency in job["depends"]:
            if dependency not in all_ids or dependency == job_id:
                raise ValueError("dependencies must reference other defined jobs")

    completed_ids = set()
    for job_id in completed:
        if not isinstance(job_id, str) or not job_id or job_id not in all_ids:
            raise ValueError("completed ids must reference defined jobs")
        if job_id in completed_ids:
            raise ValueError("completed must not contain duplicates")
        completed_ids.add(job_id)

    # Kahn's algorithm checks the entire graph, including completed jobs.
    indegree = {job_id: len(job["depends"]) for job_id, job in job_by_id.items()}
    successors = {job_id: [] for job_id in job_by_id}
    for job_id, job in job_by_id.items():
        for dependency in job["depends"]:
            successors[dependency].append(job_id)
    ready = [job_id for job_id, degree in indegree.items() if degree == 0]
    visited = 0
    while ready:
        job_id = ready.pop()
        visited += 1
        for successor in successors[job_id]:
            indegree[successor] -= 1
            if indegree[successor] == 0:
                ready.append(successor)
    if visited != len(job_by_id):
        raise ValueError("the dependency graph must be acyclic")

    done = set(completed_ids)
    remaining = all_ids - done
    waves = []
    while remaining:
        candidates = [
            job_by_id[job_id]
            for job_id in remaining
            if all(dependency in done for dependency in job_by_id[job_id]["depends"])
        ]
        candidates.sort(key=lambda job: (-job["priority"], job["id"]))

        selected = []
        load = 0
        for job in candidates:
            if load + job["cost"] <= capacity:
                selected.append(job["id"])
                load += job["cost"]
        if not selected:
            raise ValueError("remaining jobs cannot be scheduled")

        waves.append({"job_ids": selected, "load": load})
        done.update(selected)
        remaining.difference_update(selected)

    return {"waves": waves, "total_waves": len(waves)}
