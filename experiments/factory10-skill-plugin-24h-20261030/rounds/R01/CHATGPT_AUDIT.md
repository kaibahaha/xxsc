# R01 F1 API与模型服务工厂｜ChatGPT独立审计（正式评分）

> **审计状态：COMPLETED / CONDITIONAL_ACCEPT，综合评分70/100。** WorkBuddy Job `c901454bfc4042c3` 已返回完整原始研究报告（已另存WORKBUDDY_REPORT.md并回读），ChatGPT对照官方文档独立核验。分数只代表研究报告质量，不代表插件已经安装或五个案例已经运行。

## 一、工厂目标与验收口径

F1不是简单“接几个模型API”，而是统一服务契约、访问控制、模型路由、配额预算、故障隔离、可观测性、供应链安全、持续交付的基础平台。优先级：安全合规 > 正确性 > 截止时间 > 成本；云端免费/付费模型与本地模型混合路由时，必须对数据分级与供应商许可做独立授权检查。**ChatGPT侧可调用GitHub连接器，不等于WorkBuddy环境自动拥有GitHub OAuth；Skill市场缓存不等于已安装。**

## 二、独立事实核查（已访问官方来源；尚非本地部署实测）

| 技术能力 | 独立来源与核查事实 | 判断与风险 |
|---|---|---|
| LiteLLM Proxy | 官方架构文档描述虚拟密钥、预算检查、RPM/TPM限制、模型路由/重试/回退以及PostgreSQL/Redis角色：https://docs.litellm.ai/docs/proxy/architecture | 适合作为F1的候选网关，不等于当前环境已安装 |
| LiteLLM预算 | 官方预算文档明确预算依赖数据库；无数据库时部分全局预算配置可能fail-open，无法作为成本硬上限：https://docs.litellm.ai/docs/proxy/users | **关键阻断项**：不能把无DB的budget设置视作可验证硬限额 |
| LiteLLM虚拟密钥 | 官方虚拟密钥文档提供密钥权限、默认预算和上限策略：https://docs.litellm.ai/docs/proxy/virtual_keys | 密钥只进服务端秘密存储，不能放Git或Agent报告 |
| OpenTelemetry | Python官方文档区分API与SDK，应用发出遥测需初始化SDK和Exporter：https://opentelemetry.io/docs/languages/python/instrumentation/ | 安装SDK不等于完成全链路trace；需关联request_id、model_id、cost |
| GitHub Actions OIDC | GitHub官方文档说明云端短期令牌交换、避免长期云密钥：https://github.com/github/docs/blob/main/content/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-cloud-providers.md | 需云端信任策略和最小权限，不能仅设置id-token:write就认定已授权 |

**真实性分级**：本表均为官方文档可核实的技术路线（D2）；没有对用户云端实际部署、模型额度、计费价格、权限进行实测（非D1）。是否属于WorkBuddy市场现成Skill/插件，必须以其实际manifest/SKILL.md检查结果为准。

## 三、ChatGPT独立设计的五个F1实战案例（供WorkBuddy报告逐项对照）

### 案例1：四算力池多模型路由与故障回退
目标：对一组统一的 /v1/chat/completions 请求，在本地GPU、本地CPU、免费云、付费云四类后端间按策略路由。工具候选：LiteLLM Proxy/自建路由策略、FastAPI、pytest、GitHub CI。输入：10类请求标签（敏感/公开、低/高复杂度、时限、token预算）；输出：`routing_policy.yaml`、`routing_test.json`、`failover_log.jsonl`。步骤：先定义数据分级和允许后端矩阵，再定义质量门槛和deadline，再定义成本兜底；模拟超时、429、模型返回不合规；验证“敏感任务绝不外发”“付费回退须受预算限制”“重复请求不触发递归调用”。验收：至少40条路由用例全部可解释，敏感数据越界次数=0，故障回退有明确原因码和幂等ID。风险：不同模型格式不兼容、超时后重复计费；回滚为单模型只读模式。

### 案例2：API契约与兼容性回归
目标：统一 OpenAPI v3 契约，避免前端和Agent调用接口漂移。工具候选：FastAPI、OpenAPI schema、pytest、Schemathesis（需确认版本和授权）。输入：`openapi.yaml`及20条边界样例；输出：`contract_test_report.md`、`compatibility_matrix.csv`。步骤：定义成功/错误响应、限流、超时、幂等键和request_id；生成契约测试；用旧版客户端对新版服务做回归。验收：HTTP 400/401/403/409/429/500路径有确定行为，破坏性变更必须阻断CI；不能只用happy-path 200证明兼容。失败回滚：恢复上一已签名API schema和容器镜像。

