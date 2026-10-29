# R05-A｜确定性故障注入与可重放执行追踪框架

- Unique ID: `FACTORY24-20261030-20261030-0532-R05-A`
- WorkBuddy job_id: `f8de6c9938a94e90`; initial accepted state: QUEUED.
- Scheduled Beijing: 2026-10-30 05:32; no previous job for this slot.
- Source directory (remote): `/home/workbuddy_agent/factory24_20261030/restart_20261030_0132/20261030-0532-R05/A/`
- Git branch: `exp/factory24-20261030`; Git output: `results/factory24-20261030/rounds/20261030-0532-R05/A/`.

## Scope and acceptance
Build a fully offline Python 3.11+ standard-library fault-injection and replay engine, with at least six modules: injected clock, deterministic scheduler, fault rules, trace append/read, checkpoint/recovery, replay consistency, validation. Include seeded randomness, explicit event ordering, retry/idempotency semantics, malformed trace rejection, crash/restart checkpoint semantics, and reproducible failure schedules. At least 40 standard-library unittest tests and ten adversarial counterexamples. Real test command: `python3 -m unittest discover -s tests -v`; save unedited stdout/stderr, exit code, timing. Full actual `src/`, `tests/`, `README.md`, `REPORT.md`, `TEST_RESULTS.txt`, `MANIFEST.md` with SHA256 list (exclude MANIFEST from self-hash). No pip, production access, network installation, credentials, secrets or sensitive data.

## Reliability and Git
Previous R02-A/B/C jobs each failed at ~3600 seconds without returned code. Prioritize minimal complete implementation and early Git commits before verbose narrative. WorkBuddy must push real files to this exact branch/path and read back code/test/report/manifest with actual commit SHA. If Git cannot be written, mark GIT_BLOCKED with real evidence; no invented code or commits. `AUDIT.md` is independently maintained by ChatGPT and must not be overwritten by WorkBuddy.

## Queue and audit
Submitted via actual `submit_workbuddy_task` with `conversation_id=FACTORY24-20261030-20261030-0532-R05-A`. As of submission, accepted but QUEUED. No test results, no source verified, no independent audit or score yet. WorkBuddy self-tests, if later produced, are self-tests only.
