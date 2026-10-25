# Senior Ledger Blind Benchmark — CHATGPT-R01

## Delivery identity

Experiment `SENIOR-LEDGER-20261025`, protocol V1.0, agent `CHATGPT`, run `R01`. Repository `kaibahaha/xxsc`, branch `exp/senior-ledger-20261025`, exclusive destination `/results/senior-ledger-20261025/CHATGPT-R01/`. The frozen source directory `/benchmarks/senior-ledger-20261025/` was read only. No other Agent's results were read, and no external AI generated code.

## Actual timeline (Beijing time, UTC+08:00)

| Required milestone | Observed time and evidence |
|---|---|
| Planned wakeup | `2026-10-25T12:57:58+08:00` (scheduler registration) |
| Actual start | `2026-10-25T12:57:19+08:00` (first live time widget observation; earlier than planned time, scheduler discrepancy not explained) |
| Started coding | `2026-10-25T12:58:18.140700+08:00` (first source-file filesystem write timestamp; earliest independently observed coding artifact, not an exact human keystroke time) |
| Finished coding | `2026-10-25T12:59:02.750110+08:00` (last regression-test source-file write timestamp) |
| Last Git readback completed at report cutoff | **By** `2026-10-25T13:01:29+08:00`, after independent readback of the first seven delivered files. Exact per-call completion timestamp is not exposed by connector; later report/manifest readbacks necessarily postdate this cutoff. See final execution reply for the true final readback status. |

The observed coding artifact interval was approximately **44.61 seconds**; the first clock observation to report-cutoff interval was **4 minutes 10 seconds**. These intervals are not a claim that all nine Git commits had completed at report cutoff.

## Engineering changes

The public API, exception inheritance, SQLite schema columns and existing data format remain compatible with the frozen starter. All four required modules are delivered as complete files. The implementation uses only Python standard library and SQLite.

**Atomicity and concurrency.** Every account creation and transfer uses one explicit `BEGIN IMMEDIATE` transaction, which obtains SQLite's cross-process writer reservation before reading idempotency state or balances. Each transfer writes the two account balances, one transfer record, and exactly two journal entries in one transaction. Any exception, including a `BaseException` from the precommit callback, rolls back the entire transaction. Each connection is closed in `finally`. The SQLite connection timeout is 30 seconds to tolerate ordinary short-lived lock contention.

**Idempotency and validation.** IDs remain untrimmed nonblank strings; bool is rejected as an integer amount or opening balance. Values are bounded to signed SQLite 64-bit integers. The first committed request stores its exact payload. A duplicate with identical payload returns the same five-key receipt before balance checks and without callback; any different payload raises `Conflict`. A recipient credit overflow raises `Conflict` before DML, and insufficient funds raises `InsufficientFunds` without persistence.

**Audit.** A single read transaction captures all accounts, transfers and journal entries consistently. The audit checks account opening balance plus net journal deltas, nonnegative bounded balances, exactly two matching journal entries for each committed transfer, no orphan entries, and no uncommitted or malformed transfer. On failure it raises `InvariantViolation` without changing data. The result contains only `accounts`, `transfers`, and `total_balance`.

## Actual tests

The frozen public test file's exact Git blob SHA was independently verified as `242db970a4700aa83e18afcf8b5fb905e6c01947` before execution. The local execution environment provided Python **3.13.5**, not Python 3.11; this compatibility limitation is explicitly disclosed.

| Suite | Executed | Passed | Failed | Errors | Actual process exit |
|---|---:|---:|---:|---:|---:|
| Frozen public `test_public.py` | 23 | 23 | 0 | 0 | 0 |
| Independent `test_regression.py` | 22 | 22 | 0 | 0 | 0 |
| **Total executed** | **45** | **45** | **0** | **0** | **0** |
| Python 3.11 verification | NOT_EXECUTED | — | — | — | — |
| Hidden grading tests | NOT_EXECUTED | — | — | — | — |

The self-authored regression suite exercises strict input bounds, untrimmed IDs, callback rollback and retry, global idempotency, conflicting payloads, 64-bit overflow, thread and process contention, durable reopen, audit tampering and non-repair behavior. The Python 3.13 multiprocessing fork warning is preserved verbatim in `TEST_RESULTS.txt`; it did not cause test failure. No hidden-test result or score is predicted.

## Git evidence and limitations

Each completed file was committed separately using GitHub's contents API, then independently fetched from the same branch and checked for exact content equality. The verified code commits are:

- `__init__.py`: `421299857cec9ab46133b448396a0481957008d3`
- `errors.py`: `037c9b454d70d65f2757a02e05b78b656b472bc6`
- `db.py`: `7c37341b7dd126cc5dffab8592c574892bff3999`
- `service.py`: `4d9e700303b9fa2ab0062726ab9ed1eef30e6edb`
- `test_regression.py`: `65b099e855a29253c7d1309cbf0c2f8aab911cd7`
- `TEST_RESULTS.txt`: `244cc2cfa92a29088f9e9d6873c05f07bb832f0f`
- `RUN_LOG.md`: `444a1a7af83fb973df97c07fe12573bb787a8d2b`

The final `MANIFEST.md` records Git paths and blob SHAs, including the subsequent report commit. A manifest cannot embed its own final Git blob SHA without changing that SHA; its own SHA is therefore to be supplied in the external final delivery receipt after independent Git readback. The exact final readback time similarly cannot be truthfully prewritten into the file whose commit and readback are still pending. No Git write failure was observed as of this report cutoff. An attempted malformed read-only GitHub branch URL returned HTTP 400; it was corrected and did not affect source or results.

**Risk statement:** 45/45 locally executed tests passed on Python 3.13.5. This is evidence of these specific tests only, not a guarantee about Python 3.11, adversarial hidden tests, or runtime behavior under every lock-contention pattern.
