"""M06 -- dynamic poll + per-provider scheduling.

Two responsibilities:

1. **Planning** (``PollPlanner.plan`` / ``schedule_manifest``): compute each
   provider's own cadence and an offset table. Offsets are computed *inside* a
   provider sub-pool, never across the global pool: the workorder explicitly
   forbids using ``60/N`` on a heterogeneous pool. ChatGPT's K slots use the
   documented schedule (K=2 -> :00/:30, K=5 -> :00/:12/:24/:36/:48, ...).
   Nothing here creates a real platform schedule; the manifest is a proposal a
   human registers, and planned vs actual wake-ups are stored separately.

2. **Polling** (``PollPlanner.poll_once``): the 9-step wake-up of
   ``06_LIFECYCLE_AND_HANDOFF.md``, fail-closed:
   disabled / unadmitted / draining agents cannot claim; an unreadable BOARD is
   ``BOARD_UNKNOWN`` (never "empty board"); without Controller the output is a
   CLAIM_PROPOSED (a proposal), never a lease.
"""

from __future__ import annotations

import importlib.util
import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any
from zoneinfo import ZoneInfo

from .adapters.github_mailbox import AdapterContext
from .adapters.providers import build_adapter
from .adapters.registry_view import AgentRecord, RegistryView
from .errors import AglError, ErrorCode
from .storage.github import GitHubStorage, canonical_json_bytes, utc_now
from .storage.ledger import EventLedger


def compute_offsets(k: int, cadence_minutes: int = 60) -> list[int]:
    """Equal-spaced offsets for ``k`` slots of one provider.

    Exact division uses integer spacing; otherwise minutes are rounded and
    de-duplicated (``QUANTIZED`` in the manifest), never rejected.
    """
    if k < 1:
        raise AglError(ErrorCode.INVALID_INPUT, f"slot count must be >= 1, got {k}")
    if cadence_minutes < k:
        raise AglError(
            ErrorCode.INVALID_INPUT,
            f"cadence {cadence_minutes}min cannot host {k} non-overlapping slots",
        )
    if cadence_minutes % k == 0:
        step = cadence_minutes // k
        return [i * step for i in range(k)]
    offsets: list[int] = []
    for i in range(k):
        minute = int(round(i * cadence_minutes / k))
        if minute not in offsets:
            offsets.append(minute)
    return offsets


def core_available(module: str) -> bool:
    """Detect a Codex-owned core module without importing/executing it."""
    try:
        return importlib.util.find_spec(f"agl.{module}") is not None
    except (ImportError, ValueError):
        return False


@dataclass(frozen=True)
class ScheduleSlot:
    agent_id: str
    provider_id: str
    account_scope: str
    cadence_minutes: int | None
    offset_minutes: int | None
    minute_in_hour: int | None
    timezone: str
    schedule_id: str | None
    planned_next_utc: str | None
    source: str
    note: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "provider_id": self.provider_id,
            "account_scope": self.account_scope,
            "cadence_minutes": self.cadence_minutes,
            "offset_minutes": self.offset_minutes,
            "minute_in_hour": self.minute_in_hour,
            "timezone": self.timezone,
            "schedule_id": self.schedule_id,
            "planned_next_utc": self.planned_next_utc,
            "source": self.source,
            "note": self.note,
            "verified": False,
        }


@dataclass
class PollOutcome:
    run_id: str
    agent_id: str
    provider_id: str
    status: str                      # DRY_RUN | CLAIM_PROPOSED | REFUSED | NO_ELIGIBLE_TASK | BOARD_UNKNOWN | RESUME_TASK
    planned_at: str
    actual_at: str
    task_id: str | None = None
    event_id: str | None = None
    claim_path: str | None = None
    controller_state: str = "CONTROLLER_UNAVAILABLE"
    admission: dict[str, Any] | None = None
    notes: list[str] = field(default_factory=list)
    ok: bool = True

    def as_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "agent_id": self.agent_id,
            "provider_id": self.provider_id,
            "status": self.status,
            "planned_at": self.planned_at,
            "actual_at": self.actual_at,
            "task_id": self.task_id,
            "event_id": self.event_id,
            "claim_path": self.claim_path,
            "controller_state": self.controller_state,
            "admission": self.admission,
            "notes": self.notes,
            "ok": self.ok,
        }


