"""Generate valid pool configurations for N=2..20.

Used by tests and by ``agl gen-pool`` to prove the registry has no hard-coded
five-agent ceiling. These are *test fixtures*, not authorisation to run them:
every generated agent starts as PENDING_PROBE unless ``admission`` is overridden.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PROVIDER_DEFAULTS = {
    "chatgpt": {"interval_minutes": 60, "slot_budget_example": 5, "reserved_other_use": 2,
                "account_scope": "chatgpt-main"},
    "workbuddy": {"interval_minutes": 20, "capacity": None, "account_scope": "workbuddy-main"},
    "codex": {"interval_minutes": None, "capacity": None, "account_scope": "codex-main"},
}

CAPABILITY_SETS = {
    "chatgpt": ["research", "requirements", "review", "code_draft"],
    "workbuddy": ["code_execution", "test_run", "git_write"],
    "codex": ["architecture", "complex_coding", "review"],
}


def _split(n: int, mix: dict[str, int] | None) -> dict[str, int]:
    if mix:
        total = sum(mix.values())
        if total != n:
            raise ValueError(f"mix totals {total} but n={n}")
        return dict(mix)
    # default: spread across three providers, chatgpt first
    order = ["chatgpt", "workbuddy", "codex"]
    out = {p: 0 for p in order}
    for i in range(n):
        out[order[i % len(order)]] += 1
    return out


def build_pool(
    n: int,
    *,
    mix: dict[str, int] | None = None,
    admission: str = "ADMITTED_ACTIVE",
    project_id: str = "AGL-TEST-POOL",
    repo: str = "kaibahaha/xxsc",
    ref: str = "exp/agensh-lite-v4.2-controller-mvp-20261025",
    runtime_root: str | None = None,
) -> dict[str, Any]:
    counts = _split(n, mix)
    agents: list[dict[str, Any]] = []
    for provider, count in counts.items():
        if count == 0:
            continue
        defaults = PROVIDER_DEFAULTS.get(provider, {"account_scope": f"{provider}-main"})
        caps = CAPABILITY_SETS.get(provider, ["code_execution"])
        for i in range(count):
            agent_id = f"{provider.upper()}_{i + 1:02d}"
            agents.append({
                "agent_id": agent_id,
                "provider_id": provider,
                "account_scope": defaults["account_scope"],
                "adapter_id": "github_mailbox",
                "enabled": True,
                "agent_kind": "scheduled_or_triggered",
                "runtime_mode": "scheduled",
                "capabilities": list(caps),
                "preferred_domains": [],
                "outbox": f"05_outbox/{agent_id}",
                "max_inflight_tasks": 1,
                "schedule_id": None,
                "trigger_type": "scheduled" if provider != "codex" else "manual_or_scheduled",
                "admission_status": admission,
                "timezone": "Asia/Shanghai",
            })
    schedules = {}
    for provider, count in counts.items():
        if count == 0:
            continue
        entry = dict(PROVIDER_DEFAULTS.get(provider, {"account_scope": f"{provider}-main"}))
        entry["capacity_verified"] = False
        entry["real_schedule_status"] = "UNVERIFIED"
        entry["user_approval_required"] = True
        schedules[provider] = entry
    return {
        "schema_version": "1.0",
        "project_id": project_id,
        "mode": "shadow",
        "repo": repo,
        "ref": ref,
        "runtime_root": runtime_root or f"factory/projects/{project_id}",
        "timezone": "Asia/Shanghai",
        "pool": {
            "min_active": 2,
            "active_agent_ids": [a["agent_id"] for a in agents],
            "offset_policy": "per_provider_schedule",
            "allow_agent_join_leave": True,
            "max_primary_tasks_per_run": 1,
            "limit_policy": "no_fixed_global_max",
            "admission_required": True,
            "active_agent_ids_meaning": "desired_enabled_only_not_verified_runtime_active",
        },
        "agents": agents,
        "controller": {
            "backend_preference": "git_cas",
            "lease_mode": "atomic_controller_only",
            "allow_unverified_claim_as_lock": False,
            "projection_single_writer": True,
            "admission_required_for_new_lease": True,
        },
        "provider_schedules": schedules,
        "registry_version": "2.0",
    }


def save_pool(n: int, path: str | Path, **kwargs: Any) -> dict[str, Any]:
    cfg = build_pool(n, **kwargs)
    Path(path).write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return cfg
