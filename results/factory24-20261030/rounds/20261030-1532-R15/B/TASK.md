# Deterministic CRDT replica anti-entropy and causal merge simulator

- Unique task: `FACTORY24-20261030-20261030-1532-R15-B`
- Actual async WorkBuddy job_id: `2a22271866934425` (accepted in R15)
- Scheduled slot: Beijing 2026-10-30 15:32; submitted after slot time.
- Work directory: `/home/workbuddy_agent/factory24_20261030/restart_20261030_0132/20261030-1532-R15/B/`
- Git: `kaibahaha/xxsc` branch `exp/factory24-20261030`; sole destination `/results/factory24-20261030/rounds/20261030-1532-R15/B/`.

## Engineering contract
Python 3.11+ standard library only, offline. >=6 functional modules: vector_clock,dot,orset,pncounter,lww_register,replica,network,anti_entropy,codec,faults. Core features: causal contexts, observed-remove OR-Set, PN counter, deterministic LWW, partition/heal, duplicate/out-of-order delivery, convergence. Implement documented invariants, injectable clock, deterministic failure injection, idempotency, crash/restart recovery and strict input bounds. >=40 independently named unittest cases, >=10 adversarial cases. Actually run `python3 -m unittest discover -s tests -v`, save real exit code and verbatim output. Required actual source under src/, tests/, README.md, REPORT.md, TEST_RESULTS.txt, MANIFEST.md (SHA256 payload hashes, exclude self). Deliver minimal runnable slice first; expand and commit before 3600s hard limit. Git write/push and independent readback of source+test+report+manifest required; no secrets, credentials, personal data, .env or production files. Never fabricate commit or PASS. If Git unavailable, preserve real local bytes and report GIT_BLOCKED; no code reconstruction from summary. Do not alter ChatGPT-owned management files or other projects.
