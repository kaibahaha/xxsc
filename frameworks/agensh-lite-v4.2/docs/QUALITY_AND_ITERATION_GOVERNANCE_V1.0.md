# Agensh-Lite 协作质量与迭代治理规范 V1.0

- 日期：2026-10-26
- 状态：研究草案 / 待架构评审冻结
- 适用：Lite-M、Lite-M+、Lite-P；ChatGPT、Codex、WorkBuddy 等异构 Agent
- 性质：源代码证据 + 本项目工程规则；**本文件新增的门禁并非微软原项目的原样要求**。

## 1. 核心结论

微软 Agensh 不是“每个 Agent 做完后必须由下一个 Agent 审核”的固定流水线。其公开工作指令是：Agent 自主发现任务、声明 CLAIM、实施、对照参考行为自测、提交 PR、遇冲突重新同步与测试、合并、发布 PATCH_SUMMARY，再继续工作。共享上下文包含 FACT、OBSERVED、FAIL、CLAIM、PATCH_SUMMARY。其公开复现实验配置允许 **零必需 PR 审批**，因此不能声称微软已经实现了普遍强制的异人审核门禁。我们应借鉴其异步协作和证据共享机制，**自行增加基于风险的独立复核制度**。

## 2. 来源与证据层级

| 发现 | 原始依据 | 解释边界 |
|---|---|---|
| 自组织工作循环：发现、认领、实施、验证、合并 | `microsoft/Agensh/README.md`、`prompts/agents.txt` | 不是中央调度器逐项派单 |
| 认领冲突：CLAIM 碰撞时直接协商 | `prompts/agents.txt` | CLAIM 是协作声明，不等于严格原子租约 |
| 自检：参考行为与实现行为在相同输入上比较 | `prompts/agents.txt` | 证明微软要求自检，不等于自检必然正确 |
| 合并冲突：同步 main 后重新检查 | `prompts/agents.txt` | 合并前需重新验证；不是所有任务都有独立审查者 |
| 知识共享：FACT、OBSERVED、FAIL、CLAIM、PATCH_SUMMARY | `board-service/README.md`、`shared_lessons.py` | 短摘要+按需展开详情 |
| FAIL 可使同作者最近候选补丁失效 | `shared_lessons.py` | 属于共享上下文状态，不是完整质量验收引擎 |
| 事件去重、顺序派发、ACK、重试和重启恢复 | `mini-router/README.md` | 这是基础设施确定性逻辑 |
| 共享服务不会运行 Agent 声称的验证命令 | `board-service/README.md` | 元数据核验与实际运行测试必须分离 |
| 复现实验允许 PR 零必需审批、CI merge gate 关闭 | `REPRODUCE.md` | 不能将独立审核描述成微软的强制规则 |

源代码：https://github.com/microsoft/Agensh
论文：https://arxiv.org/abs/2609.26781
复现：https://github.com/microsoft/Agensh/blob/main/REPRODUCE.md

## 3. 我们的设计原则（规范性要求）

1. **符号层 / 神经层分离。** Watchdog 只验证身份、状态、权限、引用、哈希、版本、时间、事件、证据存在性及可机检门禁；Agent 执行语义审查、架构判断、代码修复和复杂测试分析。Watchdog 不凭“PASS”文字判断代码质量。
2. **提交不等于验收。** 执行者自检仅可达到 `SELF_TESTED`；需要独立验证的任务不得直接进入 `ACCEPTED`。
3. **审核对象绑定不可变版本。** 审核结果绑定 `task_id + candidate_commit_sha + evidence_digest + review_id`；代码变化后旧审核不再覆盖新候选。
4. **证据与意见分开。** 代码、测试输出、日志和复现命令属于证据；模型给出的“已修好”“合格”属于声明。
5. **事件追加，不覆盖历史。** 新一轮修复产生新的 `attempt_id`、候选提交和审查记录；BOARD 是投影，不是唯一历史。
6. **允许异步自治，不允许越权合并。** Agent 可以主动领单，但不得自行签发需要独立复核的最终批准。
7. **有限重试和升级。** 相同失败不得无界重复；超预算或无法解决时生成升级工单，保留完整上下文。
8. **失效安全。** Watchdog、GitHub 或审核者不可用时保留交付，暂停受保护的合并和授租，不伪造成功。