### 案例3：多租户限流、预算与计费账本
目标：对十大工厂设置工厂级和任务级预算上限。候选：LiteLLM Virtual Keys + PostgreSQL + Redis + 账本服务。输入：工厂ID、任务ID、RPM/TPM、每日预算、最大并发；输出：`budget_reconciliation.md`、`usage_ledger.csv`。步骤：设置密钥权限与配额，模拟并发突发/429/预算耗尽/重试，核对提供商账单与本地用量。验收：并发压测下不越过硬上限（允许明示结算延迟的误差边界），预算耗尽必须fail-closed；**未连接PostgreSQL时不能宣称LiteLLM预算有硬限制**。失败策略：停止付费路由、保留本地模型路径和账本证据。

### 案例4：请求级可观测性与SLO
目标：追踪每条任务从ChatGPT派单到WorkBuddy、模型调用和Git交付的完整因果链。候选：OpenTelemetry Python SDK、结构化日志、Prometheus/Grafana（均需独立部署）。输入：`trace_id`、`job_id`、`factory_id`、`model_id`；输出：`slo_report.md`、延迟分位数、失败归因、队列深度。步骤：贯穿统一trace_id，记录排队时长、模型推理时长、写Git时长和回读校验；使用测试任务模拟失败与超时。验收：抽样30条任务可从派单追溯至提交或失败终点，P95延迟有清晰分母，日志不含token/原始敏感prompt。失败策略：保留最小审计日志而关闭高成本遥测导出。

### 案例5：安全发布与供应链防护
目标：对API网关、SDK和MCP插件建立受控发布流程。候选：GitHub Actions、OIDC、依赖扫描、容器镜像签名、分支保护。输入：PR、测试报告、依赖锁文件、发布清单；输出：`release_manifest.md`、SBOM、签名和回滚标记。步骤：CI执行静态检查/单测/契约测试/密钥扫描，生成不可变版本；OIDC换取短期部署权限；灰度5%→20%→100%，以错误率和P95阈值控制推进。验收：任何硬编码凭据或契约破坏均阻断发布；故障可一键恢复上一镜像，审计链可定位提交SHA。风险：错误授权与越权部署；未完成最小权限策略前只允许演练环境发布。

## 四、WorkBuddy报告100分正式审计量表

| 维度 | 上限 | 当前评分 |
|---|---:|---|
| 来源与事实证据 | 25 | **21** |
| 工厂战略契合度 | 20 | **16** |
| Skill/Plugin可执行性与具体使用技巧 | 20 | **12** |
| 五个实战案例的可复现性 | 20 | **12** |
| 风险、成本、限制及真实性 | 15 | **9** |
| **总分** | **100** | **70 / 100** |

审计时重点核验：精确Skill名称是否有本地manifest；市场插件是否安装；MCP是否真有OAuth；命令语法是否来自help；费用是否有时间戳；五案例是否给出输入/输出/验收/回滚；是否误把本地功能替代当同SaaS账号访问；预算和数据安全是否fail-closed。缺任何一项都应明确扣分，不能因报告篇幅长就高分。

## 五、执行建议与未核验项

优先级建议：先固化OpenAPI和幂等日志，再做一个本地模型与一个云模型的最小路由；接着引入PostgreSQL预算账本与限流；随后补齐OpenTelemetry链路追踪和CI/CD安全发布。未经实际连接器授权不得直接访问外部账号；未经真实压测不得承诺吞吐、SLA或单次成本。以上是独立核查基线，不是对WorkBuddy报告的最终评价。

**报告状态**：WorkBuddy原文已保存并Git回读。以下为本轮正式审计的主要事实纠偏与案例验收意见。


---

## 六、WorkBuddy原报告逐项独立交叉核验（2026-10-29/30）

**报告优点（已证实的研究动作）**：WorkBuddy通过真实MCP返回13,933字符原始报告，明确区分CLI内置、市场缓存未安装、第三方MCP需授权与理论方案；列出CLI v2.177.0、两个市场、`plugin list`/ `mcp list`为空，并给出插件目录、技能路径、五个不同案例及EVIDENCE_LOG。对“未安装不等于可用”的界限把握较好。这些事实来自WorkBuddy的自述执行日志，ChatGPT没有远端Shell直接复现每条命令，证据等级应为“WorkBuddy执行报告+市场路径”，而非ChatGPT亲自执行。

**重大问题1（可明确证伪）：原报告声称“CodeBuddy无内建scheduler”，与CodeBuddy官方定时任务文档直接冲突。** 官方文档支持`/loop`、CronCreate/CronList/CronDelete、持久化调度，并明确`GET/POST/DELETE /api/v1/scheduled-tasks`。同时文档说明会话级任务随退出清除、durable可持久化、重复触发可能跳过、循环任务3天自动过期。应更正为“原生调度存在，但其持久化、生命周期和桥接环境实际权限需单独验收”。官方依据：
- https://www.codebuddy.cn/docs/cli/scheduled-tasks
- https://www.codebuddy.cn/docs/cli/release-notes/v2.84.0

