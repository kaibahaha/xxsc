---
document_id: AGL-DECISION-ARCHIVE-20261026-POST-SCREENSHOT
schema_version: "1.0"
title: "Agensh-Lite V4.2｜截图锚点之后的架构、定时协作、消息机制与部署决策增量归档"
version: "1.0"
recorded_date: "2026-10-26"
timezone: Asia/Shanghai
status: "会话决策归档／非冻结生产规范"
project: "Agensh-Lite / 无人软件工厂 4.0"
source_scope: "截图‘Agensh-Lite V4.2：距离真正运行，还需要几个回合？’所指讨论之后，当前可见的连续会话及既有项目文件核对"
related_documents:
  - "Agensh_Lite_协作质量与迭代治理规范_V1.0.md"
  - "frameworks/agensh-lite-v4.1/01_ARCHITECTURE_AND_AUTHORITY.md"
  - "frameworks/agensh-lite-v4.1/02_GITHUB_LAYOUT_AND_WRITES.md"
  - "frameworks/agensh-lite-v4.1/04_UEM_EVENTS_AND_DELIVERY.md"
  - "frameworks/agensh-lite-v4.1/05_SHARED_MEMORY_AND_CONTEXT.md"
  - "frameworks/agensh-lite-v4.1/06_LIFECYCLE_AND_HANDOFF.md"
  - "frameworks/agensh-lite-v4.2/docs/CLOUD_CONTROLLER.md"
---

# Agensh-Lite V4.2｜截图锚点之后的架构、定时协作、消息机制与部署决策增量归档 V1.0

> **用途**：为下一轮 Agensh-Lite V4.2／Lite-M+ 集成、Markdown 协议、Mini Controller、Watchdog、Actions 部署和多 Agent 定时任务提供可独立阅读的决策依据。  
> **归档原则**：记录“讨论过什么、达成了什么、哪些尚未验证”，不将讨论或 AI 建议伪装成已实施事实；不覆盖已有冻结基线，不将微软原版与本项目的新增要求混淆。

## 0. 范围、证据级别和重要边界

### 0.1 截图时间锚点与时间边界

用户提供截图显示另一轮对话标题为 **「Agensh-Lite V4.2：距离真正运行，还需要几个回合？」**，截图中有“现在回到主任务，接下来还要他们各自干几个回合和工作量，能把系统搭建起来运行”和核查 Codex PR #1、WorkBuddy PR #2 的提示。本归档**从该截图代表的后续讨论主题出发**，汇总当前可见聊天中随后形成的决策与约束，重点包括：Lite-M/M+/P、GCP/Oracle/双 VM、GitHub Actions、微软 Agensh 协作机制、异步收件箱、错峰定时任务、Controller/Watchdog 职责及费用评估。

**可核实性边界**：截图不是此前另一窗口的完整逐字聊天记录；不能据此声称找到了那个窗口的全部历史消息。这里按可见会话和已存在的项目文档汇总，**不是对所有跨窗口、所有隐含工具记录的逐条法务式审计**。未提供实际运行日志的部署与运行状态均标记为“待实测”。

### 0.2 与先前已归档内容的区别

已有《Agensh_Lite_协作质量与迭代治理规范_V1.0.md》（2026-10-26，149 行）覆盖：微软源码基础、CLAIM/FACT/FAIL、作者自检、按风险分级独立审核、审查绑定 commit、状态机、返工次数、Watchdog 符号层及基本 Markdown 规范。**本文件不代替它**，主要增补其后讨论中尚未集中归档的部署选型、定时工作方式、消息机制、成本边界、操作纪律和决策变化；重复处仅作索引与必要澄清。

### 0.3 证据标签

- **[已讨论达成共识]**：用户与助手在可见对话中已明确认可该设计原则，但未必已部署。
- **[候选／建议]**：提出方案并分析利弊，未最终批准或没有真实验收。
- **[已核验事实]**：本次查看了已存在文件或 GitHub 数据；不等于软件已经集成可运行。
- **[微软原版]**：来自 `microsoft/Agensh` 官方仓库、论文或代码说明，与我们的定制要求分开。
- **[必须验证]**：仅凭聊天不能确认的权限、调度、可靠性、单价、CPU/内存或兼容性。
- **[纠偏]**：对早先容易过度概括或相互矛盾的表达作界线澄清，避免成为生产协议中的错误假设。

## 1. 全部核心共识速查

| 编号 | 达成的共识/仍保留的选项 | 成熟度 | 归档要点 |
|---|---|---|---|
| D01 | **Markdown 即程序；GitHub 是跨 Agent 的共享事实与协作中心** | 已讨论达成共识 | 人类可读协议 + 机器可读事件；Git 负责历史、SHA、PR/差异，不等于实时数据库 |
| D02 | **Agent 的聊天上下文极简，权威上下文外置于 Git** | 已讨论达成共识 | 定时任务提示词仅留角色、入口、不可逾越约束、短摘要、路径；不要滚雪球携带全文 |
| D03 | **定时唤醒节奏与业务任务生命周期解耦** | 已讨论达成共识 | Agent A 一小时后返回仍要按 TASK_ID/版本/返工查询，不按“第几轮”决定任务 |
| D04 | **Git 看板 + 事件账本可充当异步消息中心，无需为了现阶段专建实时聊天服务器** | 已讨论达成共识 | 但必须实现目标收件箱、游标、ACK、幂等、超时、恢复，不能只写大段日志 |
| D05 | **符号（确定性 Python）与神经（AI 认知、编码、审查）明确分层** | 已讨论达成共识 | Controller/Watchdog 检查真实引用、唯一性、权限和状态，不假装审核语义质量 |
| D06 | **Controller 不等于 Markdown；Watchdog 是 Controller 的监督模块** | 已讨论达成共识 | 可为一个 Python 代码库、一个轻量主服务/执行入口，避免维护两套独立规则引擎 |
| D07 | **GitHub Actions 可代替 GCP 执行轻量、短生命周期控制脚本** | 候选／待可靠性压测 | 它不是常驻服务；事件/定时触发、临时 runner、持久状态必须落 Git/外部存储 |
| D08 | **立即且唯一的排他认领不能仅靠 Actions“收到事件”保证** | 已讨论达成共识 | 严格授租需要原子提交/条件写入、权威所有者和 fencing；否则只能 SOFT_CLAIM 或静态分区 |
| D09 | **不默认部署 Mattermost 式实时通信服务** | 已讨论达成共识 | 因 ChatGPT 本身是错峰定时醒来，实时推送也不会自动唤醒普通 ChatGPT 定时聊天 |
| D10 | **任务提交、自检、独立 QA、集成验收是不同状态** | 已讨论达成共识；详见已有 V1.0 | 微软原版并不强制所有 PR 审批；我们的风险门禁是附加机制 |
| D11 | **部署成本优化应以真实事件数、每次工作流 job 的实际分钟数测量** | 已讨论达成共识 | 不能以“55 个 Agent 必定触发 118800 次工作流”作为唯一预算 |
| D12 | **GCP e2-micro、Oracle A1、第二台 e2-micro 与 Actions 都是候选部署载体** | 尚未最终冻结 | 后续倾向 Actions 优先做符号层，但不能据此认定 GCP 全部桥接职责已被替代 |
| D13 | **保留 Lite-M 纯 Markdown 降级路径；优先研发 Lite-M+ 轻量治理** | 已讨论达成共识 | Lite-P 是后续扩展；避免先引入重型云服务架构 |
| D14 | **每次 Wake-up：先读消息和旧任务，再领新任务；每次交付：写后回读与交接** | 已讨论达成共识 | 先处理返工、阻断和有效租约，避免旧任务在 3–4 轮后被忘记 |
| D15 | **主动提出最佳实践与风险优化，不要等用户自行摸索** | 用户明确表达的交互偏好 | 不能以某一轮语音承诺替代账户级可持久记忆或系统设置的确认 |

