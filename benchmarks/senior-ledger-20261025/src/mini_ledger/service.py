"""Deliberately flawed starter implementation. Repair it; preserve API."""
from __future__ import annotations

from .db import connect, initialize
from .errors import Conflict, InsufficientFunds, InvalidRequest, NotFound

MAX_UNITS = (1 << 63) - 1


def _check_id(value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise InvalidRequest("ID must be a nonblank string")


class Ledger:
    """Durable money-integer ledger backed by a single SQLite file."""

    def __init__(self, path: str, *, on_before_commit=None):
        if not isinstance(path, str) or not path:
            raise InvalidRequest("path must be a nonempty string")
        self.path = path
        self.on_before_commit = on_before_commit
        initialize(path)

    def create_account(self, account_id: str, initial_balance: int = 0) -> None:
        _check_id(account_id)
        if not isinstance(initial_balance, int) or initial_balance < 0:
            raise InvalidRequest("initial_balance must be nonnegative integer")
        with connect(self.path) as conn:
            if conn.execute("SELECT 1 FROM accounts WHERE account_id=?", (account_id,)).fetchone():
                raise Conflict("duplicate account")
            conn.execute(
                "INSERT INTO accounts(account_id, opening_balance, balance) VALUES (?, ?, ?)",
                (account_id, initial_balance, initial_balance),
            )

    def balance(self, account_id: str) -> int:
        _check_id(account_id)
        with connect(self.path) as conn:
            row = conn.execute("SELECT balance FROM accounts WHERE account_id=?", (account_id,)).fetchone()
            if row is None:
                raise NotFound(account_id)
            return row["balance"]

    def snapshot(self) -> dict[str, int]:
        with connect(self.path) as conn:
            rows = conn.execute("SELECT account_id, balance FROM accounts ORDER BY account_id").fetchall()
            return {r["account_id"]: r["balance"] for r in rows}

    def transfer(self, request_id: str, source: str, target: str, amount: int) -> dict:
        _check_id(request_id)
        _check_id(source)
        _check_id(target)
        if not isinstance(amount, int) or amount <= 0:
            raise InvalidRequest("amount must be positive integer")
        receipt = {
            "request_id": request_id, "source": source, "target": target,
            "amount": amount, "status": "committed",
        }

        with connect(self.path) as conn:
            # BUG: any duplicate key succeeds, even if payload differs.
            existing = conn.execute(
                "SELECT request_id FROM transfers WHERE request_id=?", (request_id,)
            ).fetchone()
            if existing is not None:
                return receipt

            src = conn.execute("SELECT balance FROM accounts WHERE account_id=?", (source,)).fetchone()
            dst = conn.execute("SELECT balance FROM accounts WHERE account_id=?", (target,)).fetchone()
            if src is None or dst is None:
                raise NotFound("account missing")
            if src["balance"] < amount:
                raise InsufficientFunds("insufficient funds")

            # BUG: separate auto-commit statements; concurrent callers can
            # both spend the same money. Injected failures leave partial state.
            conn.execute("UPDATE accounts SET balance = balance - ? WHERE account_id=?", (amount, source))
            conn.execute("UPDATE accounts SET balance = balance + ? WHERE account_id=?", (amount, target))
            conn.execute("INSERT INTO transfers VALUES (?, ?, ?, ?, ?)",
                         (request_id, source, target, amount, "committed"))
            conn.execute("INSERT INTO journal(request_id,account_id,delta) VALUES (?,?,?)",
                         (request_id, source, -amount))
            conn.execute("INSERT INTO journal(request_id,account_id,delta) VALUES (?,?,?)",
                         (request_id, target, amount))
            if self.on_before_commit is not None:
                self.on_before_commit(request_id)
        return receipt

    def audit(self) -> dict:
        # BUG: conservation sum is not enough to detect forged journal entries,
        # malformed transfers, or a single corrupted account balance.
        with connect(self.path) as conn:
            accounts = conn.execute("SELECT balance FROM accounts").fetchall()
            transfers = conn.execute("SELECT COUNT(*) AS n FROM transfers").fetchone()["n"]
            return {
                "accounts": len(accounts),
                "transfers": transfers,
                "total_balance": sum(r["balance"] for r in accounts),
            }
