# AGL-WB-ADAPTERS-R01｜WorkBuddy 适配器与执行桥交付报告

- 工单：`frameworks/agensh-lite-v4.2/workorders/AGL-WB-ADAPTERS-R01/TASK.md`
- 承接方：WorkBuddy（工程集成 / GitHub 适配 / 执行系统）
- 冻结基线：`2d4c1a6fc0792a1182777262b41bfb4c09c0b5d2`
- 工单基线分支：`exp/agensh-lite-v4.2-controller-mvp-20261025`
- 开发分支：`dev/agl-v4.2-workbuddy-adapters`
- PR：#2 <https://github.com/kaibahaha/xxsc/pull/2>（draft，未合并）
- 交付目录：`frameworks/agensh-lite-v4.2/deliveries/WORKBUDDY_ADAPTERS_R01/`
- 报告生成时间：2026-10-26T00:40+08:00（UTC 2026-10-25T16:40Z）

## 1. 结论摘要

四个模块均已落地为可运行代码，并在**真实 GitHub 仓库**与**真实 git 对象**上完成写入、独立回读、幂等、冲突与执行验证。控制器（M01/M03/M04/M05/M07/M09）未实现、也未复制，`poll` 只产出 `CLAIM_PROPOSED` 并显式标注 `CONTROLLER_UNAVAILABLE`。

| 项目 | 结果 |
|---|---|
| M02 GitHub Storage Adapter | 完成；真实仓库写入 + 独立回读 SHA 全部一致 |
| M06 Dynamic Poll + AgentAdapter | 完成；K=1..6 错峰表与规范逐字一致；只读 provider 不可发布 |
| M08 Executor Bridge | 完成；真实子进程运行、exit code、原始日志、STALE/BLOCKED 路径 |
| M10 CLI / CI / 测试 | 完成；11 条子命令，默认 dry-run，`--apply` 三重显式门禁 |
| 自动化测试 | **115 passed / 2 skipped**（skip 为无凭据只读探针触发限流；限流更严时为 3 skipped，均不影响 115 项通过） |
| 真实 PR | 已创建（draft），未合并 |

## 2. 提交与分支实况

本地开发历史（`git log`）：

```
6055f2e fix(adapter): never borrow ambient credentials; accept subdirectory worktrees
1fdf4d1 chore(ci): stage workflow definition under factory/ci (token lacks workflow scope)
0cf0237 feat(factory): M02 GitHub storage + M06 poll/adapters + M08 executor + M10 CLI
2d4c1a6 (baseline) dispatch: freeze V4.2 R01 Codex core and WorkBuddy adapters workorders...
```

远端分支发布链（因为执行环境 **`github.com:443` 不可达**，`git push` 无法使用，改用 Git Data API 以同语义发布：blob → 嵌套 tree → commit → fast-forward ref）：

| SHA | 说明 |
|---|---|
| `02566162b99b1bd0711e321ae55b714efbad9346` | 代码主提交（38 个文件，blob SHA 逐个与本地 `git hash-object` 比对通过） |
| `6961e58a7d85b9aeceebf006225c95893c8ececa` | 真实回读探针 1 |
| `a0ae03b595f36bc7af17a72209b05cf601e3a1be` | 真实回读探针 2（幂等基准） |
| `246ad41105f0` / `0954f21521ca` | 事件 manifest / 事件目标投递 |
| `fec0b9a02b03` | 能力探针写入（outbox） |
| `34f316bd965a` / `c5d5dcdd4f83` | 任务种子 / BOARD CAS 投影 |
| `e5b099a5ed19` … `ef19faa19196` | CLAIM_PROPOSED、run record、run meta、ACK、cursor |

> 说明：远端历史是「基线 + 1 个压缩提交 + N 个探针提交」，本地是 3 个语义提交。两者**内容一致**但对象历史不同，原因是 git 协议被阻断；本地历史以 `git-bundle/workbuddy-adapters.bundle` 形式随交付保存，便于审计与复现。

## 3. 模块实现

