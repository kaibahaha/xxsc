"""Atomic, idempotent, concurrency-safe SQLite integer ledger."""
from __future__ import annotations

from .db import initialize, transaction
from .errors import Conflict, InsufficientFunds, InvalidRequest, InvariantViolation, NotFound

MAX_UNITS = (1 << 63) - 1


def _check_id(value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise InvalidRequest("ID must be a nonblank string")


def _check_units(value: object, *, minimum: int) -> None:
    if type(value) is not int or not minimum <= value <= MAX_UNITS:
        raise InvalidRequest(f"amount must be an integer in [{minimum}, {MAX_UNITS}]")


def _receipt(request_id: str, source: str, target: str, amount: int) -> dict:
    return {
        "request_id": request_id, "source": source, "target": target,
        "amount": amount, "status": "committed",
    }


class Ledger:
    """Persist balances, requests, and exactly two journal entries per transfer."""

    def __init__(self, path: str, *, on_before_commit=None):
        if not isinstance(path, str) or not path:
            raise InvalidRequest("path must be a nonempty string")
        self.path = path
        self.on_before_commit = on_before_commit
        initialize(path)

    def create_account(self, account_id: str, initial_balance: int = 0) -> None:
        _check_id(account_id)
        _check_units(initial_balance, minimum=0)
        with transaction(self.path, write=True) as conn:
            if conn.execute("SELECT 1 FROM accounts WHERE account_id=?", (account_id,)).fetchone():
                raise Conflict("duplicate account")
            conn.execute(
                "INSERT INTO accounts(account_id, opening_balance, balance) VALUES (?, ?, ?)",
                (account_id, initial_balance, initial_balance),
            )

    def balance(self, account_id: str) -> int:
        _check_id(account_id)
        with transaction(self.path) as conn:
            row = conn.execute(
                "SELECT balance FROM accounts WHERE account_id=?", (account_id,)
            ).fetchone()
            if row is None:
                raise NotFound(account_id)
            return row["balance"]

    def snapshot(self) -> dict[str, int]:
        with transaction(self.path) as conn:
            rows = conn.execute(
                "SELECT account_id, balance FROM accounts ORDER BY account_id"
            ).fetchall()
            return {row["account_id"]: row["balance"] for row in rows}

    def transfer(self, request_id: str, source: str, target: str, amount: int) -> dict:
        _check_id(request_id)
        _check_id(source)
        _check_id(target)
        _check_units(amount, minimum=1)
        if source == target:
            raise InvalidRequest("source and target must differ")
        receipt = _receipt(request_id, source, target, amount)
        with transaction(self.path, write=True) as conn:
            existing = conn.execute(
                "SELECT source, target, amount, status FROM transfers WHERE request_id=?",
                (request_id,),
            ).fetchone()
            if existing is not None:
                if (existing["source"], existing["target"], existing["amount"], existing["status"]) != (
                    source, target, amount, "committed"
                ):
                    raise Conflict("request_id already used with a different payload or status")
                return receipt

            src = conn.execute(
                "SELECT balance FROM accounts WHERE account_id=?", (source,)
            ).fetchone()
            dst = conn.execute(
                "SELECT balance FROM accounts WHERE account_id=?", (target,)
            ).fetchone()
            if src is None or dst is None:
                raise NotFound("account missing")
            if src["balance"] < amount:
                raise InsufficientFunds("insufficient funds")
            if dst["balance"] > MAX_UNITS - amount:
                raise Conflict("recipient balance overflow")

            conn.execute(
                "UPDATE accounts SET balance=balance-? WHERE account_id=?", (amount, source)
            )
            conn.execute(
                "UPDATE accounts SET balance=balance+? WHERE account_id=?", (amount, target)
            )
            conn.execute(
                "INSERT INTO transfers(request_id, source, target, amount, status) "
                "VALUES (?, ?, ?, ?, 'committed')", (request_id, source, target, amount)
            )
            conn.execute(
                "INSERT INTO journal(request_id, account_id, delta) VALUES (?, ?, ?)",
                (request_id, source, -amount),
            )
            conn.execute(
                "INSERT INTO journal(request_id, account_id, delta) VALUES (?, ?, ?)",
                (request_id, target, amount),
            )
            if self.on_before_commit is not None:
                self.on_before_commit(request_id)
        return receipt

    def audit(self) -> dict:
        """Read-only, transactionally consistent audit; never repair corruption."""
        with transaction(self.path) as conn:
            accounts = conn.execute(
                "SELECT account_id, opening_balance, balance FROM accounts"
            ).fetchall()
            transfers = conn.execute(
                "SELECT request_id, source, target, amount, status FROM transfers"
            ).fetchall()
            journal = conn.execute(
                "SELECT request_id, account_id, delta FROM journal ORDER BY entry_id"
            ).fetchall()

            by_account = {row["account_id"]: row for row in accounts}
            by_request = {row["request_id"]: row for row in transfers}
            deltas = {account_id: 0 for account_id in by_account}
            entries = {request_id: [] for request_id in by_request}

            for row in journal:
                account_id, request_id = row["account_id"], row["request_id"]
                if account_id not in by_account or request_id not in by_request:
                    raise InvariantViolation("orphan journal entry")
                deltas[account_id] += row["delta"]
                entries[request_id].append((account_id, row["delta"]))

            for row in accounts:
                opening, balance = row["opening_balance"], row["balance"]
                if not (0 <= opening <= MAX_UNITS and 0 <= balance <= MAX_UNITS):
                    raise InvariantViolation("account balance out of bounds")
                if balance != opening + deltas[row["account_id"]]:
                    raise InvariantViolation("account balance does not reconcile")

            for row in transfers:
                request_id = row["request_id"]
                amount = row["amount"]
                if (row["status"] != "committed" or type(amount) is not int
                    or not 1 <= amount <= MAX_UNITS or row["source"] == row["target"]):
                    raise InvariantViolation("malformed or uncommitted transfer")
                expected = [(row["source"], -amount), (row["target"], amount)]
                if len(entries[request_id]) != 2 or sorted(entries[request_id]) != sorted(expected):
                    raise InvariantViolation("transfer journal mismatch")

            return {
                "accounts": len(accounts),
                "transfers": len(transfers),
                "total_balance": sum(row["balance"] for row in accounts),
            }