class PollPlanner:
    def __init__(
        self,
        registry: RegistryView,
        storage: GitHubStorage,
        ledger: EventLedger,
        *,
        run_id: str,
        runner_available: bool = False,
        token_present: bool = False,
        now_fn=None,
    ) -> None:
        self.registry = registry
        self.storage = storage
        self.ledger = ledger
        self.run_id = run_id
        self.runner_available = runner_available
        self.token_present = token_present
        self._now = now_fn or (lambda: datetime.now(timezone.utc))

    # -- planning -----------------------------------------------------------#
    def plan(self, provider_id: str | None = None) -> list[ScheduleSlot]:
        slots: list[ScheduleSlot] = []
        for provider in self.registry.providers():
            if provider_id and provider != provider_id:
                continue
            agents = sorted(self.registry.by_provider(provider), key=lambda a: a.agent_id)
            pcfg = self.registry.provider_schedules.get(provider, {}) or {}
            cadence = pcfg.get("interval_minutes")
            cadence = int(cadence) if cadence is not None else None
            if cadence is None:
                for rec in agents:
                    slots.append(ScheduleSlot(
                        rec.agent_id, provider, rec.account_scope, None, None, None,
                        rec.timezone, rec.schedule_id, None, "NATIVE_UNVERIFIED",
                        "cadence unknown: register in the platform UI and record the real interval",
                    ))
                continue
            offsets = compute_offsets(len(agents), cadence)
            basis = "EQUAL_SPACED_WITHIN_PROVIDER"
            for rec, offset in zip(agents, offsets):
                slots.append(ScheduleSlot(
                    rec.agent_id, provider, rec.account_scope, cadence, offset,
                    offset % 60, rec.timezone, rec.schedule_id,
                    self._next_occurrence(offset, rec.timezone), basis,
                ))
        return slots

    def _next_occurrence(self, offset_minutes: int, tz_name: str) -> str:
        now = self._now()
        try:
            tz = ZoneInfo(tz_name)
        except Exception:
            tz = timezone.utc
        local = now.astimezone(tz)
        candidate = local.replace(minute=0, second=0, microsecond=0) + timedelta(minutes=offset_minutes)
        if candidate <= local:
            candidate += timedelta(minutes=60)
        return candidate.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

    def schedule_manifest(self) -> dict[str, Any]:
        slots = self.plan()
        providers: dict[str, Any] = {}
        for slot in slots:
            bucket = providers.setdefault(slot.provider_id, {
                "cadence_minutes": slot.cadence_minutes,
                "account_scope": slot.account_scope,
                "slots": [],
                "registration_required": True,
            })
            bucket["slots"].append(slot.as_dict())
        return {
            "generated_at": utc_now(),
            "project_id": self.registry.project_id,
            "verified": False,
            "approval_required": True,
            "creates_real_schedule": False,
            "note": "This manifest is a proposal. No platform schedule is created or modified by this tool; "
                    "a human must register it and then record the real schedule_id.",
            "providers": providers,
            "offset_policy": "per_provider_schedule",
            "global_pool_size": self.registry.pool_size,
        }

    # -- polling ------------------------------------------------------------#
    def poll_once(self, agent_id: str, *, allow_write: bool = False) -> PollOutcome:
        # A retry of the same run_id must produce byte-identical events, otherwise
        # the immutable write would report a collision instead of being idempotent.
        meta = self._read_run_meta(agent_id)
        planned = meta.get("started_at") if meta else (
            self._now().isoformat(timespec="seconds").replace("+00:00", "Z")
        )
        decision = self.registry.admission(agent_id)
        rec = self.registry.agents.get(agent_id)
        provider = rec.provider_id if rec else "unknown"

        def refused(reason: str, notes: list[str] | None = None) -> PollOutcome:
            return PollOutcome(
                self.run_id, agent_id, provider, "REFUSED", planned, utc_now(), None, None,
                None, "CONTROLLER_UNAVAILABLE", decision.as_dict(), [reason] + (notes or []),
                ok=False,
            )

        if rec is None:
            return refused("UNKNOWN_AGENT")
        if not decision.allowed:
            return refused(f"ADMISSION_DENIED:{decision.reason}")

        ctx = AdapterContext(
            storage=self.storage, ledger=self.ledger, runtime_root=self.registry.runtime_root,
            run_id=self.run_id, token_present=self.token_present,
            runner_available=self.runner_available,
        )
        adapter = build_adapter(rec, ctx)
        health = adapter.health()
        if health.status == "UNAVAILABLE":
            return refused(f"AGENT_UNHEALTHY:{health.detail}")

        cursor = self.ledger.get_cursor(agent_id)
        read = adapter.read(cursor=cursor.get("cursor"))
        if not read.board_known:
            return PollOutcome(
                self.run_id, agent_id, provider, "BOARD_UNKNOWN", planned, utc_now(),
                notes=["board projection unreadable; fail closed, no new claim"],
                admission=decision.as_dict(), ok=False,
            )

        handoff = self._read_handoff(agent_id)
        if handoff and str(handoff.get("status", "")).upper() in ("OPEN", "IN_PROGRESS"):
            return PollOutcome(
                self.run_id, agent_id, provider, "RESUME_TASK", planned, utc_now(),
                task_id=handoff.get("task_id"), controller_state=self._controller_state(),
                admission=decision.as_dict(),
                notes=["existing HANDOFF still open; continue before claiming anything new"],
            )

        candidates = self._eligible_tasks(rec, read.tasks, read.tasks)
        if not candidates:
            outcome = PollOutcome(
                self.run_id, agent_id, provider, "NO_ELIGIBLE_TASK", planned, utc_now(),
                notes=["no READY task matches capabilities/permissions/dependencies"],
                admission=decision.as_dict(),
            )
            if allow_write and getattr(adapter, "supports_publish", True):
                self._write_run_record(outcome, cursor.get("cursor"))
            return outcome

        task = candidates[0]
        event = {
            "event_id": f"EV-{self.run_id}-CLAIM-{task['task_id']}",
            "project_id": self.registry.project_id,
            "task_id": task["task_id"],
            "producer": agent_id,
            "target_agents": ["CONTROLLER"],
            "kind": "CLAIM_PROPOSED",
            "source": "github",
            "observed_at": planned,
            "summary": f"{agent_id} proposes claim on {task['task_id']} (soft claim, not a lease)",
            "raw_ref": f"{self.registry.repo}@{self.storage.ref}:{task.get('path', '')}",
            "spec_hash": task.get("spec_hash"),
            "run_id": self.run_id,
        }

        event_id = event["event_id"]
        claim_path = None
        writable = bool(getattr(adapter, "supports_publish", True))
        if allow_write and writable:
            write = self.ledger.publish_outbox(agent_id, self.run_id, event)
            claim_path = write.path

        status = "DRY_RUN"
        if allow_write:
            status = "CLAIM_PROPOSED" if writable else "CLAIM_PENDING_WRITE"

        outcome = PollOutcome(
            self.run_id, agent_id, provider, status,
            planned, utc_now(), task["task_id"], event_id, claim_path,
            self._controller_state(), decision.as_dict(),
        )
        if allow_write and writable:
            self._write_run_record(outcome, cursor.get("cursor"))
        if not writable:
            outcome.notes.append(
                "provider has no write credential: proposal must be committed by a write-capable agent or operator"
            )
        return outcome

    # -- helpers ------------------------------------------------------------#
    def _controller_state(self) -> str:
        return "CORE_AVAILABLE" if core_available("controller") else "CONTROLLER_UNAVAILABLE"

    def _eligible_tasks(
        self, rec: AgentRecord, tasks: list[dict[str, Any]], all_tasks: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        by_id = {t.get("task_id"): t for t in all_tasks}
        done = {tid for tid, t in by_id.items() if str(t.get("status", "")).upper() in ("DONE", "ACCEPTED")}
        out = []
        for task in tasks:
            if str(task.get("status", "")).upper() != "READY":
                continue
            allowed = task.get("allowed_agents") or []
            if allowed and rec.agent_id not in allowed:
                continue
            needed = task.get("capabilities") or []
            if needed and not (set(needed) & set(rec.capabilities)):
                continue
            deps = task.get("dependencies") or []
            if any(dep not in done for dep in deps):
                continue
            out.append(task)
        out.sort(key=lambda t: (str(t.get("priority", "P3")), str(t.get("task_id"))))
        return out

    def _read_run_meta(self, agent_id: str) -> dict[str, Any]:
        snap = self.storage.read_file(
            f"{self.registry.runtime_root}/09_runs/{agent_id}/{self.run_id}.json"
        )
        if not snap.exists:
            return {}
        try:
            return json.loads(snap.text)
        except Exception:
            return {}

    def _read_handoff(self, agent_id: str) -> dict[str, Any] | None:
        snap = self.storage.read_file(f"{self.registry.runtime_root}/09_runs/{agent_id}/HANDOFF.json")
        if not snap.exists:
            return None
        try:
            return json.loads(snap.text)
        except Exception:
            return None

    def _write_run_record(self, outcome: PollOutcome, cursor: str | None) -> None:
        rec = self.registry.agents[outcome.agent_id]
        path = f"{self.registry.runtime_root}/09_runs/{outcome.agent_id}/{outcome.run_id}.md"
        body = "\n".join([
            f"# RUN {outcome.run_id}",
            "",
            f"- agent_id: {outcome.agent_id}",
            f"- provider_id: {outcome.provider_id}",
            f"- account_scope: {rec.account_scope}",
            f"- mode: {rec.runtime_mode}",
            f"- planned_at: {outcome.planned_at}",
            f"- actual_at: {outcome.actual_at}",
            f"- status: {outcome.status}",
            f"- task_id: {outcome.task_id or '-'}",
            f"- event_id: {outcome.event_id or '-'}",
            f"- cursor_in: {cursor or '-'}",
            f"- controller: {outcome.controller_state}",
            f"- notes: {'; '.join(outcome.notes) or '-'}",
            "",
        ])
        try:
            self.storage.write_immutable(
                path, body.encode("utf-8"), idempotency_key=f"run:{outcome.run_id}",
                message=f"run record {outcome.agent_id}/{outcome.run_id}",
            )
            try:
                self.storage.write_immutable(
                    f"{self.registry.runtime_root}/09_runs/{outcome.agent_id}/{outcome.run_id}.json",
                    canonical_json_bytes({
                        "run_id": outcome.run_id,
                        "started_at": outcome.planned_at,
                        "status": outcome.status,
                        "task_id": outcome.task_id,
                        "event_id": outcome.event_id,
                    }),
                    idempotency_key=f"run-meta:{outcome.run_id}",
                    message=f"run meta {outcome.agent_id}/{outcome.run_id}",
                )
            except AglError:
                pass
            self.storage.cas_publish_projection(
                f"{self.registry.runtime_root}/09_runs/{outcome.agent_id}/_last.json",
                canonical_json_bytes({
                    "run_id": outcome.run_id, "started_at": outcome.actual_at,
                    "status": outcome.status, "task_id": outcome.task_id,
                }),
                self.storage.read_file(
                    f"{self.registry.runtime_root}/09_runs/{outcome.agent_id}/_last.json"
                ).blob_sha,
            )
        except AglError:
            # run records are best-effort evidence; never mask the poll outcome
            pass
