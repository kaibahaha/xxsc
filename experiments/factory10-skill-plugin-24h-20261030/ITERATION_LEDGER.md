# 十大工厂Skill研究｜跨轮质量与动态RSI实验台账

实验：FACTORY10-SKILL-24H-20261030。固定100分五维权重：证据25、战略20、技巧20、案例20、风险15。所有分数只评价**研究报告质量**，不代表部署成功；未取得完整原文时不打分。每次更新须先回读Git最新blob SHA，合并后提交并再次回读，避免覆盖其他轮次。

| 轮次 | 工厂 | WorkBuddy Job | 状态 | 评分（证据/战略/技巧/案例/风险） | 总分 | 同厂上次/Δ | 主要缺陷或反馈 | 当轮方法调整 | 效果验证 |
|---|---|---|---|---|---:|---|---|---|---|
| R01 | F1 API与模型服务 | `c901454bfc4042c3` | DONE / AUDITED / Git回读 | 21/16/12/12/9 | **70** | 首圈基线 | 原生调度误判、Agent API与推理网关混淆、硬预算误判 | 提出M1文档优先、M2能力/语法证据、M3案例负例与回滚 | 基线，无纵向效果 |
| R02 | F2 软件与开源程序 | `f77da8aaab28496d` | DONE / AUDITED / Git回读 | 22/18/16/15/10 | **81** | 首圈基线（与F1不同厂，不计算Δ） | P0：worktree非安全沙箱、headless权限过宽；P1：GPL/AGPL许可判断过度简化、环境缺git/docker | M1官方文档核对；M2工具边界/命令核验；M3五案例负例/回滚 | M1具体错误已修复；M2部分有效；M3文本完整但运行NOT_TESTED |
| R03 | F3 游戏与互动体验 | `5b8ee940847e42f2` | DONE / AUDITED / Git回读 | 20/19/16/16/12 | **83** | 首圈基线（跨厂分数不计算Δ） | P0：声称完整代码却未附源码/日志，普通SHA非防篡改；P1物理模型未校准 | M1 19条证据；M2权限边界反例；M3五案例状态+种子重放 | M1部分有效，M2文本基本有效，M3部分有效；实际复现仍不足 |
| R04 | F4 图像与视觉创作 | `5458b23070ac460c` | **FAILED_RATE_LIMIT_429** / Job done仅为错误响应 / STATUS已回读 | NOT_EVALUABLE | — | 首圈基线 | 原派单有反馈，后续追单返回429，未形成研究正文 | M1证据/连接状态、M2版权隐私、M3五案例 | 无正文，无法检验 |

| R05 | F5 视频与音频内容 | `6f4057fc78094c63` | **FAILED_RATE_LIMIT_429** / Job done仅为错误响应 / STATUS已回读 | NOT_EVALUABLE | — | 首圈基线 | 原派单有反馈，后续追单返回429，未形成研究正文 | M1官方证据、M2商用许可、M3案例正反测试 | 无正文，无法检验 |
| R06 | F6 研究与报告 | `52441e82f15942ab` | **FAILED_RATE_LIMIT_429** / Job done仅为错误响应 / STATUS已回读 | NOT_EVALUABLE | — | 首圈基线 | 原派单有反馈，后续追单返回429，未形成研究正文 | M1原始来源/工件、M2学术证据/许可、M3案例复现 | 无正文，无法检验 |
| R07 | F7 AI for Science科学研究 | `1941bb3a79e84c7f` | DONE_SUMMARY_ONLY / 完整报告未取得 / NOT_EVALUABLE | NOT_EVALUABLE | — | 首圈基线 | MCP仅返回约1309字摘要及私有报告路径/12工件自述，Git无原始正文或审计 | M1来源+实跑工件、M2科学有效性、M3五案例负例 | 有方法回应摘要，未见原文，暂不可评分 |