## 2. 讨论演化全景：从架构搭建到低成本自治运营

以下是**按可见讨论的主题顺序**整理的回合群，而非杜撰精确发言时间。

| 阶段 | 用户提出的问题 | 最终形成的判断 | 遗留缺口 |
|---|---|---|---|
| S01 | Codex 和 WorkBuddy R01 开发后，是否还需要很多轮才能运行？ | 不必先完整实现 Lite-P；先完成 Lite-M+ 的最小集成、验证真实闭环 | 两个 Draft PR 尚未合并、云上未验收 |
| S02 | 纯 Markdown 与深度 Controller 的边界在哪里？ | Markdown 能传任务和留历史，不能天然保证跨文件原子状态、租约排他、及时超时恢复 | 选择 L0/L1 的真实权威写入技术 |
| S03 | 常驻程序放 GitHub 还是 GCP VM？ | 最初倾向 GCP 运行 Mini Controller，GitHub 存状态与代码 | GCP 配置与成本、持久性 |
| S04 | 现有 GCP e2-micro 还要跑 CodeBuddy Bridge、FastAPI、MCP，看门狗是否需要扩容？ | Watchdog 很轻；真正占内存的是 CodeBuddy/桥接运行时；1 GB 整体紧张 | CodeBuddy 实测内存和会话量 |
| S05 | GCP 桥接方案是否正好匹配无人软件工厂？ | 通信桥应升级为轻量控制中心，但直接互调只能是可验证的加速通道；Git 异步链为底座 | ChatGPT Actions/MCP、Buddy 反向调用权限逐项验证 |
| S06 | 能否申请 Oracle 免费 ARM 或第二个 GCP 账号？ | 可作为高内存/双机选项，不应阻塞首轮部署；两个 1GB VM 不能合并成单个 2GB 内存地址空间 | Oracle 库存、ARM 兼容、免费资格、GCP 结算资格 |
| S07 | GCP 免费外流 1GB 是否太少？ | Watchdog 优先只读 Git 路径、commit/tree/blob SHA、frontmatter 等元数据；不需每轮下载全部正文 | 按真实仓库变化测出站/入站数据量 |
| S08 | 微软原版符号/神经、第三方审计究竟如何设计？ | 微软有事件路由与共享上下文，Agent 自主实现、自检、协作；我们新增独立 QA 分级门禁 | 社区实测同行审查频率不可臆测 |
| S09 | 研究微软核心机制并编写规范 | 已有《协作质量与迭代治理规范 V1.0》研究草案，保存过 Library + GitHub 规范分支 | V1.1 还需 Codex/Buddy 独立评审后冻结 |
| S10 | ChatGPT 定时任务带入太多历史怎么办？ | 只保留很短的运行摘要与 Git 指针，详细证据、状态、旧轮交接全部外置 | 热/温/冷上下文大小与按需索引规则 |
| S11 | 各 Agent 每小时运行一次、整体每 20 分钟有一位醒来，审查返工会不会隔几轮？ | 将调度时间与业务状态脱钩；旧任务、返工和未读消息优先于新任务 | 租约到期、旧版审查、迟到结果的故障注入 |
| S12 | 55 个 Agent 是否需要 Controller 全文审查？ | 不需要。Watchdog 只做符号化证据与状态核验，内容质量由 Agent/独立测试把关 | 真实流水线证据格式 |
| S13 | 微软 Controller 与我们看板是什么关系？ | 微软没有统一中心总指挥；我们 Mini Controller 也是协作协议引擎而非大型 AI 调度总脑 | 单实例权威授租能力 |
| S14 | Controller/Watchdog 是否可放 GitHub？ | 可将 Python 放 GitHub Actions 按事件/定时运行；不再必需为纯巡检常驻 VM | Actions 延迟、漏触发、短任务成本、持久状态 |
| S15 | 公有 Actions 免费、私有月分钟如何影响使用？ | 公有标准 Runner 免费但内容公开；私有有分钟配额，按 job 计费；不能把敏感业务看板为省钱全部公开 | 测量每次实际 job 计费时长 |
| S16 | 微软是否每次认领都需要中心 Controller？ | 否；微软 Gitea/Mattermost/board-service/mini-router 是在线事件基础设施，CLAIM 是协作声明 | 我们是否要提高为严格排他事务 |
| S17 | 微软有实时消息通道，我们是否缺这块？ | 微软 Mattermost DM 可协同，定时 Agent 不需要照搬；我们的 Git 消息账本 + 未读收件箱即可满足异步时效 | ACK/游标/目标路由/积压恢复 |
| S18 | 写看板和日志是不是消息看板？每轮苏醒先看板是否足够？ | 方向正确；但“提交成功”和“消费者确认”不同，必须持久化入站事件、版本和回执 | 防止重复处理、缺失、冲突 |
| S19 | 还有什么机制遗漏？ | 唯一授权、租约/fencing、审核绑定 SHA、返工上限、Controller 故障恢复、24h 压力测试 | 形成下一轮工单与验收矩阵 |
| S20 | 用户要求总结这些没有落成 Markdown 的共识 | 本文件系统性归档，并明确哪些只是候选而非已部署 | 独立评审、版本冻结、工单执行 |

## 3. 三种 Agensh-Lite 运行模式与演化路线

### 3.1 Lite-M：纯 GitHub Markdown（零常驻进程）

- Agent 由各平台原生定时器唤醒，自行拉取 GitHub 的任务、状态摘要、消息与自身 HANDOFF。
- 用规范化 TASK / CLAIM / EVENT / DELIVERY / REVIEW / ACK 文件沟通；每人自有写入范围，`BOARD.md` 是可重建视图。
- 可采用静态任务分区和软认领。**不承诺强排他锁、立即响应或多文件事务原子性**。
- 适合低并发试运行、旁路影子实验、Controller 故障后仍可继续的非共享破坏性工作。

### 3.2 Lite-M+：推荐的当前开发重心

- 保留 Lite-M 的原生 Agent 定时唤醒与 Git 事件账本。
- 加确定性的 Mini Controller，内部集成 Watchdog；负责事件去重、授权、状态机、超时、重建 BOARD、审计、告警。
- 可部署于 GCP 常驻单实例，也可将其中**无状态、可重跑、非实时的部分**放在 GitHub Actions；真正需要即时独占判定的原子授权需单独验证一致性方案。
- QA 由独立 Agent 和真实测试执行器承担，不消耗 Controller 的大模型额度。

### 3.3 Lite-P：未来深度扩展

- 动态 Agent 池、跨模型能力目录、时延/质量/价格路由、高并发隔离、复杂联邦授权与高可用。
- 并非当前启动条件；不能将 Lite-P 任务全压给 Codex 后迟迟无法做真实 24h 试运行。

### 3.4 路线演变结论

最初偏好“GCP e2-micro 常驻 Mini Controller”；随着讨论深入，发现 GitHub Actions 可以给 Watchdog 和部分 Controller 符号规则提供临时云执行环境，减少 VM 维护费用。因此**部署层从 GCP 优先，转为 Actions 优先做轻量符号层的候选方案**。但没有正式宣告废除 GCP：GCP 上的 CodeBuddy `--serve`、API/MCP 桥接是另一类长期在线服务，Actions **不能等价替代其监听端口与即时模型桥接功能**。

