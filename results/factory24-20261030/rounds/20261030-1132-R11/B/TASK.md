# FACTORY24-20261030-20261030-1132-R11-B

- Title: Append-only tamper-evident audit ledger with inclusion proofs
- Source job_id: `b4811053fb6e4b47`
- WorkBuddy accepted submission, not completed code.
- Planned slot: 2026-10-30 11:32 Asia/Shanghai (R11/24).
- Full specification: Modules canonical_codec, records, hash_chain, append_store, merkle_proofs, checkpoint, verifier, recovery, fault_injection. API append/verify/inclusion_proof/verify_proof/checkpoint/restore. Canonical JSON, domain-separated SHA256, tenant isolation, duplicate event id idempotence, immutable history, monotonic sequence, fsync and partial tail, deterministic recovery. Ten adversarial probes: tamper payload, reorder, forged hash, missing sequence, replay, cross-tenant proof, truncated tail, fsync error, checkpoint mismatch, Unicode canonicalization ambiguity.

## Execution, tests and Git delivery

Python 3.11+ stdlib only; offline, no pip, no credentials, no production access. Workdir /home/workbuddy_agent/factory24_20261030/restart_20261030_0132/20261030-1132-R11/B/. Git repo kaibahaha/xxsc, branch exp/factory24-20261030, ONLY results/factory24-20261030/rounds/20261030-1132-R11/B/. At least 6 functional modules, 40 independently counted unittest tests including 10 adversarial, injectable clock, deterministic regression, fault injection, idempotence/recovery. Commit runnable src/ tests/ README.md as early checkpoint, then iterate. Run exactly python3 -m unittest discover -s tests -v, save true exit code and full output in TEST_RESULTS.txt. Deliver src/, tests/, README.md, REPORT.md, TEST_RESULTS.txt, MANIFEST.md with SHA256 for all payload files excluding MANIFEST itself, source job_id and real commit SHA. Git push and independently read back source, test, report and manifest; no invented results. Never commit .env/tokens/private keys/PII; do not write outside experiment root or touch another branch.

Acceptance: >=6 modules; >=40 stdlib unittest; >=10 adversarial cases; exact test command with real exit code; actual Git code/test/readback; independently verified by ChatGPT in separate audit. Any failed/queued job remains unverified.
