# Agensh-Lite｜多 Agent 质量互审、迭代闭环与符号治理强制规范 V1.0

> 文件性质：**研究依据 + 拟议工程规范**（`PROPOSED_FOR_R02_ADOPTION`）；**不是**已经部署生效的运行规则。
>
> 研究日期：2026-10-26；适用：Lite-M（Markdown 看板）、Lite-M+（Mini Controller / Watchdog）、Lite-P（完整 Controller）。
>
> 研究基线：Microsoft `microsoft/Agensh@0468a3e6a58b51dc2b84871fcaa0df22b0d1033e`；我们的 `kaibahaha/xxsc@2d4c1a6fc0792a1182777262b41bfb4c09c0b5d2`，并核对 R01 开发分支的已有质量门禁。
>
> 重要标记：`[M]` 微软论文或源码确证；`[A]` 我们为跨平台定时 Agent 新增的规则；`[T]` 需要实测的工程假设。**不得将 [A] 称为微软原版规定。**

## 0. 核心结论

1. **微软原版默认是“每名 Agent 自主领单—工作—按验收标准自验—合并—发布 PATCH_SUMMARY—继续领单”的循环 [M]，不是“每份代码必须经另一 Agent 审计”的统一强制门禁。** 原论文第 2.1 节和附录 A 明确写出流程。
2. **同行审核、撤销先前批准、修订、重新审核、第三方整合**在微软多 Agent 实验轨迹中出现并逐渐标准化 [M]，尤其 32、128、1024 Agent 的案例。这些是观测到的组织行为，不应被冒称为默认内建强制审批状态机。
3. 微软 `board-service/verifier.py` 仅检查 NOTE 结构与占位证据字样，**不会实际运行测试** [M]。微软 `mini-router` 管消息持久化、去重、失败重试与 ACK；质量内容仍由 Agent/实际工具判断 [M]。
4. 我们将上述经验工程化为**神经/符号分治** [A]：Watchdog 只执行确定性、可复算的身份/版本/时序/转移/证据引用/完整性校验；AI Agent 做需求理解、设计、编码、真实测试、反例发现与独立代码审查。Watchdog 不能把 `PASS` 文字当成测试通过。
5. 为了防止“自己审自己、反复修改、状态混乱”，对**高风险生产代码**规定独立审查与具体版本的不可变审查记录 [A]。每轮候选代码、反馈和修复必须有独立 ID；后续改动使旧审查不再适用于新版本；修复最多尝试约定轮数后升级，而不是无穷返工。
6. **我们的 Mini Controller 属于面向可靠性的原创增强 [A]**。微软强调无中央分配者、Agent 自组织；我们用单主符号状态仲裁，不应说微软本身就有同样的集中授租 Controller。

## 1. 微软 Agensh 的确证机制：原文、代码、真正的边界

### 1.1 共同的五步合作循环 [M]

来源：论文 §2.1 与 `prompts/agents.txt` 第 68–79 行。

`Gather context → Claim sub-task → Take action → Verify results → Merge progress → 新一轮 Gather context`

- **Gather context**：理解共享目标、同伴消息、已证实 FACT/FAIL 和当前进度。
- **Claim**：声明范围，重叠时消息协商。CLAIM 是工作意图和去重提示，非天然排他锁。
- **Take action**：独立实现，及时上报可复用发现。
- **Verify**：**执行者自己**对照该子任务验收标准测试和修订，不符合则继续修改。
- **Merge**：将验证后的贡献并入共享 Git 工作区，发生冲突就同步最新代码、解决冲突并**重新验证**，然后发表 `PATCH_SUMMARY(files,idea,evidence)`。

原版提示词允许作者自行合并到 main。**默认循环没有强制“候选先经另一 Agent REVIEW_APPROVED 才能 merge”**。这是我们未来需要明确增强的重点。

### 1.2 由协作轨迹涌现的同行质量机制 [M]

来源：论文 §3.2，按规模区分：

| 微软观测 | 证据中的具体行为 | 对我们的启发（非微软强制条文） |
|---|---|---|
| 8 Agent | 同行协商模块接口；发现 CLAIM 重叠后修改工作边界 | 先冻结接口，避免重复劳动 |
| 32 Agent / PHP-src | 多个同行起初认可贡献；另一 Agent 找到**具体反例**；既有认可被撤销；作者修复；再次审核；**同行合并** | 反例必须推翻**对应旧候选版本**的通过状态；保留审计链 |
| 128 Agent / pandoc | 审核者依据专业经验被选择；作者发 commit 给同行验证并整合；失败后重新协商更完善的流程 | 以能力选审核者；独立审查与整合可有不同角色 |
| 1024 Agent / pandoc | 多个候选 Integrator，择一接单，取消其余请求；同行失败时由另一人接管 | 有承接/撤销机制，避免重复整合和无人值守死锁 |