## 4. Git 是事实源；BOARD 只是投影；Agent 的上下文来自持久任务包

### 4.1 不要把四种对象混为一谈

| 对象 | 定位 | 是否可覆盖 | 消费方式 |
|---|---|---|---|
| `TASK.md` | 任务需求、约束、验收标准、版本 | 原任务冻结；变更创建新版本 | Agent 按需读取全文 |
| `EVENT-*.json` | 已发生且带标识的不可变事件 | 不可覆盖，只可追加纠错 | Controller/Agent 按事件 ID 消费 |
| `INBOX / ACK / CURSOR` | 特定 Agent 的未读消息与处理水位 | 状态可版本化更新，日志追加 | 每次唤醒优先读取 |
| `BOARD.md` / `CURRENT.json` | 全局任务与未处理事件的**索引/投影** | 仅唯一投影写者更新，可由事件重建 | 先读短摘要，再跳转关联资料 |

**硬结论**：“看板是事实源”是交流中的口语表达。严谨定义是：**Git 中的授权任务、不可变事件、提交 SHA、证明材料和回执组成持久化事实记录；BOARD.md 是这些事实的物化视图，不是唯一原始证据。** 这样才能在看板损坏时重建，也能避免 Agent 互相覆盖同一文件。

### 4.2 聊天定时任务上下文极简

定时任务原生指令仅固定：

1. `AGENT_ID / ROLE / REPO / BRANCH / PROJECT_ID / POLICY_PATH`。
2. 启动检查顺序、禁止事项、单轮最长任务数、预算与截止规则。
3. 上次运行的**短摘要/运行回执链接**（可选）；严禁把几十轮完整交付、代码、长日志或其他 Agent 的对话复制进任务配置。
4. 本轮从 Git **重新查询**当前状态、未读消息、未关闭任务、依赖、有效授权和 HANDOFF；不能信任定时任务已包含的旧状态。
5. 结束仅向定时对话回报简短 `RUN_REPORT`，详细输出写 Git（引用真实 SHA/路径）。

推荐短报告字段：`run_id, agent_id, task_id, input_head_sha, action, outcome, produced_event_ids, commit_sha, readback, blocked_reason, next_pointer`。不在聊天窗口复述长正文。若 Git 不可读，应报 `BOARD_UNKNOWN` 而非谎称“没有任务”。

### 4.3 HOT/WARM/COLD

- **HOT**：本次用户规则、Agent 权限、活跃 TASK、有效 grant、未读紧急消息、返工和最近阻断。
- **WARM**：该任务近 1–2 次交接、相关 FACT/FAIL、仍未解决的 Finding、必要的差异摘要。
- **COLD**：全部旧轮代码、详尽运行日志、历史事件、PR 讨论、重复上下文等；保存在 Git 按指针查找。
- 任何摘要压缩不得删除真实证据或关键禁令。

## 5. 时间驱动只是唤醒；业务由任务、事件与状态机驱动

### 5.1 真实场景

每位 ChatGPT 定时 Agent **每小时唤醒一次**；多位 Agent **错峰**，总体约每 20 分钟出现一位可领单 Agent。例如 A 在 `:00`、B 在 `:20`、C 在 `:40`，下一小时 A 再来。另有“最多五个 ChatGPT 定时 Agent”以及 WorkBuddy 可安排大量定时 Agent（用户提出约 50 个）的容量设想。**这里只描述讨论中的配置与目标，不把平台计划准点、模型配额或 50 个真实活跃实例当作本次核验事实**。先前 V4.1 文档还给出五工位 `:00/:12/:24/:36/:48` 的候选排班，两套节拍不能混写；部署必须以实际启用任务列表为准。

A 交付后 B 可能立刻提出缺陷；A 再次唤醒时相隔一小时甚至两三轮。此时 A 已可能做了新工作；如果依赖聊天记忆，旧任务审查可能丢失或误绑定。

### 5.2 统一唤醒协议（规范建议）

```text
WAKE
  00 鉴权并读取 POLICY / AGENT_ID / REPO / 当前真实时间
  01 Git HEAD / BOARD 投影 / 自己的 inbox / cursor
  02 检查上一任务：有效授权、未处理 Finding、返工、超时、移交
  03 处理已提交但未 ACK 的消息，修复游标；阻断事件优先
  04 如持有有效旧任务且未完成，则继续或申请合法续租
  05 否则筛选依赖满足、权限允许、未被合法占用的新 TASK
  06 提交 CLAIM_PROPOSED；必须等权威授权或只做 SOFT_CLAIM 安全工作
  07 按需加载 TASK 原件、当前 commit、相关 FACT/FAIL 和最小历史
  08 执行；产出版本化交付/测试证据/请求复核/新消息
  09 WRITE → REREAD → ACK；提交 HANDOFF 与短 RUN_REPORT
  10 到时退出；留下未完成状态和下轮入口
```

优先级建议：`安全/撤销/STOP` > `未处理高优先级消息` > `已有任务返工或到期租约` > `依赖解除的已领任务` > `新 READY`。更细的优先级与公平性必须由正式 POLICY 冻结。

### 5.3 消灭“第 N 轮 = 第 N 阶段”的错误推理

- `RUN_ID` 是一次唤醒；`TASK_ID` 是长期逻辑工作；`ATTEMPT_ID` 是某次修复尝试；`REVIEW_ID` 绑定一个具体 commit。
- 同一个 TASK 可以跨多次 RUN、多个 Agent、多个 ATTEMPT。第三轮发生的审核可能针对第一轮的 commit。
- 迟到的作者必须先核对最新状态；已被别人接管、旧 epoch 或已验收的旧任务不能继续更新权威状态。
- 交接包必须保留 `task_id + spec_hash + candidate_sha + unresolved_findings + last_decision + next_action + evidence_refs`。

## 6. GitHub 看板同时承担异步消息中心：可行，但必须有“收件箱协议”

### 6.1 对微软 Mattermost 的取舍

[微软原版] `microsoft/Agensh` 的 Gitea 是共享工作区，Mattermost 是消息接口，`mini-router` 是每 Agent 的常驻事件侧车，`board-service` 保存短 FACT/OBSERVED/FAIL/CLAIM/PATCH_SUMMARY；直接消息可触发在线 Agent 的当前回合，路由器负责持久化、ACK、去重、重试。

[本项目共识] ChatGPT 定时聊天通常休眠，普通 GitHub commit **不能直接唤醒它，也不能直接向普通聊天会话推送一个外部消息**。因此短期不必另建 Mattermost：以 Git 不可变消息、目标收件箱和下次定时醒来主动读取构成**可靠异步消息系统**。实时桥接仅是以后加速层。

### 6.2 不能只在一份大 Markdown 日志末尾追加自然语言

必须让每条消息拥有：

- 稳定 `event_id/message_id`、`project_id/task_id`、发送 Agent、目标 Agent 列表；
- `kind`（如 `REVIEW_REQUESTED`, `CHANGES_REQUESTED`, `FAIL_PUBLISHED`, `HANDOFF_READY`, `LEASE_GRANTED`）、优先级、发生时间；
- `payload_ref`、`source_commit_sha`、完整性 hash 和因果关联 `causation_id`；
- 每个收件人的 `SEEN / ACK / HANDLED` 回执及消费水位，去重键 `(event_id,target_agent)`；
- 超时、冲突和读取失败记录，必要时归入待恢复队列。

