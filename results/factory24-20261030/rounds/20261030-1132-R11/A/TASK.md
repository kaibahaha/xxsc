# FACTORY24-20261030-20261030-1132-R11-A

- Title: PRE-RESTART lease scheduler recovery / crash-consistent journal and fencing
- Source job_id: `e5909f9386404880`
- WorkBuddy accepted submission, not completed code.
- Planned slot: 2026-10-30 11:32 Asia/Shanghai (R11/24).
- Full specification: Parent interrupted job 9712edf966b54027; failed retry 6f4ee441c0d34b3f. First read-only inspect old A workdirs; salvage if possible without touching originals, else rebuild. Modules: models, journal, state_machine, lease_manager, clock, recovery, scheduler, fault_injection, validation. API schedule/acquire/heartbeat/ack/fail/recover. Require fsync WAL, torn tail, fencing tokens, expiry redelivery, deterministic tie-break, idempotence. Ten adversarial probes: duplicate schedule, stale ack, stale heartbeat, torn WAL, checksum mismatch, crash between append/apply, fsync failure, clock rollback, expiry boundary, concurrency.

## Execution, tests and Git delivery

Python 3.11+ stdlib only; offline, no pip, no credentials, no production access. Workdir /home/workbuddy_agent/factory24_20261030/restart_20261030_0132/20261030-1132-R11/A/. Git repo kaibahaha/xxsc, branch exp/factory24-20261030, ONLY results/factory24-20261030/rounds/20261030-1132-R11/A/. At least 6 functional modules, 40 independently counted unittest tests including 10 adversarial, injectable clock, deterministic regression, fault injection, idempotence/recovery. Commit runnable src/ tests/ README.md as early checkpoint, then iterate. Run exactly python3 -m unittest discover -s tests -v, save true exit code and full output in TEST_RESULTS.txt. Deliver src/, tests/, README.md, REPORT.md, TEST_RESULTS.txt, MANIFEST.md with SHA256 for all payload files excluding MANIFEST itself, source job_id and real commit SHA. Git push and independently read back source, test, report and manifest; no invented results. Never commit .env/tokens/private keys/PII; do not write outside experiment root or touch another branch.

Acceptance: >=6 modules; >=40 stdlib unittest; >=10 adversarial cases; exact test command with real exit code; actual Git code/test/readback; independently verified by ChatGPT in separate audit. Any failed/queued job remains unverified.
