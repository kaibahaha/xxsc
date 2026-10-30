# FACTORY24-20261030 — R17 / 20261030-1732-R17 ROUND_REPORT

## Timing and actual connector operations
- Scheduled slot: **2026-10-30 17:32 Asia/Shanghai**, restart anchor 2026-10-30 01:32, R17 of 24. Operations began approximately 17:28–17:29, with three programming jobs accepted around 17:32 and the report written afterward. The scheduled slot is a naming anchor, not a claim of exact scheduler firing.
- Real `bridge_health`: HTTP 200, `status=ok`, `codebuddy_reachable=true`, **version=3.4-candidate**, `active_jobs=0`, `running_jobs=0`, `queued_jobs=0`, `pending_queue_depth=0`, `remote_orphan_count=0`, `possible_remote_overlap=false` at first observation. Current health response was **truncated before max_concurrent_jobs**; observed running concurrency later=1, prior configured value=1, current configured max **NOT_INDEPENDENTLY_VISIBLE**. Current health exposes `max_slot_seconds=2100`, `max_queue_wait_s=3600`, `max_queue_size=100` (configuration, not experimentally proven queue ceiling).
- Initial `list_workbuddy_jobs(limit=50)`: 154 total, newest 50 shown. No running/queued in visible window and explicit health queued_jobs=0; **Q_before=0 by authoritative health snapshot**, with list enumeration limited to newest 50. This is not a claim that all 154 historical jobs were individually inspected.
- Decision per shared-queue rule Q=0: **3 programming tasks** planned and **3/3 actually accepted** by asynchronous `submit_workbuddy_task`. Additionally, one separate read-only audit of previously completed R11-B was submitted, and counts as a real shared-queue job but not a new programming task.
- No execute synchronous blocking, duplicate POST, model switching, server restart, cancel, or other factory/branch modifications.

## Programming submissions
| Task | Unique ID | Title | Accepted job_id | State at latest check | Git code/tests | Independent audit /100 |
|---|---|---|---|---|---|---|
| A | `FACTORY24-20261030-20261030-1732-R17-A` | Crash-consistent transactional Outbox/Inbox | `e247b90359204a84` | QUEUED | GIT_PENDING | PENDING / N/A |
| B | `FACTORY24-20261030-20261030-1732-R17-B` | Bounded incremental binary-frame parser | `1299ee08ce2b47ac` | QUEUED | GIT_PENDING | PENDING / N/A |
| C | `FACTORY24-20261030-20261030-1732-R17-C` | Deterministic distributed snapshot coordinator | `deace1cca1ea4069` | QUEUED | GIT_PENDING | PENDING / N/A |

- All three actual submit responses included the exact job IDs above; none are claimed as completed. Each requires Python3.11+ stdlib, >=8 modules, >=40 real unittest, clock/fault injection, complete source/tests/README/REPORT/TEST_RESULTS/MANIFEST, true test exit code and real Git commit/readback. **Actual source files=0 independently obtained; tests run=0 independently verified; verified programming throughput=0** at report time.
- Program Git commit SHA=NONE for A/B/C; their `TASK.md` and `AUDIT.md` are ChatGPT metadata only, not program delivery.

## Queue observations and capacity
- Initial Q_before=0; R17 audit `7a82c98b70834941` became RUNNING, queued=0.
- After A submission: **Q_after_A=4** (A + three unrelated queued programming probes, with audit running).
- After B submission: **Q_after_B=5**; after C: **Q_after_C=6**.
- Later `list_workbuddy_jobs` showed three additional queued research retries, hence **Q_peak_observed_R17=9**, running=1, queued=9 at that snapshot. Breakdown queued: **FACTORY24 programming=3, FACTORY10 research=3, other=3**. Audit of R11-B=RUNNING and belongs to FACTORY24, but is not counted in queued. Observed total active=10 at that later snapshot, inferred from list; health should be rechecked for latest exact count.
- **Q_high_watermark (whole experiment, as known from existing ledger and this run)=9**. Earlier reported historical maximum=7. **QUEUE_MAX_NOT_REACHED**: health configuration `max_queue_size=100` is not empirical proof of max capacity. Observed queue acceptance proves >=9 queued at a snapshot. No 429 or capacity rejection observed in this round; first historical 429 raw error remains UNKNOWN, do not fabricate.
- External job submissions occurred concurrently, so the change Q=0 to Q=9 is **not solely caused by FACTORY24**. Observed queued growth +9 over a short, nonuniform interval; hourly rate not reliable from these snapshots. Exact queue waiting and execution durations for A/B/C: **NOT_YET_MEASURABLE** (all still queued). The displayed elapsed values are age since submission, not running duration.
- Current bridge version differs from previous R16 v3.3; this round did not request or perform the change. New configured max_slot_seconds=2100 means timeout behavior may differ from prior 3600-second failures. Do not mark >30m running as failed without server terminal state.