**消息提交成功 ≠ 已被目标 Agent 看见；看见 ≠ 完成处理；处理 ≠ 代码验收。** 这些必须分状态记录。聊天内“已通知”不作为 Git 收件证据。

### 6.3 状态示意

```text
创建消息 → GIT_COMMITTED → INBOX_VISIBLE
                            ↓
                  AGENT_SEEN → PROCESS_ACKED
                                   ↓
                     业务处理/评审/返工事件（另走业务状态机）
```

异常分支：`WRITE_UNKNOWN`, `DELIVERY_UNKNOWN`, `ACK_MISSING`, `EVENT_COLLISION`, `REPLAY_REQUIRED`。ACK 遗失时，应先独立回读再修复回执，不能直接重做有副作用的业务动作。

### 6.4 异步消息示例（建议模式，不是现有实现）

```json
{
  "schema_version":"1.0",
  "event_id":"EV-20261026-000123",
  "project_id":"AGL42",
  "task_id":"TASK-0017",
  "kind":"CHANGES_REQUESTED",
  "from_agent":"GPT-B",
  "target_agents":["GPT-A"],
  "producer_run_id":"RUN-GPTB-20261026T102000+0800",
  "candidate_commit_sha":"40hex-actual-git-commit-required",
  "payload_ref":"factory/tasks/TASK-0017/reviews/REVIEW-002.md",
  "payload_sha256":"sha256-of-canonical-payload",
  "causation_id":"EV-20261026-000090",
  "created_at_utc":"2026-10-26T02:20:00Z",
  "priority":"HIGH"
}
```

示例字符串是 Schema 占位，**不代表已真实提交的 SHA/事件**。

### 6.5 标准消息处理顺序

`读取 HEAD → 当前 inbox 索引 → 游标之后的新消息 → 筛选目标身份 → 验证消息文件与引用 → 与自己的历史 ACK 去重 → 处理或生成 BLOCKED → 写处理回执 → 独立回读 → 推进游标`。读不到 Git 必须标 `UNKNOWN`，不能将空响应判定为“无消息”。

### 6.6 “消息放哪儿”的结论

**不放在 Actions 的临时磁盘；也不只放在聊天上下文。** 推荐放 GitHub 的不可变事件和每 Agent 独立收件箱索引内。Actions 可充当路由器/校验器/重建器，但不是长期消息服务器；Controller 可按需生成 inbox 投影。未来若存在秒级协作需求，再单独评估 Mattermost/NATS/云队列，现阶段无强制必要。

## 7. Controller 与 Watchdog：一个小型符号控制系统，两组明确职责

### 7.1 它们不是什么

- **不是**独立于 Git 的第二套 AI 大脑；不负责长文本理解、需求正确性、代码语义或架构水平判断。
- **不是**一个大 Markdown 文件；Markdown 定义规则但不能自行执行排他锁。
- **不是**两个分别拥有独立状态与写入权的竞争性 Controller。不能出现两名 BOARD 主写者。
- **不是**为了全仓库“全文对齐”而每分钟读取全部代码与 Markdown 的扫描器。

### 7.2 模块建议

| 模块 | 主要职责 | 是否需要理解全文 |
|---|---|---|
| `event_ingest` | 比对 Git commit/tree，增量找到新事件；验证 event ID、路径、schema | 否；必要时读新事件结构化载荷 |
| `message_router` | 将定向事件计入目标 inbox，维护 per-agent cursor / ACK | 否 |
| `claim_grant` | 原子认领／事务状态／授权与 fencing（L1） | 否，但**必须有真实原子权威** |
| `state_machine` | 任务状态合法跳转、依赖 DAG、权限、版本约束 | 否 |
| `board_projector` | 从事件重建 `CURRENT.json` 和 `BOARD.md` | 否 |
| `watchdog` | 超时、重复事件、权限异常、空转、ACK 缺失、老版本误审、失联 | 否 |
| `audit_report` | 故障证据、重放记录、对账汇总 | 否 |
| `agent_qa`（外部） | 检查交付内容/代码实现/业务符合度 | **是；属于神经层，不放符号控制程序** |
| `test_runner`（外部） | 实际运行测试命令并出真实日志、退出码 | 运行代码，不靠摘要词语裁决 |

可用一个 Python 项目和统一 Schema 实现前七项；部署上用一条短进程、定时 Job 或常驻 API 皆可。**“Watchdog + Controller 合二为一”指代码与状态治理统一，不意味着每个非实时巡检必须永远占用一台 VM。**

### 7.3 Watchdog 的流量策略

先获取远端 HEAD / tree / paths / blob SHA；无变化直接结束。仅在新增事件、变更任务 metadata、提交新的审核结果时读取对应结构化记录。对于代码内容，Watchdog 只要核对：commit 存在、路径属于权限白名单、测试/审查指向同一 commit、evidence hash 和来源正确；不需要阅读源代码正文。真正需要语义审计时，创建 `REVIEW_REQUESTED` 交给 Agent。

**边界澄清**：检查 Git blob SHA 只证明对象或字节版本一致，不能证明测试真的运行；“PASS”字符串也不构成 QA 通过。若测试真实性是硬门禁，还需独立 Runner 提供可信的 test job ID、退出码、环境和同一提交关联。

## 8. 认领唯一性、Git 事务与 GitHub Actions 的硬限制

### 8.1 为什么仅靠看板会冲突

A、B 同时读到 `TASK-17 READY`，分别写一份 `CLAIM`；Git 允许两个 Agent 各自成功创建文件，而不意味着全局只能有一个胜者。GitHub Actions 收到提交事件也可能延迟调度。因此不能把“我已提交 CLAIM”视为“我有正式的共享状态写入权”。

### 8.2 三种可行层级（不应混用）

- **L0：纯 Git Soft Claim**。Agent 做静态分区工作、草案、独立评审。碰撞交由后续协议决定；无真正排他保障。
- **L1-A：短生命周期单写者 + Git 条件更新**。所有严格认领由同一逻辑单写入口处理，使用读当前 ref/期望版本、原子条件更新与写后回读；事件历史需足以重建授权与防迟到状态。必须验证在并发/重试/调度掉队下真的只有一个胜者。
- **L1-B：GCP 常驻服务 + 持久化事务状态**。对强时效共享操作提供串行事务、持久租约与授权 API；再向 Git 发表可验证结果。更直接但要运行 VM、管理持久磁盘与安全。

GitHub 的单一文件按 SHA 条件更新**不构成 TASK/CLAIM/GRANT/BOARD 多文件原子事务**；Actions `concurrency` 可以减少同组并行，但它也可能取消或替换排队中的运行，不能代替持久事件队列和事务日志。

### 8.3 认领协议建议

```text
READY 的任务 → Agent 写不可变 CLAIM_PROPOSED
   → Controller 校验版本/依赖/权限/冲突
   → 原子授予唯一 GRANT + fencing_epoch
   → 把 grant 发布为可回读的权威记录
   → Agent 读取并比对真实 grant 才开始共享写动作
   → 续约/超时/撤销全用新事件，不抹旧事件
```

迟到旧 Agent 的结果可以归档但不得覆盖新 epoch 的权威状态。**如果“原子发布且可回读的 grant”尚未被验收，必须标 `SOFT_CLAIM_ONLY`，不得在对外报告写“严格唯一认领已实现”。**

## 9. GitHub Actions：它能做什么、不能做什么

### 9.1 运行本质