| R08 | F8 机器人感知与动作 | `fc588db4b904442c` | **PENDING / QUEUED**（list_jobs约3220秒、0字；get_result通用running无正文）/ STATUS Git回读 | NOT_EVALUABLE | — | 首圈基线 | 共享单执行槽积压，尚无原文/审计；未重复派单 | M1官方来源+可复核工件、M2仿真/真机安全、M3五例负例/停机 | 延迟证据，尚不可评估 |

## 交付目录和防重
- R01：`rounds/R01/` 三文件完整、已回读，禁止重复派单。
- R02：`rounds/R02/FEEDBACK_TO_BUDDY.md` 已在派单前创建并回读，完整反馈内容实际发给WorkBuddy；`STATUS.md` 与 `ADAPTATION.md` 已写并回读。R02原文、独立审计、STATUS、反馈及ADAPTATION均已Git回读，Job `f77da8aaab28496d` DONE；**禁止重复派单R02**。下一轮R03须读取R02审计及ADAPTATION，并把三项研究方法改进实际注入WorkBuddy prompt。
- R11–R20对照同厂R-10；R21–R24对照同厂R-20与R-10。跨厂改进只比方法证据，不直接把不同工厂总分差当成因果效果。

- R03：F3首圈，唯一Job `5b8ee940847e42f2`；派单后[ running ]，尚无正文；反馈与ADAPTATION已写入Git并回读，研究报告/评分待补交。下一轮必须先追单，不重复派单。

- R04：F4首圈，唯一WorkBuddy Job `5458b23070ac460c`，派单后仍PENDING/0字；反馈、ADAPTATION、STATUS已Git写入并逐项回读。R03 Job `5b8ee940847e42f2` 尚未返回正文，下一轮应先追R03和R04，不重复派单。R04研究报告与审计评分待补交。

- R05：F5首圈唯一Job `6f4057fc78094c63`；真实派单后list_jobs=QUEUED/0字；反馈、ADAPTATION已写入并回读；本轮无原文/审计评分。R03/R04两个Job仍QUEUED/0字；R06须优先追取并补交，不得为R03/R04/R05重复派单。

- R06追单回收R03：WorkBuddy R03 DONE、原文及83/100审计均已Git回读，R03状态和自适应记录已补交；R04/R05仍QUEUED/0字，R06唯一Job `52441e82f15942ab` QUEUED/0字。R06反馈/ADAPTATION/STATUS已真实提交并回读；禁止重复submit R03–R06。R07须先追R04/R05/R06，再开展F7。

- R07追单修正：通过真实WorkBuddy get_result分别回读R04/R05/R06，均为429使用频率限制，提示北京时间2026-10-30 23:00重置；三轮STATUS已更新并独立Git回读，研究正文不存在。桥接器显示done/143字只是错误返回，不能计为研究成功；禁止重复派单。R07 F7唯一Job `1941bb3a79e84c7f` 已实际submit，最后查询RUNNING/0字；R07 FEEDBACK、ADAPTATION、STATUS已写并回读。后续先追R07并按实际结果更新总账，不虚构审计分数。
- R08 F8首圈唯一Job `fc588db4b904442c`；FEEDBACK已先Git写入回读且完整嵌入真实MCP prompt，STATUS/ADAPTATION写入回读；首查[running]/0字，NOT_EVALUABLE。R07 Job已DONE但仅返回摘要和私有文件路径，Git未有完整原文，不得将摘要当审计报告或重复派单。R09先追R08，按实际结果更新。

- R08同轮17:56 Phoenix复查：MCP bridge_health=HTTP200/v3.3，active_jobs=5、max_concurrent_jobs=1；list_jobs显示唯一Job `fc588db4b904442c` QUEUED约3220秒、0字，get_result返回通用[running]约3230秒、0字。Git原报告及审计仍404。STATUS已写入并逐字回读，commit `6553333072ff102c36c28161879c2680b18422bd`；R08仍NOT_EVALUABLE。R09计划时段未到，不提前派单。