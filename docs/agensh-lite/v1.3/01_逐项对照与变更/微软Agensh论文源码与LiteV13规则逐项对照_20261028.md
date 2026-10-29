# 微软 Agensh 论文/开源代码 ↔ Agensh-Lite V1.3 候选规则逐项对照

- 版本：2026-10-28，独立核对，**不是**微软官方对我们项目的认证。
- 微软源码：`microsoft/Agensh@0468a3e6a58b51dc2b84871fcaa0df22b0d1033e`（2026-10-22 初始发布，当前查到的官方 `main` 同 SHA）。
- 论文：*Agensh: Scaling Organizational Intelligence to 1,024 Agents*，arXiv `2609.26781v1`；在线原文 https://arxiv.org/html/2609.26781 ；PDF https://arxiv.org/pdf/2609.26781 。
- 旧版：三卷 `V1.2.1`，Library `/微软蜂群去中心化项目/00_现行纲领/`；新三卷 `V1.3-DRAFT` 为候选，不发生静默生效。

**证据等级**：`M1`=论文明确+官方代码可定位；`M2`=论文描述但代码不能单独证实所有效果；`L`=我们的平台适配/风险治理，微软没有完全相同实现；`N`=微软无此强制规则或与原版相反，需要撤回；`U`=尚待独立真实部署验证。**“功能等价”仅指设计语义近似，不等于我们已经实现。**

**决定**：`继承`直接采用原则；`适配`换载体或唤醒方式；`放宽`从硬停机降成建议；`保留本地`对确有真实风险的个性化安全治理；`撤回`不必要的刚性约束；`未定`需要真实环境确认。

## I. 自组织与 Git 共享工作区

| ID | 原版微软论文（章节）与源码锚点 | V1.2.1 先前规则/候选分歧 | V1.3 逐项裁定 | 等级 |
|---|---|---|---|---|
| MS-01 | §2.1 五步 Gather/Claim/Act/Verify/Merge；`prompts/agents.txt` 68–79 | 卷2§5 将每轮描述为12步业务事务 | **继承五步循环；不要求一轮全部执行**，12步改为可选检查参考 | M1 |
| MS-02 | §1、§2.1 无中央任务分配；`prompts/agents.txt` 35–43 | Python `choose-ready`、Controller准入可能演变成中央派单 | **不设强制中央分派**，Agent自己发现并选择任务 | M1 |
| MS-03 | §3.2 相同 Prompt、角色自发出现；Appendix A | 预先固定多角色 QA/Integrator职责 | **临时角色自组织、角色可协商**；必要权限仍有区分 | M1 |
| MS-04 | §2.1 Agent自己拟子任务；`scripts/pbench_run.sh` 415–422 只建未分配 Issue | 首轮需从提前派好的 READY 任务中挑选 | **保留自主发现/开 Issue**；可有用户优先任务但不是唯一入口 | M1 |
| MS-05 | §2.2 Shared Workspace；`prompts/agents.txt` 70–78 | 每人各写 Markdown/分支 | **继承个人分支/原件与共享 Git 合并**；Markdown是本地载体 | M1/L |
| MS-06 | §2.2 Git 保留版本/冲突；`prompts/agents.txt` 76–77 | “状态/PR审批错误即整体停机”风险 | **冲突局部处理**：拉最新 main、重新验证、再合并；不停止其他工作 | M1 |
| MS-07 | §2.1 完成后进入下一轮探索；`prompts/idle.txt` | 没任务就 BLOCKED 或停止队列 | **允许继续探索**；无新任务可 `NO_NEW_EVENT`，等待下一轮 | M1 |
| MS-08 | §3.2 各角色自发形成集成关系、反例撤回批准 | 强制中央指定某一Integrator | **同行协商/自组织集成**；受保护写入仍有真实授权 | M2/L |
| MS-09 | §3.2 8 Agent 重叠 Claim 通过对话重新分工 | 碰撞一律 `BLOCKED_CONTESTED` | **撤回全局阻断**；两个软 Claim 可以保留，冲突则沟通 | M1 |
| MS-10 | §3.2 1024 Agent 同领域多集成者，可择先回应 | 固定一个永恒集成者 | **允许候选集成人选动态选择**；生产受保护写需 Git 实权 | M2/L |

## II. 消息、共享知识与上下文

