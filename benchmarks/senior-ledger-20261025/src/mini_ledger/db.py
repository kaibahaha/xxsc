"""SQLite database access and immutable schema for the ledger exercise.

The schema is part of the contract. Candidates may change connection or
transaction handling, and may add indexes, but must not delete history.
"""
import sqlite3

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
    """Open a fresh database connection for the caller."""
    # Intentionally simplistic: audit and transfer should survive contention.
    conn = sqlite3.connect(path, timeout=0.01, isolation_level=None)
    conn.row_factory = sqlite3.Row
    return conn


def initialize(path: str) -> None:
    conn = connect(path)
    try:
        conn.executescript(SCHEMA)
    finally:
        conn.close()
