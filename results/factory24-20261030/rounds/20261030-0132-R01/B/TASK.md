# B｜增量策略DSL与安全执行器｜重启后R01待派单

- Experiment: FACTORY24-20261030
- Slot: 20261030-0132-R01 (Asia/Shanghai 2026-10-30 01:32)
- Intended unique ID: FACTORY24-20261030-20261030-0132-R01-B
- Parent interrupted job: `a154efd28abc4eb5`
- New job_id: **NONE** (submit tool blocked by safety checks before server acceptance; no retry this round)
- State: **SUBMISSION_BLOCKED / DEFERRED**; NOT QUEUED, NOT RUNNING, NOT DONE.
- Old workdir: `/home/workbuddy_agent/factory24_20261030/20261030-01/B/` (not yet checked remotely)
- New workdir: `/home/workbuddy_agent/factory24_20261030/restart_20261030_0132/20261030-0132-R01/B/`

## Specification
Lexer带行列号、Pratt Parser、AST、静态类型检查、常量折叠、三值逻辑、预算受限解释器、版本缓存和CLI。rule <name> priority <int> when <expr> then allow|deny|review；同级deny优先；禁止eval/exec；重点测试恶意输入、短路、深度预算、转义与缓存失效。

## Acceptance
Python3.11+ standard library only; ≥6 meaningful modules; ≥40 real unittest cases; inject clock/faults, deterministic regression; actually run `python3 -m unittest discover -s tests -v`, preserve exit code and raw output; deliver full `src/`, `tests/`, README.md, REPORT.md, TEST_RESULTS.txt, MANIFEST.md with SHA256. First inspect old workdir read-only; reuse valid partial code only in new directory. No secret access, no production modification, no dependency install. Target Git `kaibahaha/xxsc` branch `exp/factory24-20261030`, under `results/factory24-20261030/rounds/20261030-0132-R01/B/`; commit actual source and tests, read back. Do not report PASS until independent verification.
