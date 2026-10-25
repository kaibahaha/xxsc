# Provider 能力与权限矩阵（AGL-WB-ADAPTERS-R01）

状态语义严格按 `docs/AGENT_ADAPTER_CONTRACT.md`：`SUPPORTED / UNSUPPORTED / UNKNOWN / BLOCKED`。
`method` 说明结论来源：`REAL`＝对真实 `api.github.com` 的调用；`LOCAL_GIT`＝真实 git 对象操作（无网络）；`STATIC`＝结构性事实（平台没有该接口），不是"未测所以不知道"。

**先声明一条纪律**：ChatGPT 有 Git 连接器，不等于 WorkBuddy 也有写权限；WorkBuddy 能写，不等于 Codex 能执行。"能读"从不推导"能写"。

## 1. 实测矩阵（2026-10-25T16:19Z–16:21Z，repo `kaibahaha/xxsc`，branch `dev/agl-v4.2-workbuddy-adapters`）

| provider / agent | read | write | reread | trigger | execute | schedule | 依据 |
|---|---|---|---|---|---|---|---|
| `workbuddy:WORKBUDDY_01` | SUPPORTED | SUPPORTED | SUPPORTED | UNSUPPORTED | BLOCKED | UNKNOWN | 真实 outbox 写入 + 独立回读一致（`evidence/real_probe.log`） |
| `chatgpt:CHATGPT_01` | SUPPORTED | UNSUPPORTED | UNSUPPORTED | UNSUPPORTED | UNSUPPORTED | UNKNOWN | 真实分支读取成功；写入由适配器结构性拒绝 |
| `codex:CODEX_01` | SUPPORTED | SUPPORTED（探针写入时） | SUPPORTED | UNSUPPORTED | UNKNOWN | UNKNOWN | 与 workbuddy 共用 Git 信箱；执行端无验证通道 |
| `custom:*` | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | 新增 provider 只加 Adapter，未探针前一律 UNKNOWN |

`execute=BLOCKED` 对 WorkBuddy 表示"本会话未绑定 runner"，绑定后为 `SUPPORTED`（`tests/adapters/test_providers.py::test_workbuddy_writes_own_outbox_and_reports_executor` 覆盖两种分支）。

## 2. 逐项说明

### read
- WorkBuddy / ChatGPT / Codex 均通过同一 `GitHubMailboxAdapter.read()` 读取 `01_tasks/`、`03_events/`、`08_projections/BOARD.md`，并用 per-agent cursor 过滤已消费事件。
- 实测：`kaibahaha/xxsc@dev/agl-v4.2-workbuddy-adapters` 读取成功（HEAD 随写入推进，两次探针 HEAD 分别为 `0954f21`、`fec0b9a`）。
- 若 403/404/限流 → `BLOCKED`/`UNKNOWN`，绝不返回"空板"。

### write
- **ChatGPT 永久 `UNSUPPORTED`**：该部署下聊天会话没有仓库写 API；适配器 `supports_publish=False`，即使调用方给 `--apply` 也不会写（`tests/integration/test_event_pipeline.py::test_chatgpt_agent_cannot_write_claim`）。其产物只能作为 `TEST_REQUEST`/note 交给有写权限的成员提交。
- **WorkBuddy/Codex `SUPPORTED`**（有凭据时）：仅写自己的 `05_outbox/<AGENT>/<RUN_ID>/`，路径白名单先于网络请求校验。
- 证据：`fec0b9a`（probe write）、`e5b099a`（CLAIM_PROPOSED outbox）。

### reread
- 写后**第二次独立请求**读取，复算 sha256，并比对 blob/commit SHA。任一项不符 → `UNKNOWN_WRITE`。
- 实测：`matches=true`（`GITHUB_ROUNDTRIP_EVIDENCE.md` §2）。

### trigger
- 三平台一律 `UNSUPPORTED`：本部署没有可验证的 webhook/唤醒 API。ChatGPT 计划任务只能在**下一次真实唤醒**时读取新状态；WorkBuddy 若配置了 URL 也只标 `UNKNOWN`（配置≠会触发）。
- 因此跨平台接力只能靠 Git 信箱 + 各自节拍，代码中不存在"实时推送"的假实现。

### execute
- WorkBuddy：绑定 runner → `SUPPORTED`（真实 `subprocess`，见 `evidence/local_evidence.log` 的 `status: PASS` + exit 0）；未绑定 → `BLOCKED` 且返回 `BLOCKED_EXECUTOR`。
- ChatGPT：`UNSUPPORTED`（无已验证 shell/CI 工具）。
- Codex：`UNKNOWN`（其云端执行存在于自身平台，本侧无已验证端点）。

### schedule
- 三平台均 `UNKNOWN`：无公开排班 API，无法核验真实 `schedule_id` / 实际唤醒。
- `plan-schedules` 只产出**待人工登记**的清单，字段 `verified=false`、`creates_real_schedule=false`，并把 `planned_at` 与 `actual_at` 分开记录在 run record 中。

## 3. 排班容量与错峰（不是全局 60/N）

| provider | 小时节拍 | 子池规模 | 偏移（分钟） | 说明 |
|---|---|---|---|---|
| chatgpt | 60 | K=1..6 | `[0]` `[0,30]` `[0,20,40]` `[0,15,30,45]` `[0,12,24,36,48]` `[0,10,20,30,40,50]` | 与验收矩阵 C0-04 逐字一致 |
| workbuddy | 20（配置示例） | 任意 | 在 20 分钟内均分（如 2 个 → `[0,10]`，4 个 → `[0,5,10,15]`） | 使用自身节拍，不占 ChatGPT 槽位 |
| codex | 未验证（null） | 任意 | `None` + `NATIVE_UNVERIFIED` | 无节拍就不编造时刻 |

全局 N 只用于统计成员数，从不作为除数。`tests/adapters/test_offsets.py::test_offsets_are_per_provider_not_global` 用 N=10（4+4+2）断言 ChatGPT 仍为 `[0,15,30,45]`。

## 4. 配额与准入

| provider | 配置容量 | 是否已验证 | 行为 |
|---|---|---|---|
| chatgpt | 5 槽 − 预留 2 = 3 | 否（示例值） | 超 3 个只告警 `QUOTA_UNVERIFIED`，不冒充无限 |
| workbuddy | null | 否 | 警告"未知，不得视为无限" |
| codex | null | 否 | 同上 |
| 任一 provider（`capacity_verified=true`） | 实数 | 是 | 超限 → `PROVIDER_QUOTA_EXCEEDED` 硬失败 |

准入：仅 `ADMITTED_ACTIVE` 且 `enabled` 且非 `DRAINING` 的 agent 可领单；`PENDING_PROBE`/`REGISTERED`/`DRAINING`/`UNAVAILABLE` 一律 `ADMISSION_DENIED`（`tests/adapters/test_registry_pool.py`）。

## 5. 升级为 SUPPORTED 的条件

| 当前 | 需要什么证据 |
|---|---|
| trigger = UNSUPPORTED | 平台提供可验证的 webhook/唤醒 API，并实测一次真实触发（含请求 id、时间、接收方日志） |
| schedule = UNKNOWN | 平台开放排班查询，返回真实 `schedule_id` 与 `fired_at`，与 `planned_at` 对账 |
| codex execute = UNKNOWN | 已验证的 Codex 执行端点 + 一次真实 TEST_RESULT 回传 |
| ChatGPT write = UNSUPPORTED | 不在本迭代目标内；若未来有写通道，需新增 Adapter 能力并重新走探针，不得直接改开关 |
