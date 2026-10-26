# Agensh-Lite V4.2｜R01 后全量共识、架构决策与待落地事项归档 V1.0

> **文件类型**：阶段性决策纪要 / ADR 索引 / 下一版本实施输入（Markdown）  
> **整理日期**：2026-10-26（北京时间）  
> **讨论起点**：截图所示对话《Agensh-Lite V4.2：距离真正运行，还需要几个回合？》，其内容涉及核对 Codex PR #1、WorkBuddy PR #2 及剩余交付轮次。  
> **覆盖范围**：以该节点为锚点，覆盖之后关于 Lite-M/Lite-M+/Lite-P、Markdown 管理、微软 Agensh、独立审查、上下文、错峰定时、消息协作、Controller/Watchdog、GCP/Oracle/双 GCP、GitHub Actions、容量与费用、运行与验收等讨论。  
> **归档状态**：讨论共识已整理；不是已部署声明，不自动取代既有 V1.0 治理规范或冻结基线。  
> **证据等级**：`已核验` = 本次读取 GitHub / 已归档文档 / 官方资料；`讨论共识` = 用户与助手达成的目标和原则；`建议未冻结` = 可行方案但尚未做实施选择；`待实测` = 缺少运行证据。  
> **项目仓库**：`kaibahaha/xxsc`；微软原版：`microsoft/Agensh`。  
> **保密提醒**：本文件不收录密钥、令牌或账号秘密；公开仓库内不得存内部任务明文或私有凭据。

---

## 0. 执行摘要：最重要的 14 条结论

1. **长期方向是“无状态 Agent + Git 外部记忆 + 确定性符号控制 + Agent 语义判断”**，而不是让一个定时会话连续积累所有历史。
2. **各 Agent 自带平台级唤醒计划**；ChatGPT 定时任务错峰接续（例如每约 20 分钟有一个 Agent 醒来、同一身份约每小时醒一次），WorkBuddy 可以配置更多定时 Agent；调度触发时间与任务生命周期必须解耦。
3. **聊天/定时任务上下文只保留简短状态摘要**（这轮做了什么、下一步是什么、指向 Git 的 ID/路径/commit），详细代码、审查、修复和证据归 Git。上下文不能依赖三四轮之前的聊天记忆。
4. **GitHub 是协作事实源，不只是“一个巨型 BOARD.md”**。BOARD 是索引/派生视图；不可变事件、任务原文、交付 commit、review、findings、ACK、返工轨迹是可追溯事实。需要通过回读和版本哈希证明落库，而不是“写了就当送达”。
5. **不需要为当前非实时协作另建常驻 Mattermost 消息服务器**；可以在 Git 中增设结构化的异步消息、收件箱、ACK、重试与超时规则，并让 Agent 每轮启动先读取未处理消息。该选择是“满足现阶段”，不等于具备微软式秒级实时推送。
6. **Watchdog 是纯符号/确定性校验模块**：ID、唯一性、身份、路径、Git SHA、Schema、状态转换、权限、认领冲突、租约、重复消息、审查绑定、回读、超时、BOARD 重建。它**不评价正文含义、不推断代码正确性、不替 Agent 做内容审核**。
7. **Mini Controller 包含 Watchdog，但不等于 BOARD.md**：它还负责授租/冲突裁决、事件消费/去重、状态机、失败恢复和必要时的索引重建。一套轻量 Python 系统即可，逻辑模块分开，不必两个重量级常驻系统。
8. **严格独占认领不能仅靠 Markdown“我认领了”解决**。若暂时无可验证的序列化授租权威，就明确标注 `SOFT_CLAIM`，采用静态分区与碰撞检测；不得宣称“已实现强原子认领”。
9. **作者自检 ≠ 独立验收**。微软原版要求自测、PR 冲突后复验，但官方复现允许零必需审批；我们的增强是按风险级别引入独立 Agent 评审、可复现测试、提交 SHA 绑定及返工上限。
10. **返工与审查是基于任务和候选版本，而不是醒来轮次**。审查晚几个小时到达并不必然导致上下文丢失；返工以独立队列/消息推回原作者或接管 Agent，保留原证据，新修复产生新 attempt、commit、审核结果。
11. **微软原版是去中心化协作 + 常驻共享服务**：Gitea、Mattermost、board-service、mini-router、MySQL；并非每次 CLAIM 都由中央 Controller 审批，也没有统一 15/20 分钟轮询标准。我们借鉴其协议与事件机制，不照搬整套重设施。
12. **执行位置有候选方案，但尚未最终冻结**：原拟 GCP e2-micro 运行桥接及 Mini Controller；又研究双 GCP、Oracle A1、GitHub Actions。对于轻量 Python Watchdog，Actions 可运行；但严格低延迟授租可能需要在线权威或经过实证的 Git CAS 协议，Actions 的异步事件启动本身不提供瞬时互斥。
13. **GitHub Actions 费用取决于“工作流运行次数 × 每次计费时长”，不是 Git 文字内容大小**。对 55 Agent 高密度事件一律逐条启动 Job 可能代价很高，优先做事件聚合、幂等批处理与低频兜底；不要为省钱直接公开内部工作仓库。
14. **R01 仍是候选代码，不是已上线工厂**。截至本次回读，Codex PR #1 与 WorkBuddy PR #2 都是 open/draft/unmerged；下一步先落实 Lite-M+ 最小可运行闭环和故障验收，再决定是否推进完整 Lite-P 的 R03–R05。

---

## 1. 起点、已归档文档与本次新增范围

### 1.1 截图锚点

截图显示一段关于“接下来的 Agent 需要再干几个回合才能把系统搭起来”的讨论，以及助手回答标题 **《Agensh-Lite V4.2：距离真正运行，还需要几个回合？》**，其中已核对 **Codex PR #1** 和 **WorkBuddy PR #2**。截图没有展示整条回答的全部正文；本归档将它当作时间与主题锚点，而非假定屏外内容已全部可见。

### 1.2 原先的完整开发轮次设想

| 原先轮次 | 工作目标 | 现阶段判断 |
|---|---|---|
| R01 | Codex 实现 Controller / Lease / 状态与回放基础；WorkBuddy 实现 GitHub Adapter / Poll / Executor / CLI | **已有两个独立 draft PR；不等于集成运行** |
| R02 | Core 与 Adapter 统一接口、目录、错误和交付契约 | **应优先执行** |
| R03 | 云端 Controller、权限及可靠写回 | 视 Lite-M+ 的最小功能是否已满足而精简 |
| R04 | 多模型异构扩缩容、故障/恢复 | 必要基础先验收，动态路由可推迟 |
| R05 | 至少 24 小时真实无人值守影子运行 | 在基础链路完成后执行，不能用设计文档代替 |

原先估算 Codex 还需 2–3 轮、WorkBuddy 3–4 轮是**当时的开发规划估算**，不是客观的剩余工时承诺。随后讨论转向“先把 Lite-M+ 跑通”，不必等全部深度版开发完成。