GitHub Actions 是触发后启动临时 Runner、执行 YAML Workflow 中的脚本、结束即销毁的短生命周期计算环境。**可以运行 Python Controller 的事件验证、Watchdog、BOARD 重建和周期对账，不适合作为 `codebuddy --serve`、MCP/HTTP 常驻桥接的替身**。临时 Runner 上的本地 SQLite 文件不会自动保留到下一次运行，必须把权威状态放 Git 或持久事务系统。

### 9.2 公有与私有仓库边界

- **公开仓库**：代码、看板、任务和历史可能被全网读取和检索；陌生人通常不能直接 push，但可以 fork 和发 PR。公网可读不是“只有拿到网址的人才看得到”。标准 GitHub-hosted Runner 用于公开仓库可免费；收费 large runner 例外。
- **私有仓库**：标准 Runner 的免费分钟按 GitHub 仓库所有者账户的方案配额计；GitHub Free 讨论中采用 2,000 分钟/月，超出按具体 SKU 收费。
- 业务机密、Agent 内部指令、凭据、敏感交付不应因为省分钟就公开。可考虑**公开通用 Controller 源代码、私有任务/证据仓库**，但跨库触发/令牌权限/日志泄露仍需工程验证。

### 9.3 规格与费率（2026-10-26 官方案例，最终以 GitHub 账单 SKU 为准）

| 项目 | 标准公有 `ubuntu-latest` | 标准私有 `ubuntu-latest` |
|---|---|---|
| CPU | 4 vCPU | 2 vCPU |
| 内存 | 16 GiB | 8 GiB |
| 临时 SSD | 14 GB | 14 GB |
| 计算费 | 标准 Runner 免费 | GitHub Free 先扣账户含 2000 分钟/月（若该套餐） |
| 超额参考单价 | 不适用标准公有 Runner | Linux 2-core x64：$0.006/计费分钟 |
| 每 job 计费 | — | 不足一分钟按一分钟向上取整 |

[官方资料] https://docs.github.com/en/actions/reference/runners/github-hosted-runners  
[官方资料] https://docs.github.com/en/billing/concepts/product-billing/github-actions  
[官方资料] https://docs.github.com/en/billing/reference/actions-runner-pricing

官方文档还列出 `ubuntu-slim` 1 CPU / 5 GB / 14 GB、私有约 $0.002/分钟的不同计费 SKU（兼容性需测），本方案**不默认切换或承诺适配**。

### 9.4 调度与触发不可忽略的限制

- `schedule` 最短支持 5 分钟级 Cron，但高负载时可能延迟乃至遗漏，常见整点更拥挤；**不能当严格实时调度器**。
- `schedule` 工作流要求工作流定义存在于默认分支等触发条件；实验分支上的 YAML 文件不等于已经定时运行。
- Actions 自身使用默认 `GITHUB_TOKEN` 推送生成的普通 `push`，通常**不会再自动触发下一轮 `push` Workflow**；`workflow_dispatch`/`repository_dispatch` 是明确例外。不要设计无休止自动触发链，也不能误以为自动触发必定发生。
- Actions 的 `concurrency` 并不是持久可靠队列；被替换/漏执行后要靠 Git 账本扫描差集恢复。
- 真正由 GitHub App / 特定身份写入的事件能否触发目标 Workflow、令牌 scope 与私有库写权限，都必须实测。

[官方资料] https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow  
[官方资料] https://docs.github.com/en/actions/how-tos/troubleshoot-workflows

### 9.5 GitHub Action 费用不能机械按 Agent 数估算

**计费估算统一假设**：30 天、每个工作流只有一个标准 Linux 2-core job、每次 job 总执行时间不超过 1 分钟且按 1 分钟计费；GitHub Free 私有账户剩余足额 2000 分钟，其他 Workflows 不占配额，使用参考价 $0.006/分钟。**这些是假设，不是实测账单或本账号确认配额**。

| 触发组织方式 | 月 job 数 | 预估计费分钟 | 用完 2000 免费分钟后的参考增量 |
|---|---:|---:|---:|
| 每小时一轮集中巡检 | 720 | 720 | $0 |
| 每 20 分钟一轮集中巡检 | 2,160 | 2,160 | $0.96 |
| 每 10 分钟一轮集中巡检 | 4,320 | 4,320 | $13.92 |
| 每 5 分钟一轮集中巡检 | 8,640 | 8,640 | $39.84 |
| 55 个 Agent，每人每小时认领、交付、评审各独立触发一次 | 118,800 | 118,800 | $700.80 |

**重要区分**：最后一行是“每个细粒度事件都单独运行一个 job”的极端高频方案；不是 55 个 Agent 的固有成本，更不是推荐实施方案。若一个 job 运行超过一分钟或有多个并行 job，计算不同；此外事件还要考虑 API 限流、队列与实际延迟。

**当前成本优化建议**：将每次认领的排他裁决从“等待一个新 Actions 启动”中解耦；正常结构化写入留在 Git；对审查、状态投影和漏单差分采用事件触发可合并处理 + 10/20/60 分钟兜底。真正即时授租需 L1 权威事务，不能靠调低 Actions Cron 周期假装得到。

## 10. GCP、Oracle、第二台 GCP：讨论过的部署备选

### 10.1 用户现有路线 A：GCP US e2-micro 云端桥接

用户提出的组件：`codebuddy --serve :8080`、FastAPI `:8787`、MCP Server、GitHub 共享看板、Secret Manager、SSH Deploy Key、静态 IP、2 GB swap；云端电脑关机也能工作。**这些是规划中的能力清单，不能因为文档列出就认定服务已经部署或双向调用已验收。**

本轮得出的判断：Watchdog/结构化 Git 核验本身占用内存和流量很低，瓶颈是 CodeBuddy 的进程峰值、Node/MCP、桥接调用及 CPU。e2-micro 1 GB RAM 适合低负载试验，完整桥接应先做驻留和并发压测。`swap` 不是物理 RAM。对模型执行侧的复杂任务应优先使用原平台云端 Runner，不压在 1 GB VM 上。

### 10.2 出入流量

讨论中的 Google Cloud e2-micro Always Free 通常附带每月约 1 GB 的合格公网出站网络额度（按官方区域和流量类别具体约束核对），**不是 Controller“只能处理 1 GB Git 文本”的意思**。入站/出站、Google 服务间区域传输和外部 IPv4 费用另行区分。仅凭 1GB 数字不能精确预测账单；应实际采样 Git HEAD 查询、事件增量、重试与完整拉取的字节数。Watchdog 使用路径/SHA 增量判断，通常大幅小于代码库全文重拉。

### 10.3 Oracle A1 Always Free

讨论过使用 Oracle ARM 资源承载更重的 CodeBuddy/MCP 桥接，GCP 留轻量治理。优点是潜在更高 RAM；风险是免费实例库存、开户资格、回收策略、ARM 包依赖和服务账号登录。**Oracle 实例尚未确认申请成功，不能作为上线的前置条件**。此前对 Oracle 免费 CPU/RAM 的数字在聊天中有不同时间口径，不在本文件冻结为保证数值，必须以注册时官方报价和控制台为准。

### 10.4 第二个 Google 登录账号申请另一台免费 e2-micro

用户提出通过另一 Google 账号增加机器。讨论结论：另一 Gmail **不自动意味着额外一份免费配额**，须核对独立 Cloud Billing 账户和 Google 新用户／Always Free 资格，不建议为了获取优惠规避资格规则。两台 1 GB VM 可以物理隔离“治理”和“CodeBuddy 桥接”，但不能解决单个超过 1 GB 的进程内存需求。双机需要额外运维、身份与故障隔离设计。

### 10.5 本阶段部署未定事项

