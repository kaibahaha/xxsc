# A｜持久化租约调度器与崩溃恢复｜重启后R01待派单

- Experiment: FACTORY24-20261030
- Slot: 20261030-0132-R01 (Asia/Shanghai 2026-10-30 01:32)
- Intended unique ID: FACTORY24-20261030-20261030-0132-R01-A
- Parent interrupted job: `9712edf966b54027`
- New job_id: **NONE** (submit tool blocked by safety checks before server acceptance; no retry this round)
- State: **SUBMISSION_BLOCKED / DEFERRED**; NOT QUEUED, NOT RUNNING, NOT DONE.
- Old workdir: `/home/workbuddy_agent/factory24_20261030/20261030-01/A/` (not yet checked remotely)
- New workdir: `/home/workbuddy_agent/factory24_20261030/restart_20261030_0132/20261030-0132-R01/A/`

## Specification
READY/LEASED/ACKED/FAILED/DEAD状态机；线程安全claim；fencing token；续租/超时回收；幂等去重；CRC32 JSONL WAL、截断恢复与checkpoint；确定性退避与DLQ；CLI。重点测试并发claim、重启、断电、损坏日志和过期token。

## Acceptance
Python3.11+ standard library only; ≥6 meaningful modules; ≥40 real unittest cases; inject clock/faults, deterministic regression; actually run `python3 -m unittest discover -s tests -v`, preserve exit code and raw output; deliver full `src/`, `tests/`, README.md, REPORT.md, TEST_RESULTS.txt, MANIFEST.md with SHA256. First inspect old workdir read-only; reuse valid partial code only in new directory. No secret access, no production modification, no dependency install. Target Git `kaibahaha/xxsc` branch `exp/factory24-20261030`, under `results/factory24-20261030/rounds/20261030-0132-R01/A/`; commit actual source and tests, read back. Do not report PASS until independent verification.