### 1.3 已单独形成的 Markdown（本纪要不重复取代）

《**Agensh-Lite 协作质量与迭代治理规范 V1.0**》已经双处保存，149 行：

- ChatGPT Library：`/全自动工厂实践/Agensh_Lite_协作质量与迭代治理规范_V1.0.md`。
- GitHub：`kaibahaha/xxsc`，分支 `docs/agl-v4.2-quality-governance-20261026`，路径 `frameworks/agensh-lite-v4.2/docs/QUALITY_AND_ITERATION_GOVERNANCE_V1.0.md`，当时提交 `258f351`。
- 内容已包括：微软原版证据、符号/神经分层、分级审核、审查绑定 commit、返工、基础状态机、必要字段和验收场景。
- 当前性质：**研究草案，待 Codex 与 WorkBuddy 独立评审后发布冻结 V1.1**。

**本文件专门归档后续大量尚未系统写成 Markdown 的“运营协议、上下文治理、消息、定时、云端部署/成本、Actions 替代、接口边界、风险和实施决策变化”。**

---

## 2. 从截图之后的讨论脉络（按主题出现顺序重构）

> 以下为主题级时序，不是假造精确到分钟的逐字会话转录。涉及未实测方案，保留原讨论的条件句。

| 序号 | 讨论问题 | 已达成的共识 / 结果 | 状态 |
|---|---|---|---|
| 01 | R01 之后还要几轮才能真运行 | 原拟 R02–R05；先集成验证再谈运行 | 共识 |
| 02 | 已验证的 ChatGPT 定时任务可直接读写 Git，是否还要大量程序 | 强化 Markdown 即程序；保留纯 Markdown 启动方式，不为简单文本工作部署重系统 | 共识 |
| 03 | 微软源码/工程思想与自己系统对照 | 不能把“借鉴微软”说成“全部已复刻”；按行为契约对应 CLAIM、失败共享、事件路由、恢复 | 共识 |
| 04 | 三种实施形态 | Lite-M（纯看板）、Lite-M+（看板 + Mini Controller）、Lite-P（完整深度平台） | 已形成方案 |
| 05 | 哪些事 Markdown 不易维护 | 并发认领、状态机、事件去重、游标、超时接管、重建索引、授权不可由自由文本可靠执行 | 共识 |
| 06 | Mini Controller 放哪儿 | 初议 GCP e2-micro；桥接与控制分工，常驻仅做轻量确定性管理 | 建议未冻结 |
| 07 | 用户提供 GCP 纯云端桥接架构 | GCP 还要承载 CodeBuddy `--serve`、FastAPI、MCP、Git 与 Secret Manager；不能把其负载只当 Watchdog | 共识 |
| 08 | 1 GB 是否要扩容 | Watchdog 本身很省，CodeBuddy + Bridge 常驻是主要不确定性；先测，过载再升级 | 待实测 |
| 09 | 申请 Oracle 免费 ARM | 可作为较大内存桥接备选；但开通、空闲回收、ARM 兼容、额度/库存不确定，不能阻塞主计划 | 条件备选 |
| 10 | 第二个 Google 账号再申请一台 e2-micro | 双机器可分离控制与桥接，但每台仍只 1 GB；免费资格按结算规则，不等于两个 Gmail 必然两份额度 | 条件备选 |
| 11 | Git 同步数据量和 1 GB GCP 出口 | Markdown、编号、hash、状态均为小文本；按增量索引/HEAD/SHA 检查，正常不需每轮读所有正文 | 共识 |
| 12 | Watchdog 是审内容还是元数据 | Watchdog 只做规则、记录、证据引用和版本一致性；Agent 负责真正代码审查 | 强共识 |
| 13 | 微软是否也这么划分 | 微软 board-service 用确定性校验、mini-router 处理事件；Agent 自己验证代码。我们严格的 QA 门禁是增强，不是原样照搬 | 已核查 |
| 14 | Agent 自审有何价值，是否需要第三方 | 作者自测是必要非充分；按任务风险安排不同 Agent 独立复核，结果带证据 | 已写 V1.0 |
| 15 | 评审发现问题，回原作者再改，会不会无限返工 | 用 attempt/finding/版本与有限重试管理；两轮同类失败升级，避免互相无限驳回 | 已写 V1.0，运营细节见本档 |
| 16 | 微软第三方评审是否强制 | 不是所有 PR 强制经第三方批准；共享发现、复验及自发协同机制存在 | 已核查 |
| 17 | 把质量治理研究形成 Markdown | 已产生 V1.0 并双存 Library/GitHub，未并入冻结分支 | 已完成 |
| 18 | ChatGPT 定时任务是否继承长上下文 | 为长期运行应只保留摘要，完整记录落 Git；定时任务只是计算窗口，不是唯一长期记忆 | 强共识 |
| 19 | 错峰：每 20 分钟换人、同一 Agent 一小时后返回，是否“记不住旧事” | 时间驱动/状态驱动分离；各轮从 Git 恢复，先处理未关闭任务/返工，再领新活 | 强共识 |
| 20 | Agent 是否读取完整历史 | 不读全历史，只先读最新摘要、Inbox、BOARD、任务指针；必要时再读原件/diff/review | 强共识 |
| 21 | 50 个 Buddy Agent + 少量 ChatGPT Agent 扩大规模 | 适合分布式异步模式，但协调复杂度、权限与并发会先成为瓶颈；不能把“可设 50 个”直接等价于吞吐量 | 共识/待压测 |
| 22 | Watchdog 仅看摘要是否足够 | 不信任摘要文字；应核实其指向的 Git SHA、文件、事件与状态，必要时读结构化头部 | 强共识 |
| 23 | Controller 与 Watchdog 是一套还是两套 | 同一轻量 Python 系统内的两个职责模块；Watchdog 巡检，Controller 执行关键状态动作 | 强共识 |
| 24 | Controller 是否能直接部署 Git，而不放 GCP | Git 本身不运行常驻进程；GitHub Actions 可执行短时 Python Job，状态需另行持久化 | 方案备选 |
| 25 | Actions 公有/私有、CPU/内存/流量/免费分钟 | 规格足够、临时盘不持久、公有标准 Runner 免费、私有有分钟额度；不能把 Actions 当秒级实时租约服务器 | 已查/实施未定 |
| 26 | 公有仓库是否只读 | 外界可以阅读和 fork，不能直接推送未经授权的修改；公开可被搜索，不只是“有网址的人可见” | 已澄清 |
| 27 | 55 Agent 各类事件触发成本 | 每个微事件都独立启动 Job 可能高成本；要合并事件与低频兜底 | 共识 |
| 28 | 微软标准是什么，应看原版还是自己的复刻 | 以官方 `microsoft/Agensh` 论文/源码为原版基线；自己的 `kaibahaha/xxsc` 是第二基线 | 强共识 |
| 29 | 微软有即时消息，我们缺什么 | 原版用 Mattermost + Router 提供异步/及时通知；我们当前只有轮询看板，无同等直接消息推送 | 已确认差距 |
| 30 | Actions 能否充当消息服务器 | 不能长期驻留；可临时校验/路由/补偿。当前非实时需求可改成 Git 持久化 Inbox/ACK | 强共识 |
| 31 | 消息怎么“返回”到 ChatGPT | 普通 ChatGPT 定时任务不能被 Git 消息直接唤醒；下次按自身计划醒来主动读取针对自己的未读消息 | 强共识 |
| 32 | 看板是不是已经相当于消息系统 | 日志只是事实发布层；补足地址、持久消息 ID、接收状态、ACK、重试和有序消费后可作为可靠异步消息层 | 强共识 |
| 33 | 任务领取与消息冲突还有什么缺口 | 原子化授租、租约过期/接管、审查 commit 绑定、恢复/可追溯仍是必须单独实施的控制逻辑 | 强共识 |
| 34 | 用户希望每次下指令就得到最佳实践提醒 | 助手应主动提示“隐藏成本、上下文、权限、并发和验收风险”；跨新会话的稳定生效需在可用个性化设置中明确配置，不能仅靠口头保证永久记住 | 交互偏好 |

