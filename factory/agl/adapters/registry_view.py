"""Adapter-side view over the agent registry configuration.

This is **not** M01. M01 (Codex) owns authoritative schema validation. This
module is the adapter plane's defensive preflight: it must fail closed when the
config is unsafe, and it must never upgrade an unverified capability to a
usable one. When Codex's ``agl.config`` is importable the CLI reports that the
core validator exists and defers to it for schema-level acceptance
(``--core-validation``), while still running these adapter invariants.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from ..errors import AglError, ErrorCode
from .types import AdmissionDecision

PROTECTED_REFS = {"main", "master"}
ADMISSION_ACTIVE = "ADMITTED_ACTIVE"
ADMISSION_TERMINAL = {"UNAVAILABLE", "DRAINING", "REJECTED"}


@dataclass(frozen=True)
class AgentRecord:
    agent_id: str
    provider_id: str
    account_scope: str
    adapter_id: str
    enabled: bool
    capabilities: tuple[str, ...]
    preferred_domains: tuple[str, ...]
    allowed_reads: tuple[str, ...]
    allowed_writes: tuple[str, ...]
    outbox: str
    max_inflight: int
    trigger_type: str
    admission_status: str
    schedule_id: str | None
    timezone: str
    cadence_minutes: int | None
    runtime_mode: str
    agent_kind: str
    raw: dict[str, Any] = field(default_factory=dict, compare=False)

    @property
    def state(self) -> str:
        if not self.enabled:
            return "DISABLED"
        return self.admission_status

    def as_dict(self) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "provider_id": self.provider_id,
            "account_scope": self.account_scope,
            "adapter_id": self.adapter_id,
            "enabled": self.enabled,
            "capabilities": list(self.capabilities),
            "allowed_reads": list(self.allowed_reads),
            "allowed_writes": list(self.allowed_writes),
            "outbox": self.outbox,
            "max_inflight": self.max_inflight,
            "trigger_type": self.trigger_type,
            "admission_status": self.admission_status,
            "state": self.state,
            "schedule_id": self.schedule_id,
            "timezone": self.timezone,
            "cadence_minutes": self.cadence_minutes,
            "runtime_mode": self.runtime_mode,
            "agent_kind": self.agent_kind,
        }


@dataclass
class ValidationIssue:
    code: str
    message: str
    agent_id: str | None = None
    severity: str = "error"

    def as_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "message": self.message,
            "agent_id": self.agent_id,
            "severity": self.severity,
        }


@dataclass
class ValidationReport:
    ok: bool
    issues: list[ValidationIssue]
    pool_size: int
    providers: dict[str, int]
    active_ids: list[str]

    def errors(self) -> list[ValidationIssue]:
        return [i for i in self.issues if i.severity == "error"]

    def warnings(self) -> list[ValidationIssue]:
        return [i for i in self.issues if i.severity == "warning"]

    def as_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "pool_size": self.pool_size,
            "providers": self.providers,
            "active_ids": self.active_ids,
            "errors": [i.as_dict() for i in self.errors()],
            "warnings": [i.as_dict() for i in self.warnings()],
        }


class RegistryView:
    def __init__(
        self,
        project_id: str,
        repo: str,
        ref: str,
        runtime_root: str,
        timezone: str,
        min_active: int,
        active_ids: tuple[str, ...],
        agents: dict[str, AgentRecord],
        provider_schedules: dict[str, dict[str, Any]],
        raw: dict[str, Any],
        issues: list[ValidationIssue] | None = None,
    ) -> None:
        self.project_id = project_id
        self.repo = repo
        self.ref = ref
        self.runtime_root = runtime_root.strip("/")
        self.timezone = timezone
        self.min_active = min_active
        self.active_ids = active_ids
        self.agents = agents
        self.provider_schedules = provider_schedules
        self.raw = raw
        self.issues = issues or []

    # -- construction -------------------------------------------------------#
    @classmethod
    def from_config(cls, cfg: dict[str, Any]) -> "RegistryView":
        report = validate_config(cfg)
        if not report.ok:
            first = report.errors()[0]
            raise AglError(
                ErrorCode(first.code if first.code in ErrorCode.__members__ else "SCHEMA_INVALID"),
                f"{first.code}: {first.message}",
                {"issues": [i.as_dict() for i in report.errors()]},
            )
        return cls._build(cfg, report.issues)

    @classmethod
    def load(cls, path: str | Path) -> "RegistryView":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls.from_config(data)

    @classmethod
    def _build(cls, cfg: dict[str, Any], issues: list[ValidationIssue]) -> "RegistryView":
        tz = cfg.get("timezone", "UTC")
        schedules = cfg.get("provider_schedules", {}) or {}
        agents: dict[str, AgentRecord] = {}
        for raw in cfg.get("agents", []):
            provider = str(raw["provider_id"])
            pcfg = schedules.get(provider, {}) or {}
            agent_id = str(raw["agent_id"])
            outbox = str(raw.get("outbox") or f"05_outbox/{agent_id}")
            allowed_writes = tuple(raw.get("allowed_writes") or [outbox])
            allowed_reads = tuple(raw.get("allowed_reads") or ["01_tasks", "03_events", "07_receipts", "08_projections"])
            agents[agent_id] = AgentRecord(
                agent_id=agent_id,
                provider_id=provider,
                account_scope=str(raw.get("account_scope") or f"{provider}-main"),
                adapter_id=str(raw.get("adapter_id") or "github_mailbox"),
                enabled=bool(raw.get("enabled", False)),
                capabilities=tuple(raw.get("capabilities") or ()),
                preferred_domains=tuple(raw.get("preferred_domains") or ()),
                allowed_reads=allowed_reads,
                allowed_writes=allowed_writes,
                outbox=outbox,
                max_inflight=int(raw.get("max_inflight_tasks", raw.get("max_inflight", 1)) or 1),
                trigger_type=str(raw.get("trigger_type") or (pcfg.get("schedule_policy") or "scheduled")),
                admission_status=str(raw.get("admission_status") or "PENDING_PROBE"),
                schedule_id=raw.get("schedule_id"),
                timezone=str(raw.get("timezone") or pcfg.get("timezone") or tz),
                cadence_minutes=(
                    int(raw["cadence_minutes"]) if raw.get("cadence_minutes") is not None
                    else (int(pcfg["interval_minutes"]) if pcfg.get("interval_minutes") is not None else None)
                ),
                runtime_mode=str(raw.get("runtime_mode") or raw.get("agent_kind") or "scheduled"),
                agent_kind=str(raw.get("agent_kind") or "scheduled_contributor"),
                raw=raw,
            )
        pool = cfg.get("pool", {}) or {}
        return cls(
            project_id=str(cfg.get("project_id") or "UNKNOWN"),
            repo=str(cfg.get("repo") or ""),
            ref=str(cfg.get("ref") or ""),
            runtime_root=str(cfg.get("runtime_root") or "factory/projects/UNKNOWN"),
            timezone=str(tz),
            min_active=int(pool.get("min_active", 2)),
            active_ids=tuple(pool.get("active_agent_ids") or ()),
            agents=agents,
            provider_schedules=schedules,
            raw=cfg,
            issues=issues,
        )

    # -- queries ------------------------------------------------------------#
    def enabled_agents(self) -> list[AgentRecord]:
        return [a for a in self.agents.values() if a.enabled]

    def get(self, agent_id: str) -> AgentRecord:
        if agent_id not in self.agents:
            raise AglError(ErrorCode.NOT_FOUND, f"unknown agent_id: {agent_id}")
        return self.agents[agent_id]

    def by_provider(self, provider_id: str) -> list[AgentRecord]:
        return [a for a in self.enabled_agents() if a.provider_id == provider_id]

    def providers(self) -> list[str]:
        return sorted({a.provider_id for a in self.enabled_agents()})

    @property
    def pool_size(self) -> int:
        return len(self.enabled_agents())

    def admission(self, agent_id: str) -> AdmissionDecision:
        rec = self.agents.get(agent_id)
        if rec is None:
            return AdmissionDecision(agent_id, False, "UNKNOWN", "UNKNOWN_AGENT")
        if not rec.enabled:
            return AdmissionDecision(agent_id, False, "DISABLED", "AGENT_DISABLED")
        if rec.admission_status in ADMISSION_TERMINAL:
            return AdmissionDecision(agent_id, False, rec.admission_status, f"ADMISSION_{rec.admission_status}")
        if rec.admission_status != ADMISSION_ACTIVE:
            return AdmissionDecision(
                agent_id, False, rec.admission_status,
                "PROBE_PENDING_ADMISSION" if rec.admission_status != "REGISTERED" else "NOT_PROBED",
            )
        return AdmissionDecision(agent_id, True, ADMISSION_ACTIVE, "ADMITTED")

    def can_write(self, agent_id: str, path: str) -> bool:
        rec = self.get(agent_id)
        p = path.strip("/")
        return any(p == w or p.startswith(w.strip("/") + "/") for w in rec.allowed_writes)

    def provider_capacity(self, provider_id: str) -> dict[str, Any]:
        pcfg = self.provider_schedules.get(provider_id, {}) or {}
        capacity = pcfg.get("capacity")
        if capacity is None and pcfg.get("slot_budget_example") is not None:
            capacity = int(pcfg["slot_budget_example"]) - int(pcfg.get("reserved_other_use") or 0)
        return {
            "provider_id": provider_id,
            "capacity": capacity,
            "capacity_verified": bool(pcfg.get("capacity_verified", False)),
            "used": len(self.by_provider(provider_id)),
            "state": "VERIFIED" if pcfg.get("capacity_verified") else "UNVERIFIED",
        }

    def eligible_agents(self, capability: str | None = None) -> list[AgentRecord]:
        out = []
        for rec in self.enabled_agents():
            if self.admission(rec.agent_id).allowed and (
                capability is None or capability in rec.capabilities
            ):
                out.append(rec)
        return out

    def as_dict(self) -> dict[str, Any]:
        return {
            "project_id": self.project_id,
            "repo": self.repo,
            "ref": self.ref,
            "runtime_root": self.runtime_root,
            "timezone": self.timezone,
            "pool_size": self.pool_size,
            "min_active": self.min_active,
            "active_ids": list(self.active_ids),
            "providers": {p: len(self.by_provider(p)) for p in self.providers()},
            "provider_capacity": {p: self.provider_capacity(p) for p in self.providers()},
            "agents": [a.as_dict() for a in self.agents.values()],
        }


# --------------------------------------------------------------------------- #
# validation
# --------------------------------------------------------------------------- #

_REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


def validate_config(cfg: dict[str, Any]) -> ValidationReport:
    issues: list[ValidationIssue] = []

    def err(code: str, msg: str, agent_id: str | None = None) -> None:
        issues.append(ValidationIssue(code, msg, agent_id, "error"))

    def warn(code: str, msg: str, agent_id: str | None = None) -> None:
        issues.append(ValidationIssue(code, msg, agent_id, "warning"))

    if not isinstance(cfg, dict):
        err("SCHEMA_INVALID", "config root must be an object")
        return ValidationReport(False, issues, 0, {}, [])

    for key in ("schema_version", "project_id", "repo", "ref"):
        if not cfg.get(key):
            err("SCHEMA_INVALID", f"missing required top-level field: {key}")

    repo = str(cfg.get("repo") or "")
    if repo and not _REPO_RE.match(repo):
        err("SCHEMA_INVALID", f"repo must be 'owner/name', got {repo!r}")

    ref = str(cfg.get("ref") or "")
    if ref in PROTECTED_REFS:
        err("NO_PERMISSION", f"ref {ref!r} is protected; adapters may not bind to it")

    tz = str(cfg.get("timezone") or "")
    if tz:
        try:
            ZoneInfo(tz)
        except (ZoneInfoNotFoundError, ValueError):
            err("INVALID_TIMEZONE", f"unknown timezone {tz!r}")

    agents_raw = cfg.get("agents")
    if not isinstance(agents_raw, list) or not agents_raw:
        err("SCHEMA_INVALID", "agents must be a non-empty list")
        return ValidationReport(False, issues, 0, {}, [])

    seen: dict[str, int] = {}
    for idx, raw in enumerate(agents_raw):
        if not isinstance(raw, dict):
            err("SCHEMA_INVALID", f"agents[{idx}] must be an object")
            continue
        aid = raw.get("agent_id")
        if not aid:
            err("SCHEMA_INVALID", f"agents[{idx}] missing agent_id")
            continue
        seen[str(aid)] = seen.get(str(aid), 0) + 1

    duplicates = sorted(a for a, n in seen.items() if n > 1)
    for dup in duplicates:
        err("DUPLICATE_AGENT_ID", f"agent_id {dup!r} appears {seen[dup]} times", dup)

    provider_counts: dict[str, int] = {}
    for raw in agents_raw:
        if not isinstance(raw, dict) or not raw.get("agent_id"):
            continue
        aid = str(raw["agent_id"])
        provider = raw.get("provider_id")
        if not provider:
            err("SCHEMA_INVALID", "provider_id is required", aid)
            continue
        if not raw.get("capabilities"):
            err("SCHEMA_INVALID", "capabilities must be non-empty", aid)
        atz = str(raw.get("timezone") or tz)
        if atz:
            try:
                ZoneInfo(atz)
            except (ZoneInfoNotFoundError, ValueError):
                err("INVALID_TIMEZONE", f"unknown timezone {atz!r}", aid)
        outbox = str(raw.get("outbox") or "")
        if outbox and not outbox.strip("/").startswith(f"05_outbox/{aid}"):
            err(
                "PATH_NOT_WHITELISTED",
                f"outbox {outbox!r} must live under 05_outbox/{aid}/",
                aid,
            )
        if raw.get("enabled"):
            provider_counts[str(provider)] = provider_counts.get(str(provider), 0) + 1

    pool = cfg.get("pool", {}) or {}
    active = [str(x) for x in (pool.get("active_agent_ids") or [])]
    enabled_ids = sorted({str(r["agent_id"]) for r in agents_raw if isinstance(r, dict) and r.get("enabled") and r.get("agent_id")})
    if sorted(active) != enabled_ids:
        err(
            "ACTIVE_MISMATCH",
            f"active_agent_ids {sorted(active)} != enabled agents {enabled_ids}",
        )

    min_active = int(pool.get("min_active", 2))
    if len(enabled_ids) < max(2, min_active):
        err(
            "N_TOO_SMALL",
            f"pool N={len(enabled_ids)} is below required minimum {max(2, min_active)}",
        )

    if pool.get("limit_policy") not in (None, "no_fixed_global_max"):
        warn("LIMIT_POLICY", f"unexpected limit_policy {pool.get('limit_policy')!r}")

    schedules = cfg.get("provider_schedules", {}) or {}
    for provider, used in provider_counts.items():
        pcfg = schedules.get(provider, {}) or {}
        capacity = pcfg.get("capacity")
        if capacity is None and pcfg.get("slot_budget_example") is not None:
            capacity = int(pcfg["slot_budget_example"]) - int(pcfg.get("reserved_other_use") or 0)
        if capacity is None:
            warn("QUOTA_UNVERIFIED", f"{provider}: quota unknown; must not be treated as unlimited")
            continue
        if pcfg.get("capacity_verified"):
            if used > int(capacity):
                err(
                    "PROVIDER_QUOTA_EXCEEDED",
                    f"{provider}: {used} enabled agents exceed verified capacity {capacity}",
                )
        else:
            warn(
                "QUOTA_UNVERIFIED",
                f"{provider}: capacity {capacity} not verified; {used} agents enabled (advisory only)",
            )
        reserved = pcfg.get("reserved_other_use")
        if reserved and used + int(reserved) > int(pcfg.get("slot_budget_example", capacity)):
            warn(
                "QUOTA_RESERVED_OVERLAP",
                f"{provider}: enabled {used} + reserved {reserved} exceeds declared budget",
            )

    for provider, pcfg in schedules.items():
        iv = pcfg.get("interval_minutes")
        if iv is not None and int(iv) <= 0:
            err("SCHEMA_INVALID", f"{provider}: interval_minutes must be > 0")

    ok = not any(i.severity == "error" for i in issues)
    return ValidationReport(ok, issues, len(enabled_ids), provider_counts, sorted(active))