关键辨析：微软论文**证明出现过**这些协作现象，并未证明它对每次交付都强制执行，亦未给出全局统一的“最多三轮审核”等条款。

### 1.3 共享上下文的五种类型 [M]

来源：`board-service/shared_lessons.py` 与 `prompts/agents.txt`：

- `OBSERVED`：运行或观察得到的行为。
- `FACT`：可复用的已确认事实。
- `FAIL`：经事实反驳的假设/路径，减少同伴浪费预算。
- `CLAIM`：当前工作范围，默认 TTL=3600 秒；过期后不再作为活跃视图，历史仍保留。
- `PATCH_SUMMARY`：文件、想法、证据的简短摘要，便于下一个 Agent 继续工作。

源码中一个新 `FAIL` 可撤销**同作者 thread_id + delegation_id 匹配的最近 PATCH_SUMMARY 候选**的 `_verified_checkpoint` 标志；不是“任意 FAIL 永久否定全项目所有提交”。补丁摘要在近期视图中可按身份/委派更新，完整历史保存在数据库。

`board-service/verifier.py` 仅做文本格式与弱证据过滤。**写了 verified/passed 字样 ≠ 独立验证成功。** 我们不得照搬该启发式作为 QA_GREEN。

### 1.4 事件、游标、恢复属于符号基础设施 [M]

来源：`mini-router/src/state.ts`、`dispatcher.ts`、`board_client.ts`：

- 事件状态 `pending / sending / sent / failed / retrying`；以 `(event_id,target_agent)` 去重，按 `(agent,source)` 保存 cursor。
- 事件批次序列化进入单个 Agent 会话；完成 turn 后标已投递；失败采用递增退避（源码最多 5 次），重启恢复 `sending`。
- 读取共享看板失败明确为 **UNKNOWN，不是 EMPTY**；增量 snapshot 失败再回退全量 read。
- Agent 本轮有实质发现却没有发表共享知识时，有提醒机制；不能为了完成配额伪造事实。
- 微软源码的 `sent` 只代表消息投递流程状态，**不是代码质量验收，也不是业务 DONE**。

### 1.5 三种基础设施边界 [M]

- Git / Gitea：共享文件、私有工作分支、历史和合并冲突。
- Mattermost：群消息与紧急点对点协调。
- Shared Board / MySQL：结构化发现、工作意图、近期视图和完整历史。
- 由每个 Agent 的 Prompt 定义合作循环，单 Agent harness 负责模型思考和工具调用，基础设施管传递和恢复。

**我们的差别**：[A] 以 GitHub + 定时轮询替代微软部分实时通知；以 Markdown/事件目录替代 Board Service+MySQL 的大部分协作层；Mini Controller 只执行确定性的符号约束，不替代 Agent 决策。

## 2. 总体原则：神经/符号分治

| 层 | 责任 | 禁止越权 |
|---|---|---|
| `Symbolic Watchdog` | ID/Schema、版本、唯一性、Git SHA、状态转移、归属、事件去重、超时、游标、依赖、文档引用、冲突、看板投影、证据清单存在性、有限重试 | **不得**根据测试日志的单词 `PASS` 断言程序正确；不得评价需求满足性；不得自行伪造测试、修复代码 |
| `Neural Author` | 需求理解、方案、编码、作者自检、测试请求、候选发布、依据反馈修复 | **不得**给自己签发独立 QA；不得自改他人审查结果；不得绕过版本锁 |
| `Neural Reviewer` | 独立阅读 TASK、源代码 diff、测试与运行日志，提出可复现反例；给出 `APPROVE / CHANGES_REQUESTED / BLOCKED` | 不得直接把“作者说测试通过”当证据；若自己改了候选代码，需交由其他独立者复核 |
| `Neural Integrator` | 跨模块整合、解决合并冲突、运行整合测试、给出集成证据 | 不得仅凭个人合并成功自动签发业务验收 |
| `Authorized Acceptor` | 对产物是否符合业务目标作最终裁决 | 不得仅凭文件存在或 ACK 认定完成 |

身份必须有 `agent_id + provider_id + account_scope + independence_group`；模型名称/署名文字不等于身份认证。首次执行能力须有真实平台的 Git 读写/测试探针。

