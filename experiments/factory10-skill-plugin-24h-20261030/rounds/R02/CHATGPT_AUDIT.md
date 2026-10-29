# R02 / F2 软件与开源程序工厂｜ChatGPT独立质量审计

- 实验：FACTORY10-SKILL-24H-20261030；本轮 R02 / F2（首圈 BASELINE）
- WorkBuddy Job：f77da8aaab28496d；MCP任务状态：done，报告尾部 RESULT_STATUS: COMPLETE
- 原始报告：WORKBUDDY_REPORT.md（已真实Git提交并回读）
- 审计结论：**81/100，CONDITIONAL_ACCEPT**。可作为F2选型及试验设计初稿，不代表插件已安装、代码已运行或生产系统已通过测试。
- 审计方法：对照WorkBuddy原文、R01审计及CodeBuddy/GitHub/GNU官方公开资料；本轮ChatGPT确实通过GitHub连接器读写本实验分支，但**没有独立远端Shell复现WorkBuddy自述的37项命令**，不把其自述“已实测”冒充双人实测。

## 一、固定量表与评分

| 维度 | 满分 | R02 | 扣分理由 |
|---|---:|---:|---|
| 来源与事实证据 | 25 | **22** | 37项EVIDENCE_LOG、路径、版本和负例证据丰富；缺关键原始stdout、文件内容哈希、第三方独立运行复核，部分“已实测”其实是文档读取 |
| 工厂战略契合度 | 20 | **18** | 围绕开源解构、Markdown任务合同、多Agent盲测、CI门禁、桥接器可靠性；但优先级与实际环境“无git/无docker/无扫描器”的阻塞关系仍需重排 |
| Skill/Plugin使用技巧与可执行性 | 20 | **16** | 21组候选、Top5命令来源和授权边界较具体；尚未安装/调用，个别权限、工具隔离建议存在严重误解 |
| 五案例可复现性 | 20 | **15** | 每例均含目标/前提/输入/输出/正反测试/回滚/成本，较R01完善；但案例C安全隔离不成立、案例B权限过宽、案例A许可证判断失准，所有案例未运行 |
| 风险、成本、限制及真实性 | 15 | **10** | 诚实披露未安装、价格未核实、缺依赖；但工作区隔离误当安全边界、GPL/AGPL一刀切和高权限headless命令需要P0/P1纠正 |
| **合计** | **100** | **81** | **研究质量良好，有条件接受；实施就绪度不足** |

**比较限制**：R01 F1评分70/100、R02 F2评分81/100，研究对象不同、复杂度不同，不构成“同厂提升11分”的证据。R02是F2第一次基线，真正同厂对比从R12开始。

## 二、已核验的关键事实与证据等级

1. **CodeBuddy确有原生定时任务**：官方scheduled-tasks文档支持 /loop、CronCreate/CronList/CronDelete、持久化任务、daemon接管和跳过重叠运行。R02明确在E25/E26/E30纠正了R01错误。官方：https://www.codebuddy.cn/docs/cli/scheduled-tasks
2. **插件市场与安装状态不可混同**：官方说明Marketplace可发现插件，但install/enable/registry/cache各有不同语义；R02列出209个候选目录及0安装，是WorkBuddy本机检查的自述证据，不能从官方文档独立证实其机器实时数量。官方：https://www.codebuddy.cn/docs/cli/plugin-marketplaces 和 https://www.codebuddy.cn/docs/cli/plugins-reference
3. **GitHub连接器权限是按执行环境独立的**：ChatGPT本轮确实使用GitHub连接器读写实验分支；不能据此推定WorkBuddy本机GitHub MCP已经授权。R02 E10的PAT是该市场插件manifest配置方式，不能泛化为GitHub所有集成只能用PAT。官方GitHub App授权亦可按仓库范围配置：https://docs.github.com/en/rest/apps/installations
4. **headless权限需要收紧**：官方明确非交互 -p/-y 和 permission mode 行为；-y加上宽泛Bash权限不是沙箱，最小权限自动化建议dontAsk+明确allow/deny并隔离执行环境。官方：https://www.codebuddy.cn/docs/cli/headless 与 https://www.codebuddy.cn/docs/cli/permission-modes
5. **Worktree不是安全沙箱（P0）**：官方Worktree FAQ明确说明子代理在文件层面隔离，但权限与主Agent相同，理论上可操作worktree外的文件。R02案例C写“Agent_i只可见dir_i与题目、--add-dir限定”，不成立；--add-dir是扩大受信目录，不是强制访问边界。官方：https://www.codebuddy.cn/docs/cli/worktree 与 https://www.codebuddy.cn/docs/cli/permissions
6. **GPL/AGPL并非一律禁止复制（P1）**：R02案例A将“GPL/AGPL依赖→禁止直接复制”当通用规则，过度简化。GPL允许在遵守许可证条件下复制、修改和再分发，AGPL另有网络交互义务；需按组件/传播方式/兼容性/商用场景具体审查。GNU官方：https://www.gnu.org/licenses/gpl-faq.en.html

