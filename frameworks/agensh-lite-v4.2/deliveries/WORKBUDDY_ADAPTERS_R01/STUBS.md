# 待集成的 Codex 接口（STUBS）

本文件列出适配器侧**故意留白**的位置，以及 Codex 交付后如何接线。原则：不发明第二套互斥定义，不用 mock 冒充核心。

| 能力 | 当前实现 | 期望由 Codex 提供 | 接线点 | 缺失时的行为 |
|---|---|---|---|---|
| 配置权威校验（M01） | `adapters/registry_view.py` 的适配器侧前置校验 | `agl.config.validate(cfg)` 返回权威 schema 结论 | `cli._ctx()`：若 `core_available("config")` 则先调它，再跑本地不变量 | 仅跑本地前置校验，并在 `validate-config` 输出中注明 `adapter_preflight_only` |
| 事件账本（M03） | `storage/ledger.py`（Git 文件级幂等 + manifest 摘要） | `agl.events.Ledger` 的 `(event_id,target)` 幂等、ACK 与 cursor 权威实现 | `EventLedger.put_event/put_receipt/advance_cursor` 增加后端委派 | 以 Git 文件为唯一事实，语义等价但非权威 |
| 任务状态机/DAG（M04） | `poll._eligible_tasks` 只读 `STATUS/DEPENDS_ON` | `agl.task_state` 的合法转移与依赖判定 | `PollPlanner._eligible_tasks` 改为调用核心 | 只按文件头字段筛选，状态推进一律不做 |
| 原子授租/fencing（M04） | 无；`CLAIM_PROPOSED` + `CONTROLLER_UNAVAILABLE` | `agl.leases.grant(task_id, agent_id, attempt, epoch)` 返回 `GRANTED` / `CLAIM_PROPOSED` | `PollPlanner.poll_once` 在写 claim 后调用；只有 `GRANTED` 才允许后续共享写 | 永远只提议，不宣称排他 |
| 交接与上下文（M07） | `09_runs/<agent>/<run_id>.md|.json` + `HANDOFF.json` 只读 | `agl.handoff` 的 `TASK_ID/SPEC_HASH/DECISION_LOG/OPEN_ISSUES/NEXT_ACTION/EVIDENCE_REFS` 结构 | `poll._read_handoff` 改为解析核心结构 | 按 `status=OPEN` 续作，其余字段透传 |
| 权威 BOARD 投影（M09） | `cli.build_board`（明确标注非权威） | `agl.audit.rebuild()` 输出权威 `BOARD.md` | `cmd_rebuild_board` 若核心可用则改用核心 | 生成 `adapter projection`，禁止授租 |
| 审计/重放（M09） | `cmd_audit` 的完整性检查（摘要、缺失投递、cursor 形态） | 事件重放 + 投影一致性对比 | `cmd_audit` 合并两份报告 | 只报适配器可见的问题，不宣称全局一致 |
| Schema 冻结（M01/M03） | 事件字段按 V4.1 `event.schema.json` 手写校验（必填 + target 非空） | `agl.schemas` 的 `Event/Task/Ack/Handoff` 类型 | `normalize_event` 前置调用 | 手写校验，字段名严格对齐 V4.1，不新增互斥字段 |

## 已知字段差异（待 Codex 确认）

1. **`run_id` 与 `attempt_id`**：适配器事件带 `run_id`，尚未有 `attempt_id`。若核心以 `(task_id, attempt_id)` 表示一次尝试，需要在 `CLAIM_PROPOSED` 事件中补字段；当前留空并在 `STUBS` 标注。
2. **`fencing_epoch`**：`TEST_RESULT` 未携带 epoch（无租约可携带）。核心接管后应由 `grantLease` 返回并在结果中回填。
3. **`spec_hash` 来源**：当前来自 TASK.md 的 `SPEC_HASH` 行或任务 JSON；若核心以内容哈希计算，需要统一算法（当前不自行计算 spec 哈希，避免"两套哈希"）。
4. **ACK 目标**：`07_receipts/<AGENT>/<EVENT_ID>.json` 的 `target` 字段默认 `GITHUB`；若核心要求 `EVENT_INBOX`/`CONTROLLER` 语义，需在 `put_receipt(target=...)` 显式传入。

## 集成顺序建议

1. `agl.config` → `validate-config` 切权威校验（低风险，最先做）。
2. `agl.events` → ledger 委派，跑现有 115 个测试回归。
3. `agl.leases` → `poll` 从"提议"升级为"授租后执行"，补 100 并发抢租与旧 epoch 拒绝的跨模块测试。
4. `agl.audit` → 用核心重建 BOARD，与适配器投影逐字节比对。

每一步都必须保留"核心缺失时 fail-closed"的降级路径，避免合并后反而失去可运行性。
