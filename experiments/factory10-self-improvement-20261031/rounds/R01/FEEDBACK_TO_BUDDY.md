# R01 / F1 — FEEDBACK_TO_BUDDY（派单前冻结）
实验 FACTORY10-SELF-IMPROVEMENT-20261031；计划北京时间2026-10-31 10:25；F1 API与模型服务；本轮属于新实验BASELINE，不得与旧实验R01混号。跨小时反馈：本次无R00，标NO_PREVIOUS_HOUR，下一轮R02必须以本轮审计为通用方法基线。
## 可核实的同专题历史参考（HISTORICAL_REFERENCE，非本实验基线）
旧实验：experiments/factory10-skill-plugin-24h-20261030/rounds/R01/WORKBUDDY_REPORT.md、CHATGPT_AUDIT.md、STATUS.md；Job=c901454bfc4042c3；旧报告ChatGPT评分70/100：证据21、战略16、技巧12、案例12、风险9。旧报告工作亮点：区分插件市场缓存/实际安装/第三方MCP授权/理论自建；实际列举CodeBuddy CLI及市场路径；报告中列5案例。旧报告内容为历史证据，不代表现行环境事实。
## SAME_FACTORY_DEFECT_REGISTER（旧审计明确指出的缺陷；本轮要求深度整改）
- P0-SF01：旧报告§3称“CodeBuddy无内建scheduler”；旧审计§六问题1依据CodeBuddy官方scheduled-tasks文档确认有 /loop、CronCreate/CronList/CronDelete、scheduled-tasks API。修复：查官方文档，精确区分会话任务/持久任务/自动到期/桥接环境是否实际支持；写出只读验证命令和反例。验收：不得再称无原生调度；列出处和适用版本；不擅自创建定时任务。
- P0-SF02：旧报告§2候选①及案例A把 codebuddy --serve Agent REST/ACP服务称作通用多模型推理网关。修复：从官方 http-api.md 与LiteLLM Proxy官方架构拆出 Agent控制面、OpenAI兼容推理面、策略路由层、鉴权/账本层；给出端点协议对照、最小请求样例和未验证边界。验收：不把 /api/v1/runs、ACP 等同 /v1/chat/completions；路由切换必须区分人工/策略自动。
- P0-SF03：旧报告案例C称 models.json 为每租户配独立apiKey即可实现额度隔离。修复：补租户身份映射、服务端授权、原子RPM/TPM、数据库预算账本、幂等计费、重试和429；查LiteLLM官方预算数据库依赖与fail-open风险。验收：明确models.json仅模型配置，不能宣称多租户硬配额；设计fail-closed故障注入和账本对账。
- P1-SF04：旧报告称models.json apiKey明文存储，未优先给出官方支持的环境变量引用。修复：核对官方models文档，展示只用虚拟占位符的安全样例、最小权限及秘密轮换。验收：无真实token；不建议密钥提交Git。
- P1-SF05：旧报告若干插件只见manifest/README，未实装；--fallback-model、security-scan --auto等语法未证明；“CLI/插件免费”未核官方价格。修复：区分命令已在本机只读实测/仅文档支持/待安装/需授权，提供help或官方URL及日期；未核价格标UNVERIFIED。验收：不得虚构执行与成本。
- P1-SF06：旧报告案例B/D/E缺契约负例、端到端trace关联、脱敏、灰度阈值、回滚时限和OIDC信任边界。修复：给可复跑的样例输入/预期输出/失败注入/量化验收。
## 五个历史案例逐案整改（每案必须返回“旧问题→修复动作→新证据→验收结论”）
A 多模型路由：保留多模型价值，拆Agent入口与LLM Gateway；≥10条可手工复现的路由/429/超时/敏感数据测试，明确计费与回退。
B API契约：补OpenAPI差异和401/403/409/429/500负例、版本破坏性变更CI阻断、样例请求/输出。
C 多租户限流计费：重新设计可信身份+原子预算账本，预算耗尽与数据库故障fail-closed、对账、重试去重。
D 可观测性：跨ChatGPT→MCP→CodeBuddy→Git关联job_id/trace_id；30条trace抽样、脱敏检查和遥测中断降级。
E 供应链/灰度：SBOM、签名、OIDC、PR门禁、5%→20%→100%灰度阈值、回滚SLO、无密钥泄漏验证。
## 本轮强化目标和验收
本轮F1聚焦“云端单槽WorkBuddy MCP稳定链路如何与可插拔模型服务/工厂级预算/插件治理衔接”，不得改变生产桥接器。官方一手证据至少8条，标注来源URL/访问日期/版本；给候选插件/Skill的真实状态与授权/费用；五案例每案目标、输入、工具、最小命令、预期输出、失败路径、回滚、验收、成本及权限。对SF01-SF06逐条作有证据的整改对照表，未实测的只写设计建议。不得安装、授权、切模型、改生产或读取凭据。研究尽量8-12分钟内完成，最多12次网络检索，最多1子代理。
## 下轮跨专题方法迁移预注册
R02 F2可检验的通用方法候选：①每条关键能力同时列“官方证据/本环境执行证据/未验证项”，目标关键主张证据覆盖≥90%；②每个案例必须含至少一个负面测试及回滚判据，目标5/5。只有R01报告和独立审计完成后才可据实际结果确定是否采用，不预先宣称有效。