| ID | 微软论文与源码 | V1.2.1规则/实际差异 | V1.3裁定 | 等级 |
|---|---|---|---|---|
| MS-11 | §2.2 Message Interface 用 Mattermost 频道/私信；`prompts/agents.txt` 15–20 | 用 Git 消息文件承载 | **适配**；消息逻辑保留，持久可见要验证，不冒称 Mattermost 实现 | M1/L |
| MS-12 | §2.2 Shared Context 五种短类型；`shared_lessons.py` 14–17 | 加入大量任务/事件状态/多维对象 | **五类共享知识继续使用**；复杂机器状态只用于确有需求的场景 | M1 |
| MS-13 | §2.2 短事实与历史搜索；`board-service/shared_lessons.py` 15–17 | 为减少上下文发明固定字节预算 | **继承短摘要/详情指针**；不引入未经实证的全局 KB 硬配额 | M1/N |
| MS-14 | Appendix A；`shared_lessons.py` 普通100字符、PATCH 300 | 超出建议字数算错、强制多次重写 | **放宽**；100/300 是微软服务端的共享 gist 字段限制，不是我们的自然语言评价必须精确 500 字 | M1/N |
| MS-15 | §2.2 `FAIL` 复用，`prompts/agents.txt` 24–30 | 遇失败只计数不交流经验 | **继承 FAIL 为高价值共享资产**，指向可复核细节 | M1 |
| MS-16 | `board-service/README.md` + `unfold.py` | 读取完整目录树再逐个打开 | **继承索引→grep→unfold**；不默认全库阅读；Agent可自主扩检 | M1 |
| MS-17 | `board-service/main.py` 535–649 `grep` 必须有词或类型；返回最多500 | 总目录枚举可无限扩张 | **参考类型和关键词检索**；500不是跨平台硬规定 | M1 |
| MS-18 | `shared_lessons.py` 17，近期视图最多2000条 | 认为增量快照能绝对保证零上下文增长 | **纠正**：原版 `board_read` 仍有大窗口和回退，Lite不可承诺恒定 Token | M1 |
| MS-19 | `board_client.ts` 62–104 先 Snapshot，失败读 board | `RUN_PACKET` 由 Python 集中规划全部研究内容 | **撤回强制全量装配器**；只供近期增量摘要及入口，Agent自主检索 | M1/N |
| MS-20 | `board-service/main.py` 237–259 每 agent/board cursor 不倒退 | 每次清空、重读整段会话 | **适配为 Git 可重放水位**；必须防漏但不要求新DB | M1/L |
| MS-21 | `board-service/unfold.py` 细节一次展开，不回灌公共摘要 | 每条大分析都写进共享看板 | **摘要与长记录分离**，本人产物可长，公共提示短 | M1 |
| MS-22 | `board_client.ts` 40–51 看板不可达标 UNKNOWN 非空 | 无消息视为无任务，无工具继续 | **继承 UNKNOWN 与 EMPTY 区分**，只阻断依赖该证据的操作 | M1 |

## III. 事件驱动、定时轮询与失败恢复