- **纯符号治理**（短任务、分钟级巡检）优先试 GitHub Actions。
- **CodeBuddy 实时 API/MCP 服务**仍可能需要 VM 或其他长期在线运行环境；Actions 不能替代。
- **强排他、低延迟授租**若 Git-only 方案经并发验收失败，则选 GCP 小型在线 Controller；不能以“免费”牺牲唯一性。
- 不让未拿到的 Oracle 免费资源延迟 GitHub MVP 的开发。

## 11. 安全与权限：运行时身份、公开代码和任务数据严格分离

1. GitHub 公开仓库任何人可读取与 fork，**陌生人没有当然的原仓库 push 权限**；但公开后敏感任务可能被搜索和复制，删除不能保证互联网副本消失。
2. `multi-agent-board` 私有仓库是讨论中的拟议项目；当前已有开发资产在 `kaibahaha/xxsc`。不得在没核对仓库和分支时假定迁移完成。
3. Agent 不应共用全仓写入凭据作为默认最安全方案。可由 Controller 集中受控写，或者为受控 agent 独立分配权限及写路径。授权成功与“真实是同一个人在操作”不同，角色身份也须写入事件。
4. 不将凭据写入 Git、日志、工件、沙盒 tarball；GCP Secret Manager 是一个可选托管方案，VM 服务账号用最小 IAM；不能把 `--auth none` 的 CodeBuddy 外网服务长期公开。
5. GitHub Actions 需要 `permissions` 最小化、限制仓库事件来源和未可信 PR 的令牌权限；公共 Runner 的事件触发不能执行未可信 fork 提供的高权限代码。
6. 平台安全拒绝后不能更换工具路径绕过；记录 BLOCKED 并在授权后恢复。

## 12. 审查、返工与消息协调的联合流程

**已记录于 V1.0 的 QA 机制**：微软原版自主开发和自检、PR 合并；我们增加风险分级独立 QA。这里补充跨轮异步会话中的协调状态。

```text
TASK_READY → CLAIM_PROPOSED → [GRANT/安全分区]
  → AUTHOR_WORKING → AUTHOR_SELF_TESTED → DELIVERY_COMMITTED
  → REVIEW_REQUESTED（发定向消息）→ REVIEWER_WORKING
  ├─ APPROVED(绑定 candidate_sha) → INTEGRATION/ACCEPTED
  └─ CHANGES_REQUESTED(绑定 finding_id + sha)
          → AUTHOR_INBOX_PENDING
          → 作者下次醒来处理返工/或合法移交替代作者
          → ATTEMPT+1 / NEW_COMMIT / NEW_EVIDENCE
          → NEW_REVIEW_REQUESTED（旧 review 不自动通过）
```

- **审查者不一定必须是固定专职 Agent**。可由下一位符合权限且独立的 Agent 抽取 QA 工作；但关键任务须按风险门禁，不能作者自行签发独立合格。
- **返工优先于任意新任务**要服从截止、租约与阻断规则，不允许让同一作者在两个权威 lease 上并行乱写。
- **证据同步**：作者交付 commit 变更后，旧审核只针对旧版本；不可用 `APPROVED` 自由文字覆盖不同 SHA。
- **重复评审应增量化**：同一 finding 已修复的变更 diff + 必要回归；最多两三轮失败按既有 V1.0 升级，不无限相互驳回。
- **可替代作者**：原作者失联或长期受限，合法接管由新 epoch/grant 确认；旧成果保存而非删除。

## 13. 建议的 Git Markdown 文件群（在现有 V4.1 路径上增量补充）

```text
projects/<PROJECT_ID>/
  00_policy/
    POLICY.md                   # 权限、角色、WIP、风险和仲裁规则
    CONTROLLER_CONTRACT.md      # 控制器原子性、执行模式与失败规则
  01_tasks/<TASK_ID>/
    TASK.md                     # 任务正文：需求与验收标准
    attempts/<ATTEMPT_ID>/DELIVERY.md
    reviews/<REVIEW_ID>.md
    findings/<FINDING_ID>.md
  02_claims/<TASK_ID>/<EVENT_ID>.json
  03_events/<YYYYMMDD>/<EVENT_ID>.json
  04_notes/<TYPE>/<EVENT_ID>.json
  05_outbox/<AGENT_ID>/<RUN_ID>/
    HANDOFF.md
    RUN_REPORT.md
  06_evidence/<TASK_ID>/<RUN_ID>/
  07_receipts/<TARGET>/<EVENT_ID>.json
  08_projections/
    BOARD.md
    CURRENT.json
    INBOX/<AGENT_ID>.json       # 按目标生成的未读/待处理索引
  09_runs/<AGENT_ID>/<RUN_ID>.md
  10_archive/
  11_controller/
    REPLAY_CHECKPOINT.json      # 仅作可重建快照；不冒充事务锁
    WATCHDOG_AUDIT.md
    COST_METRICS.jsonl
```

**约束**：上述为兼容 V4.1 的增量候选布局，文件名和 Schema **尚未合并冻结**，不得擅自把所有历史数据从既有目录搬迁。`08_projections` 单写、原始事件 append-only；每个 Agent 的 inbox 是索引，不是唯一消息存储。不要给每个 Agent 一份互相覆盖的根 `BOARD.md`。

## 14. 统一运行日志摘要与落地纪律

### 14.1 任务唤醒侧的短反馈模板

```text
RUN_ID: RUN-...
AGENT_ID: GPT-A
BOARD_HEAD: <observed SHA or UNKNOWN>
INBOX: received=3, handled=2, blocked=1
TASK: TASK-0017 / ATTEMPT-0003
RESULT: DELIVERY_COMMITTED | BLOCKED | NO_ELIGIBLE_TASK
DELIVERY_REF: repo@commit:path
READBACK: VERIFIED | UNKNOWN | FAILED
NEXT: <next event/issue pointer>
```

Agent 在 ChatGPT 定时聊天中只需输出这些短字段及少量人类可读结论；真实代码、审计步骤、测试输出、完整 findings 与事件原件都在 Git。

### 14.2 何为已送达/已成功

| 声明 | 最低证据 | 不可混淆 |
|---|---|---|
| “我写入 Git 了” | 真实 commit + 同分支回读 + blob/hash | API 请求发出不等于成功 |
| “我已发消息给 B” | 目标 inbox 可见、有 event_id/commit | B 尚不一定看到 |
| “B 已读” | `SEEN` 回执 | 不代表 B 已执行 |
| “B 已处理” | `PROCESSED_ACK` + 业务事件引用 | 不代表 QA 通过 |
| “代码通过 QA” | 真实测试+独立审核针对同一 SHA 的证据 | 不可用作者自报 PASS 替代 |
| “任务正式 DONE” | 完整状态链 + 被授权集成/验收 | 交付不等于合并上线 |

### 14.3 平台失败时

- Git 读失败：`BOARD_UNKNOWN`；不能假装 `EMPTY`。
- 写入超时：先同分支回读，再根据 event ID 和 hash 决定补 ACK 还是重试。
- Actions 漏触发：下一轮从上次 checkpoint 到当前 HEAD 做未处理事件差集；消息不能依赖“通知一定发送到聊天窗口”。
- Python Controller 宕机：历史可重放，单写授权必须先查清是否已提交，避免双写。
- 作者/审查者失联：新增接管/阻断事件，保留所有过往尝试。

## 15. R01 当前证据、未验收事项与推进 R02 的现实约束

### 15.1 仓库/PR 观察（2026-10-26 本轮连接器只读核对）