## 4. 风险分级与独立审查门禁

| 等级 | 任务举例 | 最低门禁 | 独立复核 |
|---|---|---|---|
| R0 | 文档排版、非行为性改名 | 自检 + 格式检查 | 抽检 |
| R1 | 常规业务功能、普通测试 | 自检 + 自动测试 + 独立 Agent 检查 | 必须，允许抽样深度 |
| R2 | 关键 API、数据迁移、跨模块集成 | 自检 + 独立 Agent 审核 + 可重现测试 | 必须且审核者不同于作者 |
| R3 | 租约、fencing、凭据、权限、删除、生产部署 | 双重独立验证（静态审计 + 真实执行证据），必要时人工批准 | 必须；不能由作者独自放行 |

“独立”至少要求不同执行身份；高风险任务优先不同模型或不同提供方，并记录是否读取作者的自评，以便衡量审查独立性。

## 5. 标准状态机

`READY → CLAIMED → IMPLEMENTING → SELF_TESTED → REVIEW_PENDING → REVIEW_APPROVED → INTEGRATION_PENDING → ACCEPTED`

分支：
- `REVIEW_PENDING → CHANGES_REQUESTED → IMPLEMENTING`：原作者修复或经授权转交另一 Agent。
- `SELF_TESTED / REVIEW_PENDING → BLOCKED`：证据缺失、环境故障、依赖不可用。
- `INTEGRATION_PENDING → INTEGRATION_FAILED → IMPLEMENTING`：集成失败重新修复与复审。
- `CLAIMED → EXPIRED`：超时，仅撤销执行权，不抹除已提交证据。
- `ANY → QUARANTINED`：检测到身份冲突、越权、证据伪造或不可恢复的一致性问题。

Watchdog 必须校验每次状态转换的事件来源、前置状态和授权；只有具备明确测试或独立审核证据的事件才可推进对应门禁。

## 6. 每次迭代的必需记录

- `task_id`：任务唯一 ID；`attempt_id`：本轮唯一 ID；`agent_id`：实际执行身份。
- `source_commit_sha`：任务基线；`candidate_commit_sha`：本轮代码版本。
- `claim_id` / `grant_id` / `fencing_token`：若启用 Mini Controller 的严格授租则必填；纯看板软认领标记 `SOFT_CLAIM`，不得冒称原子授权。
- `test_command`、`test_environment`、`test_results_uri`、`test_exit_code`、`evidence_digest`。
- `reviewer_id`、`reviewed_commit_sha`、`review_findings`、`review_decision`、`review_evidence_uri`。
- `parent_attempt_id`、`fixes_findings`、`handoff_to`、`event_id`、`recorded_at_utc`。

缺少关键字段只能进入 `EVIDENCE_INCOMPLETE`，不能自动验收。

## 7. 交叉审查与返工纪律

1. 作者交付：提交代码、测试日志、已知缺陷、自检结论。作者不能为自己签发独立审核通过。
2. 独立审核：先读取任务验收标准和候选提交，再读取证据；对高风险项执行自己的测试或反例验证，输出逐条 Finding（严重度、定位、复现步骤、预期、实际）。
3. 审核结果仅有 `APPROVE`、`CHANGES_REQUESTED`、`BLOCKED`；不得只写“看起来不错”。
4. 返工：原作者针对 Finding 修复，生成新 attempt、新 commit、新证据；审核者只重验受影响区域及必要回归，不无差别重复全部工作。
5. 每个 Finding 具稳定 `finding_id`；修复时必须标注 `FIXED`、`WONT_FIX`（需授权）、`NOT_REPRODUCED`（附证据）。
6. 同类问题两轮仍失败，或三轮未能完成，自动升级给更强模型/架构审查；不允许两个 Agent 无限互相驳回。
7. 审核通过后，如候选 commit 发生变化，批准失效；重新触发至少差异复核。
8. 集成失败由独立 `INTEGRATION_FAILED` 事件驱动返工；不得修改旧审核记录来掩盖失败。

## 8. Watchdog（符号层）的边界