证据级别说明：上述官方资料核验为“公开官方文档确认”；WorkBuddy的37项CLI输出、环境中git/docker/uv缺失、插件目录数、版本与hooks均属于“WorkBuddy自述的远端检查”，没有ChatGPT独立Shell执行证据；本轮GitHub文件存在与读写是ChatGPT连接器真实验证。

## 三、重大问题与整改优先级

### P0-1：多Agent盲测隔离设计不满足安全/公平要求
原文案例C：“Agent_i 只可见 dir_i 与 FROZEN_TASK.md；--add-dir 限定”。官方说明worktree仅用于防冲突，不能阻止越目录访问；--add-dir扩展信任范围。整改：每个Agent使用独立容器/VM或独立权限凭据、只读题目挂载、无其他Agent答案路径、隔离网络/进程，评审再匿名化；若无法提供安全隔离，标为“协作式隔离、非盲测防作弊”。验收：负例尝试读取他人目录应被系统权限拒绝（不是提示词拒绝），有实际访问控制日志；当前无docker，应标BLOCKED而非可实施。

### P0-2：无人值守写入命令授权过宽
案例B给出 codebuddy -p ... -y --permission-mode acceptEdits --allowedTools "Bash,Read,Edit,Write"，并用Bash(git push)禁令防推送。这不足以建立完整仓库/命令安全边界，广泛Bash可通过其他命令触发写入/网络行为；GitHub MCP权限也要单独控制。整改：最小化允许工具、使用dontAsk+精确allow/deny、只读源仓库与临时工作区、独立GitHub App最小仓库权限、PR创建人工审批。验收：故意尝试git push、访问其他目录、输出凭据，全部被执行环境阻断且留日志；不能仅靠提示词/一条disallowedTools规则。

### P1-3：许可证结论过度简化
案例A把GPL/AGPL一律列为“禁止直接复制”。整改：建立 SPDX/许可证版本、复制/修改/链接/再分发/网络提供服务场景的许可矩阵，未知许可默认停止代码复用但允许合理的只读分析；复杂组合须法律审查。验收：至少MIT、Apache-2.0、GPLv3、AGPLv3、无许可证五类测试样例，输出具体义务而非绝对禁止。

### P1-4：工具真实可运行性仍有硬阻塞
WorkBuddy报告E21称云端无git、uv/uvx、docker和扫描器，因此工作包A/B/C/D大量命令无法在其当前环境直接运行。整改：先提供“零安装只读GitHub API”方案与“经审批补齐依赖”方案，明确哪些案例无需本机git，哪些完全阻塞。验收：每案列出执行环境检查、缺失依赖、替代路径、人工授权关口；不能把方案命令算成运行成功。

### P1-5：门禁测试的100%覆盖与真实能力需要分开
案例D要求负例检出率100%，但仅给出三类样例且尚未安装扫描器；“AKIA...”字符串也不能证明真实密钥检测覆盖。整改：使用合成密钥/安全测试夹具，定义可复现样本集、误报率、漏报率、阻断结果、扫描器版本；不要使用真实凭据。验收：每类至少3个正/负样例及实际CI阻断日志，未运行则NOT_TESTED。

### P2-6：优先级/商业价值需重排
报告将github、安全扫描、chainguard、PR审计、CI模板列为Top5，但本环境缺git与运行时，且未对GitHub现有ChatGPT连接器和CodeBuddy插件的实际授权/运行成本做量化比较。建议优先验证“GitHub只读读取+Markdown合同+静态审计+可追溯提交”，再逐步引入安全Hook与CI发布。

## 四、WorkBuddy五案例逐案评价

| 工作包 | 结论 | 必须补强的验收 |
|---|---|---|
| A 开源仓库解构 | 方向可行，LICENSE/SBOM-lite/commit溯源有价值；许可证一刀切错误 | 提供真实冻结commit、依赖层级许可证矩阵、缺失许可与私有依赖处置；非标准SBOM不得冒称标准 |
| B Markdown合同→PR | 对无人软件工厂高度契合，但headless命令授权过宽、PR审批与自动化边界不清 | 最小权限工作区、契约测试失败阻断、Git提交SHA+回读、不得越权推送 |
| C 多Agent盲测 | 流程设计不错，但worktree不能证明安全隔离，当前环境无git/docker | OS级隔离、答案不可见负例、冻结测试哈希、匿名化和独立评审；缺隔离即不宣称盲测可信 |
| D 安全供应链门禁 | 负例驱动值得保留，但实际扫描器未装、100%只是设计目标 | 合成样本、版本化检测规则、漏报/误报、CI真正block而非warn、回滚日志 |
| E 桥接器可靠性 | 最贴近当前系统，五类失败模型合理 | 固定只读源码快照、事件序列/幂等键、模型切换interrupted、重试去重、Git写入回读；无源码只可提出测试计划 |

## 五、ChatGPT独立设计的五个可实施实验（均为方案，尚未执行）

