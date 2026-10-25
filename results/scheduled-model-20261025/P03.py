"""P03 - 带依赖与容量上限的确定性批调度.

SCHED-CODE-20261025-BLIND-T5-R2
Deliverable: results/scheduled-model-20261025/P03.py
Entrypoint : schedule(jobs, completed, capacity) -> dict

仅使用 Python 3.11 标准库。
"""

from __future__ import annotations

_REQUIRED_FIELDS = ("id", "depends", "cost", "priority")


def _is_real_int(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _is_non_empty_str(value) -> bool:
    return isinstance(value, str) and value != ""


def _validate(jobs, completed, capacity):
    """Validate inputs and return (job_specs, completed_set, capacity).

    job_specs maps job id -> (cost, priority, depends tuple).
    """
    if not isinstance(jobs, list):
        raise ValueError("jobs must be a list")
    if not isinstance(completed, list):
        raise ValueError("completed must be a list")
    if not _is_real_int(capacity) or capacity <= 0:
        raise ValueError("capacity must be a positive integer (bool rejected)")

    specs: dict = {}
    for index, job in enumerate(jobs):
        if not isinstance(job, dict):
            raise ValueError("jobs[%d] must be a dict" % index)
        for field in _REQUIRED_FIELDS:
            if field not in job:
                raise ValueError("jobs[%d] is missing required field %r" % (index, field))

        job_id = job["id"]
        depends = job["depends"]
        cost = job["cost"]
        priority = job["priority"]

        if not _is_non_empty_str(job_id):
            raise ValueError("jobs[%d].id must be a non-empty string" % index)
        if job_id in specs:
            raise ValueError("duplicate job id %r" % (job_id,))

        if not isinstance(depends, list):
            raise ValueError("jobs[%d].depends must be a list" % index)
        seen_deps = set()
        for dep in depends:
            if not _is_non_empty_str(dep):
                raise ValueError("jobs[%d].depends entries must be non-empty strings" % index)
            if dep in seen_deps:
                raise ValueError("jobs[%d].depends contains duplicate entry %r" % (index, dep))
            seen_deps.add(dep)

        if not _is_real_int(cost):
            raise ValueError("jobs[%d].cost must be an integer (bool rejected)" % index)
        if cost < 1 or cost > capacity:
            raise ValueError("jobs[%d].cost must satisfy 1 <= cost <= capacity" % index)
        if not _is_real_int(priority):
            raise ValueError("jobs[%d].priority must be an integer (bool rejected)" % index)

        specs[job_id] = (cost, priority, tuple(depends))

    # ---- validate depends references / self loops -------------------------
    for job_id, (_cost, _priority, depends) in specs.items():
        for dep in depends:
            if dep == job_id:
                raise ValueError("job %r depends on itself" % (job_id,))
            if dep not in specs:
                raise ValueError("job %r depends on undefined job %r" % (job_id, dep))

    # ---- validate completed ----------------------------------------------
    completed_set = set()
    for entry in completed:
        if not _is_non_empty_str(entry):
            raise ValueError("completed entries must be non-empty strings")
        if entry in completed_set:
            raise ValueError("completed contains duplicate entry %r" % (entry,))
        if entry not in specs:
            raise ValueError("completed references undefined job %r" % (entry,))
        completed_set.add(entry)

    # ---- the whole dependency graph must be acyclic -----------------------
    _assert_acyclic(specs)

    return specs, completed_set, capacity


def _assert_acyclic(specs):
    """Kahn's algorithm over the full graph; any remaining node means a cycle."""
    indegree = {job_id: 0 for job_id in specs}
    dependents: dict = {job_id: [] for job_id in specs}
    for job_id, (_cost, _priority, depends) in specs.items():
        for dep in depends:
            dependents[dep].append(job_id)
            indegree[job_id] += 1

    queue = [job_id for job_id in specs if indegree[job_id] == 0]
    processed = 0
    while queue:
        node = queue.pop()
        processed += 1
        for child in dependents[node]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)

    if processed != len(specs):
        remaining = sorted(job_id for job_id in specs if indegree[job_id] > 0)
        raise ValueError("dependency graph contains a cycle involving %r" % (remaining,))


def schedule(jobs, completed, capacity):
    """Deterministic wave scheduler with dependencies and a capacity budget.

    Each wave considers jobs that are not yet done and whose dependencies were
    already done *before* the wave started (jobs picked in the current wave do
    not unlock their dependents until the next wave).  Candidates are ordered
    by ``(-priority, id)`` and greedily packed: a job that does not fit the
    remaining capacity is skipped and the sweep continues with the following
    candidates.

    Complexity: O(V + E) for validation plus O(W * (V log V)) for the wave
    sweep (W waves, each sorting the candidate set); space O(V + E).
    Inputs are never mutated.
    """
    specs, done, capacity = _validate(jobs, completed, capacity)

    waves = []
    remaining = set(specs) - done

    while remaining:
        # Candidates: dependencies satisfied before this wave starts.
        candidates = [
            job_id
            for job_id in remaining
            if all(dep in done for dep in specs[job_id][2])
        ]
        candidates.sort(key=lambda job_id: (-specs[job_id][1], job_id))

        chosen = []
        load = 0
        for job_id in candidates:
            cost = specs[job_id][0]
            if load + cost <= capacity:
                chosen.append(job_id)
                load += cost

        if not chosen:
            raise ValueError(
                "no schedulable job: %d job(s) remain but none fits capacity %d"
                % (len(remaining), capacity)
            )

        waves.append({"job_ids": chosen, "load": load})
        # Jobs chosen here only count as done for the *next* wave.
        done = done | set(chosen)
        remaining = remaining - set(chosen)

    return {"waves": waves, "total_waves": len(waves)}


if __name__ == "__main__":  # pragma: no cover - manual smoke check
    sample = [
        {"id": "a", "depends": [], "cost": 2, "priority": 5},
        {"id": "b", "depends": [], "cost": 2, "priority": 4},
        {"id": "c", "depends": ["a"], "cost": 1, "priority": 10},
        {"id": "d", "depends": [], "cost": 1, "priority": 3},
    ]
    print(schedule(sample, [], 3))