**边界说明**：其间还出现过“高级语音与普通语音的区别”的独立产品问答，且当时回答误理解为高级/低级编程语言；该问答没有形成 Agensh-Lite 系统架构决议，不将错误说明纳入本规范。

---

## 3. 三种实施形态与路线演进

### 3.1 Lite-M：纯 Markdown / Git 驱动（可最早启动）

- GitHub 存任务、看板、Claim、事件、交付、审查和游标；Agent 由 ChatGPT/WorkBuddy/Codex 的原生定时器独立唤醒。
- 采用静态分区、每身份独立工作目录、单人写 BOARD、追加式事件和提交回读，最大限度避免竞争。
- 不跑独立服务器；可以只依赖 GitHub 提供的提交与历史功能。
- **能力边界**：软认领的碰撞可以检测、但不能保证任意并发情况下绝不重复开工；复杂租约回收及跨文件状态一致性难以纯 Markdown 保证。

### 3.2 Lite-M+：推荐优先落地的轻量增强版

- 保留 Lite-M 的事实源、Agent 自主定时和低成本特征。
- 增加一个 Mini Controller（Python）执行确定性部分；Watchdog 是其中子模块。
- 主要管：事件校验、状态推进、去重、ACK/cursor、投影、超时、认领授权、故障恢复、读写回证据。
- 可先用周期脚本/Actions 做**非实时**职责；如果确实需要无等待的独占授租，再以在线单一权威组件承接，不盲目扩张全平台。
- **关键标准**：强独占仅在序列化权限/事务/条件更新有真实实现与竞争测试证据时才宣称成立；否则退回 `SOFT_CLAIM`。

### 3.3 Lite-P：深度版（暂不作为开始工作的前提）

- 在 Lite-M+ 基础上增加多模型动态路由、资源池、复杂恢复、可观测性、消息实时化、扩容和安全策略。
- 当前 R01 两个 PR 可作为资产；不应因其已存在而强迫一口气部署全套。
- Codex 的每 5 小时与每 7 天使用额度、WorkBuddy 点数、重试成本需要纳入未来调度，而非当前先实现高开销路由。

**阶段决策**：先让 Lite-M/Lite-M+ 产生真实的“领取→交付→独立评审→返工/接受→下一轮”的闭环，再以压力测试数据决定是否建设 Lite-P。

---

## 4. 推荐目标架构：看板/事件、符号控制、神经执行三层

```text
                 GitHub（长期可追溯的事实与协作中心）
          task specs / immutable events / commits / evidence
             board projection / inbox / ACK / cursors
                              ▲  ▲
                  条件写入/回读 | Git/API
                              ▼  ▼
   Mini Controller（可为在线单进程，或非实时 Actions Job）
      状态机 / Claim Grant / 去重 / 消费游标 / 权限边界
      └─ Watchdog：Schema/SHA/唯一性/超时/异常/索引重建
                              ▲  ▲
            定时唤醒/下一轮消费 | 事件发布、交付、反馈
                              ▼  ▼
         ChatGPT 定时 Agent / WorkBuddy / Codex / 其他模型
            语义理解、自主决策、编码、自测、独立审查、修复
```

### 4.1 三种“真相”不能混淆

1. **规范真相**：任务 `TASK.md` 的要求和验收标准，必须绑定固定版本。
2. **发生真相**：实际 Git commit、事件、执行日志、审查结论，时间与身份可追溯。
3. **展示真相**：`BOARD.md`、短摘要、统计表只是上述事件的**投影**；不应把人工手写摘要当作独立权威。

### 4.2 “Markdown 即程序”的准确边界

Markdown 是协议、输入、记录、证据索引和状态表现形式；**不是自动锁、不是可执行数据库事务、不是运行 Python 的服务器**。确定性约束仍要由 Git 原子原语、GitHub API/受控写入者或 Python 控制程序执行。

### 4.3 One Writer 原则

- 同一个权威状态不允许两个不协调的 Controller 同时无条件写入。
- Agent 可以分散提交事件、自己的交付与收件箱回执，BOARD 由统一投影器更新。
- 写失败要记录，回读失败要重试/熔断，不得宣布成功。
- GitHub API 对**一个 Git 对象或一个 ref 的条件更新**可能构成原子竞争点；**一次普通多文件 push 或多个顺序 Contents API 写入，不自动构成跨文件事务**。
- 如果使用 SQLite，它在本机可做事务，但实例被销毁或多个 VM 各持一份 SQLite 时，不能充当全局唯一租约权威。

---

## 5. 错峰定时：上下文和任务生命周期必须解耦

### 5.1 当前业务场景

有多个 ChatGPT 定时 Agent 错峰苏醒，相邻 Agent 约 20 分钟接续，但同一 Agent 可能隔约 60 分钟才再次启动。一个任务交付后，下一名审查者可能隔 20–60 分钟才检查；作者再收到返工信息时又过几轮。WorkBuddy 可能有更多不同频率的 Agent，复杂性更强。

**讨论结论**：不能让“第 N 轮会话记忆”定义任务；应由 `TASK_ID + ATTEMPT_ID + COMMIT_SHA + REVIEW_ID` 关联整个生命周期。

### 5.2 每次唤醒的固定入口（建议写入所有定时提示词）

```text
WAKEUP
  1. 读取公共协议版本 / 当前 Git HEAD / Agent 自己的 cursor。
  2. 只读最新 BOARD 投影、自己的 Inbox 摘要和未关闭任务索引。
  3. 按优先级处理：安全/权限阻断 > 有效返工 > 已领取未完成
     > 依赖被解除的原任务 > 新任务申请。
  4. 对选中任务按需取原 TASK、关联版本、最近 finding、代码 diff。
  5. 核实 claim/grant 和候选 commit 的版本一致性后才工作。
  6. 执行、提交完整证据，追加结构化 Event / Message。
  7. 写后回读，更新 cursor/ACK，并在定时会话中只保留简短摘要。
END TURN
```