| ID | 微软论文与源码 | V1.2.1或历史脚本的候选风险 | V1.3裁定 | 等级 |
|---|---|---|---|---|
| MS-23 | Appendix B.1 Event-Driven Runtime，`mini-router/src/main.ts` | “事件必须立即通知”与定时视为不同业务架构 | **协作语义复用，唤醒实现适配**；定时消费较慢不等于新任务模型 | M1/L |
| MS-24 | Appendix B.1 dispatcher wakes on queued events；`dispatcher.ts` | 要求严格指定 :10 开始才合法 | **放宽**：真实到点有新事件就处理；时间错位不是业务失败 | M1/L |
| MS-25 | Appendix C 30秒/3秒错峰激活 | 把错峰时刻当过期截止，早晚3分钟终止 | **撤回**：错峰只是组织节奏，不是任务失效条件 | M2/N |
| MS-26 | Appendix C 实验总计6h预算，T-45m/T-5m提醒 | 直接取消任何 stop_at | **严格保留明确总截止/授权预算**；软轮询时间与硬生产线分离 | M1/L |
| MS-27 | Appendix B.1 idle 10m 提醒继续，`prompts/idle.txt` | 10分钟无任务即停机、判失效 | **改为提醒/继续**，不终止有效Agent任务 | M1/N |
| MS-28 | `mini-router/src/state.ts` 41–57 `(dedup_key,agent)` 唯一键 | 只靠模型记忆判重复 | **适配稳定事件ID、收件人去重**，是否Git实现待测 | M1/L |
| MS-29 | `state.ts` 47–57 `pending/sending/sent/failed/retrying` | 业务成果/消息投递混成一个成功状态 | **保留传输状态与业务完成区分**，不要求普通Agent逐轮填5张状态表 | M1 |
| MS-30 | `state.ts` 20–26、194–269 默认5次退避重试 | 严格一次失败立即整个停机，或无限重试 | **采用有界重试+局部失败**；具体次数待平台实践，不照搬5为死线 | M1/L |
| MS-31 | `state.ts` 271–279 重启 `sending→pending` | 某轮执行一半就宣布永远失败 | **待处理事件重投/恢复**；防副作用重复另行处理 | M1/L |
| MS-32 | `mini-router/src/listeners/gitea/listener.ts` 36–66 先 ingest 再推进 cursor | 用最大已见消息序号跳过缺页 | **继承不跨缺洞的可靠消费语义**；不需要预先实现复杂全量一致性引擎 | M1/L |
| MS-33 | `mini-router/src/listeners/mattermost/listener.ts` 71–113 重连补拉；初始10min回看且游标进程本地 | 宣称官方确保任意停机时间历史必达 | **明确原版也有限制**；我们的长停机补扫须用Git实验单独证明 | M1/U |
| MS-34 | `dispatcher.ts` 125–201 事件完成后 `sent`；失败局部 retry | `sent`/ACK = 任务/交付完成 | **严格区分**；不能对已发送而未真正执行的任务假报完成 | M1 |
| MS-35 | Appendix B.2、`mini-router/mcp-notice-shim.cjs`：工具返回中注入紧急消息 | 认为定时Agent可在睡眠/运行中被普通Git消息秒级中断 | **不支持的实时能力不得声称有**；下轮发现并处理 | M1/L |
| MS-36 | `board-service/main.py` 262–295 短 lease 防并发 notice 消费 | 把 Claim 的协作TTL误当整个代码强租约 | **区分消息消费小租约与代码写权限**；不提前建全局租约服务 | M1 |

## IV. 验证、合并、规则治理与平台特性

| ID | 微软论文与源码 | Lite的异同 | V1.3裁定 | 等级 |
|---|---|---|---|---|
| MS-37 | §2.1 Verify；`prompts/agents.txt` 75–76 自测参考行为 | 一律要求独立两名QA才做任何普通任务 | **撤回普遍强制双签**；代码合理自测为默认，审查按真实风险升级 | M1/N |
| MS-38 | §3.2 PHP-src 反例推翻旧认可，随后重新测试 | 把任何同事的赞同视为永久批准 | **保留反例、修正、重新验证**；必要时复核新提交 | M2 |
| MS-39 | `REPRODUCE.md` 422–424：实验 PR 零批准可合并、CI 门禁关闭 | 声称微软原生必须强制R0–R3、独立QA签名 | **明确是本项目LOCAL增强**；不应宣称微软普遍采用 | M1/L |
| MS-40 | §2.2 Git 分支版本与冲突；`prompts/agents.txt` 76–77 | 受保护分支/真正权限未验证却自称安全 | **保留 Git 实权验证**；最低要求不误报，具体授权结构尚待L0决定 | M1/L |
| MS-41 | §3.2 工作流程自组织演化 | 强制所有流程变化经过大规模集中委员会 | **允许团队讨论/改良作业方法**；只对生产授权/标准变更保留受控批准 | M2/L |
| MS-42 | `REPRODUCE.md` 337–363 + `tools/pbench_score_report.py` | 用文档数、任务数、机器人次数替代最终成果 | **以真实构建和测试结果为主**；指标算法和评测器版本须交代 | M1 |
| MS-43 | `scripts/pbench_run.sh` 93–117 `EXPORT_FAILED` 不等于零分 | 写入失败/未知一概报成功，或仅凭超时重写 | **保留独立交付回读与未知状态**；Git/Drive跨平台副作用属LOCAL加强 | M1/L |
| MS-44 | 微软研究场景：ProgramBench 六小时黑盒复刻 | 我们目标是多月游戏/应用项目，自带真实用户/UX | **只能适配，不可宣布微软已证明长期生产可靠性** | M2/L/U |
| MS-45 | 微软统一worker prompt仅身份不同，Appendix A；`agent/entrypoint.sh` 121–126 | 让定时指令自增长、每轮把三卷全文灌回会话 | **定时启动口令固定短**，详细任务与证据放Git；ChatGPT UI特殊性属LOCAL | M1/L |
| MS-46 | 微软无规定ChatGPT最终回复200汉字；其100/300是board字段 | 把“少于200字”做成严格字数校验阻断 | **撤回硬字符验收**；用户可见尽量一两句，不反复精确计数 | N/L |
| MS-47 | 微软源码无“七类AGL JSON Schema”对应实现 | V1.2.1 七Schema和五种状态机必须全部生效才能启动任何研究 | **保留作历史候选机检资产，不作为任何轮次的普遍必跑门槛**；受保护动作另论 | L/N |
| MS-48 | 原版 MySQL+Mattermost+ACP；完整事件协议在 `mini-router` | 我们只用Git与少量Python就声称100%功能等价 | **明确非等价**：无中途消息注入、无MySQL事务，长积压可靠性待测试 | M1/L/U |
| MS-49 | 微软不同 Worker/Gitea账号；`secret-service/` + `agent/entrypoint.sh` | 所有Agent共用同一高权写令牌却称强权限分离 | **必须识别实际Git身份**；必要生产保护仍靠平台权限，不靠Prompt | M1/L/U |
| MS-50 | 微软没有在公开 Prompt 强制原版“每轮 12 步全部完成” | 一轮漏一个检查步骤便标系统FAIL | **放宽为场景相关检查**；人身/凭据/不可逆写入的真门禁保留 | N/L |

