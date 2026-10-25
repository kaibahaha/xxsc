"""SQLite connection and schema helpers for the durable MiniLedger."""
from __future__ import annotations

from contextlib import contextmanager
import sqlite3
from collections.abc import Iterator

SCHEMA = """
CREATE TABLE IF NOT EXISTS accounts (
    account_id TEXT PRIMARY KEY,
    opening_balance INTEGER NOT NULL,
    balance INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS transfers (
    request_id TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    target TEXT NOT NULL,
    amount INTEGER NOT NULL,
    status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS journal (
    entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id TEXT NOT NULL,
    account_id TEXT NOT NULL,
    delta INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS journal_request ON journal(request_id);
"""


def connect(path: str) -> sqlite3.Connection:
    """Return a new autocommit connection with a generous SQLite lock wait."""
    conn = sqlite3.connect(path, timeout=30.0, isolation_level=None)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def transaction(path: str, *, write: bool = False) -> Iterator[sqlite3.Connection]:
    """Close every connection; commit once or roll back on *any* failure.

    BEGIN IMMEDIATE serializes competing writers before checking balances or
    request IDs. Read transactions use BEGIN for a single audit snapshot.
    """
    conn = connect(path)
    try:
        conn.execute("BEGIN IMMEDIATE" if write else "BEGIN")
        try:
            yield conn
            conn.commit()
        except BaseException:
            conn.rollback()
            raise
    finally:
        conn.close()


def initialize(path: str) -> None:
    conn = connect(path)
    try:
        conn.executescript(SCHEMA)
    finally:
        conn.close()
