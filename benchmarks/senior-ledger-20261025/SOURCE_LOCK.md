# SOURCE LOCK — SENIOR-LEDGER-20261025

This file pins the **read-only source-of-truth** for the one-problem senior engineering benchmark. It is a checksum registry, **not a solution**.

- Repository: `kaibahaha/xxsc`
- Benchmark branch: `exp/senior-ledger-20261025`
- Frozen source snapshot commit (before this manifest): `a6834ed534060043b914f865e9f49940cb5475b0`
- Frozen benchmark root: `/benchmarks/senior-ledger-20261025/`
- Allowed result root: `/results/senior-ledger-20261025/<unique-agent-id>/`
- Source files are **never** modified by solver agents. Evaluate their result copy only.
- Candidate must not read another agent's result folder; test authors must not write answers to this branch.
- Verify against Git *blob* SHA and source snapshot above; branch HEAD may move as agents submit and is not a stable source fingerprint.

| Frozen file (relative to benchmark root) | Git blob SHA |
|---|---|
| `README.md` | `c44d4f173dd83ac9f648584da7904fa6f4897dd1` |
| `TASK.md` | `c7ab6a32b44495995ff86f1a3b02346cbc28da2d` |
| `AGENT_PROMPT.md` | `885e7531b0b944113088eec32e9efb57c6fbfb9e` |
| `pyproject.toml` | `2228956a74642ff2c320b1b64ad35fa699fb7ceb` |
| `src/mini_ledger/__init__.py` | `02ac8109cb1ef82ef3338f1db97b9b7af7783fa3` |
| `src/mini_ledger/errors.py` | `a099061138fc8d55c52eae35f87c34e0e461467e` |
| `src/mini_ledger/db.py` | `183b1533442c3069927cefa90e34873dc78ab989` |
| `src/mini_ledger/service.py` | `cc4f6d83e8b9b4ac1cbee736bf16322631f783cb` |
| `tests/test_public.py` | `242db970a4700aa83e18afcf8b5fb905e6c01947` |

Baseline smoke run by benchmark author using Python **3.13.5** (3.11 unavailable in author sandbox): **23 public tests, 11 passed, 10 failures, 2 errors**. These failures are intentional starter defects. Solvers should use 3.11 where available, and must disclose actual interpreter used. This smoke run does not certify 3.11 execution.

Acceptance scores require independently executed tests and Git readback; model self-reported success is not proof. 
