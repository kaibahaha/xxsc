# FACTORY24-20261030｜R05 真实派单、队列容量与交叉验收报告

- Slot: `20261030-0532-R05`; scheduled Beijing 2026-10-30 05:32. This report reflects live MCP observations in the scheduled run, not a simulation.
- Bridge: `bridge_health` HTTP 200, version **3.3**, `codebuddy_reachable=true`, `max_concurrent_jobs=1`, `min_run_timeout_ms=3600000`; `active_jobs=6` before submission, **7** after. `active_jobs` includes RUNNING+QUEUED and does **not** indicate 7 simultaneous executions.
- `list_workbuddy_jobs(limit=50)`: total 100 jobs at entry (50 displayed), 101 after submission (50 displayed). Recent active jobs are visible; older historical jobs truncated, so do not claim complete global historical enumeration.
- At entry RUNNING=1 (research F3 `5b8ee940847e42f2`), QUEUED=5: programming 3 (R03-A `fd0bc26fcc7b489b`, R03-B `e09bacf7e42349a1`, R04-A `5669468a86524c07`), research 2 (F4 `5458b23070ac460c`, F5 `6f4057fc78094c63`), other 0. `Q_before=5`.
- Adaptive rule Q>=5 => attempt **1** new programming task. Actual `submit_workbuddy_task` accepted `FACTORY24-20261030-20261030-0532-R05-A` (deterministic fault injection and replay engine), `job_id=f8de6c9938a94e90`; independently re-listed as **QUEUED**, not RUNNING/DONE. `Q_after_A=6`, `Q_peak=6`, experiment observed `Q_high_watermark=6`.
- After submission RUNNING=1 (research F3), QUEUED=6: programming 4 (R03-A/B, R04-A, R05-A), research 2 (F4/F5), other 0. New programming jobs accepted=1/1, rejected=0, 429=0 observed, queue-capacity refusals=0 observed, no duplicate POST. `QUEUE_MAX_NOT_REACHED`: evidence only establishes **queue capacity >=6 waiting jobs**, not the exact maximum. Total active 7 = 1 running + 6 queued.
- Waiting-time evidence from list is elapsed age while still QUEUED, not execution time: R03-A ~7466s, R03-B ~7450s, R04-A ~3634s, F4 ~5717s, F5 ~1939s at first observation. R05-A ~4s queued at first post-submit list. Exact `queued_at`/`started_at` timestamps are not exposed; do not infer precise start times. R05-A execution duration: **N/A**.
- Queue growth this round: +1 waiting job; service execution throughput for this programming factory: **0 successful code jobs**, 1 additional terminal execution failure (R02-C); no completion claims.

## Prior rounds and independent audit status

| Round / job | Observed status | Execution/result evidence | Git code/test | Independent audit |
|---|---|---|---|---|
| R02-A `15a3ffc753c64dcb` | FAILED | 3600s hard timeout, 0 result text (prior verified) | MISSING_SOURCE | N/A, pending remote disk check |
| R02-B `8529435fc4da4624` | FAILED | 3600s hard timeout, 0 result text (prior verified) | MISSING_SOURCE | N/A, pending remote disk check |
| **R02-C `7db4a2fa2edc4ab0`** | **FAILED** | Direct `get_workbuddy_result` says `[task failed]`, 3600s hard-kill, `status=error`, no result text | Git directory listing: only TASK.md/AUDIT.md | N/A; no source for P0-P3 evaluation |
| R03-A `fd0bc26fcc7b489b` | QUEUED | No run result yet | Git directory TASK.md/AUDIT.md only | PENDING |
| R03-B `e09bacf7e42349a1` | QUEUED | No run result yet | Git directory TASK.md/AUDIT.md only | PENDING |
| R04-A `5669468a86524c07` | QUEUED | No run result yet | Git directory TASK.md/AUDIT.md only | PENDING |
| **R05-A `f8de6c9938a94e90`** | **QUEUED** | Accepted, 0 output, not executed | GIT_PENDING | PENDING |

Old PRE-RESTART A/B/C `9712edf966b54027`, `a154efd28abc4eb5`, `fb21843915d24025` remain historical INTERRUPTED, with no final outputs. R01 after restart was submission BLOCKED and did not create new jobs.

**Important finding:** R02 A/B/C have now all hit the 3600s hard-kill boundary. **3/3 execution failures and 0/3 verified source deliveries**; this is not evidence of failing unit tests, because no test outputs were returned. WorkBuddy remote workspace may retain partial files; Git absence is verified but remote disk absence is not. No separate audit job was submitted because no finished source was available and the single executor queue is congested. No independent 100-point score or P0-P3 code defects are fabricated.

## R05 new task and Git ledger

- Topic: deterministic fault injection and replay trace engine, >=6 Python modules, >=40 standard-library unittest tests, injected clock, seeded reproducibility, checkpoints, crash recovery, 10 adversarial cases.
- New unique ID `FACTORY24-20261030-20261030-0532-R05-A`; source job `f8de6c9938a94e90`.
- Target `results/factory24-20261030/rounds/20261030-0532-R05/A/` on repository `kaibahaha/xxsc`, branch `exp/factory24-20261030`.
- ChatGPT metadata commits: TASK.md `aa0a28dcefb135b7363fd3481cb42eabcfcf79d1`, AUDIT.md `d37544a1c7b51ed84fb405a6a4a18885480cd88e`, R02-C AUDIT update `2c3a51678ead83755150d20397aec7ee8bcdea05`.
- WorkBuddy actual source/test/README/REPORT/TEST_RESULTS/MANIFEST **not delivered**; code files verified=0, `GIT_PENDING`. No self-test result, no independent test exit code or score yet. Metadata commit and readback will be independently verified after writes; do not treat metadata verification as code verification.
- No modifications to bridge configuration, models, other jobs or other branches; no extra automation created. Next round should inspect prior timeouts' remote workdirs when possible, reconcile Git source delivery, and check R03/R04/R05 terminal states without duplicating jobs.

**R05 status at report creation: 1 accepted new job, QUEUED; queue high-watermark 6; GIT_METADATA_WRITING / GIT_CODE_PENDING; audit PENDING.**
