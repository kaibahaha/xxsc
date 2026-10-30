# R11 F1 API与模型服务工厂｜同厂R01定向整改委托书
- 实验 FACTORY10-SKILL-24H-20261030；R11为计划Phoenix 2026-10-29 20:00/北京2026-10-30 11:00；本次补跑，按计划轮次仍为R11/F1，不改变后续F2/R12。
- **同厂旧版R01**：WorkBuddy Job `c901454bfc4042c3`，完整报告 `rounds/R01/WORKBUDDY_REPORT.md`、独立审计 `rounds/R01/CHATGPT_AUDIT.md`、状态 `rounds/R01/STATUS.md` 均已实际Git回读；R01 **70/100**（证据21/25、战略16/20、技巧12/20、五案例12/20、风险9/15）。R01 ADAPTATION不存在（404），不得虚构。R01是F1历史基线，不得以R10 F10报告替代。
- **保留优点**：R01给出CodeBuddy v2.177.0、市场/已安装/第三方授权分层，列出本地CLI `plugin list`/ `mcp list`及五类F1业务案例，原文约13933字；这些属于WorkBuddy自述远端CLI，非ChatGPT独立Shell复现。保留能力矩阵、明确未安装、官方文档优先及多模型安全合规>正确性>截止时间>成本的策略。

## R01具体缺陷→修复动作→官方核验→验收标准
1. **P0-1 原生调度错误否定**：R01原文断言“CodeBuddy无内建scheduler”，与官方 `https://www.codebuddy.cn/docs/cli/scheduled-tasks`、`/loop`、CronCreate/CronList/CronDelete、持久化/会话级任务及API文档相矛盾。原因是仅凭市场列表/记忆否定内建功能。R11必须读取当前官方文档+CLI版本/help，列出调度模式、任务寿命、重叠触发、鉴权及桥接限制，给至少一个反例。**验收**：明确纠正旧断言并提供URL/版本/命令/证据，不把官方存在误写成当前桥接环境已授权。
2. **P0-2 Agent入口误当模型推理网关**：R01案例A把`codebuddy --serve`视作通用LLM多模型路由。官方 `https://www.codebuddy.cn/docs/cli/http-api`说明Agent Runs/ACP；LiteLLM `https://docs.litellm.ai/docs/proxy/architecture`是独立模型网关候选。R11必须提供Agent控制面、LLM推理面、租户鉴权、成本账本四层架构图/表及实际API契约，禁止无证据声称OpenAI Chat Completions兼容。**验收**：列出实际端点/请求响应样例、与模型网关接口差异，任何未部署组件标PLAN_ONLY。
3. **P0-3 models.json并非多租户硬预算**：R01案例C称“为每租户配独立apiKey实现额度隔离”，未实现可信身份绑定、原子预算账本、并发限流、重试去重；参考 `https://www.codebuddy.cn/docs/cli/models`、`https://docs.litellm.ai/docs/proxy/users`。R11需设计服务端fail-closed预算，说明PostgreSQL/Redis或等价原子账本、预算保留/结算/并发超限/429回退。**验收**：≥10条并发/故障负例，给伪代码/SQL事务或实际脚本、不可把静态配置当已实现硬上限。
4. **P1-4 密钥与CLI**：R01暗示`models.json`明文apiKey且部分`--fallback-model`、`security-scan --auto`语法未经help确认。官方models支持环境变量引用。R11须给`--help`或manifest精确出处，区分只读实测与示意；示例只用占位符，绝不读取或输出真实凭据。**验收**：Top5每个候选给manifest/官方链接、安装状态、语法验证级别和授权要求。
5. **P1-5 费用与SLO/供应链**：R01将CLI/插件免费概括过宽；D trace仅进入Collector无跨Job关联，E灰度缺阈值与回滚时延。R11须区分插件许可/模型token/托管/CI额度/运营费；没有官方价格就UNKNOWN；定义trace_id/job_id/commit SHA、P95、429/超时、脱敏和签名/OIDC最小权限。**验收**：明确计费来源日期、≥30条端到端追踪验收方案、灰度5→20→100和故障回滚门槛。

## R01五案例逐一整改（逐案回复，不可省略）
- **A 四算力池路由**：保留四算力池；输入10类数据标签+40请求测试，区分Agent/LLM网关，输出`ROUTING_POLICY.md`+`ROUTE_TESTS.jsonl`；负例敏感外发/429/超时/递归回退；按模型价格与token记账，失败退回只读单模型。
- **B API契约测试**：保留OpenAPI；输入`openapi.yaml`和旧客户端，输出schema diff/compat matrix；覆盖400/401/403/409/429/500、幂等冲突与破坏性变更；无授权不部署，失败回滚签名schema。
- **C 限流计费**：重做；输入工厂/租户ID、RPM/TPM、预算和并发，输出`LEDGER_RECONCILIATION.md`；注入并发竞态、重试重复计费、DB断连；预算fail-closed，明确数据库/缓存费用和权限。
- **D 可观测与安全**：保留但补齐；输入trace_id/job_id/model_id/Git SHA，输出`TRACE_AUDIT.jsonl`、脱敏日志；30条端到端链路、PII泄露负例，Collector不可达时降级到安全最小日志。
- **E 安全发布/灰度**：保留；输入PR/依赖锁/SBOM/OIDC策略，输出`RELEASE_MANIFEST.md`、签名/回滚日志；恶意依赖、过宽权限、5%灰度P95越线负例必须阻断；部署动作PLAN_ONLY不执行。
五案例每个都必须给目标、实际候选Skill/Plugin、输入、操作/精确命令、输出、正反测试、验收阈值、权限与费用、回滚、RUN/PLAN/BLOCKED和依赖阻塞。不得仅复述旧案。

## 跨厂通用方法迁移（不是F1旧版）
- 最近完成R10/F10完整研究76/100（18/19/15/15/9），已回读其原报告和独立审计；观察到**完整正文可交付，但自述RUN脚本未在本实验Git提供**、NO FAKES Act法律状态误判、外部官方来源与本地缓存混计。R02/F2 81分仍有worktree误当安全隔离、headless广泛Bash授权；R03/F3 83分仍缺完整可重放源码。以上仅迁移研究方法，不复制其他工厂业务结论。
- **M1**：所有重要能力/法律/费用断言先查现行官方文档+版本；外部官方来源、本地CLI、市场缓存分开计数；否定性断言附反证检查。
- **M2**：凡声称RUN必须在报告正文附最小可运行源码+固定输入+原始stdout/exitcode/版本；否则SELF_REPORTED_NOT_REPRODUCED，不能仅给私有路径或另一实验路径。
- **M3**：严格区分工作区隔离/OS权限/模型服务/Agent控制面/账号授权；每例提供安全负例、成本、回滚及执行状态。
本轮深挖目标：修复R01三项P0、给可复现的网关与预算模拟而非空泛产品清单；目标≥10条官方外部来源、≥12候选及Top5可核语法、五案例字段齐全、≥2个报告内可复现实验、0条未经证据支持的“已部署/已授权”。
**必须输出对照表：R01问题原句→本轮修订→官方/CLI/工件证据→已解决/部分/未解决。** 明确本轮同厂对照评分和错误复发只能由ChatGPT在报告完成后独立审计计算，WorkBuddy不得自评分或自称提升。不得安装插件、切模型、授权、写其他实验、读/输出密钥、改生产服务。