### M02 `factory/agl/storage/`
- `transports.py`：`RestTransport`（stdlib urllib，401/403/404/409/422/5xx/网络异常分类，限流识别，token 全链路脱敏）与 `LocalGitTransport`（真实 `hash-object`/`read-tree`/`write-tree`/`commit-tree`/`update-ref <new> <old>`，CAS 由 git 自身强制）。
- `github.py`：`read_ref` / `read_file` / `write_immutable` / `readback` / `cas_publish_projection`。不可变写入永不覆盖：同路径同哈希 → `IDEMPOTENT_REPLAY`，不同哈希 → `CONFLICT`；写后**独立第二次读取**并复算 sha256、比对 blob/commit；写调用结果不明 → `UNKNOWN_WRITE` 后**只读对账**，绝不盲重发。`main/master` 在构造期即拒绝绑定，路径白名单在发请求前校验。
- `ledger.py`：`03_events/<date>/<event_id>/_manifest.json` + `<AGENT>.json`，实现 per-(event_id,target) 结构幂等（对应微软 `UNIQUE KEY (dedup_key, agent)`）；同 event_id 不同 payload → `EVENT_ID_COLLISION`（对**所有** target 生效）；`put_receipt` 幂等；cursor 只能单调前进且走 CAS。

### M06 `factory/agl/adapters/` + `poll.py`
- 统一 `probe/read/publish/reread/observe_schedule/health`；能力四态 `SUPPORTED/UNSUPPORTED/UNKNOWN/BLOCKED`，并记录 `method`（`REAL`/`LOCAL_GIT`/`STATIC`/`MOCK`），避免"配置即能力"。
- `chatgpt` 适配器强制只读（`supports_publish=False`），即使调用方给了写权限也不会写；`workbuddy` 有 runner 时 `execute=SUPPORTED`，否则 `BLOCKED_EXECUTOR`；`codex` 的 `execute` 保持 `UNKNOWN`；未知 provider 落到 `CustomAdapter`，全部 `UNKNOWN`，无需改核心。
- 排班：`compute_offsets(K, 60)` 精确复现规范表（K=1..6），非整除时量化去重而不是拒绝；**只在 provider 子池内错峰**，全局 N 不参与除数。
- `poll_once`：准入 → handoff 续作 → BOARD 可读性 → 任务匹配 → CLAIM_PROPOSED。任一环节失败即 fail-closed（`REFUSED` / `BOARD_UNKNOWN`），且不写任何共享路径。同一 `run_id` 重跑时事件字节稳定（`observed_at` 取自 run meta），因此重试是幂等重放而不是冲突。

### M08 `factory/agl/execution.py`
- `TEST_REQUEST`（不可变 JSON）→ `Runner`（真实 `subprocess`）→ `stdout.log`/`stderr.log`（原始字节 + sha256）→ `TEST_RESULT`（绑定 `commit_sha`、exit code、日志哈希、环境 id）→ `ACK`。
- worktree HEAD ≠ 请求 commit → `STALE_TEST`，不执行；无 runner → `BLOCKED_EXECUTOR`；超时 → `TIMEOUT` 且保留部分日志；命令不存在 → `ERROR`。
- `PASS` 的 `business_acceptance` 恒为 `PENDING_CORE`；`ensure_business_acceptance()` 在缺 M04 时抛 `CONTROLLER_UNAVAILABLE`，从代码层面阻止"测试通过=验收通过"。

### M10 `factory/agl/cli.py`
`validate-config` / `gen-pool` / `plan-schedules` / `probe` / `poll` / `submit-event` / `reconcile` / `rebuild-board` / `audit` / `run-sample-test` / `verify-roundtrip` / `offsets`。
默认 dry-run；`--apply` 必须同时给出 `--repo --branch --project` 且与配置一致，分支不得为 `main/master`，路径必须在白名单内。退出码：0 成功、2 配置/门禁、3 阻断、4 测试失败、5 SHA 过期、6 冲突/碰撞。

## 4. 真实证据（摘要，详见同目录文件）

