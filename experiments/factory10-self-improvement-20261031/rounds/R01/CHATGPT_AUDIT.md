# R01 F1｜ChatGPT独立审计（证据完整性优先）
- Experiment: FACTORY10-SELF-IMPROVEMENT-20261031
- Job: aab758d7c33d4631
- WorkBuddy server: DONE；远端自述已产出382行报告，MCP只返回1517字摘要。
- Git source: rounds/R01/WORKBUDDY_REPORT.md为**实际MCP返回摘要**，已独立回读；不是远端382行全文。
- 正式评分：**NOT_EVALUABLE**。固定权重证据25/战略20/技巧20/案例20/风险15，但未取得全文和五案例具体命令/证据，不虚构五维分数；旧实验70/100不作为本轮分数或改善Δ。
## 一、对实际返回摘要的独立核查（截至2026-10-31）
| 问题 | WorkBuddy摘要主张 | ChatGPT独立核查 | 判断 |
|---|---|---|---|
| SF01 原生调度 | v2.57.0已支持定时，v2.156.0 daemon持久接管，v2.168.3默认30天 | 官方v2.57.0 https://www.codebuddy.cn/docs/cli/release-notes/v2.57.0；v2.156.0 https://www.codebuddy.cn/docs/cli/release-notes/v2.156.0；v2.168.3 https://www.codebuddy.cn/docs/cli/release-notes/v2.168.3 均支持。注意总览 https://www.codebuddy.cn/docs/cli/scheduled-tasks 仍称循环3天，存在文档/任务类型或版本差异，不能混用。 | **核心纠偏已证实；具体有效期按任务类型/版本待澄清** |
| SF02 Agent入口≠LLM推理网关 | --serve暴露Agent REST/ACP，非通用 /v1/chat/completions | 官方 https://www.codebuddy.cn/docs/cli/http-api 列Agent接口；https://docs.litellm.ai/docs/proxy/architecture 列模型推理代理的/chat/completions、预算、路由。 | **核心纠偏已证实；未实测本机接口** |
| SF03 models.json≠多租户硬预算 | 需独立租户身份与DB预算 | https://www.codebuddy.cn/docs/cli/models 是模型配置与上游url；https://docs.litellm.ai/docs/proxy/users 明确无DB预算不生效且fail-open。 | **核心纠偏已证实；未实测预算故障注入** |
| SF04 环境变量密钥 | 声称已纠正 | https://www.codebuddy.cn/docs/cli/models 支持 ${VAR_NAME} 引用和600权限。摘要未给实际样例。 | **官方能力确认；整改细节不可核** |
| SF05 插件/价格/命令 | 自称明确标UNVERIFIED | https://www.codebuddy.cn/docs/cli/plugin-marketplaces 区分install与enable，插件状态必须查registry/cache；摘要未提供原始help或费用来源。 | **不可核** |
| SF06 五案例负例、追踪、灰度 | 自称5例已补齐 | 382行正文未返回，不能查五案例是否包含真实输入/输出/负例/回滚/量化指标。 | **不可核** |
## 二、SAME_FACTORY_REMEDIATION（历史参考，不是本实验R-10）
- SF01: PARTIAL（旧错误已纠正，但30天与3天需按任务类型核对）；SF02: PARTIAL（架构正确，接口实测未见）；SF03: PARTIAL（架构正确，预算fail-closed未实测）；SF04/SF05/SF06: NOT_VERIFIABLE（缺全文）。
- resolved_count: 0（严格口径：未取得完整整改证据，不将部分纠偏记为完全关闭）。
- recurred_count: UNKNOWN；新增缺陷：**P0-DELIVERY-01：研究正文仅留远端，MCP返回摘要，ChatGPT无法逐条审计、正式评分与Git完整归档**。
- historical_score_delta: NOT_COMPARABLE；同厂正式评分：NOT_EVALUABLE。
## 三、跨厂方法迁移：R02 F2必须真实注入并验证
- M1 **交付完整性优先**：WorkBuddy必须直接返回完整正文（如超长，返回可验证分段并保证ChatGPT可取到全部），不得只说“已保存远端”；指标：MCP返回可读正文覆盖100%、关键主张官方链接可核≥90%。若工具返回有长度上限，标PARTIAL而非伪装完整。
- M2 **版本差异和负例双验收**：每项重要CLI/API主张核对官方版本与文档冲突；五案例每案包含至少一个失败注入与回滚判据；指标5/5，未实际执行的仅称方案。
## 四、独立评价结论
本轮**云端任务实际完成、派单反馈实际注入、Git四项已可回读**，但**研究全文尚未交付ChatGPT**，因此“研究完成”≠“独立审计完成”。下轮优先补齐R01远端全文，随后才能评分、复核历史六缺陷的真正修复效果；不因自述“零违规”直接认定生产系统无变化。

