"""Public behavioral tests. They are intentionally incomplete: hidden audit
uses independent cases, thread/process contention and fault injection.
"""
from __future__ import annotations

import os
import sqlite3
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor

from mini_ledger import (
    Conflict, InsufficientFunds, InvalidRequest, InvariantViolation, Ledger, NotFound,
)


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "ledger.sqlite")
        self.db = Ledger(self.path)
        self.db.create_account("alice", 100)
        self.db.create_account("bob", 0)

    def tearDown(self):
        self.tmp.cleanup()

    def test_transfer_and_balances(self):
        out = self.db.transfer("t1", "alice", "bob", 40)
        self.assertEqual(out, {"request_id": "t1", "source": "alice", "target": "bob", "amount": 40, "status": "committed"})
        self.assertEqual(self.db.snapshot(), {"alice": 60, "bob": 40})

    def test_duplicate_exact_idempotent(self):
        out = self.db.transfer("t1", "alice", "bob", 95)
        self.assertEqual(out, self.db.transfer("t1", "alice", "bob", 95))
        self.assertEqual(self.db.snapshot(), {"alice": 5, "bob": 95})

    def test_duplicate_changed_payload_conflicts(self):
        self.db.transfer("t1", "alice", "bob", 20)
        with self.assertRaises(Conflict):
            self.db.transfer("t1", "alice", "bob", 21)
        self.assertEqual(self.db.snapshot(), {"alice": 80, "bob": 20})

    def test_duplicate_other_destination_conflicts(self):
        self.db.create_account("carol")
        self.db.transfer("same", "alice", "bob", 10)
        with self.assertRaises(Conflict):
            self.db.transfer("same", "alice", "carol", 10)

    def test_insufficient_no_side_effect(self):
        with self.assertRaises(InsufficientFunds):
            self.db.transfer("too-much", "alice", "bob", 101)
        self.assertEqual(self.db.snapshot(), {"alice": 100, "bob": 0})
        self.assertEqual(self.db.audit()["transfers"], 0)

    def test_missing_account_no_side_effect(self):
        with self.assertRaises(NotFound):
            self.db.transfer("missing", "alice", "ghost", 1)
        self.assertEqual(self.db.snapshot(), {"alice": 100, "bob": 0})

    def test_self_transfer_rejected(self):
        with self.assertRaises(InvalidRequest):
            self.db.transfer("self", "alice", "alice", 7)
        self.assertEqual(self.db.audit()["transfers"], 0)

    def test_amount_bool_rejected(self):
        with self.assertRaises(InvalidRequest):
            self.db.transfer("bool", "alice", "bob", True)

    def test_opening_balance_bool_rejected(self):
        with self.assertRaises(InvalidRequest):
            self.db.create_account("charlie", True)

    def test_duplicate_account_conflict(self):
        with self.assertRaises(Conflict):
            self.db.create_account("alice", 100)

    def test_nonblank_ids(self):
        with self.assertRaises(InvalidRequest):
            self.db.transfer("  ", "alice", "bob", 1)

    def test_negative_amount_rejected(self):
        with self.assertRaises(InvalidRequest):
            self.db.transfer("neg", "alice", "bob", -1)

    def test_overflow_initial_balance(self):
        with self.assertRaises(InvalidRequest):
            self.db.create_account("huge", 1 << 63)

    def test_credit_overflow_is_atomic(self):
        self.db.create_account("maxed", (1 << 63) - 1)
        with self.assertRaises(Conflict):
            self.db.transfer("overflow", "alice", "maxed", 1)
        self.assertEqual(self.db.snapshot()["alice"], 100)

    def test_rollback_on_injected_crash(self):
        def fail(_request_id):
            raise RuntimeError("simulated crash immediately before commit")
        failed = Ledger(self.path, on_before_commit=fail)
        with self.assertRaises(RuntimeError):
            failed.transfer("crash", "alice", "bob", 10)
        self.assertEqual(self.db.snapshot(), {"alice": 100, "bob": 0})
        self.assertEqual(self.db.audit()["transfers"], 0)
        self.db.transfer("crash", "alice", "bob", 10)
        self.assertEqual(self.db.snapshot(), {"alice": 90, "bob": 10})

    def test_reopen_is_durable(self):
        self.db.transfer("persist", "alice", "bob", 15)
        reopened = Ledger(self.path)
        self.assertEqual(reopened.snapshot(), {"alice": 85, "bob": 15})
        self.assertEqual(reopened.transfer("persist", "alice", "bob", 15)["status"], "committed")
        self.assertEqual(reopened.audit()["transfers"], 1)

    def test_audit_clean(self):
        self.db.transfer("one", "alice", "bob", 10)
        self.db.transfer("two", "bob", "alice", 4)
        self.assertEqual(self.db.audit(), {"accounts": 2, "transfers": 2, "total_balance": 100})

    def test_audit_detects_tampered_balance(self):
        self.db.transfer("one", "alice", "bob", 8)
        with sqlite3.connect(self.path) as c:
            c.execute("UPDATE accounts SET balance=balance+1 WHERE account_id='bob'")
        with self.assertRaises(InvariantViolation):
            self.db.audit()

    def test_audit_detects_forged_journal(self):
        self.db.transfer("one", "alice", "bob", 8)
        with sqlite3.connect(self.path) as c:
            c.execute("UPDATE journal SET delta=delta+1 WHERE delta>0")
        with self.assertRaises(InvariantViolation):
            self.db.audit()

    def test_audit_detects_missing_entry(self):
        self.db.transfer("one", "alice", "bob", 8)
        with sqlite3.connect(self.path) as c:
            c.execute("DELETE FROM journal WHERE delta>0")
        with self.assertRaises(InvariantViolation):
            self.db.audit()

    def test_concurrent_same_request_once(self):
        gate = threading.Barrier(8)
        def call(_):
            gate.wait(timeout=5)
            return self.db.transfer("shared", "alice", "bob", 9)
        with ThreadPoolExecutor(max_workers=8) as pool:
            receipts = list(pool.map(call, range(8)))
        self.assertEqual(len(receipts), 8)
        self.assertEqual(self.db.snapshot(), {"alice": 91, "bob": 9})
        self.assertEqual(self.db.audit()["transfers"], 1)

    def test_concurrent_overdraw_prevented(self):
        gate = threading.Barrier(8)
        def call(i):
            gate.wait(timeout=5)
            try:
                self.db.transfer(f"multi-{i}", "alice", "bob", 30)
                return True
            except InsufficientFunds:
                return False
        with ThreadPoolExecutor(max_workers=8) as pool:
            successes = list(pool.map(call, range(8)))
        self.assertEqual(sum(successes), 3)
        self.assertEqual(self.db.snapshot(), {"alice": 10, "bob": 90})
        self.assertEqual(self.db.audit()["transfers"], 3)

    def test_snapshot_order(self):
        self.db.create_account("aaa", 2)
        self.assertEqual(list(self.db.snapshot()), ["aaa", "alice", "bob"])


if __name__ == "__main__":
    unittest.main()