### 2.1 Markdown 可见性与事实语义

- Git 历史和只追加证据形成**可追溯、可检测更改**的记录；不等同绝对不可篡改。保护分支、最小权限、外部审计快照用于防止历史被重写。
- `BOARD.md` 是**投影与导航页**；正式事实应来自不可变任务规格、候选提交、独立审查、证据与最终验收。
- 证据链严格分层：`GIT_VERIFIED` ≠ `SELF_TESTED` ≠ `INDEPENDENT_QA_GREEN` ≠ `BUSINESS_ACCEPTED`。
- 绝不让两个 Agent 同时无条件编辑同一个共享 BOARD；只保留一个受控写者。其他 Agent 只写自己的事件与 RUN 目录。

## 3. 必须区分的三个状态维度 [A]

禁止将任务状态、候选版本状态和事件投递状态混为一谈。

| 维度 | 状态 | 解释 |
|---|---|---|
| `Task.status` | `READY, CLAIMED, ACTIVE, REVIEW_WAIT, INTEGRATING, DONE, BLOCKED, CANCELLED` | 任务业务生命周期 |
| `Candidate.status` | `DRAFT, SELF_TESTED, REVIEW_PENDING, CHANGES_REQUESTED, QA_GREEN, SUPERSEDED, REJECTED` | **特定 commit/spec** 的交付候选 |
| `Delivery.status` | `PENDING, SENDING, ACKED, FAILED, UNKNOWN` | 单次事件与证据投递状态 |

`Task.DONE` 的必要条件：绑定版本的 QA、整合验证和有权最终验收齐全；若任务政策仅要求文档草稿，验收政策可单独降低门槛，但必须在 TASK 初始固定，不得交付后修改规则自我放行。

**最小闭环：**

`READY → CLAIMED → ACTIVE → SELF_TESTED(candidate v1) → REVIEW_PENDING → [CHANGES_REQUESTED → ACTIVE(candidate v2) → SELF_TESTED → REVIEW_PENDING]* → QA_GREEN → INTEGRATING → DONE`

上面是**我们拟议的加强版流程 [A]**，不是微软原始硬编码流程。只有授租权威真实存在才允许标记强 `CLAIMED`；Lite-M 无可信强租约时用 `CLAIM_PROPOSED` 与静态任务分区。

## 4. 审核模式：既不人人审核所有任务，也不允许高风险自批 [A]

### 4.1 按风险等级决定独立审查

| 级别 | 任务示例 | 强制要求 |
|---|---|---|
| P0 高危 | 密钥、认证、权限、资金/数据删除、生产部署 | 作者自测 + 独立代码审查 + **独立实测/安全核对** + 用户/明确授权的最终批准；未知即阻断 |
| P1 核心 | Controller、并发租约、数据迁移、共享状态机、执行权限 | 作者自测 + 另一独立 Agent 审查 + 同 SHA 真正回归测试 + 集成批准 |
| P2 常规编码 | API、模块、普通 Bug 修复 | 作者自测 + 另一 Agent 快速审查；可用可信自动测试辅助，但不得代替必要的人/Agent 判断 |
| P3 低风险 | 文档、注释、非功能格式 | Watchdog 结构校验 + 作者自检；独立抽检或按策略审查 |

**P0/P1 不因审查 Agent 离线就默许通过。** 无法测试要写 `BLOCKED_EXECUTOR`，无法获取证据写 `UNKNOWN`。审查 Agent 可为同类 AI 但尽量选择不同 provider/model/context；“同一份作者报告换个窗口读一遍”不构成真实独立测试。

### 4.2 审查者分配

1. 与作者不同的 `agent_id`；对 P0/P1 尽量不同 `independence_group`。
2. 审查者必须取得冻结 TASK、`spec_hash`、待审 `commit_sha`、完整 diff 与原始证据入口。
3. 选择依据：能力、任务领域、风险、剩余预算、工作负载；不是强制让“下一个领单的 Agent”自动审核上一单。
4. 审查者可兼任下一单作者，但审查工单有单独任务 ID、预算、截止与审查记录；不能因审查未做而静默继续生产。
5. 审查与整合是**不同动作**；两者可以由一个合格 Agent 承担，但必须留下两套可核验的不同证据。
6. 若审核者不可用，Watchdog 创建 `REVIEW_UNASSIGNED`；下一次可重新分配，严禁默认批准。

## 5. 返工、反例和撤销批准的不可混乱纪律 [A]