---
# R01 F1 完整报告追回后的正式复核（本节取代前述NOT_EVALUABLE最终状态；保留原审计历史以追溯）
- Recovery job: `93de654703984b20`，只读读取原远端报告，无重新研究；MCP返回原文382行、21275字符，Git WORKBUDDY_REPORT.md更新commit `caa912f35febeaf4aec6cb3d0f8bf1abb7b72f6d`，blob `c6d0137ad338f031399c065190621be0d9e65d43`，逐字回读VERIFIED；原1517字摘要保留为WORKBUDDY_SUMMARY_ORIGINAL.md。
- **正式评分79/100**：证据22/25、战略18/20、操作技巧14/20、五案例14/20、风险真实性11/15。状态CONDITIONAL_ACCEPT_FOR_RESEARCH，不代表生产实现。旧实验F1 R01 70/100仅历史参考；因研究范围/证据口径不同，不能机械认定+9分为同厂因果改进。

## 五维评分依据
|维度|得分|独立理由|
|---|---:|---|
|证据25|22|382行完整正文、9条一手URL、随包CLI文档与命令节选；但未提供完整原始stdout/版本化SHA，个别版本/端点/价格推断未独立实测。|
|战略20|18|Agent控制面/推理网关/模型供给/治理分层准确契合F1，能连接FactoryOS单槽桥接；L2及预算未部署。|
|技巧20|14|L1/L2请求示例、预算账本、可观测和灰度路径具体，但L1请求体及响应码未实际调用，`cosign verify --key oidc ...`是不能直接复跑的占位示意，部分模型重试参数跨层混用。|
|五案例20|14|A-E均具输入/输出/负例/回滚/验收；均为设计级，未执行，C的fail-closed只是建议，E签名命令和D遥测降级假设未验证。|
|风险真实性15|11|区分未安装/未授权/价格UNKNOWN，未触生产；但“CODEBUDDY_IS_SANDBOX变量存在→已受管沙箱”不充分，未证明执行环境的OS隔离；个别工具可用性断言过度。|
|合计|**79**|全文交付已修复；研究质量可评价，实施就绪度不足。|

## SAME_FACTORY_REMEDIATION 历史旧实验六项缺陷独立复核
- SF01 原生调度存在：**RESOLVED（文档概念）**。官方 `https://www.codebuddy.cn/docs/cli/scheduled-tasks`、版本发布说明支持CronCreate/loop；任务有效期依类型和版本，不把3天/30天混淆；运行态未实测。
- SF02 `--serve`不是通用LLM推理网关：**RESOLVED（协议边界）**。官方 `https://www.codebuddy.cn/docs/cli/http-api` 和 `https://docs.litellm.ai/docs/proxy/architecture`；L1/L2实际请求未实测。
- SF03 models.json不能提供租户硬预算：**RESOLVED（配置边界）**。官方 `https://www.codebuddy.cn/docs/cli/models` 和 `https://docs.litellm.ai/docs/proxy/users`；LiteLLM无DB时预算/虚拟key行为需按具体机制区分，fail-closed尚未实现。
- SF04 环境变量密钥：**PARTIAL**。官方支持`${ENV_VAR}`，但本轮未实际验证凭据轮换和权限；安全示例有。
- SF05 插件/价格/命令：**PARTIAL**。未核价格标UNVERIFIED正确；但报告§5.5将`--fallback-model`视作未在CLI出现，而旧实验F2 E33有`codebuddy --help`报告此选项，需重新核验版本与模式（旧实验称仅`--print`有效），不能据“未在文档找到”否定存在。
- SF06 五案例负例与回滚：**PARTIAL**。5/5已提供负例和回滚字段，但缺真实执行；E的`cosign verify --key oidc ...`是非可执行示例，D的遥测中断本地100%落盘未经验证。
- strict resolved_count=3/6（概念纠偏层），partial_count=3/6；recurred_count=0（旧三P0错误原句未复述）；new_issues=3组（fallback-model核查冲突、签名/OIDC示例不可复跑、环境隔离与跨层参数未经实测）。
- **同厂评分Δ：NOT_COMPARABLE**（旧70分为另一实验、另一版报告）；新实验R01正式基线79/100，R11再次研究F1时以此为基线逐项整改。

## 与R02 F2跨小时迁移的时序
- R02启动前R01全文确实尚未回传，故R02以“全文缺失”作为M1交付改进基线是合法、可核验的；R02完成后MCP完整返回15843字符，Git回读通过，M1在交付层判EFFECTIVE。
- 本R01全文追回发生于R02研究完成**之后**，不可倒填为R02派单前已经取得全文，也不能改写当时的反馈证据。
- R11同厂专项重点：①`--fallback-model`CLI真实版本语法；②LiteLLM DB故障预算fail-closed的隔离模拟；③E的Sigstore/cosign签名命令与OIDC信任域；④五案例真实只读/模拟验收。
