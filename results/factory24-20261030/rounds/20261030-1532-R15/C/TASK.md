# Checkpointed bounded-memory streaming ETL with exactly-once sink commits

- Unique task: `FACTORY24-20261030-20261030-1532-R15-C`
- Actual async WorkBuddy job_id: `6d6908762aef4d48` (accepted in R15)
- Scheduled slot: Beijing 2026-10-30 15:32; submitted after slot time.
- Work directory: `/home/workbuddy_agent/factory24_20261030/restart_20261030_0132/20261030-1532-R15/C/`
- Git: `kaibahaha/xxsc` branch `exp/factory24-20261030`; sole destination `/results/factory24-20261030/rounds/20261030-1532-R15/C/`.

## Engineering contract
Python 3.11+ standard library only, offline. >=6 functional modules: framing,parser,schema,transforms,checkpoint,sink,dead_letter,pipeline,faults. Core features: streaming JSONL/CSV, byte offsets, UTF-8 boundaries, poison quarantine, transactional sink segments, crash-safe checkpoints and dedupe. Implement documented invariants, injectable clock, deterministic failure injection, idempotency, crash/restart recovery and strict input bounds. >=40 independently named unittest cases, >=10 adversarial cases. Actually run `python3 -m unittest discover -s tests -v`, save real exit code and verbatim output. Required actual source under src/, tests/, README.md, REPORT.md, TEST_RESULTS.txt, MANIFEST.md (SHA256 payload hashes, exclude self). Deliver minimal runnable slice first; expand and commit before 3600s hard limit. Git write/push and independent readback of source+test+report+manifest required; no secrets, credentials, personal data, .env or production files. Never fabricate commit or PASS. If Git unavailable, preserve real local bytes and report GIT_BLOCKED; no code reconstruction from summary. Do not alter ChatGPT-owned management files or other projects.
