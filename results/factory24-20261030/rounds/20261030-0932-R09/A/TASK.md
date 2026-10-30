# FACTORY24-20261030-20261030-0932-R09-A

- Title: Crash-consistent transactional Outbox/Inbox and deduplicated delivery engine
- Source job_id: `15df528355094f8e` (accepted by WorkBuddy MCP Stable)
- Workdir: `/home/workbuddy_agent/factory24_20261030/restart_20261030_0132/20261030-0932-R09/A/`
- Target: `results/factory24-20261030/rounds/20261030-0932-R09/A/` in `kaibahaha/xxsc`, branch `exp/factory24-20261030`.
- Python 3.11+ stdlib only. Modules: models, injectable clock, framed CRC WAL, atomic transaction store, leased outbox, durable inbox dedup, retry scheduler, fault injector, verifier. Must enforce transaction atomicity, crash replay, stale lease token rejection, inbox idempotency, fair retries, frame bounds, thread safety.
- At least 40 distinct unittest methods, 10 adversarial counterexamples, deterministic fault injection and crash recovery; run `python3 -m unittest discover -s tests -v` and save true exit code.
- Required Git artifacts: `src/`, `tests/`, `README.md`, `REPORT.md`, `TEST_RESULTS.txt`, `MANIFEST.md` with per-file SHA256 and no self-hash. Early incremental code push recommended before 3600s timeout. Git readback required. No secrets or production data. Do not overwrite TASK/AUDIT/ROUND_REPORT/INDEX.
- Submission: ACCEPTED, status QUEUED; source/tests not yet delivered. Prompt delivered to WorkBuddy contains full detailed specifications.