| 内容 | 核验结果 | 解释 |
|---|---|---|
| GitHub 原仓库 | `kaibahaha/xxsc` | 已可读取；并非已部署完整在线工厂 |
| R01 冻结基线 | `exp/agensh-lite-v4.2-controller-mvp-20261025` @ `2d4c1a6fc0792a1182777262b41bfb4c09c0b5d2` | 既有架构/模板基线，禁止当成已合并运行程序 |
| Codex PR #1 | `dev/agl-v4.2-codex-controller` @ `5f9afb8b9a90f95a79ade47bd6ed5734711ff72d` | Draft、open、未合并；Controller/lease/state 方向 |
| WorkBuddy PR #2 | `dev/agl-v4.2-workbuddy-adapters` @ `260e596f3e8cff772a7d3de58e3527685e949721` | Draft、open、未合并；Git storage/poll/CLI/bridge 方向 |
| 治理规范 V1.0 | 已独立归档到 Library、GitHub 文档分支 | 草案，尚未冻结 V1.1 |

以前阶段有 Codex 116/116 以及 WorkBuddy 115 通过、2 项受限跳过等报告陈述；**本归档没有在完整集成环境重新运行这些测试**，不得由“单 PR 测试通过”推断跨模块生产可用。

### 15.2 下一轮集成不可跳过的问题

1. Codex 与 WorkBuddy Python import/package/CLI/API 契约统一，不能出现 `factory.agl` 与 `agl` 混用导致运行失败。
2. 单一权威授租：原先本地 SQLite 的锁不能自然扩大为云上所有 Agent 共享排他；需要持久状态和受控发布的实际并发测试。
3. GitHub 结构化事件与 Agent inbox 游标真正打通，不能只把 Markdown 模板写好。
4. `BOARD` 投影从事件可确定性重建，并可在 Actions/GCP 重启后复原。
5. GitHub Actions 权限、默认分支 workflow、私有/公开数据隔离经过真实试跑；从聊天说“可用”不等于定时环境拿到了同样连接权限。
6. CodeBuddy Bridge 是独立产品能力，不能因为 Actions 已经跑 Watchdog 就宣称 ChatGPT/Codex 双向模型调用完成。
7. QA 不接受作者自评充当独立门禁；不能用测试文本 PASS 自动判定。

## 16. 可直接转成 R02 工单的验收矩阵（新增）

| ID | 场景/故障注入 | 必须观察到的结果 | 优先级 |
|---|---|---|---|
| T01 | A、B 同时读同一个 READY 并申请 | 严格 L1 模式只有一个有效 GRANT；L0 明确拒绝共享写 | P0 |
| T02 | 同一 `event_id` 向同一收件人重放 100 次 | 只产生一次业务处理效果，回执可恢复 | P0 |
| T03 | ChatGPT 每小时醒一次，其他 Agent 20 分钟错峰审查 | A 下轮优先发现旧任务的 Finding，不依赖上一轮聊天记忆 | P0 |
| T04 | A 新领任务后，旧任务审查延后两轮到达 | 无遗失、无错误覆盖；返工有独立索引与优先级 | P0 |
| T05 | Review APPROVED 后候选 commit 变化 | 旧审批对新 commit 自动失效 | P0 |
| T06 | Git push 成功但客户端超时 | 回读确认后补 ACK，不重复发布业务事件 | P0 |
| T07 | 控制器 Actions 工作流漏触发一次 | 下次通过事件差集找回未处理消息 | P0 |
| T08 | Actions 并发两次重建 BOARD | 最终只有一个合法投影版本，历史不丢 | P0 |
| T09 | Agent 未读消息积压 200 条 | 保留全部事件；按目标和优先级索引，不丢旧消息 | P1 |
| T10 | Fencing 授权过期后旧 Agent 迟到交付 | 迟到候选可存证，不得推进当前权威状态 | P0 |
| T11 | Git HEAD 未变化重复巡检 100 次 | 不下载全文、不生成无意义 BOARD 提交、无多余 AI 调用 | P1 |
| T12 | 任务/引用路径存在但内容 SHA 不匹配 | 阻断授权/状态提升并给出可追溯错误 | P0 |
| T13 | 作者自报测试 PASS，但无真实运行证据 | 不进入 QA_GREEN | P0 |
| T14 | 真实测试失败、评审者提交 FAIL | 指定旧候选失效或重验；创建定向返工消息 | P0 |
| T15 | 相同 Finding 连续两轮未修复 | 自动升级/换审查策略，不无限复读 | P1 |
| T16 | repo/API 被拒绝权限 | 限定停写，保留源和日志，不用新工具绕安全检查 | P0 |
| T17 | ChatGPT 5 工位与 WorkBuddy 多工位长时间错峰 | 实测任务遗漏率、等待 P95、重复率；不以计划时间当实际执行 | P1 |
| T18 | public Controller repo + private 业务数据 | 无凭据/任务敏感信息渗入 public Actions 日志或 artifact | P0 |
| T19 | VM 关闭 / Oracle 不可用 | Git 异步 Agent 在安全 L0 范围继续；需要在线桥接的事项显式 BLOCKED | P1 |
| T20 | 24h / 72h 连续运行与自动恢复 | 事件、TASK、ACK、BOARD、QA 计数可逐笔对账；有总成本统计 | P2 |

## 17. 优先级、未决问题与不得伪称的结论

### 17.1 已有共同方向（适合作为 V4.3 候选约束）

- 短定时上下文、Git 完整持久事实、每轮恢复自身 HANDOFF。
- 用户任务与 Agent 消息同一 Git 协作体系，但业务状态与消息送达状态分开。
- Watchdog 不读全部内容、不做语义审查；Agent+测试 Runner 审查真正的代码质量。
- Controller 与 Watchdog 逻辑同一 Python 项目；全局最终任务状态只有一个权威投影写者。
- 认领不靠时间错峰保证无冲突；真正的排他动作必须有可信原子授租，软认领明确标注。
- Lite-M+ 先上线可验证最小闭环；深度模型路由和复杂可观测平台留以后。

### 17.2 仍未冻结，需要选择/测量

| 开放问题 | 原因 | 决策建议/验证方式 |
|---|---|---|
| O01 Controller 到底全部放 Actions 还是关键授权放 GCP？ | Actions 非实时且非持久交易服务 | 先 T01/T07/T08 冲突、漏触发测试，再按要求决定是否保留 GCP 服务 |
| O02 是否需要秒级消息？ | 当前定时 ChatGPT 无需秒级唤醒 | 先 Git inbox；只有明确时延 SLA 再考虑实时消息总线 |
| O03 私有仓库还是公私隔离？ | 免费分钟 vs 商业任务机密 | 优先私有试运行，测量真实成本；不得为省钱公开敏感事实 |
| O04 Agent 数量/排班真实情况 | 聊天提到 3 个 20min、5 个 Agent、WorkBuddy 50 个 | 读取调度系统真实 enabled 配置后冻结角色表 |
| O05 GCP e2-micro 是否留桥接？ | Bridge/MCP/CodeBuddy 不适合 Actions 常驻 | 单独做 CodeBuddy 内存和真实 API 权限压测 |
| O06 Oracle/第二台 GCP 是否必要？ | 免费配额资格和安装不确定 | 不能阻塞 Git MVP；真实需求出现后采购/申请 |
| O07 两个 R01 PR 如何合并？ | 接口、事务权威、测试仍未验证 | R02 提交兼容契约 + 并发回归矩阵 + 单主集成 PR |
| O08 哪些审查强制由不同模型完成？ | 成本与质量需要经验数据 | 沿用 V1.0 风险分层，24h shadow 记录证据 |
| O09 自动反馈最佳实践能否跨所有新会话持久生效？ | 对话中的口头承诺不保证账户配置 | 在个人化设置中明确定义偏好并核对，不把一轮语音答复视为永久系统规则 |