**重大问题2（架构概念混淆）：`codebuddy --serve`是CodeBuddy Agent应用的REST/ACP入口，不等于一个通用、支持任意客户端OpenAI Chat Completions协议的多模型推理网关。** 官方文档列`/api/v1/runs`、`/api/v1/acp`等Agent接口；不能把其健康检查成功解释为三种模型的通用推理代理和自动路由均可用。F1应将“Agent任务编排入口”与“模型推理/租户计费网关”拆成两层；后者可独立评估LiteLLM或自建网关。官方依据：
- https://www.codebuddy.cn/docs/cli/http-api
- https://docs.litellm.ai/docs/proxy/architecture

**重大问题3（租户隔离与预算）：`models.json`是用户/项目级模型配置，不是多租户计费系统。** WorkBuddy案例C称“为每租户配独立apiKey实现额度隔离”，但没有租户身份绑定、预算账本、并发原子扣减和服务端授权逻辑，无法由配置文件自动提供硬配额。需引入可信身份层、独立密钥与数据库账本、原子限流、成本核算及重试去重。LiteLLM官方明确预算功能依赖数据库，无DB时相关预算可能fail-open：
- https://www.codebuddy.cn/docs/cli/models
- https://docs.litellm.ai/docs/proxy/users

**重要问题4（密钥风险描述不完整）：** WorkBuddy说`models.json`的`apiKey`明文存储，但CodeBuddy官方文档支持`${ENV_NAME}`环境变量引用，建议`models.json`权限600且不要提交真实密钥。报告应优先推荐环境变量/秘密管理，而不是先配置明文再补救：
- https://www.codebuddy.cn/docs/cli/models

**重要问题5（工具与费用证据不足）：** 多个插件只核实manifest/README，尚未验证安装后命令是否真实可执行；`--fallback-model`、`security-scan --auto`等用法应先查具体help；“CLI/插件本身免费”未提供官方授权/许可证和外部服务费用核验。官方插件市场文档说明`install`、`enable`、`reload-plugins`语义不同，必须分别验收：
- https://www.codebuddy.cn/docs/cli/plugin-marketplaces

**重要问题6（安全发布与观测验收缺口）：** WorkBuddy案例D仅要求trace进入Collector，缺跨Job/模型/Git关联与PII脱敏检查；案例E未列明确灰度阈值、回滚时延和签名校验；案例B仅用浏览器工具不能证明OpenAPI schema契约覆盖。OpenTelemetry需要SDK/Exporter正确配置，GitHub Actions OIDC也需云端信任策略：
- https://opentelemetry.io/docs/languages/python/instrumentation/
- https://github.com/github/docs/blob/main/content/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-cloud-providers.md

## 七、对WorkBuddy五个案例逐案验收点评

| WorkBuddy案例 | 审计判断 | 最低补强要求 |
|---|---|---|
| A 多模型路由 | **需重构**：混淆Agent --serve与通用模型推理网关，模型切换不等于策略路由 | 区分Agent入口与LLM Gateway；提供40条策略测试、数据分级、429/超时/幂等测试、成本账本 |
| B API契约测试 | **部分可行**：有脚手架与OpenAPI产物，但“0违约”无覆盖范围定义 | 生成schema差异报告，验证401/403/409/429/500、版本兼容与破坏性变更阻断 |
| C 限流计费 | **不满足生产要求**：models.json不能直接提供租户硬配额 | 数据库+原子计量+身份隔离+并发压测+对账；预算fail-closed |
| D 可观测与安全 | **部分可行**：插件目录证据较好，运行期可观测尚未验 | 30条端到端trace可追溯；敏感字段脱敏；安全门禁失败可重放 |
| E 供应链与灰度 | **方向正确，实施不足**：未给灰度阈值与权限最小化验证 | PR门禁、SBOM/签名、OIDC信任、5%→20%→100%阈值和自动回滚演练 |

## 八、正式评分解释、修复优先级与接受条件

- **证据21/25**：本地市场、文件路径和CLI检查相对扎实；扣4分在于缺关键manifest条目快照/版本hash、个别命令语法未独立验证。
- **战略16/20**：覆盖F1关键领域；扣4分在于把Agent API当模型网关，模型/租户架构分层不足。
- **技巧12/20**：给出了插件命令和路径，但未安装、未执行，且租户隔离/回退机制有未经证实的操作建议。
- **案例12/20**：五例领域覆盖好，然而可复现输入、阈值、负面测试、回滚时序不足，案例A/C有关键架构问题。
- **风险9/15**：有权限边界、密钥与付费风险提醒，但遗漏预算fail-open、内建调度事实与部分供应链/成本约束。

**结论：70/100，CONDITIONAL_ACCEPT（研究素材可用，不能直接作为生产部署手册）。** P0修正“原生调度不存在”的事实错误、拆分Agent API与LLM Gateway、重做多租户硬配额；P1补齐安装命令实测、供应链门禁、价格来源和压测；P2再比较不同插件的商业价值。严禁在此轮自动安装或更改现有服务。

**五个ChatGPT独立补充实战案例**已在本文件第三节给出，且与WorkBuddy五案例逐一形成验收对照；这些同样属于方案设计，尚未实际部署。评分已完成，但业务执行成功率仍为“未实测”。
