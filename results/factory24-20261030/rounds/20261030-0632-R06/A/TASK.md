# R06-A｜崩溃一致性多分区消息队列与消费者组恢复

- Unique task ID: `FACTORY24-20261030-20261030-0632-R06-A`
- Accepted WorkBuddy job_id: `a5076503a4164622`
- Status at submission: **QUEUED** (not RUNNING or DONE).
- Parent job: none; this is a new topic, distinct from previous R02–R05 tasks.
- Workspace: `/home/workbuddy_agent/factory24_20261030/restart_20261030_0132/20261030-0632-R06/A/`.
- Repository `kaibahaha/xxsc`, branch `exp/factory24-20261030`, code delivery under `results/factory24-20261030/rounds/20261030-0632-R06/A/`.

## Full technical acceptance contract

Implement a Python 3.11+ standard-library-only, deterministic crash-consistent append-only multi-partition queue. At least six distinct working modules: `record_codec.py` (length-prefixed binary records and CRC32), `segment_store.py` (append/fsync/segment rotation), `partition_log.py` (monotonic per-partition offsets and scan), `consumer_group.py` (durable per-group ACK/offset and idempotency), `recovery.py` (safe recovery of partial tail vs explicit middle corruption), `faults.py` (injectable clock and fault points), and `queue_api.py` (public interface).

Semantics: strict per-partition offsets; no duplicate offsets after restart; partition/group isolation; unacked replay; idempotent duplicate ACK; crash at write/flush/fsync/rename boundaries; reject invalid inputs and oversized records; binary payloads including empty and non-UTF8; deterministic replay; clearly documented at-least-once delivery and durability boundary (no unjustified exactly-once claim). Must not skip a corrupt middle frame silently. Only use isolated temporary test files; no production reads or secrets.

Write **at least 40 meaningful standard-library unittest cases** and **at least 10 independent adversarial counterexamples** covering corruption, truncation, reboot, ACK, segment boundary, failure injection, clock, resource closure, partition isolation and malformed inputs. Execute `python3 -m unittest discover -s tests -v` and preserve full stdout/stderr plus actual exit code in `TEST_RESULTS.txt`. Deliver complete `src/*.py`, `tests/*.py`, `README.md`, `REPORT.md`, `TEST_RESULTS.txt`, `MANIFEST.md` with SHA256 for actual files except MANIFEST itself, true job_id and commit SHA. Git commit and independent Git readback of source, test, report and manifest are mandatory; if blocked report original error and local artifact paths, not fabricated code.

**Timeout mitigation:** create a runnable minimum implementation and >=10 tests early, push first Git checkpoint within ~10 minutes, then expand and checkpoint every 10–15 minutes. Final >=6 modules/40 tests. No pip, external installs, network dependencies, credentials, production paths, other branches, or modifications to ChatGPT-managed `AUDIT.md`, `ROUND_REPORT.md`, `ledger/INDEX.md`.

## Execution evidence

- `submit_workbuddy_task` returned job_id `a5076503a4164622`.
- Subsequent `list_workbuddy_jobs(limit=50)` independently showed this exact job **QUEUED**, age 4s, output 0 characters.
- Source/tests not yet returned or verified. WorkBuddy self-tests and independent ChatGPT audit remain PENDING.