1. 每个 TASK 的需求有不可变 `spec_hash`；改变需求须新版本并标记旧评价是否失效。
2. 作者每次提交新候选都生成新的 `candidate_id = task_id + attempt_no + commit_sha`（可存完整字段，不以显示名称作为实际唯一凭据）。
3. 审查针对确切 `task_id/spec_hash/candidate_commit`，不能审核一个分支名就视为审核之后所有提交。
4. `CHANGES_REQUESTED` 必须至少有一个**可定位、可验证、可修复**的 `finding_id`，写 `severity`、`file:line` 或输入/输出、预期/实际、证据 URI、建议复现方式；不接受“感觉质量一般”作为阻断证据。
5. `FAIL` 绑定 `task_id + spec_hash + candidate_commit + test_case`，旧批准如覆盖被证伪的同一范围必须撤回；撤回写新的事件引用旧批准，**不覆盖或删除旧审核文件**。
6. 新 commit 产生后旧 QA 只作为历史，**不能自动继承**为新 commit 的 QA_GREEN；必须对新版本复核受影响区域与回归证据。
7. 作者针对 findings 修复并提交 `FIX_REPORT`，逐条引用 `finding_id`、变更位置、测试命令/环境/退出码/日志哈希；审核者重新审查。
8. 不同意见先给出测试/接口契约/复现证据；争议无法解决时建 `REVIEW_DISPUTE`，请第三方裁决，不让两名 Agent 在一个 BOARD 反复覆盖结论。
9. 默认建议**最多 3 个候选修订循环**（可由 TASK 预先配置），超过后转 `ESCALATED`：重新拆任务、换模型/审查者、升级架构裁决或请求人工授权；**不得无限轮烧额度**。
10. 发现 P0/P1 关键反例，即使先前已 `QA_GREEN`，也必须发布 `REGRESSION_FOUND` 并将对应版本状态暂停接受；若已部署，走独立回滚/修补策略，不伪称历史从未通过。
11. 并行多个审查者时分别产生审查记录；“首个回应者负责整合”的择一机制需留下选定/取消其他请求的事件，避免多名 Integrator 各自合并。
12. 超时不等于失败；缺乏反馈标 `REVIEW_STALE/UNKNOWN`，只按授权的接管策略调度，不给旧 Agent 擅自扣上失败标签。

## 6. Agent 每轮工作与审查的标准操作规程 [A]

**Author 周期（定时唤醒）**

1. 读 `AGENTS.md/POLICY.md`、自己 HANDOFF、Git 最新事件水位、TASK 和相关 FACT/FAIL。
2. 检查静态分区或有效租约、截止、读写范围；失败先停共享写。
3. 只对获准范围编码，明确本轮当前 `spec_hash`、base SHA。
4. 独立自检，运行真实可用的测试工具，保留命令、运行环境、stdout/stderr、exit code 和真实 Git SHA。无运行工具标 `TEST_NOT_RUN`。
5. 写 `SUBMISSION` 和 `PATCH_SUMMARY`，状态最多 `SELF_TESTED`；由 Git 写后回读生成可核验证据。
6. 创建 `REVIEW_REQUEST` 并退出当前阶段；未得 Reviewer 反馈时可认领**不同**任务，不必空等，但不得自签本任务完成。
7. 下一轮若收到 `CHANGES_REQUESTED`，优先在期限内处理旧工单、写 `FIX_REPORT`、发布新候选；过期仍保留交接，安全移交。

**Reviewer 周期（独立唤醒）**

1. 读 `REVIEW_REQUEST`、TASK/spec 和待审具体 SHA；若 SHA 改变标 STALE，要求重派。
2. 独立读实际 diff/相关源码；按风险运行或委托可信执行器运行测试；检查边界输入、失败路径、回归和权限。
3. 只写自己的 `REVIEW_REPORT` 和必要 `FAIL/FACT`；结论 `APPROVE / CHANGES_REQUESTED / BLOCKED / UNCERTAIN`。
4. `APPROVE` 必须指出具体 commit、spec、覆盖范围和测试证据；只有静态阅读不得声称“已运行”。
5. 若审查者亲自改了候选文件，原则上转为共同作者；需要另一独立审查者确认新版本。
6. 形成 `ACK` 和 `HANDOFF`，下一轮 Integrator/作者才消费；不把消息投递 ACK 当 QA。

**Integrator / Acceptor 周期**