### 5.3 长上下文压缩规则

**仅保留在 ChatGPT 定时结果/摘要中的信息**：本轮身份、Run ID、任务 ID、状态、关键结论（1–3 行）、变更 commit/文件路径、待审核或返工 ID、下次行动、当前阻断。

**必须只以 Git 为长期依据的详细信息**：任务全文、图表/附件引用、代码、测试原始输出、审查意见、失败栈、事件序列、长推理过程的可共享结论与证据。

长篇聊天不是可审计事实。Agent 可以利用自身工作时的局部上下文，但每次执行**都必须由远端持久状态重新定位当前工作**。

### 5.4 延迟审查导致返工的处理

- 审查员针对确切的 `candidate_commit_sha` 开审，而非“上一轮的人最后说了什么”。
- 作者可能已进入新任务；返工通过 `findings/` + 收件箱建立可领取的工作项，拥有自己的优先级和截止期。
- 普通返工可等待作者下一轮；严重缺陷冻结受影响任务的 `ACCEPTED` / 后续依赖，必要时换 Agent 修复。
- 修复不覆盖过去记录；新 `attempt_id` 和 `candidate_commit_sha` 必须与旧审查区分。
- 原审核批准对新 commit **默认不适用**；重新执行差异复核和必要回归测试。
- 有限返工：两轮同类失败、三轮仍无法完成等情况应升级，而不是无限循环。

---

## 6. 消息共享：不新增实时服务器，但必须有可靠异步消息协议

### 6.1 微软的差异

微软原版同时具有 Gitea 工作区、Mattermost 消息与 board-service 共享发现，mini-router 负责投递、去重、断线重试、持续的 ACP 会话。我们目前已经有“Git 任务与日志”，但还缺**地址化消息、消费确认与可靠恢复**。这才是差距，并不意味着必须先部署 Mattermost。

### 6.2 本项目的选择

- **当前不要求秒级消息互通**；ChatGPT 休眠时不能因为 Git 里写了一条 Markdown 就被直接唤醒。
- 所有 Agents 下次按照平台本来计划唤醒，**先查自己 Inbox、未处理 ACK 和返工/冲突事项**。
- 在线 Buddy 可更频繁消费；不要求所有 Agent 以相同节拍执行。
- GitHub Actions 可用于异步校验、整理和补偿，**不能作为永不下线的消息服务器**。
- “无需另建消息服务器”的前提是**可靠异步消息模块仍要实现**，不能仅靠单份大看板里的自由文本留言。

### 6.3 最小消息状态

`CREATED → COMMITTED → AVAILABLE → ACKED → CONSUMED / RESOLVED`；失败分支 `RETRY_PENDING / DEAD_LETTER / BLOCKED`。

特别区分：

- `COMMITTED`：Git 已写入，不代表 Agent 看见。
- `ACKED`：收件人确认读到，不代表业务完成。
- `RESOLVED`：任务/冲突已按证据处理，不代表消息已删除。

### 6.4 最小消息字段（示例，建议 schema）

```yaml
schema_version: '1.0'
message_id: MSG-20261026-000123
idempotency_key: task:AGL-001:review:RV-003
from_agent: WB-02
to_agent: CHATGPT-C
type: REVIEW_REQUEST
priority: normal
task_id: AGL-001
attempt_id: ATT-002
candidate_commit_sha: '<40-hex-git-commit>'
created_at_utc: '2026-10-26T02:00:00Z'
expires_at_utc: null
status: COMMITTED
ack_ref: null
payload_ref: factory/tasks/AGL-001/reviews/RV-003.md
```

这个只是**建议协议样例**，不是现有代码已支持的已冻结 Schema。机读部分可存 YAML frontmatter 或 JSON；不必全部装在聊天提示词中。

### 6.5 消息防丢条件

1. 发送端写 Git 得到 commit SHA，并**独立回读**。
2. 接收端按 cursor 增量扫描，不将消息有无等同于本地聊天上下文有无。
3. ACK 是独立的幂等事件；重复送达不重复推进任务状态。
4. 未 ACK 达到期限由 Watchdog 检查并重发通知/移入待处理队列，保留原 message_id。
5. 收件人停用、消息过期、证据缺失产生 `DEAD_LETTER` 或 `BLOCKED`，不得悄悄丢弃。
6. GitHub Actions 漏触发或延迟时，下一次主动扫描能从**持久事件历史**补消费。

### 6.6 不要把 Git 历史误当不可篡改账本

Git commit SHA、历史与分支保护提供**可检测修改**的基础，但仓库管理员仍可能强推、删分支、改可见性；“不可篡改”只有在权限、禁止强推、保护规则、备份/外部锚定等前提下才近似成立。必须明确威胁模型和审计权限。

---

## 7. Watchdog 与 Controller：合一部署，分离职责

### 7.1 Watchdog（只读校验优先）

可由一个 Python 脚本包实现并按需执行，主要核验：

| 校验对象 | 具体规则 | 是否需读业务正文 |
|---|---|---|
| 文件/记录唯一性 | `TASK_ID`、`ATTEMPT_ID`、`EVENT_ID`、`MESSAGE_ID` 不冲突 | 通常不需要 |
| 版本一致性 | Git HEAD、文件 blob SHA、任务版本、评审 `reviewed_commit_sha` | 通常不需要 |
| 状态机 | 事件合法、前置状态存在、转移授权正确 | 结构化字段即可 |
| 租约/认领 | grant 是否存在、是否过期、fencing token 是否新鲜 | 结构化字段即可 |
| 消息可靠性 | Inbox、cursor、ACK、重放、超时、死信 | 结构化字段即可 |
| 任务依赖 | DAG、前置验收是否满足 | 结构化任务元数据 |
| 证据索引 | referenced file/commit/test artifact 是否存在、hash 是否匹配 | 只在必要时访问对象 |
| 看板投影 | 重建 BOARD 是否与事件账本一致 | 不必语义审查 |
| 故障恢复 | OOM、限流、漏唤醒、断线、重试、写后回读 | 系统指标/日志 |

Watchdog **不能仅检查摘要“写得像不像真的”**，而必须核对摘要的版本指针和可机检证据。它不是 QA 评审者，不能因为看到 `PASS` 字样就断定代码可运行。

### 7.2 Controller（关键路径必须有确定性的授权）

- 维护任务状态转换和策略权限，阻止非法状态晋级。
- 接收 `CLAIM_PROPOSED`，执行**真实的互斥决策**，发出 `LEASE_GRANTED` 或拒绝。
- 为 grant 引入版本/epoch/fencing；旧授权失效后，过期 Agent 不得覆盖新执行者结果。
- 将用户定义的审核门禁、超时/升级、事务性变更、无副作用回放落成代码。
- 严格区分“事件已经接收”与“业务已经被批准”。