1. **GitHub公开仓库溯源解构**：输入公开仓库owner/repo+固定commit；用已连接GitHub只读读取README、LICENSE、manifest、目录；输出ARCHITECTURE.md、DEPENDENCY_MATRIX.md、LICENSE_DECISION.md、SOURCE_LOCK.md；负例为缺许可证/版本不一致/二进制文件不可读；验收所有架构断言带文件路径与commit，缺授权不得复制；不依赖WorkBuddy本机git。
2. **Markdown合同驱动的安全PR流水线**：输入CONTRACT.md(AC1–AC5)与隔离分支；CodeBuddy候选feature-dev、pr-review-toolkit、GitHub连接器，独立测试runner；输出PATCH.diff、TEST_RESULTS.txt、PR_REVIEW.md、READBACK.md；负例包括测试失败、越权路径、错误分支、失效授权；验收所有AC有自动测试映射、未经批准不发布，失败保留证据；先在沙箱试验。
3. **三Agent独立编程盲测**：输入冻结题目、隐藏测试和评分规则哈希；每Agent使用隔离执行身份与容器/VM，代码互不可见；输出每Agent匿名解答、测试原始日志、SCOREBOARD.md；负例跨目录读取与共享缓存泄漏必须被OS权限阻断；验收盲测可重复，无法隔离则仅做普通并行对比。
4. **供应链门禁校准实验**：输入含合成凭据、已知脆弱依赖和无害代码的夹具；候选security-scan/chainguard/CI；输出GATE_MATRIX.csv、FALSE_POSITIVES.md、RULE_VERSION.md；正负样本各至少3个，记录误报/漏报与真正阻断；未安装时仅允许编制夹具和协议，不可宣称门禁通过。
5. **桥接器中断恢复与Git幂等实验**：输入固定Job ID事件流（submit→queued→running→interrupted/done→Git commit→readback）；使用独立模拟器/测试分支，不碰生产桥接器；输出EVENT_LOG.jsonl、DEDUP_REPORT.md、STATE_TRANSITION.md；注入超时、模型切换、重复submit、Git提交成功但回读失败等负例；验收同一轮不重复派单，丢失响应能以Job ID恢复，提交与回读状态独立记账。

## 六、V2.0跨厂自适应执行验收

本轮的反馈来源是R01/F1的通用方法教训，不是F2历史基线。R02反馈包确实已提交Git，R02 WorkBuddy原文§⑦也逐项回应。

| 调整 | 真实响应证据 | ChatGPT判断 | 下轮验证要求 |
|---|---|---|---|
| M1 官方文档/版本优先 | E25/E26/E30修复“无scheduler”；E24对“无GitHub Actions专章”限定范围 | **已解决该具体错误；通用有效性仍待更多轮验证** | R03对重要平台功能附版本/官方链接，不作无范围否定 |
| M2 能力边界+命令证据 | §2.1列21组候选；§2.2 Top5语法；§2.4分Agent/MCP/CI/部署/定时器；E29发现help与实际CLI冲突 | **部分有效**：显著改进证据透明度，但案例C仍把worktree误当访问控制 | R03增加“安全隔离 vs 工作区隔离”反例核查、至少一条CLI负例 |
| M3 五案例负例/回滚 | §④五个工作包均含异常测试、输出、回滚与费用未知标记 | **形式已落实，真实执行效果NOT_TESTED** | R03对每例增加“阻塞依赖/运行状态/最小验收样本”，不因字段完整宣称可运行 |

**效果判定**：R02方法遵循度高于R01文本，但跨工厂分数不可归因。仍发现worktree权限边界和许可证过度限制两个新问题，说明改进不是单向、自动、保证成功的。

## 七、传给R03/F3的三项研究方法改进

- **M1（保留）**：任何“平台不支持/只能/自动保证”结论必须附官方文档+版本+已验证范围；至少8项重要能力断言有可核验出处。
- **M2（强化）**：工具能力分为“生成/编排/实际执行/权限隔离/生产发布”五层；每个游戏制作Skill标明是否仅生成素材/脚本、是否真正运行引擎与构建。若涉及插件权限、Agent沙箱、游戏资产授权，必须提供反例检查，禁止把目录隔离当安全沙箱。
- **M3（强化）**：五个F3案例分别给出固定输入、可观察输出、正反测试、成本/许可、回滚、**执行环境阻塞与实际运行状态**；至少一个案例需覆盖确定性模拟/随机种子重放，避免“世界不撒谎”被模型幻觉破坏。

**给R03的研究方向**：F3游戏与互动体验工厂应重点比较游戏引擎Skill/插件、代码与关卡生成、游戏数值/模拟、资产流水线、自动化试玩、打包发布及知识驱动玩法。可用WishTree Discover的IceCube主题作为案例背景，但不能假称已有引擎或插件授权。最多继承上述三项方法，不能复制F2业务方案。

## 八、审计结论与下一步

**81/100，CONDITIONAL_ACCEPT**：F2研究质量较R01的表达方式明显更规范，尤其证据日志、插件状态分层和五案例结构；但无安装/执行验证，且多Agent安全隔离与headless权限两项P0问题必须在实施前修复。R12再次研究F2时，必须把本审计所有P0/P1、五例评价与分项评分完整反馈给WorkBuddy，逐条对比是否解决；不能仅依据分数升高宣布RSI有效。

本轮未安装插件、未授权第三方MCP、未修改桥接器或任何生产代码。