## Prior-round R16 and unfinished audits
- R16-A original job `eaebe2e61cb644ca`: earlier original result reported **UPSTREAM_OOM / no valid code** despite list `done`; this round's fresh `get_workbuddy_result` attempt failed internally, so no new status upgrade. R16-A remains **NO_VERIFIED_SOURCE / N/A**. Previous R15-A/B/C were FAILED with zero verified code, not retested.
- Earlier R11-B original job `b4811053fb6e4b47` still reports author self-test **69 unittest PASS / exit 0**, 10 modules, but GitHub connector fetches for its `src/ledger/engine.py`, `tests/test_ledger.py` and `README.md` returned 404. Thus **AUTHOR_SELF_TEST_ONLY / GIT_BLOCKED / NO_INDEPENDENT_SCORE**.
- Actual independent read-only R11-B audit job accepted: `7a82c98b70834941`, at latest result **RUNNING** (~92s, 0 output). It must check real remote files, rerun standard unittest and >=10 new adversarial cases, report P0-P3 with file lines. **This is a delegated audit, not ChatGPT independently rerunning local code**. No score until actual evidence is returned; next round must follow up original audit_job_id, no duplicate audit POST.
- Historical pre-restart original A/B/C `9712edf966b54027`, `a154efd28abc4eb5`, `fb21843915d24025` were again queried: all remain **INTERRUPTED**; no original job was restarted or rewritten. Existing historical Git files preserved.

## GitHub commits and verification
- Target ONLY `kaibahaha/xxsc`, branch `exp/factory24-20261030`, root `results/factory24-20261030/`.
- Six R17 metadata files created and independently read back **6/6**:
  - A TASK `07275b4876ac559a45c6d2b8dbdb9c2a71327e27`, A AUDIT `cee28ccf862754a65c2838c826687d3a60e2eb1a`.
  - B TASK `a8cd526e06cd0205401646073ac3ec17656c9bd6`, B AUDIT `826a61ab72d0b0cb8c717bbdb5f543f2046d138e`.
  - C TASK `5e3834abdaf6038b7f9dfc33c13781ba09febb4e`, C AUDIT `ff0bf90c0cdaefd6debffbd9d381a6969e7a5b6b`.
- Each readback matched R17 slot and job_id. This ROUND_REPORT and ledger INDEX must be committed and read back separately; the commit of this file cannot be self-embedded without a subsequent commit.
- **GIT_COMMITTED_METADATA_ONLY / GIT_VERIFIED_METADATA_ONLY**, six verified so far. **GIT_BLOCKED_SOURCE** until complete WorkBuddy source/tests are actually obtained and independently fetched. Do not mistake management documents for code, self-tests, or independent PASS.
- Safety: no credentials, private data, or production configuration in management files; no changes to other branches/factories. R17 is not the final round; no FINAL_REPORT written.

## Next-round mandatory follow-up
Poll A/B/C original job_ids and audit `7a82c98b70834941`; independently inspect real source/test files and Git commits if available; classify failure vs genuine output, test results and code defects; update AUDIT and ledger without overwriting historical records. No retries of already accepted submissions.

## Final same-run confirmation
- A later real `bridge_health` confirmed **active_jobs=10, running_jobs=1, queued_jobs=9, pending_queue_depth=9**, HTTP200, v3.4-candidate. This corroborates the 9 queued breakdown above. `max_concurrent_jobs` remained beyond the truncated connector text; configured running limit was not directly returned.
- `get_workbuddy_result(7a82c98b70834941, wait_seconds=0)`: **RUNNING at ~131 seconds with 0 text**, not a passed independent audit. Do not duplicate-submit.
- Git initial ROUND_REPORT commit: `ca657507e09f6de33f9b8f2e04f11be23dd46f3e`; Git ledger INDEX update commit: `8059c7861debb12bf664190bd9b6ef88e82002ee`. GitHub connector independently fetched both and confirmed all four job IDs. The six R17 TASK/AUDIT metadata files were independently fetched earlier: **8/8 management files verified**. Source/tests still not obtained; program commit SHA=NONE, `GIT_BLOCKED_SOURCE`.
- Final report addendum commit is intentionally not self-embedded; verify it by a separate GitHub fetch.
