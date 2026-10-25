"""Independent regression tests for the MiniLedger transactional contract."""
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import os
import sqlite3
import tempfile
import threading
import unittest

from mini_ledger import (
    Conflict, InsufficientFunds, InvalidRequest, InvariantViolation, Ledger, NotFound,
)

MAX = (1 << 63) - 1


def _process_transfer(args):
    path, request_id, amount = args
    try:
        return Ledger(path).transfer(request_id, "source", "target", amount)
    except InsufficientFunds:
        return "insufficient"


class RegressionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.temp.name, "ledger.sqlite")
        self.ledger = Ledger(self.path)
        self.ledger.create_account("source", 100)
        self.ledger.create_account("target", 0)

    def tearDown(self):
        self.temp.cleanup()

    def _sql(self, statement, params=()):
        with sqlite3.connect(self.path) as conn:
            conn.execute(statement, params)

    def test_bool_and_numeric_bounds(self):
        for invalid in [True, False, 0, -1, MAX + 1, 1.5, "3", None]:
            with self.subTest(invalid=invalid), self.assertRaises(InvalidRequest):
                self.ledger.transfer("bad", "source", "target", invalid)
        for invalid in [True, -1, MAX + 1, 1.2, None]:
            with self.subTest(opening=invalid), self.assertRaises(InvalidRequest):
                self.ledger.create_account("invalid", invalid)
        self.assertEqual(self.ledger.audit()["transfers"], 0)

    def test_invalid_ids_preserve_original_string(self):
        for invalid in ["", " \t\n ", None, 1, False]:
            with self.subTest(invalid=invalid), self.assertRaises(InvalidRequest):
                self.ledger.create_account(invalid)
        self.ledger.create_account("  spaced  ", 2)
        self.assertEqual(self.ledger.balance("  spaced  "), 2)
        with self.assertRaises(NotFound):
            self.ledger.balance("spaced")

    def test_path_validation(self):
        for path in [None, "", 5, False]:
            with self.subTest(path=path), self.assertRaises(InvalidRequest):
                Ledger(path)

    def test_idempotency_after_balance_exhausted(self):
        first = self.ledger.transfer("same", "source", "target", 100)
        self.assertEqual(Ledger(self.path).transfer("same", "source", "target", 100), first)
        self.assertEqual(self.ledger.audit()["transfers"], 1)

    def test_conflict_payload_dimensions(self):
        self.ledger.create_account("third")
        self.ledger.transfer("once", "source", "target", 1)
        for source, target, amount in [("third", "target", 1), ("source", "third", 1), ("source", "target", 2)]:
            with self.subTest(source=source, target=target, amount=amount), self.assertRaises(Conflict):
                self.ledger.transfer("once", source, target, amount)
        self.assertEqual(self.ledger.audit()["transfers"], 1)

    def test_self_transfer_and_notfound(self):
        with self.assertRaises(InvalidRequest):
            self.ledger.transfer("self", "source", "source", 1)
        with self.assertRaises(NotFound):
            self.ledger.transfer("missing", "ghost", "target", 1)
        with self.assertRaises(NotFound):
            self.ledger.balance("ghost")

    def test_callback_rollback_and_retry(self):
        calls = []
        def crash(request_id):
            calls.append(request_id)
            raise KeyboardInterrupt("abort")
        failing = Ledger(self.path, on_before_commit=crash)
        with self.assertRaises(KeyboardInterrupt):
            failing.transfer("abort", "source", "target", 9)
        self.assertEqual(calls, ["abort"])
        self.assertEqual(self.ledger.snapshot(), {"source": 100, "target": 0})
        self.assertEqual(self.ledger.audit()["transfers"], 0)
        self.ledger.transfer("abort", "source", "target", 9)
        self.assertEqual(self.ledger.audit()["transfers"], 1)

    def test_callback_only_on_new_success(self):
        calls = []
        ledger = Ledger(self.path, on_before_commit=calls.append)
        ledger.transfer("once", "source", "target", 3)
        ledger.transfer("once", "source", "target", 3)
        with self.assertRaises(InsufficientFunds):
            ledger.transfer("overdraw", "source", "target", 100)
        self.assertEqual(calls, ["once"])

    def test_credit_overflow_is_atomic(self):
        self.ledger.create_account("full", MAX)
        with self.assertRaises(Conflict):
            self.ledger.transfer("overflow", "source", "full", 1)
        self.assertEqual(self.ledger.audit(), {"accounts": 3, "transfers": 0, "total_balance": MAX + 100})

    def test_maximum_valid_transfer(self):
        self.ledger.create_account("rich", MAX)
        self.ledger.create_account("empty")
        self.ledger.transfer("max", "rich", "empty", MAX)
        self.assertEqual(self.ledger.balance("empty"), MAX)
        self.assertEqual(self.ledger.audit()["transfers"], 1)

    def test_thread_duplicate_once(self):
        gate = threading.Barrier(12)
        def run(_):
            gate.wait(timeout=10)
            return Ledger(self.path).transfer("dup", "source", "target", 50)
        with ThreadPoolExecutor(max_workers=12) as executor:
            results = list(executor.map(run, range(12)))
        self.assertEqual(len(results), 12)
        self.assertTrue(all(r == results[0] for r in results))
        self.assertEqual(self.ledger.audit()["transfers"], 1)

    def test_thread_overdraw(self):
        def run(i):
            try:
                Ledger(self.path).transfer(f"thread-{i}", "source", "target", 21)
                return True
            except InsufficientFunds:
                return False
        with ThreadPoolExecutor(max_workers=12) as executor:
            successes = list(executor.map(run, range(12)))
        self.assertEqual(sum(successes), 4)
        self.assertEqual(self.ledger.audit()["transfers"], 4)
        self.assertEqual(self.ledger.snapshot(), {"source": 16, "target": 84})

    def test_process_duplicate_once(self):
        with ProcessPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(_process_transfer, [(self.path, "process-same", 20)] * 8))
        self.assertEqual(len(results), 8)
        self.assertTrue(all(r == results[0] for r in results))
        self.assertEqual(self.ledger.audit()["transfers"], 1)

    def test_process_overdraw(self):
        with ProcessPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(_process_transfer, [(self.path, f"process-{i}", 30) for i in range(8)]))
        self.assertEqual(sum(r != "insufficient" for r in results), 3)
        self.assertEqual(self.ledger.audit()["transfers"], 3)

    def test_audit_orphan_journal(self):
        self._sql("INSERT INTO journal(request_id,account_id,delta) VALUES ('orphan','source',0)")
        with self.assertRaises(InvariantViolation):
            self.ledger.audit()

    def test_audit_journal_unknown_account(self):
        self.ledger.transfer("one", "source", "target", 4)
        self._sql("UPDATE journal SET account_id='unknown' WHERE delta<0")
        with self.assertRaises(InvariantViolation):
            self.ledger.audit()

    def test_audit_uncommitted_transfer(self):
        self.ledger.transfer("one", "source", "target", 4)
        self._sql("UPDATE transfers SET status='pending'")
        with self.assertRaises(InvariantViolation):
            self.ledger.audit()

    def test_audit_transfer_amount_mismatch(self):
        self.ledger.transfer("one", "source", "target", 4)
        self._sql("UPDATE transfers SET amount=5")
        with self.assertRaises(InvariantViolation):
            self.ledger.audit()

    def test_audit_duplicate_journal(self):
        self.ledger.transfer("one", "source", "target", 4)
        self._sql("INSERT INTO journal(request_id,account_id,delta) VALUES ('one','source',-4)")
        with self.assertRaises(InvariantViolation):
            self.ledger.audit()

    def test_audit_negative_balance(self):
        self._sql("UPDATE accounts SET balance=-1 WHERE account_id='target'")
        with self.assertRaises(InvariantViolation):
            self.ledger.audit()

    def test_audit_never_repairs_corruption(self):
        self.ledger.transfer("one", "source", "target", 4)
        self._sql("DELETE FROM journal WHERE delta>0")
        with self.assertRaises(InvariantViolation):
            self.ledger.audit()
        with sqlite3.connect(self.path) as conn:
            count = conn.execute("SELECT COUNT(*) FROM journal").fetchone()[0]
        self.assertEqual(count, 1)

    def test_snapshot_order_and_durability(self):
        self.ledger.create_account(" AAA ", 1)
        self.ledger.create_account("aaa", 2)
        self.ledger.transfer("persist", "source", "target", 10)
        reopened = Ledger(self.path)
        self.assertEqual(list(reopened.snapshot()), [" AAA ", "aaa", "source", "target"])
        self.assertEqual(reopened.audit(), {"accounts": 4, "transfers": 1, "total_balance": 103})


if __name__ == "__main__":
    unittest.main()