1. 只整合已批准的具体候选 SHA；对 PR 冲突修复后的新 SHA 重新完成受影响测试/审查。
2. 从干净环境构建、执行跨模块契约与回归；如缺执行器保持 `INTEGRATION_BLOCKED`。
3. Integrator 给出 `INTEGRATION_VERIFIED`；符合 TASK 起始验收政策后由有权角色签发 `BUSINESS_ACCEPTED`，最后 Task `DONE`。
4. 任何一步失败生成不可变事件，而非覆写最终状态或删除旧尝试。

## 7. Watchdog 只管“符号事实”，具体边界 [A]

建议 Watchdog 的运行逻辑：

```text
read_git_ref_and_changed_paths
  -> load small task/event/review manifests
  -> validate schema, IDs, signatures/identity scope and version links
  -> detect duplicate events, stale reviews, orphan claims, missing ACK
  -> verify hash/reference against Git object metadata
  -> apply authorized deterministic state transitions
  -> write immutable AUDIT findings
  -> single-writer project BOARD projection
  -> exit or sleep
```

- 默认不读取所有 Markdown 正文；优先读 Git ref、tree、路径、Git blob SHA 和小型 manifest/frontmatter。必要时读目标文件字段和证据原始字节以计算 SHA256，但**不阅读代码语义、不对交付质量打分**。
- `git_blob_sha`、`commit_sha`、`raw_sha256` 必须分别命名，不能相互代替；内容 SHA256 如未取得真实字节不得声称重新计算。
- 检查 `TASK exists`、`candidate_commit exists`、`review references current SHA`、`reviewer != author`、`required evidence exists` 和 `state_transition allowed`。
- `required evidence exists` 仅证明文件存在，**不证明 pytest 真跑过**；真正的独立执行证明交给 Reviewer/Runner 的实际验证记录。
- 碰到阅读失败：`BOARD_UNKNOWN` / `GIT_UNKNOWN`，禁止把未知当无任务；暂停授权式共享写，已保存的个人 outbox 不清除。
- 单主写 BOARD，所有事件、反馈和候选按新增文件追加。Watchdog 可以根据前后事件重算状态，但**不能暗中删掉或改写历史评价**。
- Watchdog 同时负责风险等级门禁：P0/P1 缺独立审查不能进入 DONE；但不得自行生成假审核来满足门禁。
- 任务权威必须可冷重启恢复；GCP Mini Controller 的 SQLite 状态不是唯一永久历史，要与 Git 不可变事件和原子发布回执核对。
- Lite-M 的“CLAIM”是软认领，仅承诺静态分区下安全推进；Lite-M+ 强租约只有在真实串行事务、fencing 和 Git 独立回读验证后才允许启用。绝不把普通 Git 文件声明当作跨 Agent 强锁。

## 8. Markdown 文件群规范：建议最小目录与字段 [A]

保留已冻结 V4.1 作为历史规范，下面是 V4.2+ 的**新增草案**：

```text
projects/<PROJECT_ID>/
  00_policy/
    POLICY.md             # 单写、权限、版本、风险等级与质量门槛
    AGENTS.md             # 各 Agent 的循环/角色指令
    AGENT_REGISTRY.md     # 身份、capabilities、independence_group
  01_tasks/<TASK_ID>/
    TASK.md               # spec_hash、验收标准、风险等级、重试上限
  02_claims/<TASK_ID>/
    <EVENT_ID>.md         # 软认领 / 经授权授租回执
  03_events/<YYYYMMDD>/
    <EVENT_ID>.md         # 不可变状态/因果事件
  04_submissions/<TASK_ID>/<CANDIDATE_ID>/
    SUBMISSION.md         # 产物 SHA、作者 SELF_TESTED、证据索引
    SELF_TEST.md
  05_reviews/<TASK_ID>/<CANDIDATE_ID>/
    <REVIEW_ID>.md        # 独立审核、finding_id、证据
    FINDINGS.md           # 可复现实证缺陷
  06_fixes/<TASK_ID>/<CANDIDATE_ID>/
    FIX_REPORT.md         # 上一候选 findings → 新候选 SHA
  07_integrations/<TASK_ID>/
    INTEGRATION.md        # 合并/冲突/回归证据
  08_receipts/<TARGET>/<EVENT_ID>.md
  09_runs/<AGENT_ID>/<RUN_ID>.md
  10_projections/
    BOARD.md              # 唯一受控写者维护；重算视图
    CURRENT.json          # 可供 Watchdog 轻量机器读取
  11_archive/
```

### 8.1 必备字段（所有类型共享）

