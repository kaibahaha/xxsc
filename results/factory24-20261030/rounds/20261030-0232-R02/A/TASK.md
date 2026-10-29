# R02-A｜持久化租约调度器与崩溃恢复

- Experiment: FACTORY24-20261030
- Slot: 20261030-0232-R02 (Beijing 2026-10-30 02:32)
- Task ID: FACTORY24-20261030-20261030-0232-R02-A
- Accepted WorkBuddy job_id: `15a3ffc753c64dcb`
- Historical interrupted parent_job_id: `9712edf966b54027`
- State on initial observation: RUNNING (not yet code delivered)
- New isolated workdir: `/home/workbuddy_agent/factory24_20261030/restart_20261030_0132/20261030-0232-R02/A/`
- Historical workdir is read-only; first inspect for recoverable code, then reuse or complete in new isolated directory. Do not alter other projects.

## Functional specification

READY/LEASED/ACKED/FAILED/DEAD；线程安全claim、可注入单调时钟、fencing token、续租与过期回收、幂等键原子去重、延迟优先级队列、CRC/JSONL WAL尾部恢复、checkpoint与重放、确定性退避、DLQ、CLI。

## Required deliverables and acceptance

Python3.11+ standard library only; >=6 business modules; >=40 real unittest cases; injectable clock and deterministic fault injection. Execute `python3 -m unittest discover -s tests -v` and record real exit status, test count and failures. Deliver actual `src/`, `tests/`, `README.md`, `REPORT.md`, `TEST_RESULTS.txt`, `MANIFEST.md` with SHA256 excluding self-hash. No pip/network installation, no credentials, no production modifications. GitHub: `kaibahaha/xxsc`, branch `exp/factory24-20261030`, only `results/factory24-20261030/rounds/20261030-0232-R02/A/`; push complete code and tests, then independently read back source, test, report and record real commit SHA. If push fails, mark GIT_BLOCKED; never invent code or a commit.

This TASK.md is dispatch metadata, **not proof of source delivery or test success**.
