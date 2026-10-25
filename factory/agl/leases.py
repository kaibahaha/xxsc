"""Local transaction backend, not a Git or cross-cloud lock service.

Every decision and domain delta is committed in one BEGIN IMMEDIATE transaction.
SQLite must be a durable local file on one host, never a Git-tracked or NFS file.
"""
from contextlib import contextmanager
from copy import deepcopy
import json
from pathlib import Path
import sqlite3
from typing import Callable
from .replay import changes_between, rebuild
from .schemas import CoreError, canonical, digest, require


class SQLiteLeaseBackend:
    authority = "LOCAL_SQLITE_ONLY"

    def __init__(self, path: str | Path, *, fault: Callable | None = None):
        require(str(path) != ":memory:", "PERSISTENT_PATH_REQUIRED")
        self.path = str(path)
        self.fault = fault or (lambda point: None)
        with self.connect() as db:
            db.execute("PRAGMA journal_mode=WAL")
            db.executescript("""
            CREATE TABLE IF NOT EXISTS journal (
              seq INTEGER PRIMARY KEY, command_id TEXT NOT NULL UNIQUE,
              record TEXT NOT NULL
            );
            CREATE TRIGGER IF NOT EXISTS journal_no_update BEFORE UPDATE ON journal
              BEGIN SELECT RAISE(ABORT, 'immutable audit'); END;
            CREATE TRIGGER IF NOT EXISTS journal_no_delete BEFORE DELETE ON journal
              BEGIN SELECT RAISE(ABORT, 'immutable audit'); END;
            """)

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path, timeout=30, isolation_level=None)
        try:
            db.execute("PRAGMA synchronous=FULL")
            yield db
        finally:
            db.close()

    @staticmethod
    def _records(db):
        rows = db.execute("SELECT seq, command_id, record FROM journal ORDER BY seq").fetchall()
        records = []
        for seq, command_id, raw in rows:
            record = json.loads(raw)
            require(record["seq"] == seq and record["command_id"] == command_id, "AUDIT_ROW_MISMATCH")
            records.append(record)
        return records

    def records(self):
        self.fault("before_read")
        with self.connect() as db:
            records = self._records(db)
            rebuild(records)
            return records

    def snapshot(self):
        return rebuild(self.records())

    def transact(self, command_id, request, now, apply, *, initialize=False):
        require(isinstance(command_id, str) and bool(command_id), "MISSING_IDEMPOTENCY_KEY")
        self.fault("before_read")
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            try:
                records = self._records(db)
                state = rebuild(records)
                if initialize and records:
                    require(records[0]["command_id"] == "bootstrap", "INVALID_GENESIS")
                    db.execute("ROLLBACK")
                    return {"status": "EXISTING", "simulation": state["meta"]["simulation"]}
                old = next((r for r in records if r["command_id"] == command_id), None)
                if old:
                    require(old["request_hash"] == digest(request), "COMMAND_ID_COLLISION")
                    db.execute("ROLLBACK")
                    return deepcopy(old["result"])
                before = deepcopy(state)
                result = apply(state)
                record = {"seq": len(records) + 1, "command_id": command_id,
                          "request_hash": digest(request), "request": request, "at": now,
                          "changes": changes_between(before, state), "result": result,
                          "previous_hash": records[-1]["record_hash"] if records else "0" * 64}
                record["record_hash"] = digest(record)
                self.fault("before_append")
                db.execute("INSERT INTO journal VALUES (?, ?, ?)", (record["seq"], command_id, canonical(record)))
                self.fault("after_append")
                db.execute("COMMIT")
            except BaseException:
                if db.in_transaction:
                    db.execute("ROLLBACK")
                raise
        # An exception here means UNKNOWN_WRITE. Caller must reconcile by command_id.
        self.fault("after_commit")
        return deepcopy(result)

    def reconcile(self, command_id: str, request: dict):
        for record in self.records():
            if record["command_id"] == command_id:
                require(record["request_hash"] == digest(request), "COMMAND_ID_COLLISION")
                return {"status": "COMMITTED", "result": record["result"], "record_hash": record["record_hash"]}
        return {"status": "NOT_FOUND"}

    @classmethod
    def restore(cls, path, records, *, expected_head_hash):
        """Restore a verified immutable journal into a NEW local DB.

        expected_head_hash must come from a trusted independently read Git receipt.
        A hash chain detects corruption, not a malicious replacement of the whole log.
        """
        rebuild(records)
        require(records and records[-1]["record_hash"] == expected_head_hash, "RESTORE_HEAD_MISMATCH")
        backend = cls(path)
        with backend.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            try:
                require(not cls._records(db), "RESTORE_REQUIRES_EMPTY_DATABASE")
                for record in records:
                    db.execute("INSERT INTO journal VALUES (?, ?, ?)", (record["seq"], record["command_id"], canonical(record)))
                db.execute("COMMIT")
            except BaseException:
                db.execute("ROLLBACK")
                raise
        require(backend.records() == records, "RESTORE_READBACK_MISMATCH")
        return backend
