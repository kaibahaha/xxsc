# R16-A TASK — deterministic incremental relational query/materialized view engine

- Unique ID: `FACTORY24-20261030-20261030-1632-R16-A`
- WorkBuddy job_id: `eaebe2e61cb644ca`; submit accepted by MCP. This is not proof of successful execution.
- Local isolated path: `/home/workbuddy_agent/factory24_20261030/restart_20261030_0132/20261030-1632-R16/A/`.
- Python 3.11+ stdlib only; no pip/network/credentials/production edits.
- Build at least 8 functional modules for schema, row store, predicates, query planner, operators, incremental materialized views, WAL, recovery, faults and engine. Multi-tenant isolation, transaction commit/rollback, consistent snapshots, group-by/count/sum, deterministic serialization, WAL checksums/truncated-tail recovery, replay idempotence, injectable clock and deterministic fault injection.
- At least 40 real unittest cases and >=10 distinct adversarial cases. Run `python3 -m unittest discover -s tests -v`, record real exit code in TEST_RESULTS.txt. Deliver full `src/`, `tests/`, README.md, REPORT.md, TEST_RESULTS.txt, MANIFEST.md with SHA256 excluding self-hash.
- Only Git target: `kaibahaha/xxsc` branch `exp/factory24-20261030` path `results/factory24-20261030/rounds/20261030-1632-R16/A/`; commit and independently read back actual source+test+REPORT+MANIFEST, record SHA. No fabricated commits, no secrets.
- Execution observation: MCP accepted job, subsequent list marked DONE in ~1s but get_workbuddy_result returned `Model request paused: the daemon is still out of memory after reclaiming unused memory, so this turn cannot be processed safely. The conversation history was preserved unchanged. Restart the app to free memory, then continue.` No code/test output. Status **UPSTREAM_OOM / NOT_DELIVERED**; do not count DONE as program success.
