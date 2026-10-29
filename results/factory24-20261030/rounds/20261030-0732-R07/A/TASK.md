# FACTORY24-20261030-20261030-0732-R07-A | 崩溃一致性持久化租约调度器

- Scheduled slot: 2026-10-30 07:32 Asia/Shanghai (R07); actual submitted before nominal slot during automation execution.
- WorkBuddy job_id: `6f4ee441c0d34b3f`; accepted via submit_workbuddy_task; initial status: RUNNING.
- Historical interrupted parent_job_id: `9712edf966b54027`; failed R02 predecessor: `15a3ffc753c64dcb` (3600s timeout).
- WorkBuddy isolated workdir: `/home/workbuddy_agent/factory24_20261030/restart_20261030_0132/20261030-0732-R07/A/`.
- Scope: domain, clock, wal, store, lease, scheduler, recovery, fault；CRC32/WAL/原子快照、fencing token、CAS、幂等、FakeClock、确定性故障注入；至少40个unittest与10个反例。
- Recovery: inspect historical workdirs read-only, preserve history, reuse verified non-sensitive source if found; new job_id remains distinct.
- Constraints: Python 3.11+ standard library only; no pip/network install/credentials/production files; injectable clock, deterministic regression, fault injection.
- Required real command: `python3 -m unittest discover -s tests -v`; record real stdout/stderr/exit code in TEST_RESULTS.txt.
- Git: `kaibahaha/xxsc`, branch `exp/factory24-20261030`, target `/results/factory24-20261030/rounds/20261030-0732-R07/A/`. Deliver all actual `src/*.py`, `tests/test_*.py`, `README.md`, `REPORT.md`, `TEST_RESULTS.txt`, `MANIFEST.md` with SHA256 list excluding MANIFEST self-hash, source job_id and actual commit SHA.
- Before public push, inspect for credentials, .env, tokens, private keys, personal information and production configuration; use existing authorization without reading or exposing secrets. Independently read back actual source, tests, report, index. No Git evidence means GIT_PENDING/BLOCKED, never PASS.
- The WorkBuddy submitted prompt contains the full implementation and acceptance requirements. This TASK file is a concise audit trail, not a claim of completion.