### 7.3 部署形态

**代码层可一套包**：`controller/`（状态、Grant、事件账本、投影）+ `watchdog/`（巡检、审计、告警）+ `storage/`（Git 适配）+ `protocol/`（Schema）。

**运行层不必长期同时占两个进程**：同一个常驻进程可以调用两个模块；在 Actions 方案中可以在每次 Job 内启动同一 CLI 的不同子命令。架构上“合一”，但**Watchdog 周期检测**和**认领当下授权**不可混成一个慢速计时器。

### 7.4 GCP 云端最小基线的注意点

- 单台 GCP `e2-micro` 资源为 1 GB 内存、2 个共享 vCPU（持续份额约 0.25 vCPU）。看门狗很轻，真正未知是 `codebuddy --serve`、FastAPI、MCP 及并发子进程。
- 如果需要持久 SQLite 权威，必须实测断电重启、盘持久化、备份和单主接管；只备份 SQLite 不足以替代 Git 审计链。
- 可以先使用 systemd 监管单主服务；外部健康检查用于侦测整台 VM 掉线。

---

## 8. 部署选择：GCP、Oracle、双 GCP 和 GitHub Actions 的结论边界

### 8.1 GCP 原有定位（用户提供的路线 A）

原提案：美国区 `e2-micro` 常驻 `codebuddy --serve :8080`、FastAPI `:8787`、MCP Server、Git 同步、Secret Manager；本地电脑关机不影响。Git 是共享看板、版本与对账，Agents 通过不同接口调用 Buddy/模型。

**确认的设计方向**：控制与执行/桥接分离、凭据不入仓库、Git 做可追溯事实、多个代理可异步运行。

**未确认的技术前提**：ChatGPT Actions、Codex MCP、Buddy 反向调用所有平台的会话模型，分别需要真实支持的接口、授权和实际调用测试；不能把“画了桥接箭头”当作跨平台调用成功。

### 8.2 GCP 资源与成本讨论

- Always Free 满足条件时可获得按月折算一台 e2-micro 的实例小时数、30 GB-month 标准持久磁盘、1 GB/月符合条件的从北美出站流量；并非“总账单低于多少美元都免费”，而是**按具体资源 SKU 限额**。
- 通过增量 HEAD/tree/SHA/结构化元数据检索，Watchdog 对文本的流量可能很低；但涉及 clone、历史、artifact、依赖下载、Runner 网络与公网 IPv4 时需另行核算。
- 是否扩容应以 `free -h`、Swap I/O、OOM、RSS 峰值和真实工作量测试为准；仅多一个 Watchdog 不构成扩容理由。
- 第二台 Google e2-micro 可以物理隔离“控制/桥接”，但每台仍只有 1 GB；另一 Google 登录不自动得到另一份免费结算额度。

### 8.3 Oracle Cloud 免费 A1（备选）

讨论过将较占内存的 Buddy Bridge 放 Oracle、轻量 Controller 保留 GCP。**没有实际取得 Oracle 实例的证据**，不能把它写成已落地拓扑。

按本次复核的 Oracle 官方 Always Free 页面，A1 目前对应每月 **1,500 OCPU 小时 + 9,000 GB 小时**，相当于全年月度持续 **2 OCPU + 12 GB** 的可用量，另有相应块存储限额；需注意主区域容量不足、7 日低利用率回收、ARM 兼容与防意外计费。不能按旧 4 核/24 GB 传闻部署预算。

### 8.4 GitHub Actions 的关键机制

- `.github/workflows/*.yml` 是触发定义；Runner 是按 Job 临时分配的 VM/容器，运行完销毁，不是常驻服务器。
- 可受 `push`、PR、手动触发及 `schedule` 触发；时间计划可能延迟/漏触发，绝非严格精确的实时心跳。
- 标准 `ubuntu-latest`：**公开仓库 4 vCPU / 16 GB RAM / 14 GB 临时 SSD；私有仓库 2 vCPU / 8 GB RAM / 14 GB 临时 SSD**（以官方最新规格为准）。
- 公有仓库标准 Runner 计算分钟免费；私有仓库免费分钟和超额费率取决于账号套餐与当时定价。GitHub Actions 没有类似 Google VM “每月统一 1 GB 出站流量”的公开标准 Runner 配额承诺，不代表无限制联网。
- 标准 Runner 的工作空间、临时磁盘不持久；状态、游标、审计必须写入 Git 或其他持久存储。
- GitHub Actions 普通事件触发是异步 Job；即使使用 `concurrency`，也**不能仅靠它直接签发有严格实时保证的互斥 Grant**。
- 通常由 Actions 默认 `GITHUB_TOKEN` 触发的多数下游 `push` 工作流不会自动递归触发，必须在设计事件消费链时验证。

### 8.5 公开仓库与私有仓库选择

公有仓库并非“知道链接才能看”，任何人可能搜索、读取、fork；但外人不能未经写权限直接改动源仓库。可以考虑**公开通用 Controller 代码、私有业务任务与消息**，但跨库授权、工作流所在库计费方式、凭据暴露与日志泄密必须实测，不得假设公开代码库自动让私有业务运行免费。

### 8.6 当前没有冻结单一云端部署结论

| 候选 | 最适合 | 主要风险 | 暂定态度 |
|---|---|---|---|
| **纯 GitHub Markdown** | 小量低冲突的定时接力 | 强互斥不保证 | 保留最小可运行备份 |
| **GitHub Actions + Git** | 元数据审计、事件批处理、投影、低频心跳 | 延迟/丢触发、事件成本、租约授权语义 | **优先实测** |
| **GCP e2-micro 单主 + Git** | 在线瞬时授权、长期桥接 | 1 GB 内存、网络和 IP 成本 | 已有资源可作兜底 |
| **双 GCP e2-micro** | 桥接/控制物理分离 | 两个 1 GB、计费资格 | 可选，不是已部署 |
| **Oracle A1 + GCP** | 较重 Buddy 桥接与独立控制 | 免费配额难申请、回收、ARM | 不能阻塞路线 |
| **Lite-P 全量云平台** | 真正大规模高吞吐和可观测 | 工程复杂与维护成本 | 后置 |

**部署决策门槛**：如果业务可接受“申请任务后等下一次 Actions 批准”，且能证明唯一 Grant、漏触发恢复，则优先无常驻方案；如果需要秒级独占分配，保留轻量在线权威并用 Git 做事实和审计。

---

## 9. GitHub Actions 事件成本模型与正确优化方向

### 9.1 为什么“每一个事件触发一个 Job”可能很贵

假设 **55 个 Agent，每人每小时一轮，每轮 3 个独立事件（Claim、交付、审核）都各自启动一次 Job**，30 天：

- `55 × 3 × 24 × 30 = 118,800 次 Job / 月`。
- 如每次按 1 分钟计费：约 **118,800 计费分钟 / 月**。
- 用当时讨论的标准 Linux 价格 `$0.006 / 分钟`、假设私库套餐有 2,000 免费分钟，估算超额约 `(118800 - 2000) × 0.006 = $700.80 / 月`。

