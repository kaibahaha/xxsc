# FACTORY24-20261030-20261030-1432-R14-A — R14-A

- Title: Crash-recoverable multiplexed binary frame protocol and credit-flow engine.
- Actual async submit accepted: job_id `7afe0567bdf74102`; source execution state **QUEUED** at first post-submit list, not PASS.
- WorkBuddy workspace: `/home/workbuddy_agent/factory24_20261030/restart_20261030_0132/20261030-1432-R14/A/`.
- Only Git repository `kaibahaha/xxsc`, branch `exp/factory24-20261030`, root `/results/factory24-20261030/rounds/20261030-1432-R14/A/`.
- Python 3.11+ stdlib only; no pip/network install/credentials/production modifications.
- Implement >=8 substantive modules: protocol, codec, incremental bounded parser, stream state, credit flow, retransmission, journal+snapshot recovery, deterministic fault injection, public engine API.
- Required semantics: fragmented/coalesced frames, network byte order, magic/version/length/CRC32 validation, bounded resynchronization, per-stream sequence and ACK, duplicate idempotence, out-of-order bounded buffering, credit backpressure, retransmission with injected clock, FIN/RESET, crash recovery from CRC journal and atomic snapshot, deterministic replay.
- >=40 actual independent stdlib unittest cases, >=10 adversarial cases, fake clock, failure injection, idempotent recovery, strict memory bounds. Run `python3 -m unittest discover -s tests -v`, capture real exit code in TEST_RESULTS.txt.
- Save complete `src/`, `tests/`, README.md, REPORT.md, TEST_RESULTS.txt, MANIFEST.md (SHA256 each artifact, excluding MANIFEST itself). Do not self-hash. Prefer early minimal functional checkpoint before expanding. Commit to this branch if legitimately authorized Git capability exists; otherwise preserve actual local files and report GIT_BLOCKED without inventing commit or reconstructing source from a summary.
- Before any Git write inspect for secrets/private data. WorkBuddy must not modify ChatGPT-managed AUDIT.md, ROUND_REPORT.md, ledger/INDEX.md or other projects. ChatGPT independently verifies source, tests, report, manifest, and Git commit; author tests are SELF_TEST only.