`schema_version`, `project_id`, `task_id`, `event_id`, `run_id`, `agent_id`, `provider_id`, `created_at_utc`, `source_repo`, `source_ref`, `source_commit`, `causation_id`, `correlation_id`, `evidence_refs`, `integrity_status`。

针对代码交付另需 `spec_hash`, `base_commit`, `candidate_commit`, `attempt_no`, `author_independence_group`, `test_environment`, `test_command`, `exit_code`, `log_sha256`。

针对审核另需 `review_id`, `reviewer_agent_id`, `reviewer_independence_group`, `reviewed_candidate_commit`, `decision`, `findings`, `test_executed`, `reviewed_at_utc`。

字段应使用固定版本机器可读的 YAML Front Matter 或同目录 JSON manifest。**自然语言正文只供 Agent 判断，不作为 Watchdog 的隐式状态来源。**

### 8.2 TASK.md 最小范本

```yaml
---
schema_version: "1.0"
record_type: TASK
project_id: PROJECT-EXAMPLE
task_id: TASK-017
risk_class: P1
task_status: READY
spec_version: 1
spec_hash: "sha256:<calculated-exact-task-spec>"
required_capabilities: [python, github]
allowed_write_paths: ["factory/agl/"]
acceptance_criteria:
  - "并发争租不会签发两个同时有效的 GRANT"
  - "旧 epoch 被拒，异常重试不产生重复业务结果"
independent_review_required: true
integration_test_required: true
max_revision_cycles: 3
deadline_utc: null
---
# 工单正文
明确范围、输入、交付文件、测试和安全边界。
```

范本中的哈希是占位表示法，**不得把它当作实际计算结果或已验收证据**。

### 8.3 REVIEW_REPORT.md 最小范本

```yaml
---
schema_version: "1.0"
record_type: REVIEW
project_id: PROJECT-EXAMPLE
task_id: TASK-017
candidate_id: TASK-017-A02
review_id: REV-TASK-017-A02-01
reviewer_agent_id: CHATGPT-QA-01
reviewer_independence_group: CHATGPT
reviewed_candidate_commit: "FULL_COMMIT_SHA_REQUIRED"
spec_hash: "EXACT_SPEC_HASH_REQUIRED"
decision: CHANGES_REQUESTED
test_executed: false
reviewed_at_utc: "YYYY-MM-DDTHH:MM:SSZ"
findings: ["FIND-017-003"]
evidence_refs: ["06_evidence/TASK-017/..."]
---
# 审查结果
## FIND-017-003
严重度：P1；定位：文件:行/接口；复现步骤：……
预期：……；实际：……；证据：……
## 允许的下一动作
原作者提交新 Candidate；本审核不授权当前候选合并。
```

### 8.4 返工示例：三轮不混乱

```text
TASK-017 (spec S1)
  CANDIDATE-A01 (commit c1)
    SELF_TESTED(c1)
    REVIEW-01 => APPROVE(c1)
    REVIEW-02 => CHANGES_REQUESTED(c1, FIND-003, counterexample)
    REVOKE_APPROVAL(c1, REVIEW-01)   # 只取消对 c1 的认可
  CANDIDATE-A02 (commit c2, fixes FIND-003)
    SELF_TESTED(c2)
    REVIEW-03 => APPROVE(c2)
    INTEGRATION_VERIFIED(c2)
    BUSINESS_ACCEPTED(c2)
    DONE(c2)
```

`REVIEW-01`、`REVIEW-02` 永远保留；看板只投影“当前有效候选 c2 已验收”。无需让每个 Agent 重复审查所有历史版本。

## 9. 质量门禁与规则一致性检查 [A]

| Gate | 检查者 | 正常通过条件 | 阻断条件 |
|---|---|---|---|
| G0 SPEC | Watchdog + Author | TASK 有冻结 spec、风险、验收标准 | 缺 spec_hash、缺权限 |
| G1 DELIVERY | Watchdog | 候选真实 commit、路径、ID、回读有效 | SHA 不存在、记录冲突 |
| G2 SELF_TEST | Author / Runner | 可复现自检记录；未跑写 NOT_RUN | 伪造运行证据 |
| G3 INDEPENDENT_REVIEW | Reviewer | 必需审查明确批准当前 SHA，P0/P1 有独立证据 | 同人自批、旧 SHA、实质反例 |
| G4 INTEGRATION | Integrator / Runner | 干净基线整合和回归通过 | 新 commit 未重验、冲突未解 |
| G5 ACCEPTANCE | 授权 Acceptor | TASK 条件满足 + 证据链完整 | 未授权角色签发、缺必要 Gate |