**只是一组高压场景的算术假设，不是实际账单或各平台的真实事件频率**。若 Job 时间不足一分钟仍存在计费粒度，真实金额应以计费明细、官方当期价和使用的 Runner 为准。

### 9.2 非实时事件分类

| 事件类别 | 推荐处理 | 触发期望 |
|---|---|---|
| CLAIM / GRANT | 严格授租事务或安全的条件写入；申请方等待权威结果 | **关键路径**，不能全靠异步延迟校验 |
| MESSAGE / ACK | 先持久化，Agent 按游标读；可批量消费 | 可容忍下一次苏醒 |
| DELIVERY / PATCH_SUMMARY | Git 写入 + SHA 回读；增加轻量异步审计 | 允许批量 |
| REVIEW / FINDING | 绑定 commit，形成待处理队列与状态门禁 | 允许下一轮处理 |
| BOARD 投影/统计 | 合并多个事件一次重建 | 低频/按需 |
| 超时/死信/恢复 | 计划心跳兜底（避开整点高峰） | 例如 10–60 分钟级 |

### 9.3 建议的成本优化

- **先读 Git HEAD / event cursor**；没有新事件则无须全量文件扫描。
- Git repo 内只存摘要与结构化指针，原始测试日志和大文件适当归档、使用链接/散列索引。
- 尽量**合并多个事件为一次 Controller 执行**，而不是 55 Agent × 每次 3 个微事件各调用一次 Actions。
- 一个 Agent 一轮产生一个带多个子事件的批量提交可降低提交开销，但任何强一致的 Grant 仍必须独立确认。
- 用 GitHub 官方 usage 报告测实际 Job 时长、触发次数与消耗；没有实测前不给固定月费承诺。
- **不要用公开整个业务仓库换分钟额度**；安全代价可能远超算力费用。

---

## 10. 微软 Agensh 原版机制：已验证事实、适配与边界

### 10.1 官方原版基线

- GitHub 官方仓库：`https://github.com/microsoft/Agensh`。
- 原始论文：`https://arxiv.org/abs/2609.26781`。
- 官方工作指令：`prompts/agents.txt`。
- 组件：`mini-router/README.md`（per-worker 事件转接）；`board-service/README.md`（共享发现与工作认领）。
- 先前研究使用的上游源码锚点：`0468a3e6a58b51dc2b84871fcaa0df22b0d1033e`（用于可重复对照，官方主分支可能继续变化）。

### 10.2 源码体现的机制

1. Agent 自发现/自认领：`CLAIM`，不是每次中央审批。
2. Agent 自行针对参考行为做测试、提交 PR，merge 拒绝时同步 main 并重新检查。
3. `FACT`/`OBSERVED`/`FAIL`/`PATCH_SUMMARY` 在共享上下文及时发布，失败尤其用于阻止同伴重复无效尝试。
4. board-service 维护短摘要、历史检索、CLAIM 约 1 小时默认 TTL、失败对候选的失效标记；它不替 Agent 执行其宣称的测试命令。
5. per-worker mini-router 使用持久事件存储、去重、串行调度、ACK/重试、重启恢复和 ACP 会话，把在线新消息注入会话。
6. 原版存在同伴发现缺陷和协调行为，但**官方复现可零必需 PR 审批**；不得据此声称每个 patch 都经过第三方审核。
7. 微软运行栈包含持续在线协作服务；Agent 消息可在运行中的当前 turn 内被看到。**我们的 ChatGPT 定时 Agent 是醒来才消费，并不具备原版同样的即时打断能力**。

### 10.3 我们与原版的明确差异

| 维度 | 微软原版 | Agensh-Lite 本轮目标 |
|---|---|---|
| 通信 | Mattermost + board-service + router | Git 异步收件箱 / Events / ACK；实时通信后置 |
| 调度 | 持续在线 event router 与 ACP | 外部平台定时唤醒 + 下次补领 |
| CLAIM | 自主声明/碰撞协调 | Lite-M 软声明；Lite-M+ 可增加强 Grant |
| 共享记忆 | 服务端存储短事实和原始历史 | Git immutable events + 结构化索引 + 按需读详细内容 |
| 质量验证 | 作者自测、按需同行协作 | 按风险级别明确强制独立审核与集成测试 |
| 中央授权 | 原版不强制每次申领中央批准 | 可选单主 Mini Controller 以增强一致性 |
| 执行资源 | 常驻容器、ACP、数据库 | 使用已有 ChatGPT/Codex/Buddy 云端执行额度 |

> **结论**：复制的应是可证实的协作协议与分工原则；我们新增的强审核/严授租是自己的治理设计，必须自己测试和证明，不得挂微软背书。

---

## 11. R01 现状和接下来最小增量

### 11.1 本次真实 GitHub 回读（2026-10-26）

