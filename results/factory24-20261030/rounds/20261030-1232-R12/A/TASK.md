# FACTORY24-20261030-20261030-1232-R12-A — Event-sourced projection engine

- Job ID: `38e73a78f9e64bf8`; submission ACCEPTED, asynchronous. Topic: crash-recoverable event-sourced projections with atomic snapshots.
- Workdir: `/home/workbuddy_agent/factory24_20261030/restart_20261030_0132/20261030-1232-R12/A/`.
- At least 6 Python 3.11 standard-library modules: event_schema, append_log, projector, checkpoint, snapshot, recovery, fault_injection, clock.
- JSONL append-only log with sequence/integrity and transaction boundary, account/inventory projection, atomic snapshots and replay, idempotent event IDs, corrupt/truncated-tail handling, projection version migration, deterministic injectable clock/faults; reject malformed inputs and ensure no double counting.
- At least 40 unittest cases and >=10 adversarial cases; run `python3 -m unittest discover -s tests -v` and record actual exit code; deliver src/, tests/, README.md, REPORT.md, TEST_RESULTS.txt, MANIFEST.md with SHA256.
- Git repo `kaibahaha/xxsc`, branch `exp/factory24-20261030`, path `results/factory24-20261030/rounds/20261030-1232-R12/A/`; push early runnable checkpoints, read back source/test/report/manifest, record real commit SHA. No secrets/pip/network installs. ChatGPT alone owns AUDIT.md and ROUND_REPORT.md.
- Independent audit: PENDING; code is not verified merely because job is accepted.