## V. 按真实性分层后的决策（不是所有约束都一个待遇）

### A. 微软实证机制，应直接保持（优先复刻）

五步自组织循环、Agent自行发现和认领、私人分支、Git冲突协商、Mattermost语义上对应的定向消息、五类简短共享事实、Fail复用、增量检索与按需展开、可靠事件去重/重试、失败后继续、真实测试/验证、合并后共享、临近总截止提醒收口。

### B. 必要平台适配，必须明确标注 [ADAPT]

Git+Markdown/JSON 承载短事实与异步消息；ChatGPT/WorkBuddy 平台**定时轮询**代替 Gitea/Mattermost 实时推送；跨轮 Git 外部记忆；ChatGPT UI 的极短回执；Git idempotency/ACK/回读以覆盖缺少原版事件数据库的情况。**这些应基于微软对应语义实现，但必须跑本项目实验，不得沿用微软1024 Agent成功数据作自己的通过凭证。**

### C. 保留但按风险启用的 [LOCAL] 约束

真实平台授权、受保护写入校验、用户生产停止线、外部付费/删除副作用防重、合并前验证组合代码、真实测试证据、单项拒绝无凭据或旧SHA操作。**这些约束只挡会出错的那次写入，不应挡所有其他任务、角色或定时轮次。**

### D. 明确撤回的过度设计 [REMOVE]

每轮必须严格按计划分秒醒来；迟到即跳过/自动停用；早到无任务即宣告生产失败；正常总结超建议字数即必须重新计数改写直至合格；任何消息都须填七种状态对象；所有任务普遍双QA审批；Controller负责集中计划全部项目/强行分配每个任务；Python强制替AI判断每个知识文件的重要性；硬性规定全任务阅读4KB/8KB；两个软Claim必致全项目停机。

### E. 不能冒称微软已解决的缺口 [OPEN]

- Git-only定时场景的长停机漏消息恢复、每收件人ACK去重、Git并发写与隐藏权限差异：需要本项目独立测试。
- 当 Agent 在本轮执行时有紧急 FAIL，新Lite无法像原版 MCP shim 一样在下一次工具返回插入通知；须承认滞后并在合并点/下一轮检查。
- 真实 ChatGPT 定时任务 UI 上是否隐去工具中间过程不可由Prompt保证；只控制模型主动输出的长内容。
- 多分支开发能否采用可靠的临时组合测试、GitHub Ruleset和真正的最小权限，仍依赖当前连接/仓库配置。

## VI. 微软论文“已验证”的适用范围

