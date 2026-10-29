# FACTORY24-20261030-20261030-0732-R07-C | 多租户限流熔断与崩溃恢复控制平面

- Scheduled slot: 2026-10-30 07:32 Asia/Shanghai (R07); actual submitted before nominal slot during automation execution.
- WorkBuddy job_id: `88ba054e03ce42fe`; accepted via submit_workbuddy_task; initial status: QUEUED.
- Historical interrupted parent_job_id: `fb21843915d24025`; failed R02 predecessor: `7db4a2fa2edc4ab0` (3600s timeout).
- WorkBuddy isolated workdir: `/home/workbuddy_agent/factory24_20261030/restart_20261030_0132/20261030-0732-R07/C/`.
- Scope: model, clock, token_bucket, sliding_window, circuit, bulkhead, policy, storage, fault, gateway；原子准入、租户隔离、HALF_OPEN探针、WAL重放、幂等；至少40个unittest与10个反例。
- Recovery: inspect historical workdirs read-only, preserve history, reuse verified non-sensitive source if found; new job_id remains distinct.
- Constraints: Python 3.11+ standard library only; no pip/network install/credentials/production files; injectable clock, deterministic regression, fault injection.
- Required real command: `python3 -m unittest discover -s tests -v`; record real stdout/stderr/exit code in TEST_RESULTS.txt.
- Git: `kaibahaha/xxsc`, branch `exp/factory24-20261030`, target `/results/factory24-20261030/rounds/20261030-0732-R07/C/`. Deliver all actual `src/*.py`, `tests/test_*.py`, `README.md`, `REPORT.md`, `TEST_RESULTS.txt`, `MANIFEST.md` with SHA256 list excluding MANIFEST self-hash, source job_id and actual commit SHA.
- Before public push, inspect for credentials, .env, tokens, private keys, personal information and production configuration; use existing authorization without reading or exposing secrets. Independently read back actual source, tests, report, index. No Git evidence means GIT_PENDING/BLOCKED, never PASS.
- The WorkBuddy submitted prompt contains the full implementation and acceptance requirements. This TASK file is a concise audit trail, not a claim of completion.
