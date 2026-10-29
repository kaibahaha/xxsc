# C｜并发限流与熔断模拟平台｜重启后R01待派单

- Experiment: FACTORY24-20261030
- Slot: 20261030-0132-R01 (Asia/Shanghai 2026-10-30 01:32)
- Intended unique ID: FACTORY24-20261030-20261030-0132-R01-C
- Parent interrupted job: `fb21843915d24025`
- New job_id: **NONE** (submit tool blocked by safety checks before server acceptance; no retry this round)
- State: **SUBMISSION_BLOCKED / DEFERRED**; NOT QUEUED, NOT RUNNING, NOT DONE.
- Old workdir: `/home/workbuddy_agent/factory24_20261030/20261030-01/C/` (not yet checked remotely)
- New workdir: `/home/workbuddy_agent/factory24_20261030/restart_20261030_0132/20261030-0132-R01/C/`

## Specification
多租户固定/滑动窗口、令牌桶、可注入时钟、幂等TTL、CLOSED/OPEN/HALF_OPEN熔断器、单探针约束、故障注入、指数退避和种子PRNG抖动、权重后端、重试预算、JSONL审计回放、CLI；重点测试并发扣减、时钟倒退、重复计费与回放一致性。

## Acceptance
Python3.11+ standard library only; ≥6 meaningful modules; ≥40 real unittest cases; inject clock/faults, deterministic regression; actually run `python3 -m unittest discover -s tests -v`, preserve exit code and raw output; deliver full `src/`, `tests/`, README.md, REPORT.md, TEST_RESULTS.txt, MANIFEST.md with SHA256. First inspect old workdir read-only; reuse valid partial code only in new directory. No secret access, no production modification, no dependency install. Target Git `kaibahaha/xxsc` branch `exp/factory24-20261030`, under `results/factory24-20261030/rounds/20261030-0132-R01/C/`; commit actual source and tests, read back. Do not report PASS until independent verification.