微软论文在 ProgramBench 的五个复杂任务里报告，1→128 agents 六小时最终测试通过率均值 `19.31%→28.78%`；pandoc 1→1024 为 `33.89%→55.06%`。该**测试通过率不是我们平台任务派单/消息投递成功率**。官方 `REPRODUCE.md` 披露原实验的六小时预算、Gitea、Mattermost、MySQL、Copilot ACP、Gitea主分支默认保护策略和复现环境。我们的 Lite 尚未在同样实验条件下运行，因此所有 Git-only 定时事件和强权限声明仍应为 `NOT_RUN`。

## VII. 可核查原始链接（固定版本）

**论文：** https://arxiv.org/html/2609.26781 （§1、§2.1、§2.2、§2.3、§3.2、Appendix A/B/C）。

**官方源码版本：** https://github.com/microsoft/Agensh/tree/0468a3e6a58b51dc2b84871fcaa0df22b0d1033e

1. `prompts/agents.txt`：https://github.com/microsoft/Agensh/blob/0468a3e6a58b51dc2b84871fcaa0df22b0d1033e/prompts/agents.txt
2. `board-service/README.md`：https://github.com/microsoft/Agensh/blob/0468a3e6a58b51dc2b84871fcaa0df22b0d1033e/board-service/README.md
3. `board-service/shared_lessons.py`：https://github.com/microsoft/Agensh/blob/0468a3e6a58b51dc2b84871fcaa0df22b0d1033e/board-service/shared_lessons.py
4. `board-service/main.py`：https://github.com/microsoft/Agensh/blob/0468a3e6a58b51dc2b84871fcaa0df22b0d1033e/board-service/main.py
5. `board-service/gquery.py`：https://github.com/microsoft/Agensh/blob/0468a3e6a58b51dc2b84871fcaa0df22b0d1033e/board-service/gquery.py
6. `board-service/unfold.py`：https://github.com/microsoft/Agensh/blob/0468a3e6a58b51dc2b84871fcaa0df22b0d1033e/board-service/unfold.py
7. `mini-router/src/state.ts`：https://github.com/microsoft/Agensh/blob/0468a3e6a58b51dc2b84871fcaa0df22b0d1033e/mini-router/src/state.ts
8. `mini-router/src/dispatcher.ts`：https://github.com/microsoft/Agensh/blob/0468a3e6a58b51dc2b84871fcaa0df22b0d1033e/mini-router/src/dispatcher.ts
9. `mini-router/src/board_client.ts`：https://github.com/microsoft/Agensh/blob/0468a3e6a58b51dc2b84871fcaa0df22b0d1033e/mini-router/src/board_client.ts
10. `mini-router/src/listeners/gitea/listener.ts`：https://github.com/microsoft/Agensh/blob/0468a3e6a58b51dc2b84871fcaa0df22b0d1033e/mini-router/src/listeners/gitea/listener.ts
11. `mini-router/src/listeners/mattermost/listener.ts`：https://github.com/microsoft/Agensh/blob/0468a3e6a58b51dc2b84871fcaa0df22b0d1033e/mini-router/src/listeners/mattermost/listener.ts
12. `mini-router/src/acp_socket_channel.ts`：https://github.com/microsoft/Agensh/blob/0468a3e6a58b51dc2b84871fcaa0df22b0d1033e/mini-router/src/acp_socket_channel.ts
13. `agent/entrypoint.sh`：https://github.com/microsoft/Agensh/blob/0468a3e6a58b51dc2b84871fcaa0df22b0d1033e/agent/entrypoint.sh
14. `scripts/pbench_run.sh`：https://github.com/microsoft/Agensh/blob/0468a3e6a58b51dc2b84871fcaa0df22b0d1033e/scripts/pbench_run.sh
15. `REPRODUCE.md`：https://github.com/microsoft/Agensh/blob/0468a3e6a58b51dc2b84871fcaa0df22b0d1033e/REPRODUCE.md
16. `tools/pbench_score_report.py`：https://github.com/microsoft/Agensh/blob/0468a3e6a58b51dc2b84871fcaa0df22b0d1033e/tools/pbench_score_report.py

**验证方式**：本对照逐行核查上述目录中相关源码与论文，不代表已构建运行微软原版，也不代表本地新方案远端运行通过。源代码中缺少的机制，不以“论文精神”充作已经实现的 API。
