# R01 F1 API与模型服务工厂｜ChatGPT独立核查与审计

> 审计状态：**PRELIMINARY / NOT_EVALUABLE**。截至本版提交，WorkBuddy Job `c901454bfc4042c3` 仍运行中、尚未返回报告正文，因此不对其研究质量给分，也不伪造逐项评分。以下是ChatGPT独立核查基线与五个可执行案例。待拿到报告后必须补做逐条核对和正式评分。

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

## 四、待WorkBuddy报告返回后的100分审计量表

| 维度 | 上限 | 当前评分 |
|---|---:|---|
| 来源与事实证据 | 25 | 未评分 |
| 工厂战略契合度 | 20 | 未评分 |
| Skill/Plugin可执行性与具体使用技巧 | 20 | 未评分 |
| 五个实战案例的可复现性 | 20 | 未评分 |
| 风险、成本、限制及真实性 | 15 | 未评分 |
| **总分** | **100** | **NOT_EVALUABLE** |

审计时重点核验：精确Skill名称是否有本地manifest；市场插件是否安装；MCP是否真有OAuth；命令语法是否来自help；费用是否有时间戳；五案例是否给出输入/输出/验收/回滚；是否误把本地功能替代当同SaaS账号访问；预算和数据安全是否fail-closed。缺任何一项都应明确扣分，不能因报告篇幅长就高分。

## 五、执行建议与未核验项

优先级建议：先固化OpenAPI和幂等日志，再做一个本地模型与一个云模型的最小路由；接着引入PostgreSQL预算账本与限流；随后补齐OpenTelemetry链路追踪和CI/CD安全发布。未经实际连接器授权不得直接访问外部账号；未经真实压测不得承诺吞吐、SLA或单次成本。以上是独立核查基线，不是对WorkBuddy报告的最终评价。

**后续补交条件**：查询Job `c901454bfc4042c3` 返回完整正文 → 写WORKBUDDY_REPORT.md并Git回读 → 对照本基线逐项核验、打分和列缺陷 → 更新本文件与STATUS.md并回读。
