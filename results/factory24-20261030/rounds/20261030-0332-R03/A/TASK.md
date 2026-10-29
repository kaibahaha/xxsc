# R03-A｜可恢复DAG工作流引擎

- Task ID: `FACTORY24-20261030-20261030-0332-R03-A`
- Job ID: `fd0bc26fcc7b489b`
- Workdir: `/home/workbuddy_agent/factory24_20261030/restart_20261030_0132/20261030-0332-R03/A/`
- Git target: `results/factory24-20261030/rounds/20261030-0332-R03/A/`
- State at dispatch: QUEUED; source/tests: GIT_PENDING.

## Requirements
Python 3.11 standard library only; >=6 business modules; >=40 unittest cases. DAG cycle and missing-dependency validation; deterministic topological execution; priority and resource constraints; injectable clock; retry/backoff and idempotency; atomic snapshot plus append log crash recovery; cancellation, timeout and failure propagation; thread-safe worker scheduling; auditable event history. Fault-inject partial WAL, corruption, worker races and replay. Run `python3 -m unittest discover -s tests -v` and preserve true exit code.

## Required Git deliverables
`src/`, `tests/`, `README.md`, `REPORT.md`, `TEST_RESULTS.txt`, `MANIFEST.md` with file SHA256 and noncircular commit linkage. WorkBuddy must push to exact branch and independently read back files. No secret material or other project changes. Completion and independent audit are pending.