| 工作包 | PR | 观察到的状态 | 当前 head | 说明 |
|---|---|---|---|---|
| Codex Core | [PR #1](https://github.com/kaibahaha/xxsc/pull/1) | `open / draft / unmerged` | `5f9afb8b9a90f95a79ade47bd6ed5734711ff72d` | 事务状态、Lease/Fencing、回放基础，尚未证明端到端线上互斥 |
| WorkBuddy Adapters | [PR #2](https://github.com/kaibahaha/xxsc/pull/2) | `open / draft / unmerged` | `260e596f3e8cff772a7d3de58e3527685e949721` | GitHub 存储、轮询、执行桥接、CLI，尚未同 Core 联合验收 |

被冻结的 V4.2 源基线：`exp/agensh-lite-v4.2-controller-mvp-20261025` / `2d4c1a6fc0792a1182777262b41bfb4c09c0b5d2`。**两个 PR 都没有合并**；任何“测试通过 N 条”只能证明对应环境的局部证据，不等于无人软件工厂可自动运行。

当前集成风险：两个分支可能使用不同 Python import 根（`factory.agl` 与 `agl`），本地 SQLite Lease 与云端多 Agent 的唯一授权之间需要真正的写入协议，审核证据不能仅凭报告宣称。

### 11.2 最小可行 R02-Lite 工作内容（本纪要提出的建议）

- 合并/协调 Core 和 Adapter 接口与目录结构，统一 Schema 和异常类型。
- GitHub 结构化消息/事件/ACK/cursor、BOARD 投影、Agent 下轮补消费。
- 在不依赖质量模型的情况下完成 Watchdog 的 ID/SHA/状态/门禁检查。
- 优先完成可验证的软认领+静态分区闭环；强认领单独开票实现并压测。
- 正式门禁：由独立 Agent 对代码和真实测试结果审核，不能用 Markdown `PASS` 替代。
- GitHub Actions 可试跑**仅审计型 Job**，保留 GCP 作为强 Grant 或桥接环境的备选，不一开始完全迁走。
- 全过程严格保留实验环境、分支保护、可回滚、未认证身份不能写入。

---

## 12. 最小 Markdown 文件群与事件契约（建议，非已部署）

```text
factory/
  governance/
    GOVERNANCE.md             # 统一纪律入口与版本
    STATE_MACHINE.md          # 状态转换和授权
    REVIEW_POLICY.md          # 风险分级 QA 门禁（可引用 V1.0）
    EVENT_SCHEMA.md           # 事件 schema
    MESSAGE_PROTOCOL.md       # Inbox / ACK / 死信 / 重试
  board/
    BOARD.md                  # 由事件生成的只读投影（单写者）
  agents/
    CHATGPT-A/inbox/          # 定向消息，追加式
    CHATGPT-A/cursor.json
    WB-01/inbox/
    WB-01/cursor.json
  tasks/TASK-0001/
    TASK.md                   # 任务原始验收要求、版本
    claims/
    attempts/ATT-0001/DELIVERY.md
    reviews/RV-0001.md
    findings/FD-0001.md
  events/2026/10/EVENT-*.json
  controller/
    grants/                   # 如经真实原子协议授权
    audit/
    snapshots/
  runlogs/YYYY/MM/           # 仅简短可审计的运行摘要
```

> 若与现有 V4.1/V4.2 文件树产生路径冲突，先写 Migration Mapping，不允许直接让两个协议并行作为生产事实源。

### 12.1 一份“本轮定时会话摘要”应长什么样

```yaml
run_id: CHATGPT-A-20261026T012000Z
author: CHATGPT-A
git_head: '<sha>'
processed_events: 4
acknowledged_messages: [MSG-000101, MSG-000102]
active_task: TASK-0001
attempt: ATT-0003
delivered_commit: '<sha-or-null>'
status: REVIEW_PENDING
next_action: 'wait for review; check own inbox before new claim'
blocker: null
```

这类摘要不是任务原件，不应把它复制进每轮系统提示词形成无限增长的聊天历史。下一轮直接依照 ID 去 Git 取当前事实。

### 12.2 事件最小字段

`event_id, schema_version, event_type, task_id, attempt_id, actor_id, prior_state, next_state, ref_commit_sha, idempotency_key, recorded_at_utc, evidence_refs, signature_or_auth_context`。

允许变更事件 schema，但迁移必须有兼容层；UNKNOWN 状态不可当作 EMPTY。业务验收的 `APPROVE` 只能由授权角色且针对正确的 commit 写入。

---

## 13. 必须纳入下一轮的纪律与验收（按风险排序）

### P0：没有它们不能宣称安全运行

1. **真唯一认领**：两名 Agent 同时申领同一任务，最终至多一个有效 Grant；无法证明则公开标 `SOFT_CLAIM`，不启用争抢共享任务。
2. **状态机**：同一事件重复提交 100 次只生效一次；非法状态晋升拒绝且留痕。
3. **持久消息**：Git 写后回读；故意漏一次通知或停一个 Agent，下轮仍能补收且不会双重执行。
4. **版本审核**：作者获得 Review APPROVE 后改一个字节，旧评审不再验收新版本。
5. **返工闭环**：跨 3–4 个醒来轮次，返工仍能找到正确作者、任务版本和未关闭 Finding。
6. **故障封锁**：凭据不可用、Git 限流或写失败时不宣布认领/交付/验收成功。
7. **不可伪造审查**：Watchdog 仅核实测试记录的引用和机器退出码，不因 markdown 字面 `PASS` 放行高风险代码。

### P1：开始无人长期运行前

8. **BOARD 重建**：删除/损坏投影后，从不可变事件恢复一致状态；事件链仍完整。
9. **并发 CAS/单主**：双 Controller 并发下不得都发布有效 Grant；如做不到，必须禁止第二写者。
10. **消息信封+游标**：上千条异步消息不要求一轮全部读全文；精准找到本 Agent 未读、已 ACK、死信。
11. **任务与节拍无关**：在 20 分钟错峰与 60 分钟复醒下，一次任务历经多轮，交付/审核/返工不会错绑。
12. **费用与吞吐量**：统计实际 Actions Job 数/分钟、Git API 调用次数、延迟、重复率、重试率和 Agent 空唤醒率。
13. **安全演练**：仓库公开/私有权限检查、自动化令牌最小权限、日志脱敏、不能从 fork 未信任代码直接获得 secrets。

### P2：完整体系压力验收

14. **至少 24 小时影子运行**：多 Agent 错峰、关掉一个 Agent、网络不稳定、重复事件、错误审核、旧 Lease 重放、Runner 漏触发等故障注入。
15. **真实独立代码审查**：至少一个作者自检 PASS 但审查 FAIL 的实例，一次返工后独立重测 PASS；各轮 commit 和证据可回放。
16. **交付口径严格**：`COMMITTED`、`ACKED`、`SELF_TESTED`、`REVIEW_APPROVED`、`ACCEPTED`、`MERGED` 是不同事实，不得混计“成功交付数”。

---

## 14. 关键未决问题与冻结决策门槛

| ID | 未决问题 | 需要的证据/决策 | 未决期间的安全默认 |
|---|---|---|---|
| OPEN-01 | 正式 Controller 放 GitHub Actions、GCP 还是混合 | Claim 并发时延、单主事务验证、漏触发回补、成本 | Actions 先只承担审计与投影 |
| OPEN-02 | Git CAS/Grant 是否满足真实严格互斥 | 两个独立 Writer 并发测试 + fencing + 重启接管 | `SOFT_CLAIM` + 静态分区 |
| OPEN-03 | 原 V4.1 的目录与新 Inbox/事件 schema 如何合并 | Schema 映射、迁移测试、统一单一真相 | 不直接改动冻结基线 |
| OPEN-04 | 多少业务消息需要实时推送 | Agent SLA / 消息延迟实测 | 异步 Git Inbox + 下一轮读取 |
| OPEN-05 | 是否允许公开 Controller 源码与哪个仓库公开 | 仓库内容敏感性、token、跨库权限、账单 | 私有业务仓库优先 |
| OPEN-06 | CodeBuddy 服务驻留 e2-micro 是否稳定 | RSS/Swap/OOM、复醒、登录保持实测 | 不承诺稳定多会话 |
| OPEN-07 | ChatGPT Actions/MCP/反向调用 Buddy/Codex 的权限能否贯通 | 逐方向真实请求 + 响应 + 授权/安全验证 | 用已经验证的 Git 中转，不宣称互调已成功 |
| OPEN-08 | QA 风险门禁何时冻结 | Codex、WorkBuddy 独立审查 V1.0，发布 V1.1 | 不宣称研发已经遵守未部署的门禁 |
| OPEN-09 | 多少 Agent、何频率是性价比最优 | 平台用量、任务吞吐、失败率、复核成本 | 先小样本压测，再扩至 55 Agent |
| OPEN-10 | 外部健康检查与停用的长任务如何恢复 | 断电、停用、cron 漏发、限流的演练报告 | fail-closed；不假装始终 24h 在线 |

---

## 15. 建议的后续工作单（供 Codex/WorkBuddy/ChatGPT 共用）

### WORKORDER A：R02-Lite 协议集成

**实施者建议**：WorkBuddy 承担批量接口和测试，Codex 审核关键事务与安全；ChatGPT 独立验证协议/验收标准。

交付：单一 `EVENT_SCHEMA.md`、`MESSAGE_PROTOCOL.md`、`WAKEUP_PROTOCOL.md`、`TASK_STATE.md`、兼容适配与单元测试；每一份文档都要有示例、非法输入和升级路径。

### WORKORDER B：GitHub Actions 最小巡检探针

在隔离分支/测试库做一条可重复的 Job：读取 HEAD / cursor → 扫描新增事件 → 验证元数据 → 输出 audit → Git 写后回读。支持 `workflow_dispatch` 手动测试，记录真实队列延迟、运行时长与计费分钟。**此阶段不让 Actions 自称拥有正式强认领权威**。

### WORKORDER C：严格 Grant 能力选型验证

独立设计“纯 Git 条件写”与“在线单主 Controller”两组方案，做 100 轮双申领、过期重发、旧客户端重复提交、进程重启、跨进程访问。只有测试证明某方案安全才能采用该方案并升级 `SOFT_CLAIM` 字段为 `GRANTED`。

### WORKORDER D：错峰消息 + 返工回路盲测

分别以 20 分钟错峰与单 Agent 60 分钟复醒模拟：作者先交付、审查者发现缺陷、作者已做新任务、返回处理旧 Finding、重新交付、审查者验证新 commit。要求全程只靠 Git 恢复上下文，并核验 cursor/ACK 未丢。

### WORKORDER E：24h 影子运行

有审计基线后，开始 24h 定时持续运行；每日评价重复认领数、未 ACK 数、假通过数、平均反应延迟、每次成功验收的计算成本。真正符合验收才讨论长期运营和扩充 50+ Agent。

---

## 16. 主张来源与复核链接

### A. 已形成的现有项目文档（与本文件互补）

- Library：`/全自动工厂实践/Agensh_Lite_协作质量与迭代治理规范_V1.0.md`。
- GitHub 版本：[QUALITY_AND_ITERATION_GOVERNANCE_V1.0.md](https://github.com/kaibahaha/xxsc/blob/docs/agl-v4.2-quality-governance-20261026/frameworks/agensh-lite-v4.2/docs/QUALITY_AND_ITERATION_GOVERNANCE_V1.0.md)。
- R01 [Codex PR #1](https://github.com/kaibahaha/xxsc/pull/1)、[WorkBuddy PR #2](https://github.com/kaibahaha/xxsc/pull/2)。
- V4.2 冻结基线（分支）：`exp/agensh-lite-v4.2-controller-mvp-20261025`。

### B. 微软官方原版（不是我们的复刻仓库）

- [Agensh README](https://github.com/microsoft/Agensh)
- [论文 arXiv 2609.26781](https://arxiv.org/abs/2609.26781)
- [原版 Agent 工作指令](https://github.com/microsoft/Agensh/blob/main/prompts/agents.txt)
- [board-service 服务说明](https://github.com/microsoft/Agensh/blob/main/board-service/README.md)
- [mini-router 事件与恢复说明](https://github.com/microsoft/Agensh/blob/main/mini-router/README.md)
- [REPRODUCE 复现说明](https://github.com/microsoft/Agensh/blob/main/REPRODUCE.md)

### C. 资源/收费/运行边界官方资料（数值以最新政策为准）

- [GitHub Actions 计费与使用](https://docs.github.com/en/actions/concepts/billing-and-usage)
- [GitHub-hosted Runner 规格](https://docs.github.com/en/actions/reference/runners/github-hosted-runners)
- [Actions schedule 可能延迟/漏执行](https://docs.github.com/en/actions/how-tos/troubleshoot-workflows)
- [Google Cloud Always Free](https://docs.cloud.google.com/free/docs/free-cloud-features)
- [Google Compute Engine 共享核规格](https://docs.cloud.google.com/compute/docs/general-purpose-machines)
- [Oracle Cloud Always Free 资源](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm)

### D. 讨论资料的证据限制

- 本次归档依据：可见对话、用户提供的截图、可检索的相关前序对话背景、原已归档规范、GitHub 当前 PR 状态及部分官方规则。
- **不是每条语音逐字转写重放**；第 2 节是“结论和演进顺序”重构，不虚构精确事件时间。
- 此前助手对部分方案曾使用“肯定够”“免费就行”“可以直接代替 GCP”等过于确定的措辞。本文以**条件化决策、已知约束、待验证标准**替代，不把讨论建议写成既成部署事实。
- 现有 V1.0 治理规范里已形成的正式文本仍然保留；本纪要新增结论须经接口、竞争和 24h 运行验收才可升级为生产 SOP。

---

## 17. 可供以后复用的“一页执行纪律”

> 供所有 ChatGPT/Codex/WorkBuddy 定时 Agent 在任务说明里以极短指针引用。**不要把本篇全文注入每次定时上下文**。

1. 醒来先核对 Git HEAD、协议版本、自己的 Inbox 和 cursor；**先处理未关闭任务/返工，再领取新单**。
2. 任务内容、版本、代码、证据、审查、修复均以 Git ID 和 commit 为准；聊天摘要不是权威。
3. 未得到有效、可核验的唯一 Grant，不得以 `CLAIM_PROPOSED` 自封独占；纯软认领必须使用低冲突分区策略。
4. 写入必须回读；`COMMITTED` 不等于 `ACKED`，`ACKED` 不等于 `ACCEPTED`。
5. 作者自检不等于独立审核；高风险变更按治理规范走 review、可复现测试和授权门禁。
6. Watchdog 检元数据/一致性，不评价内容；AI Agent 做语义审查、编程、测试和反例检查。
7. 异步错峰是正常状态；迟到的 review 绑定原 candidate commit，新修复有新 attempt，不覆盖历史。
8. 定时会话只输出简短本轮摘要和 Git 指针；不累积完整历史上下文。
9. 不伪造成功，不在安全检查拒绝后绕过；UNKNOWN ≠ EMPTY、事件接收 ≠ 业务通过。
10. 未实测的跨云消息/权限/事务不得写“系统已具备”；完成 P0/P1 验收后方可进入 24h 正式影子试运行。

**阶段性总决策**：保留微软 Agensh 的去中心化“自主 Agent + 共享事实 + 协同/复核”精髓；采用 Git 的可追溯异步协议适配 ChatGPT/WorkBuddy 错峰唤醒；采用单一轻量 Python Controller/Watchdog 负责确定性治理；平台位置与强 Grant 机制待真实验证后冻结。**以少程序、低成本、强证据、可持续无人值守为约束，不为追求复杂而复制整套微软基础设施。**