**审查失败只能推动返工或安全暂停，不能删除别人的代码。** 作者可因证据确凿的修复请求主动纠错；版本改动后全部结论须重新关联。

### 9.1 Watchdog 可编码断言

```text
assert unique(event_id)
assert unique(candidate_id)
assert immutable(original_event_file)
assert task.spec_hash == review.spec_hash
assert candidate.commit == review.reviewed_candidate_commit
assert reviewer.agent_id != author.agent_id
assert dependency_states satisfy task.required_dependencies
assert no DONE without required QA/integration/acceptance
assert no QA_GREEN from existence-only check
assert no stale or expired lease advances authoritative state
assert no prior accepted fact silently overwritten
assert failed_read != empty_queue
assert no second integration winner for same (task_id, candidate_id)
assert review_revision_count <= task.max_revision_cycles or status == ESCALATED
```

真实执行需要正确读取 Git 证据以及身份验证，否则应明确为 UNKNOWN，而不是假称通过。

## 10. R02/R03 具体开发纪律与责任 [A]

### 10.1 立即作为下一轮的输入（不自动生效）

- R02 前先将本规范 **审查、冻结为 Policy**；冻结时记录政策版本 SHA。之后定时 Agent 必须显式引用该 SHA，禁止“最新聊天消息覆盖冻结规范”。
- **ChatGPT**：负责 QA 规则设计与对照研究；在特定工单担任与作者不同的审查者。
- **Codex**：负责修订 `AgentRegistration / Candidate / Review / Finding / Integration` 契约，检查 lease、fencing、审查失效与并发状态机；不要为简单 Markdown 维护花费 High 额度。
- **WorkBuddy**：开发/裁剪 Mini Watchdog、轻量 schema 校验和 Git 目录扫描；写可复现演示、反例注入与 CI 校验。
- 新规范未冻结前保留两份 R01 PR 的 Draft 状态，禁止自动合并到 main；不擅自启动定时任务、云端部署或付费 API。

### 10.2 最少十项强制验收场景

1. 两 Agent 同时 CLAIM 同任务：Lite-M 给出冲突并按静态分区控制；Lite-M+ 只能有一份有效权威 GRANT。
2. 作者自报 `PASS`，无真实测试记录：最多 `SELF_REPORTED`，不能 `QA_GREEN`。
3. Reviewer 找到反例：旧 candidate 的批准撤销，历史评价仍可回读。
4. 修改一行代码导致新 SHA：旧 Review 不被自动复用，新提交进入 REVIEW_PENDING。
5. 同一 REVIEW_ID 重试：不可产生两次业务审核事件；不同内容撞 ID 必须显式失败。
6. Reviewer 失联两轮：形成 `REVIEW_UNASSIGNED` 并再派，旧反馈不被覆盖。
7. 审查者也是候选作者：强制拒绝作为独立 QA。
8. 连续三轮返工仍失败：转 `ESCALATED`，不得无限重试消耗模型额度。
9. GitHub 超时写入未知：只读回读对账，不盲目再写。
10. 重启 Watchdog 后用事件重放重建 BOARD，结论与冷启动前一致。
11. 合并冲突解决后更改 SHA：受影响的测试与审核必须重做。
12. 只读失败与真的零任务严格区分：`UNKNOWN != EMPTY`。

### 10.3 与现有 V4.1/V4.2 的衔接

已有文档：
- `frameworks/agensh-lite-v4.1/05_SHARED_MEMORY_AND_CONTEXT.md`
- `frameworks/agensh-lite-v4.1/06_LIFECYCLE_AND_HANDOFF.md`
- `frameworks/agensh-lite-v4.1/07_QA_GATES_AND_PROVENANCE.md`
- `frameworks/agensh-lite-v4.2/workorders/REVIEW_AND_GATE_R01.md`

它们已含证据分级、独立 QA、FAIL 生效范围等部分核心纪律。**当前真正缺的是贯穿多个轮次的 Review/Revision/Revocation 因果链、按风险选 Reviewer、截止/升级纪律、元数据结构、与 Watchdog 的明确权限分工。** 后续应以本文件为增量规范，不复制改写 V4.1 冻结原件。

### 10.4 阶段验收定义