| 验证项 | 结果 | 证据 |
|---|---|---|
| 真实仓库写入 + 独立回读 | PASS | `GITHUB_ROUNDTRIP_EVIDENCE.md`；commit `a0ae03b`，blob `54276eb`，sha256 `49ad3bb`…，两次读取一致 |
| 相同 run_id 重试 | PASS（无新提交，HEAD 未变） | 同上，第二次调用返回同一 commit |
| 相同 event_id 不同 payload | PASS（`EVENT_ID_COLLISION`，exit 6） | `evidence/real_collision.log` |
| 能力探针（真实 API） | PASS（含 `method=REAL`） | `evidence/real_probe.log` |
| 真实仓库端到端 poll + ACK + cursor | PASS（`CLAIM_PROPOSED` + `MONOTONIC_NOOP`） | `evidence/real_poll_ack.log` |
| 本地 bare 仓库全流程 | PASS（真实 git SHA） | `evidence/local_evidence.log` |
| N=2/3/5/6/10/20 配置 | PASS | `evidence/local_evidence.log`、`tests/adapters/test_registry_pool.py` |
| 无 runner → BLOCKED_EXECUTOR | PASS | `evidence/local_evidence.log`、`test_execution.py` |
| 自动化测试 | 115 passed / 2 skipped | `INTEGRATION_TEST_RESULTS.txt`、`evidence/junit.xml` |

## 5. 成功 / 失败 / 未验证

**成功**：不可变写入与回读、幂等重放、冲突检测、CAS 投影、cursor 单调性、per-provider 排班、只读 provider 熔断、执行器协议与失败路径、CLI 门禁、真实 PR。

**失败（已修复，留档）**：
1. 首轮"未认证写入应被拒绝"的联网测试因环境存在 `GITHUB_TOKEN` 而**真的写入成功**，目标误落在基线分支，产生提交 `5c5e95c5de8239623556071003aa79bbec93171f`（仅新增 `factory/_probe/should-not-exist.json`，父提交即 `2d4c1a6`）。已用 `PATCH ref force` 将基线**恢复为 `2d4c1a6`**，越权文件返回 404；代码层根因修复为 `RestTransport(token="")` 表示显式未认证、不再回退环境变量，测试断言 `authenticated is False` 且写目标只允许 dev 分支。
2. `run-sample-test` 初期把仓库子目录判为"非 worktree"，导致误报 `BLOCKED_EXECUTOR`；已改为 `git rev-parse --show-toplevel` 判定，并补测试。
3. 回读探针载荷曾含墙钟时间，导致同 run_id 重试被判冲突；已改为 `run_id` 决定载荷，时间只记在回执里。

**未验证 / 未连通（不得当作已通过）**：
- ChatGPT 真实定时任务 → GitHub 的自动接力：无平台 API/Webhook，代码只提供 Git 信箱 + 各自节拍，标 `UNSUPPORTED`/`UNKNOWN`。
- WorkBuddy / Codex 云端执行器的真实远程调用：本环境只有本机子进程 runner。
- 平台真实 `schedule_id` 与 `fired_at`：`plan-schedules` 只生成待登记清单（`creates_real_schedule=false`）。
- Controller 授租、fencing、跨分支集成：依赖 Codex 分支。

## 6. 与 Codex 的集成依赖

见 `STUBS.md`。要点：`agl.config`（配置权威校验）、`agl.events`（事件账本权威实现）、`agl.controller`+`agl.leases`（原子授租/fencing）、`agl.audit`（权威 BOARD 重建）。当前以 `core_available("controller")` 探测，缺失时 CLI 输出 `CONTROLLER_UNAVAILABLE` 而非伪造可用。

## 7. 复现

```bash
# 单元 + 集成（无需网络/凭据）
cd factory && PYTHONPATH=. python3.11 -m pytest tests -q

# 本地真实 git 全流程（脚本自带 bare 仓库与任务种子）
bash factory/tools/local_evidence.sh

# 真实仓库（需 GITHUB_TOKEN）
export PYTHONPATH=factory
python3.11 -m agl.cli verify-roundtrip \
  --config factory/config/pool_probe_devbranch.example.json \
  --transport api --apply --repo kaibahaha/xxsc \
  --branch dev/agl-v4.2-workbuddy-adapters --project AGL-R01-PROBE --run-id RUN-XXX
```

## 8. 纪律声明

- 未改 `main`、未改任何盲测分支、未创建付费服务、未创建定时任务、未部署对外服务。
- 未实现或复制 Controller/Lease/Event 核心；未发明第二套互斥 schema。
- 所有 Mock/本地验证均标 `MOCK`/`LOCAL_GIT`，未冒充跨平台连通。
- 基线分支曾被误写一次，已恢复并如实记录（见 §5）。