**必须做：** ID 唯一性、Git SHA 与文件存在性、Markdown frontmatter Schema、任务依赖 DAG 检查、角色权限、重复事件、状态合法转换、软认领碰撞、租约过期、审核版本匹配、测试证据引用可达、提交后回读、BOARD 从事件重建、滞留与超时报警。

**可以按需做：** 文件哈希、Git diff 文件列表、CI 机器结果核验、自动重放无副作用状态。

**禁止做：** 根据摘要词语判断代码正确；代替 Agent 评价需求符合度；在未运行测试时把报告文字转成测试通过；绕过独立审查直接合并高风险代码。

流量优化：先比较远端 HEAD / tree / 文件路径和 SHA；无变化不读全文；仅对新增或变更的任务元数据读取结构化头部；有审计必要时再读取具体证据或完整 diff。Git blob SHA 可证明对应 Git 对象一致，不能证明内容质量。

## 9. Markdown 文件群建议

```text
factory/governance/
  GOVERNANCE.md
  REVIEW_POLICY.md
  STATE_MACHINE.md
  EVENT_SCHEMA.md
  AGENT_CONDUCT.md
  WATCHDOG_RULES.md
  SOURCES.md
factory/board/
  BOARD.md
factory/tasks/TASK-xxxx/
  TASK.md
  attempts/ATTEMPT-xxxx/DELIVERY.md
  reviews/REVIEW-xxxx.md
  findings/FINDING-xxxx.md
factory/events/YYYY/MM/EVENT-xxxx.md
factory/audit/
  AUDIT-YYYYMMDD.md
```

文件应使用固定 frontmatter（`schema_version`, `task_id`, `attempt_id`, `agent_id`, `commit_sha`, `status`, `event_id`, `created_at_utc`），详细正文留在 Markdown；Watchdog 优先只读头部与 Git 元数据。

## 10. 下一版本的强制验收场景

- 两个 Agent 同时软认领：检测冲突；启用 Controller 时只有一个有效 grant。
- 作者自评 PASS，但独立审查 FAIL：状态不得变成 ACCEPTED。
- 同一 `event_id` 重放 100 次：状态只推进一次。
- 审核 APPROVE 后作者修改一个字节：旧审核自动失效。
- 连续两轮返工失败：生成升级工单，不无限循环。
- 断网、限流、VM 重启：重放历史后 BOARD 一致，不重复执行受保护副作用。
- 作者失联：保留所有历史与候选，安全撤销授权并重新分派。
- Watchdog 不读取全文：仍能核验 ID、状态、SHA、审核绑定；不能宣称完成语义审计。
- 审核者发现与已有 FACT 矛盾的反例：追加 FAIL，标记候选需要重新验证，而不是静默覆盖旧事实。

## 11. 与微软 Agensh 的差异（明确标记）

**直接借鉴：** 自组织 CLAIM、共享短事实、FAIL 阻止重复无效尝试、异步工作循环、代码自检、PR/合并冲突后复验、基础设施事件去重与恢复。

**我们新增：** 分级强制独立审查、不可变版本绑定审核、正式 QA 门禁、返工次数上限、升级策略、GitHub Markdown 事件账本、Watchdog 符号/Agent 神经严格分工、GCP Mini Controller 的授权和看板投影。

**待进一步研究：** 微软论文完整实验轨迹中的同伴审查行为分布、PR 实际复审频率、不同团队规模的返工成本与审查收益。公开 README 和工作指令本身不足以支持“微软所有提交都必须由其他 Agent 审核”的断言。

## 12. 版本实施优先级

- P0：冻结 Schema、状态机、作者自检与独立审核门禁、审核绑定 commit、事件幂等。
- P1：实现 Watchdog 的纯元数据审计、BOARD 重建、失败升级、增量轮询。
- P2：跨 Agent 双盲/交叉复核、真实测试和连续 24 小时运行。
- P3：成本路由与不同审核策略的统计优化。

**冻结条件：** Codex 和 WorkBuddy 分别评审本规范，指出不符合微软源代码的描述、不可执行规则、竞态条件与成本过高的门禁；经独立裁决后发布 V1.1 冻结版。未经评审本 V1.0 不能声称已经部署或实现。