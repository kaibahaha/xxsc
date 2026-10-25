"""The unified provider adapter protocol (design contract from
``docs/AGENT_ADAPTER_CONTRACT.md`` + ``workorders/INTERFACE_HANDOFF.md`` §3).

Any new provider only adds an adapter; Controller/lease/UEM state machines are
never touched. Adapters must report honest states -- an unimplemented operation
returns ``UNSUPPORTED``/``UNKNOWN``/``BLOCKED`` and never a fabricated success.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from ..storage.github import VerifiedReadback, WriteReceipt
from .types import (
    CapabilityProbe,
    HealthObservation,
    ReadResult,
    ScheduleObservation,
)


@runtime_checkable
class AgentAdapter(Protocol):
    agent_id: str
    provider_id: str
    adapter_id: str

    def probe(self, principal: str | None = None, scope: str | None = None) -> CapabilityProbe:
        """Verify real tools/permissions and return per-operation states."""

    def read(self, work_ref: str | None = None, cursor: str | None = None) -> ReadResult:
        """Read board/tasks/events visible to this agent."""

    def publish(self, immutable_event: dict, idempotency_key: str) -> WriteReceipt:
        """Write an immutable event into this agent's own outbox."""

    def reread(self, receipt: WriteReceipt) -> VerifiedReadback:
        """Independent readback of a previously written artifact."""

    def observe_schedule(self, agent_id: str | None = None) -> ScheduleObservation:
        """Report the *real* schedule state; UNSUPPORTED when no API exists."""

    def health(self, agent_id: str | None = None) -> HealthObservation:
        """Availability signal used by the poll planner."""