### 17.3 纠偏与防误读（必须保留）

1. **微软 Agensh 并不是“人人每单必须第三方复审”**；官方实验允许 PR 无强制审批。本项目分级 QA 是我们增加的规范。
2. **微软并没有统一的强制 Controller 审批每次 CLAIM**；原版 CLAIM 是软声明、同伴协调，事件路由和数据库是基础设施机制。
3. **我们的 Controller 不是 BOARD.md**；它是实施结构化协议的 Python 引擎，BOARD 只是投影。
4. **“GitHub Actions 能运行 Python”不等于“GitHub 托管了常驻服务”**；MCP/CodeBuddy 在线桥接仍需其他环境。
5. **GitHub 上收到 push/event 不等于原生定时 ChatGPT 立即醒来**；后者要在下次真实调度窗口主动查收。
6. **成功发表 Git 消息不等于收件人已经处理**；严格区分 `COMMITTED`, `SEEN`, `PROCESSED`, `ACCEPTED`。
7. **Git 事件追加可以审计，但不等于不可篡改的物理保证**；有仓库管理员/强推权限者仍可改历史，应依赖权限、分支保护、签名/审计及外部留痕降低风险。
8. **GitHub Actions 单文件 SHA 写入不保证多文件事务，Actions concurrency 也不保证每笔事件都排队处理**。
9. **55 个 Agent ≠ 必然月费 $700**；这只是每 Agent 三事件各启一 Job、1 分钟/Job 的特定压力假设。
10. **曾有“以后每次都自动优化建议”口头答复**，但不能凭此断言已经创建永久跨会话记忆或所有未来会话都自动遵循；实际全局偏好应由支持的个人化设置/记忆机制确认。
11. **“高级语音和普通语音”曾被误解为高级与低级编程语言**；本项目归档只把它作为问答澄清失败案例，不把编程语言回答写入架构事实。语音档位与答案质量的关系另行核验，不在本文件做技术结论。
12. **当前 GitHub Draft PR ≠ 已部署生产系统**；不能据此宣称 24h 稳定、原子租约或双向模型调用已完成。

## 18. 建议的下一步任务分解（仅建议，尚未向 Agent 正式派单）

| 批次 | 责任建议 | 输出 | 审核重点 |
|---|---|---|---|
| R02-A 协议冻结 | Codex 主导，WorkBuddy 反审 | `EVENT_SCHEMA`, `INBOX_ACK_PROTOCOL`, `LEASE_CONTRACT`, `STATE_MACHINE` | 两阶段回执、L0/L1 认领、不可变版本关联 |
| R02-B Runner 集成 | WorkBuddy 主导，Codex 反审 | Git adapter / inbox cursor / board build / Python CLI | Git read-write-reread、API 权限、幂等 |
| R02-C Actions 探针 | 小组定时/CI | workflow + 测得每次耗时、漏触发、恢复数据 | 费用、延迟、GITHUB_TOKEN 不触发链 |
| R02-D 审核闭环 | ChatGPT/Codex/Buddy 交叉 | 作者交付→审核→返工→新版本→再审 | SHA 绑定、旧 Finding、水位恢复 |
| R03 24h 小规模影子 | 3–5 个 ChatGPT + 少量 Buddy | 逐笔事件账本和复盘报告 | 真实唤醒率、重复率、上下文恢复 |
| R04 扩到多 Agent | 按实际 WorkBuddy 配额 | 多分区并发和负载指标 | 并发安全、成本、积压 |

**治理动作**：将本文件视为“增量决策纪要”，与《协作质量与迭代治理规范 V1.0》共同供 Codex/WorkBuddy 评审；经过独立评审和失败注入后才发布冻结协议。不得未经批准修改现有定时任务、GCP VM、GitHub 主分支或自动合并 Draft PR。

## 19. 附：本轮外部来源和现有项目文件索引

### 19.1 微软官方原版（用于确定“微软如何做”，不等于我们已经实现）

- 原始仓库：`https://github.com/microsoft/Agensh`
- 研究论文：`https://arxiv.org/abs/2609.26781`
- 复现与约束：`https://github.com/microsoft/Agensh/blob/main/REPRODUCE.md`
- Agent 原生工作循环：`https://github.com/microsoft/Agensh/blob/main/prompts/agents.txt`
- Board-service 源码与规则：`https://github.com/microsoft/Agensh/tree/main/board-service`
- mini-router 事件路由器：`https://github.com/microsoft/Agensh/tree/main/mini-router`

### 19.2 GitHub Actions 官方约束与费用

- Runner 规格：`https://docs.github.com/en/actions/reference/runners/github-hosted-runners`
- 计费逻辑：`https://docs.github.com/en/billing/concepts/product-billing/github-actions`
- 逐分钟定价：`https://docs.github.com/en/billing/reference/actions-runner-pricing`
- 触发规则与令牌：`https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow`
- 计划任务遗漏/延迟：`https://docs.github.com/en/actions/how-tos/troubleshoot-workflows`

### 19.3 项目文件（与本次增量归档的关系）

- `Agensh_Lite_协作质量与迭代治理规范_V1.0.md`：研究与 QA 治理基线（已有，**不覆盖**）。
- `frameworks/agensh-lite-v4.1/01_ARCHITECTURE_AND_AUTHORITY.md`：状态权威及角色矩阵（已有）。
- `frameworks/agensh-lite-v4.1/02_GITHUB_LAYOUT_AND_WRITES.md`：目录、不可变事件及回读（已有）。
- `frameworks/agensh-lite-v4.1/03_TASK_CLAIMS_AND_LEASES.md`：L0 软 CLAIM、L1 正式 grant（已有）。
- `frameworks/agensh-lite-v4.1/04_UEM_EVENTS_AND_DELIVERY.md`：消息字段、per-agent ACK、游标（已有）。
- `frameworks/agensh-lite-v4.1/05_SHARED_MEMORY_AND_CONTEXT.md`：HOT/WARM/COLD 与 UNKNOWN/EMPTY（已有）。
- `frameworks/agensh-lite-v4.1/06_LIFECYCLE_AND_HANDOFF.md`：唤醒、继续旧任务、交接（已有）。
- `frameworks/agensh-lite-v4.1/07_QA_GATES_AND_PROVENANCE.md`：事实等级与独立 QA（已有）。
- `frameworks/agensh-lite-v4.1/08_FAILURE_SCENARIOS.md`：故障情境和恢复（已有）。
- `frameworks/agensh-lite-v4.2/docs/CLOUD_CONTROLLER.md`：既有 V4.2 云 Controller 设计（草案）。
- 本文件：**截图锚点之后增量对话达成的部署／协作决策、候选、反例和明确技术边界的集中归档**。

---

### 归档总结（一句话）

> **我们的无人软件工厂应采用“GitHub 永久任务/事件事实 + 短上下文定时 Agent 自治 + 异步 inbox/ACK + 一个可信符号控制层 + 独立语义 QA”的 Lite-M+ 架构；是否让全部符号控制运行在 GitHub Actions，取决于并发授权和漏触发恢复的真实验收，而不是取决于 Actions 的免费分钟是否够用。**

*文档性质：决策纪要与候选规范，非自动生效的生产指令。*