- `SPEC_DRAFTED`：本文件已经编写，仅是规范提案。
- `POLICY_FROZEN`：经用户/授权审查确认并绑定政策 SHA，Agent 指令实际引用。
- `IMPLEMENTED`：相关代码/Markdown 模板落库。
- `TESTED`：上述场景有真实日志、原始 SHA 和回读证据。
- `OPERATIONAL`：连续多个定时轮次跨 Agent 跑完修复—复核—整合—验收闭环。
- **禁止把文件已保存直接称为系统功能已上线。**

## 11. 来源与证据映射（固定版本）

### 论文：原始研究证据

- [论文 HTML §2.1：五步合作循环](https://arxiv.org/html/2609.26781#S2.SS1)。
- [论文 HTML §2.3：合作指令由 Prompt 实现，不是全部由 Runtime 硬编码](https://arxiv.org/html/2609.26781#S2.SS3)。
- [论文 HTML §3.2：8/32/128/1024 Agent 的协同涌现、反例推翻旧认可](https://arxiv.org/html/2609.26781#S3.SS2)。
- [论文 HTML 附录 A：同一 Agent 自验、自己提交 PR 与 merge 的默认协议](https://arxiv.org/html/2609.26781#A1)。
- [论文 HTML 附录 B：事件驱动与共享上下文传递](https://arxiv.org/html/2609.26781#A2)。

### 微软 GitHub：精确源码（不可随 main 漂移）

- [prompts/agents.txt](https://github.com/microsoft/Agensh/blob/0468a3e6a58b51dc2b84871fcaa0df22b0d1033e/prompts/agents.txt)：第 68–79 行默认循环。
- [board-service/shared_lessons.py](https://github.com/microsoft/Agensh/blob/0468a3e6a58b51dc2b84871fcaa0df22b0d1033e/board-service/shared_lessons.py)：五类 NOTE、CLAIM TTL、同作者同委派 PATCH 失效、历史重建。
- [board-service/verifier.py](https://github.com/microsoft/Agensh/blob/0468a3e6a58b51dc2b84871fcaa0df22b0d1033e/board-service/verifier.py)：文本证据检查，不执行测试。
- [board-service/main.py](https://github.com/microsoft/Agensh/blob/0468a3e6a58b51dc2b84871fcaa0df22b0d1033e/board-service/main.py)：持久化、快照、Board 权限与回放。
- [mini-router/src/state.ts](https://github.com/microsoft/Agensh/blob/0468a3e6a58b51dc2b84871fcaa0df22b0d1033e/mini-router/src/state.ts)：事件去重、重试、持久游标与恢复。
- [mini-router/src/dispatcher.ts](https://github.com/microsoft/Agensh/blob/0468a3e6a58b51dc2b84871fcaa0df22b0d1033e/mini-router/src/dispatcher.ts)：串行 turn、ACK、失败重试、知识回写提醒。
- [mini-router/src/board_client.ts](https://github.com/microsoft/Agensh/blob/0468a3e6a58b51dc2b84871fcaa0df22b0d1033e/mini-router/src/board_client.ts)：Snapshot 回退、UNKNOWN 非 EMPTY。
- [REPRODUCE.md](https://github.com/microsoft/Agensh/blob/0468a3e6a58b51dc2b84871fcaa0df22b0d1033e/REPRODUCE.md)：版本、工具链与实验可复现。
- [我们的 V4.1 采纳矩阵](https://github.com/kaibahaha/xxsc/blob/2d4c1a6fc0792a1182777262b41bfb4c09c0b5d2/frameworks/agensh-lite-v4.1/00_SOURCES_AND_ADOPTION.md)：此前已经做过的源码映射。

## 12. 风险声明与待验证项

- 微软观察到同行审核/再次审核不意味着已有公开量化指标能保证所有审核绝对可靠；我们的独立审查降低相关性错误，但仍可能产生共同盲点。
- 原版是 6 小时内、单集群、特定编码任务的研究实验；我们的跨平台、冷启动、小时级定时协同和 GCP 常驻 Watchdog 是**原创适配**，需要真实端到端测试。
- Watchdog 的单写者和强一致性取决于实际事务、持久状态和 Git 发布协议；不能由几个 Markdown 文件或 README 承诺替代测试。
- 当前仅完成规范起草与 Git/Library 文档交付；**没有启动 R02、没有自动部署 Mini Controller、没有改变任何已有定时任务，也没有批准两份 R01 PR 合并。**

---
文档目的：作为未来 `POLICY.md`、`AGENTS.md`、任务模板、审查模板与 Watchdog 校验器的**共同输入基准**。后续版本只通过新增、审核、冻结、兼容性迁移来更新，不得默默覆写历史纪律。
