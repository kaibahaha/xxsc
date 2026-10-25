"""Value objects shared by all provider adapters.

Field names follow frameworks/agensh-lite-v4.2/workorders/INTERFACE_HANDOFF.md:
``probe/read/publish/reread/observe_schedule/health`` and the four capability
states ``SUPPORTED / UNSUPPORTED / UNKNOWN / BLOCKED``.

``method`` records *how* a capability was established:

* ``REAL``       -- live call to the real provider/repository
* ``LOCAL_GIT``  -- real git plumbing against a local bare repository (no network)
* ``STATIC``     -- declared in configuration, not verified
* ``MOCK``       -- simulated for tests; never acceptable as cross-platform proof
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class CapState(str, Enum):
    SUPPORTED = "SUPPORTED"
    UNSUPPORTED = "UNSUPPORTED"
    UNKNOWN = "UNKNOWN"
    BLOCKED = "BLOCKED"


OPS = ("read", "write", "reread", "trigger", "execute", "schedule")


@dataclass(frozen=True)
class CapabilityItem:
    op: str
    state: CapState
    detail: str
    method: str = "STATIC"
    evidence: str | None = None
    verified_at: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "op": self.op,
            "state": self.state.value,
            "detail": self.detail,
            "method": self.method,
            "evidence": self.evidence,
            "verified_at": self.verified_at,
        }


@dataclass(frozen=True)
class CapabilityProbe:
    agent_id: str
    provider_id: str
    adapter_id: str
    items: dict[str, CapabilityItem]
    probed_at: str
    transport: str

    def state(self, op: str) -> CapState:
        item = self.items.get(op)
        return item.state if item else CapState.UNKNOWN

    @property
    def overall(self) -> str:
        states = {item.state for item in self.items.values()}
        if CapState.SUPPORTED in states and CapState.BLOCKED not in states:
            return "PARTIAL" if (CapState.UNSUPPORTED in states or CapState.UNKNOWN in states) else "FULL"
        if CapState.SUPPORTED in states:
            return "PARTIAL"
        return "NONE"

    def as_dict(self) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "provider_id": self.provider_id,
            "adapter_id": self.adapter_id,
            "transport": self.transport,
            "probed_at": self.probed_at,
            "overall": self.overall,
            "items": {op: item.as_dict() for op, item in self.items.items()},
        }


@dataclass
class ReadResult:
    agent_id: str
    cursor_in: str | None
    cursor_out: str | None
    board_known: bool
    tasks: list[dict[str, Any]] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "cursor_in": self.cursor_in,
            "cursor_out": self.cursor_out,
            "board_known": self.board_known,
            "task_count": len(self.tasks),
            "event_count": len(self.events),
            "notes": self.notes,
        }


@dataclass(frozen=True)
class ScheduleObservation:
    agent_id: str
    provider_id: str
    trigger_type: str
    schedule_id: str | None
    cadence_minutes: int | None
    timezone: str | None
    planned_next: str | None
    actual_last_fired: str | None
    source: str            # COMPUTED | VERIFIED_API | UNSUPPORTED
    verified: bool
    detail: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "provider_id": self.provider_id,
            "trigger_type": self.trigger_type,
            "schedule_id": self.schedule_id,
            "cadence_minutes": self.cadence_minutes,
            "timezone": self.timezone,
            "planned_next": self.planned_next,
            "actual_last_fired": self.actual_last_fired,
            "source": self.source,
            "verified": self.verified,
            "detail": self.detail,
        }


@dataclass(frozen=True)
class HealthObservation:
    agent_id: str
    status: str            # HEALTHY | DEGRADED | UNAVAILABLE
    detail: str = ""
    last_run_at: str | None = None
    checked_at: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "status": self.status,
            "detail": self.detail,
            "last_run_at": self.last_run_at,
            "checked_at": self.checked_at,
        }


@dataclass(frozen=True)
class AdmissionDecision:
    agent_id: str
    allowed: bool
    state: str
    reason: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "allowed": self.allowed,
            "state": self.state,
            "reason": self.reason,
        }
