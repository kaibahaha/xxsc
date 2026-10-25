"""Git-file mailbox adapter shared by every provider.

Transport is always GitHub (or a local bare repo in tests); the *provider*
differences live in the subclasses in :mod:`agl.adapters.providers`, which can
only downgrade -- never upgrade -- what a real probe observed.

Why a mailbox: ChatGPT scheduled tasks and WorkBuddy sessions have no mutually
authorised webhook/API in this deployment, so cross-platform hand-off is done by
immutable Git files plus each platform's own cadence. No code here pretends a
push notification exists.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from ..errors import AglError, ErrorCode
from ..storage.github import GitHubStorage, VerifiedReadback, WriteReceipt, canonical_json_bytes, utc_now
from ..storage.ledger import EventLedger
from .registry_view import AgentRecord
from .types import (
    CapState,
    CapabilityItem,
    CapabilityProbe,
    HealthObservation,
    ReadResult,
    ScheduleObservation,
)


@dataclass
class AdapterContext:
    storage: GitHubStorage
    ledger: EventLedger
    runtime_root: str
    run_id: str
    token_present: bool = False
    runner_available: bool = False
    webhook_url: str | None = None
    write_probe: bool = True
    probe_root: str = "_probe"


class GitHubMailboxAdapter:
    provider_id = "generic"
    adapter_id = "github_mailbox"
    #: False when the platform has no write credential of its own (e.g. ChatGPT)
    supports_publish = True

    def __init__(self, record: AgentRecord, ctx: AdapterContext) -> None:
        self.record = record
        self.ctx = ctx
        self.agent_id = record.agent_id
        self.storage = ctx.storage
        self.ledger = ctx.ledger

    # -- helpers ------------------------------------------------------------#
    @property
    def method(self) -> str:
        kind = self.storage.transport.kind
        return "LOCAL_GIT" if kind == "local_git" else "REAL"

    def _item(self, op: str, state: CapState, detail: str, evidence: str | None = None,
              method: str | None = None) -> CapabilityItem:
        return CapabilityItem(
            op=op, state=state, detail=detail, method=method or self.method,
            evidence=evidence, verified_at=utc_now(),
        )

    def _outbox_root(self) -> str:
        return f"{self.ctx.runtime_root}/05_outbox/{self.agent_id}"

    # -- AgentAdapter -------------------------------------------------------#
    def probe(self, principal: str | None = None, scope: str | None = None) -> CapabilityProbe:
        items: dict[str, CapabilityItem] = {}

        try:
            ref = self.storage.read_ref()
            items["read"] = self._item(
                "read", CapState.SUPPORTED,
                f"{ref.repo}@{ref.ref} readable, head={ref.commit_sha[:12]}",
                evidence=f"{ref.repo}@{ref.commit_sha}",
            )
        except AglError as exc:
            state = CapState.BLOCKED if exc.code in (
                ErrorCode.NO_PERMISSION, ErrorCode.AUTH_MISSING, ErrorCode.NOT_FOUND
            ) else CapState.UNKNOWN
            items["read"] = self._item("read", state, f"read probe failed: {exc.code.value} - {exc.message}")

        if self.ctx.write_probe and self.provider_id != "chatgpt":
            try:
                path = f"{self._outbox_root()}/{self.ctx.probe_root}/{self.ctx.run_id}.json"
                body = canonical_json_bytes({
                    "agent_id": self.agent_id,
                    "provider_id": self.provider_id,
                    "run_id": self.ctx.run_id,
                    "probed_at": utc_now(),
                    "kind": "WRITE_PROBE",
                })
                receipt = self.storage.write_immutable(
                    path, body, idempotency_key=f"probe:{self.agent_id}:{self.ctx.run_id}",
                    message=f"probe write {self.agent_id}",
                )
                items["write"] = self._item(
                    "write", CapState.SUPPORTED,
                    f"immutable write to own outbox ok ({receipt.status})",
                    evidence=f"{path}@{receipt.commit_sha}",
                )
                rb = self.storage.readback(receipt)
                items["reread"] = self._item(
                    "reread", CapState.SUPPORTED if rb.matches else CapState.BLOCKED,
                    f"independent readback matches={rb.matches}",
                    evidence=f"blob={rb.readback_blob_sha}",
                )
            except AglError as exc:
                state = CapState.BLOCKED if exc.code in (
                    ErrorCode.NO_PERMISSION, ErrorCode.AUTH_MISSING, ErrorCode.PATH_NOT_WHITELISTED
                ) else CapState.UNKNOWN
                items["write"] = self._item("write", state, f"write probe failed: {exc.code.value}")
                items["reread"] = self._item("reread", CapState.UNKNOWN, "no write to read back")
        else:
            items["write"] = self._item(
                "write", CapState.UNSUPPORTED,
                "adapter is read-only: no write credential/scope for this provider",
                method="STATIC",
            )
            items["reread"] = self._item(
                "reread", CapState.UNKNOWN, "nothing written by this adapter", method="STATIC"
            )

        items["trigger"] = self._trigger_item()
        items["execute"] = self._execute_item()
        items["schedule"] = self._schedule_item()

        return CapabilityProbe(
            agent_id=self.agent_id,
            provider_id=self.provider_id,
            adapter_id=self.record.adapter_id or self.adapter_id,
            items=items,
            probed_at=utc_now(),
            transport=self.storage.transport.kind,
        )

    def _trigger_item(self) -> CapabilityItem:
        return self._item(
            "trigger", CapState.UNSUPPORTED,
            "no verified push/webhook channel; platform reads Git on its own cadence",
            method="STATIC",
        )

    def _execute_item(self) -> CapabilityItem:
        return self._item(
            "execute", CapState.UNSUPPORTED,
            "provider exposes no verified code-execution endpoint",
            method="STATIC",
        )

    def _schedule_item(self) -> CapabilityItem:
        if self.record.schedule_id:
            return self._item(
                "schedule", CapState.UNKNOWN,
                f"schedule_id={self.record.schedule_id} declared but no API to verify it",
                method="STATIC", evidence=self.record.schedule_id,
            )
        return self._item(
            "schedule", CapState.UNKNOWN,
            "no public schedule API; planned vs actual wake-ups are recorded separately",
            method="STATIC",
        )

    # -- reads --------------------------------------------------------------#
    def read(self, work_ref: str | None = None, cursor: str | None = None) -> ReadResult:
        notes: list[str] = []
        root = self.ctx.runtime_root
        board_path = f"{root}/08_projections/BOARD.md"
        board_known = self.storage.read_file(board_path).exists
        if not board_known:
            notes.append("BOARD_UNKNOWN: projection missing; no new claim is allowed")

        tasks: list[dict[str, Any]] = []
        for name in self.storage.list_files(f"{root}/01_tasks"):
            task_dir = name.rstrip("/")
            meta = self.storage.read_file(f"{root}/01_tasks/{task_dir}/TASK.json")
            if meta.exists:
                try:
                    data = json.loads(meta.text)
                except Exception:
                    notes.append(f"unreadable TASK.json for {task_dir}")
                    continue
                data.setdefault("task_id", task_dir)
                data["path"] = f"{root}/01_tasks/{task_dir}/TASK.md"
                tasks.append(data)
            else:
                md = self.storage.read_file(f"{root}/01_tasks/{task_dir}/TASK.md")
                if md.exists:
                    tasks.append(parse_task_markdown(md.text, task_dir))

        events: list[dict[str, Any]] = []
        cursor_out = cursor
        for date in self.ledger.list_event_dates():
            for event_id in self.ledger.list_event_ids(date):
                snap = self.storage.read_file(f"{root}/03_events/{date}/{event_id}/{self.agent_id}.json")
                if not snap.exists:
                    continue
                try:
                    ev = json.loads(snap.text)
                except Exception:
                    continue
                if cursor and str(ev.get("observed_at", "")) <= str(cursor):
                    continue
                events.append(ev)
                observed = str(ev.get("observed_at", ""))
                cursor_out = max(cursor_out or "", observed) if cursor_out else observed

        return ReadResult(
            agent_id=self.agent_id,
            cursor_in=cursor,
            cursor_out=cursor_out,
            board_known=board_known,
            tasks=tasks,
            events=events,
            notes=notes,
        )

    def publish(self, immutable_event: dict, idempotency_key: str) -> WriteReceipt:
        path = f"{self._outbox_root()}/{self.ctx.run_id}/{immutable_event['event_id']}.json"
        return self.storage.write_immutable(
            path, canonical_json_bytes(immutable_event), idempotency_key=idempotency_key,
            message=f"outbox {self.agent_id} {immutable_event['event_id']}",
        )

    def reread(self, receipt: WriteReceipt) -> VerifiedReadback:
        return self.storage.readback(receipt)

    def observe_schedule(self, agent_id: str | None = None) -> ScheduleObservation:
        return ScheduleObservation(
            agent_id=agent_id or self.agent_id,
            provider_id=self.provider_id,
            trigger_type=self.record.trigger_type,
            schedule_id=self.record.schedule_id,
            cadence_minutes=self.record.cadence_minutes,
            timezone=self.record.timezone,
            planned_next=None,
            actual_last_fired=None,
            source="UNSUPPORTED",
            verified=False,
            detail="provider has no schedule API; only the platform's own UI shows real wake-ups",
        )

    def health(self, agent_id: str | None = None) -> HealthObservation:
        try:
            self.storage.read_ref()
        except AglError as exc:
            return HealthObservation(
                agent_id or self.agent_id, "UNAVAILABLE", f"read probe failed: {exc.code.value}",
                checked_at=utc_now(),
            )
        last = self.storage.read_file(f"{self.ctx.runtime_root}/09_runs/{self.agent_id}/_last.json")
        last_at = None
        if last.exists:
            try:
                last_at = json.loads(last.text).get("started_at")
            except Exception:
                last_at = None
        return HealthObservation(agent_id or self.agent_id, "HEALTHY", "repository readable",
                                 last_run_at=last_at, checked_at=utc_now())


def parse_task_markdown(text: str, task_id: str) -> dict[str, Any]:
    """Extract the lightweight task header used by 01_tasks/<ID>/TASK.md."""
    meta: dict[str, Any] = {"task_id": task_id, "status": "UNKNOWN", "dependencies": [],
                            "allowed_agents": [], "capabilities": [], "title": ""}
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# ") and not meta["title"]:
            meta["title"] = stripped[2:].strip()
        if ":" not in stripped:
            continue
        key, _, value = stripped.partition(":")
        key = key.strip().upper()
        value = value.strip()
        if key == "STATUS":
            meta["status"] = value.upper()
        elif key in ("DEPENDS_ON", "DEPENDENCIES"):
            meta["dependencies"] = [v.strip() for v in value.split(",") if v.strip()]
        elif key in ("ALLOWED_AGENTS", "OWNER"):
            meta["allowed_agents"] = [v.strip() for v in value.split(",") if v.strip()]
        elif key == "CAPABILITIES":
            meta["capabilities"] = [v.strip() for v in value.split(",") if v.strip()]
        elif key == "SPEC_HASH":
            meta["spec_hash"] = value
        elif key == "PRIORITY":
            meta["priority"] = value
    return meta
