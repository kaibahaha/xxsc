# R02-B｜可增量解析的策略DSL与安全执行引擎

- Experiment: FACTORY24-20261030
- Slot: 20261030-0232-R02 (Beijing 2026-10-30 02:32)
- Task ID: FACTORY24-20261030-20261030-0232-R02-B
- Accepted WorkBuddy job_id: `8529435fc4da4624`
- Historical interrupted parent_job_id: `a154efd28abc4eb5`
- State on initial observation: QUEUED (not yet code delivered)
- New isolated workdir: `/home/workbuddy_agent/factory24_20261030/restart_20261030_0132/20261030-0232-R02/B/`
- Historical workdir is read-only; first inspect for recoverable code, then reuse or complete in new isolated directory. Do not alter other projects.

## Functional specification

增量Lexer、Pratt Parser、AST、类型检查、常量折叠、三值逻辑、资源预算解释器、缓存版本失效、CLI；rule <name> priority <int> when <expr> then allow|deny|review，deny优先，同级稳定。

## Required deliverables and acceptance

Python3.11+ standard library only; >=6 business modules; >=40 real unittest cases; injectable clock and deterministic fault injection. Execute `python3 -m unittest discover -s tests -v` and record real exit status, test count and failures. Deliver actual `src/`, `tests/`, `README.md`, `REPORT.md`, `TEST_RESULTS.txt`, `MANIFEST.md` with SHA256 excluding self-hash. No pip/network installation, no credentials, no production modifications. GitHub: `kaibahaha/xxsc`, branch `exp/factory24-20261030`, only `results/factory24-20261030/rounds/20261030-0232-R02/B/`; push complete code and tests, then independently read back source, test, report and record real commit SHA. If push fails, mark GIT_BLOCKED; never invent code or a commit.

This TASK.md is dispatch metadata, **not proof of source delivery or test success**.
