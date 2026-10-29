# R02-C｜多租户限流与熔断策略模拟平台

- Experiment: FACTORY24-20261030
- Slot: 20261030-0232-R02 (Beijing 2026-10-30 02:32)
- Task ID: FACTORY24-20261030-20261030-0232-R02-C
- Accepted WorkBuddy job_id: `7db4a2fa2edc4ab0`
- Historical interrupted parent_job_id: `fb21843915d24025`
- State on initial observation: QUEUED (not yet code delivered)
- New isolated workdir: `/home/workbuddy_agent/factory24_20261030/restart_20261030_0132/20261030-0232-R02/C/`
- Historical workdir is read-only; first inspect for recoverable code, then reuse or complete in new isolated directory. Do not alter other projects.

## Functional specification

多租户固定/滑动窗口及令牌桶、可注入时钟、并发配额、幂等TTL、CLOSED/OPEN/HALF_OPEN、半开互斥探针、故障注入、退避抖动、权重路由、重试预算、JSONL重放审计、CLI。

## Required deliverables and acceptance

Python3.11+ standard library only; >=6 business modules; >=40 real unittest cases; injectable clock and deterministic fault injection. Execute `python3 -m unittest discover -s tests -v` and record real exit status, test count and failures. Deliver actual `src/`, `tests/`, `README.md`, `REPORT.md`, `TEST_RESULTS.txt`, `MANIFEST.md` with SHA256 excluding self-hash. No pip/network installation, no credentials, no production modifications. GitHub: `kaibahaha/xxsc`, branch `exp/factory24-20261030`, only `results/factory24-20261030/rounds/20261030-0232-R02/C/`; push complete code and tests, then independently read back source, test, report and record real commit SHA. If push fails, mark GIT_BLOCKED; never invent code or a commit.

This TASK.md is dispatch metadata, **not proof of source delivery or test success**.
