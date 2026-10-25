"""Immutable event ledger on top of :class:`GitHubStorage`.

Layout (per frameworks/agensh-lite-v4.1/02_GITHUB_LAYOUT_AND_WRITES.md):

    <root>/03_events/<YYYYMMDD>/<EVENT_ID>/_manifest.json
    <root>/03_events/<YYYYMMDD>/<EVENT_ID>/<TARGET_AGENT>.json
    <root>/05_outbox/<AGENT>/<RUN_ID>/<EVENT_ID>.json
    <root>/07_receipts/<AGENT>/<EVENT_ID>.json
    <root>/07_receipts/<AGENT>/_cursor.json
    <root>/09_runs/<AGENT>/<RUN_ID>.md
    <root>/08_projections/BOARD.md

Semantics
---------
* Idempotency is per ``(event_id, target_agent)`` -- the Git file layout makes
  this structural, matching ``UNIQUE KEY (dedup_key, agent)`` in Microsoft
  Agensh ``mini-router/src/state.ts``.
* An event id carries one canonical payload digest (stored in ``_manifest.json``).
  A second write with the same id but a different digest is an ``EVENT_ID_COLLISION``
  and is refused for *every* target, not just the one that noticed.
* Cursors only move forward, like ``_advance_board_cursor`` in
  ``board-service/main.py``; advancing is a CAS update, never a blind overwrite.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from ..errors import AglError, ErrorCode
from .github import GitHubStorage, WriteReceipt, canonical_json_bytes, sha256_hex, utc_now

REQUIRED_EVENT_FIELDS = (
    "event_id",
    "project_id",
    "task_id",
    "producer",
    "target_agents",
    "kind",
    "source",
    "observed_at",
    "summary",
    "raw_ref",
)


@dataclass(frozen=True)
class EventWrite:
    event_id: str
    target_agent: str
    path: str
    status: str          # CREATED | IDEMPOTENT_REPLAY
    receipt: WriteReceipt
    dedupe: bool


@dataclass(frozen=True)
class ReceiptWrite:
    event_id: str
    agent_id: str
    path: str
    status: str
    receipt: WriteReceipt


def event_digest(event: dict[str, Any]) -> str:
    """Digest of the event body excluding the self-referential payload_sha256."""
    body = {k: v for k, v in event.items() if k != "payload_sha256"}
    return sha256_hex(canonical_json_bytes(body))


def normalize_event(event: dict[str, Any]) -> dict[str, Any]:
    from .. import SCHEMA_VERSION

    ev = dict(event)
    ev.setdefault("schema_version", SCHEMA_VERSION)
    ev.setdefault("source", "github")
    ev.setdefault("observed_at", utc_now())
    ev.setdefault("causation_id", None)
    ev.setdefault("spec_hash", None)
    ev.setdefault("run_id", None)
    missing = [f for f in REQUIRED_EVENT_FIELDS if not ev.get(f)]
    if missing:
        raise AglError(ErrorCode.SCHEMA_INVALID, f"event missing required fields: {missing}")
    if not isinstance(ev["target_agents"], list) or not ev["target_agents"]:
        raise AglError(ErrorCode.SCHEMA_INVALID, "target_agents must be a non-empty list")
    ev["payload_sha256"] = event_digest(ev)
    return ev


class EventLedger:
    def __init__(self, storage: GitHubStorage, root: str = "factory/projects/AGL-SHADOW-001") -> None:
        self.storage = storage
        self.root = root.strip("/")

    # -- paths -------------------------------------------------------------- #
    def _date_dir(self, event: dict[str, Any]) -> str:
        stamp = str(event["observed_at"])[:10].replace("-", "")
        if len(stamp) != 8 or not stamp.isdigit():
            stamp = utc_now()[:10].replace("-", "")
        return f"{self.root}/03_events/{stamp}"

    def event_dir(self, event: dict[str, Any]) -> str:
        return f"{self._date_dir(event)}/{event['event_id']}"

    # -- writes -------------------------------------------------------------#
    def put_event(self, event: dict[str, Any], target_agent: str) -> EventWrite:
        ev = normalize_event(event)
        if target_agent not in ev["target_agents"]:
            raise AglError(
                ErrorCode.INVALID_INPUT,
                f"{target_agent} is not in target_agents {ev['target_agents']}",
            )
        edir = self.event_dir(ev)
        manifest_path = f"{edir}/_manifest.json"
        manifest = {
            "schema_version": ev["schema_version"],
            "event_id": ev["event_id"],
            "payload_sha256": ev["payload_sha256"],
            "producer": ev["producer"],
            "task_id": ev["task_id"],
            "kind": ev["kind"],
            "target_agents": sorted(ev["target_agents"]),
            "created_at": ev["observed_at"],
        }

        existing_manifest = self.storage.read_file(manifest_path)
        if existing_manifest.exists:
            import json

            try:
                current = json.loads(existing_manifest.text)
            except Exception:
                raise AglError(ErrorCode.CONFLICT, f"unreadable event manifest {manifest_path}")
            if current.get("payload_sha256") != ev["payload_sha256"]:
                raise AglError(
                    ErrorCode.COLLISION,
                    f"EVENT_ID_COLLISION: {ev['event_id']} already recorded with a different payload",
                    {
                        "event_id": ev["event_id"],
                        "existing_sha256": current.get("payload_sha256"),
                        "incoming_sha256": ev["payload_sha256"],
                        "manifest": manifest_path,
                    },
                )
        else:
            self.storage.write_immutable(
                manifest_path,
                canonical_json_bytes(manifest),
                idempotency_key=f"manifest:{ev['event_id']}",
                message=f"event manifest {ev['event_id']}",
            )

        target_path = f"{edir}/{target_agent}.json"
        try:
            receipt = self.storage.write_immutable(
                target_path,
                canonical_json_bytes(ev),
                idempotency_key=f"{ev['event_id']}:{target_agent}",
                message=f"event {ev['event_id']} -> {target_agent}",
            )
        except AglError as exc:
            if exc.code is ErrorCode.CONFLICT:
                # manifest digest matched but the target file differs -> tamper/collision
                raise AglError(
                    ErrorCode.COLLISION,
                    f"EVENT_ID_COLLISION: target file {target_path} holds different bytes",
                    {"event_id": ev["event_id"], "target_agent": target_agent},
                ) from exc
            raise
        return EventWrite(
            event_id=ev["event_id"],
            target_agent=target_agent,
            path=target_path,
            status=receipt.status,
            receipt=receipt,
            dedupe=receipt.status == "IDEMPOTENT_REPLAY",
        )

    def publish_outbox(self, agent_id: str, run_id: str, event: dict[str, Any]) -> EventWrite:
        """Write an event into the agent's own outbox (the only writable scope)."""
        ev = normalize_event(event)
        path = f"{self.root}/05_outbox/{agent_id}/{run_id}/{ev['event_id']}.json"
        receipt = self.storage.write_immutable(
            path, canonical_json_bytes(ev), idempotency_key=f"outbox:{ev['event_id']}",
            message=f"outbox {agent_id}/{run_id} {ev['event_id']}",
        )
        return EventWrite(ev["event_id"], agent_id, path, receipt.status, receipt,
                          receipt.status == "IDEMPOTENT_REPLAY")

    def put_receipt(
        self,
        agent_id: str,
        event_id: str,
        *,
        result: str,
        evidence_ref: str,
        target: str = "GITHUB",
        readback_hash: str | None = None,
        commit_sha: str | None = None,
        writer: str | None = None,
    ) -> ReceiptWrite:
        path = f"{self.root}/07_receipts/{agent_id}/{event_id}.json"
        body = {
            "schema_version": "1.0",
            "event_id": event_id,
            "target": target,
            "result": result,
            "verified_at": utc_now(),
            "evidence_ref": evidence_ref,
            "readback_hash": readback_hash,
            "commit_sha": commit_sha,
            "writer": writer or agent_id,
        }
        try:
            receipt = self.storage.write_immutable(
                path, canonical_json_bytes(body), idempotency_key=f"receipt:{event_id}:{agent_id}",
                message=f"ack {event_id} ({agent_id})",
            )
        except AglError as exc:
            if exc.code is ErrorCode.CONFLICT:
                existing = self.storage.read_file(path)
                raise AglError(
                    ErrorCode.CONFLICT,
                    f"conflicting ACK already recorded for {event_id} on {agent_id}",
                    {"existing_sha256": existing.sha256},
                ) from exc
            raise
        return ReceiptWrite(event_id, agent_id, path, receipt.status, receipt)

    # -- reads --------------------------------------------------------------#
    def list_event_dates(self) -> list[str]:
        return [n.rstrip("/") for n in self.storage.list_files(f"{self.root}/03_events")]

    def list_event_ids(self, date: str) -> list[str]:
        return [n.rstrip("/") for n in self.storage.list_files(f"{self.root}/03_events/{date}")]

    def read_manifest(self, date: str, event_id: str) -> dict[str, Any] | None:
        import json

        snap = self.storage.read_file(f"{self.root}/03_events/{date}/{event_id}/_manifest.json")
        if not snap.exists:
            return None
        return json.loads(snap.text)

    def read_event(self, date: str, event_id: str, agent_id: str) -> dict[str, Any] | None:
        import json

        snap = self.storage.read_file(f"{self.root}/03_events/{date}/{event_id}/{agent_id}.json")
        if not snap.exists:
            return None
        return json.loads(snap.text)

    def read_receipt(self, agent_id: str, event_id: str) -> dict[str, Any] | None:
        import json

        snap = self.storage.read_file(f"{self.root}/07_receipts/{agent_id}/{event_id}.json")
        if not snap.exists:
            return None
        return json.loads(snap.text)

    def iter_events(self, task_id: str | None = None) -> Iterable[tuple[str, dict[str, Any]]]:
        for date in self.list_event_dates():
            for event_id in self.list_event_ids(date):
                manifest = self.read_manifest(date, event_id)
                if not manifest:
                    continue
                if task_id and manifest.get("task_id") != task_id:
                    continue
                yield f"{date}/{event_id}", manifest

    # -- cursor -------------------------------------------------------------#
    def get_cursor(self, agent_id: str) -> dict[str, Any]:
        import json

        snap = self.storage.read_file(f"{self.root}/07_receipts/{agent_id}/_cursor.json")
        if not snap.exists:
            return {"agent": agent_id, "cursor": None, "blob_sha": None}
        data = json.loads(snap.text)
        data["blob_sha"] = snap.blob_sha
        return data

    def advance_cursor(self, agent_id: str, cursor: str, max_attempts: int = 3) -> dict[str, Any]:
        """Monotonic, CAS-guarded cursor advance (string comparison, ISO-8601 order)."""
        import json

        path = f"{self.root}/07_receipts/{agent_id}/_cursor.json"
        for _ in range(max_attempts):
            snap = self.storage.read_file(path)
            current = json.loads(snap.text)["cursor"] if snap.exists else None
            if current is not None and str(cursor) <= str(current):
                return {"agent": agent_id, "cursor": current, "status": "MONOTONIC_NOOP"}
            body = {"agent": agent_id, "cursor": cursor, "updated_at": utc_now()}
            try:
                receipt = self.storage.cas_publish_projection(
                    path, canonical_json_bytes(body), snap.blob_sha,
                    message=f"cursor {agent_id} -> {cursor}",
                )
            except AglError as exc:
                if exc.code is ErrorCode.CONFLICT:
                    continue
                raise
            return {"agent": agent_id, "cursor": cursor, "status": receipt.status,
                    "commit_sha": receipt.commit_sha}
        raise AglError(ErrorCode.CONFLICT, f"cursor CAS retries exhausted for {agent_id}")
