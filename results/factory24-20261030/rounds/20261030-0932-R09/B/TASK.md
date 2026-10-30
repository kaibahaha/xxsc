# FACTORY24-20261030-20261030-0932-R09-B

- Title: Safe incremental binary frame parser and replay-resistant session engine
- Source job_id: `a9e2565b170d4e41` (accepted by WorkBuddy MCP Stable)
- Workdir: `/home/workbuddy_agent/factory24_20261030/restart_20261030_0132/20261030-0932-R09/B/`
- Target: `results/factory24-20261030/rounds/20261030-0932-R09/B/` in `kaibahaha/xxsc`, branch `exp/factory24-20261030`.
- Python 3.11+ stdlib only. Modules: versioned wire frame with CRC, incremental parser, input validator, session state, replay-window persistence, rate/backpressure, crash-consistent checkpoints, fault injector, gateway coordinator. Must reject hostile lengths, malformed UTF8, unknown flags, replay and stale epochs, corruption, invalid ACK, partial frames; ensure bounded memory, deterministic clock, idempotency and fault recovery.
- At least 40 distinct unittest methods, 10 adversarial cases, deterministic fault injection; run `python3 -m unittest discover -s tests -v` and record true exit code.
- Required Git artifacts: `src/`, `tests/`, `README.md`, `REPORT.md`, `TEST_RESULTS.txt`, `MANIFEST.md` with SHA256; early code push, final readback, no secrets or production data, no writes outside task subtree.
- Submission: ACCEPTED, status QUEUED; source/tests not yet delivered. Full detailed specification was supplied to WorkBuddy.
