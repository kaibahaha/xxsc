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