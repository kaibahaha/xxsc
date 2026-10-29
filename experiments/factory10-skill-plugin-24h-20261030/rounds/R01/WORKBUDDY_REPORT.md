# R01 F1｜WorkBuddy 原始研究报告

- Experiment: FACTORY10-SKILL-24H-20261030
- Round: R01 / F1 API与模型服务工厂
- WorkBuddy Job ID: c901454bfc4042c3
- MCP status: done, raw report received
- Provenance: 以下原样保存 WorkBuddy MCP get_workbuddy_result 返回的完整文本，不代表 ChatGPT 已认可其所有事实。

---

I have completed the read-only investigation with real evidence. Below is the full report.

---

# R01 F1 API与模型服务工厂 Skill/Plugin实战研究（WorkBuddy）

> 证据采集时间：2026-10-29 17:06 UTC；采集环境：WorkBuddy 主机 `/home/workbuddy_agent`，CodeBuddy Code CLI v2.177.0。
> 研究方法：仅执行只读核查（版本/列表/文件读取/文档读取）。**未安装任何 Skill/Plugin/MCP，未修改配置、未切换模型、未读取凭据、未写文件、未提交 Git、未影响其他任务。** 安装类命令仅展示、不执行。

---

## 1. 本轮环境证据、日期、检查命令与候选真实性等级

### 1.1 已实测命令与输出摘要（全部真实运行）

| 命令（在本环境执行） | 输出摘要 | 证据等级 |
|---|---|---|
| `codebuddy --version` | `2.177.0` | 实测 |
| `codebuddy plugin marketplace list` | 2 个市场：`cb_teams_marketplace`（zip，https://download.codebuddy.cn/plugin-marketplace/cb_teams_marketplace.zip）、`codebuddy-plugins-official`（zip，https://download.codebuddy.cn/plugin-marketplace/codebuddy-plugins-official.zip） | 实测 |
| `codebuddy plugin list` | `No plugins installed.` | 实测 |
| `codebuddy mcp list` | `No MCP servers configured.` | 实测 |
| `cat ~/.codebuddy/plugins/installed_plugins.json` | 空文件（0 字节）；无 `plugins/cache` 目录 | 实测（文件存在） |
| `ls ~/.codebuddy/plugins/marketplaces/.../plugins` | 两个市场含大量插件目录（见 1.2） | 文件存在 |
| `codebuddy --help`（含 `--model` 列表） | 支持模型：hy4-preview, hy3, hy3-x, deepseek-v4.1-flash, step-5-preview, glm-5.3/-flash/-flashx/-5.2, space-bunny, minimax-m3.1-flash, **minimax-m3-pay**, minimax-m2.7, kimi-k3.1-pro-highspeed/-pro/-2/k2.8-preview, deepseek-v4-pro, mimo-v2.6-pro | 实测 |

### 1.2 关键文件路径（相对 `~/.codebuddy/plugins/marketplaces/`）

- `codebuddy-plugins-official/.codebuddy-plugin/marketplace.json`（官方市场清单，108KB，含全部插件元信息）
- `codebuddy-plugins-official/plugins/{github,gitlab,serena,context7,supabase,firebase,chainguard,security-scan,skills-security-check,skills-sec-audit,security-guidance,security-rules,find-skills,feature-dev,playwright-cli,testbuddy,cloudbase}/`
- `codebuddy-plugins-official/external_plugins/{api-scaffolding,api-testing-observability,backend-api-security,machine-learning-ops,cicd-automation,deployment-strategies,mcp-builder,observability-monitorin}/`
- `cb_teams_marketplace/plugins/{skill-creator,executing-marketing-campaigns,deep-research,...}/`
- 内置能力文档：`/usr/lib/node_modules/@tencent-ai/codebuddy-code/dist/web-ui/docs/cn/cli/{http-api,models,monitoring,plugins,plugin-marketplaces,mcp,mcp-apps}.md`

### 1.3 候选真实性等级（重要：区分“缓存”与“已安装”）

本环境 `installed_plugins.json` 为空、无 `cache` 目录，因此**没有任何插件处于“已安装且真实执行”状态（①）**。所有市场插件仅为“市场存在但未安装（②）”，第三方 MCP 为“需独立授权（③）”，本地模型网关等为“纯理论/需自建（④）”。市场缓存目录是**只读快照**，绝不等于已安装。

- **T1 内置/原生能力（CLI 自带，无需安装）**：`--serve` HTTP API、models.json 自定义模型、`OTEL` 可观测、内置 `mods-create` skill。
- **T2 市场存在、清单/文件已读（②，未安装）**：下文 12 个候选。
- **T3 第三方 MCP，需独立授权（③）**：github/gitlab/supabase/firebase/context7 等 MCP。
- **T4 纯理论/需自建（④）**：本地 Qwen/Phi-4 推理网关、独立“model-router/billing”插件。

---

## 2. F1 真正适用的 Skill/Plugin/MCP/CLI 候选（按优先级，≥8）

> 安装命令格式：`codebuddy plugin install <name>@codebuddy-plugins-official`（external 类加 `@codebuddy-plugins-official`）。**仅展示，未执行。** 所有插件当前均未安装。

### ① `codebuddy --serve`（HTTP API / ACP 网关）— CLI 原生，非插件
- 路径/文档：`docs/cn/cli/http-api.md`
- 功能边界：将 CodeBuddy 本身作为 API 服务暴露。提供 `REST /api/v1/*`（无状态）、`ACP /api/v1/acp`（有状态流式 JSON-RPC）、Swagger ` /api/docs`、OpenAPI ` /api/openapi.json`、健康检查 `GET /api/v1/health`。**这是 F1“可编排 API 服务 / 模型推理网关”最贴近的原生能力（Beta）。**
- 适用环节：API 服务、模型网关、对外编排入口。
- 使用步骤（展示）：`codebuddy --serve --port 8080 --session-id f1-gw`；验证 `curl http://127.0.0.1:8080/api/v1/health`。
- 输入输出：HTTP 请求（需头 `X-CodeBuddy-Request: 1`）↔ JSON/流式响应。
- 鉴权/付费：认证模式 `--auth password|none`（none 允许本机任意进程执行命令/读写文件，**仅限本机**）；云端需自建反向代理 + 网关鉴权；本能力免费，调用模型按模型计费。
- 安全限制：CORS + 自定义头防跨域；`--auth none` 高风险，禁止公网暴露。

### ② models.json 自定义模型注册（模型路由/计费杠杆）— CLI 原生
- 路径：`~/.codebuddy/models.json`（用户级）/`<ws>/.codebuddy/models.json`（项目级）
- 功能边界：注册任意 OpenAI 兼容端点（`url`+`apiKey`+`vendor`），控制 `availableModels`。**本地 Qwen/Phi-4 经 vLLM/llama.cpp 暴露 `/v1/chat/completions` 后在此注册即可被路由**（④需自建，未验证本地 GPU 可用性）。
- 适用环节：多模型路由、计费限额（按模型/密钥区分）、本地+云端混合。
- 使用步骤（展示）：编辑 models.json 加入 `{id, name, vendor, apiKey, url, maxInputTokens, supportsToolCall}`；重启会话，`/model` 选择。
- 安全限制：`apiKey` 以明文存于配置文件，**属密钥风险点**，需配合系统密钥管理（见候选⑭）。

### ③ mcp-builder（external_plugins）— Skill 指南
- 市场/路径：`codebuddy-plugins-official/external_plugins/mcp-builder`（已读 SKILL.md，Apache-2.0）
- 功能边界：指导用 Python FastMCP / TS MCP SDK 构建 MCP 服务器（工具命名、上下文分页、错误可操作化）。**对应 F1“插件接口 / 模型服务接口”供给侧。**
- 适用环节：自建模型路由/计费/可观测 MCP 接口。
- I/O：需求描述 → 生成 MCP server 代码。
- 鉴权/付费：本地、无第三方授权、无费用。

### ④ api-scaffolding（external_plugins）— agents+skills
- 市场/路径：`.../external_plugins/api-scaffolding`（已读 plugin.json + fastapi-templates SKILL.md）
- 功能边界：REST/GraphQL API 脚手架、框架选择、后端架构设计；含 agents：backend-architect、django-pro、fastapi-pro、graphql-architect；skills：fastapi-templates。
- 适用环节：API 服务代码生成。
- I/O：需求 → FastAPI/Django/GraphQL 项目骨架。**本地、无授权、无费用。**

### ⑤ api-testing-observability（external_plugins）
- 市场/路径：`.../external_plugins/api-testing-observability`（已读 plugin.json + agents/api-documenter.md）
- 功能边界：API 测试自动化、请求模拟、**OpenAPI 文档生成**、可观测性配置与监控。**对应 F1“API 契约测试”。**
- I/O：API 代码/路由 → 测试用例 + OpenAPI spec。本地、无授权。

### ⑥ backend-api-security（external_plugins）
- 市场/路径：`.../external_plugins/backend-api-security`（已读 plugin.json + 2 agents）
- 功能边界：API 安全加固、**身份验证、授权模式、速率限制（rate limiting）、输入验证**。**对应 F1“限流计费/安全”。** 本地、无授权。

### ⑦ machine-learning-ops（external_plugins）
- 市场/路径：`.../external_plugins/machine-learning-ops`（已读 plugin.json + 3 agents + ml-pipeline-workflow skill）
- 功能边界：生产 ML 流水线、实验跟踪、模型注册、自动化训练/部署工作流。**对应 F1“模型服务/推理工厂”。** 本地、无授权。

### ⑧ cicd-automation（external_plugins）
- 市场/路径：`.../external_plugins/cicd-automation`（已读 plugin.json + 4 skills + 5 agents）
- 功能边界：CI/CD 流水线、GitHub Actions/GitLab CI、自动化部署；**含 secrets-management skill（Vault / AWS Secrets Manager / 平台原生）**。**对应 F1“持续交付 + 密钥安全”。** 本地；编排 GitHub/GitLab 时需其 MCP（③）。

### ⑨ deployment-strategies（external_plugins）
- 市场/路径：`.../external_plugins/deployment-strategies`（已读 plugin.json + 2 agents）
- 功能边界：部署模式、**回滚自动化**、基础设施模板。**对应 F1“灰度发布/回滚”。** 本地、无授权。

### ⑩ security-scan（plugins，官方）
- 市场/路径：`codebuddy-plugins-official/plugins/security-scan`（已读 README）
- 功能边界：语义索引 + 多 Agent 并行扫描 + 对抗验证，支持 `--auto` 无人值守、安全门禁、Git Hook、腾讯云基线。**对应 F1“安全审计”。** 本地、无第三方授权（腾讯系基线）。

### ⑪ skills-security-check / skills-sec-audit（plugins，官方）
- 市场/路径：`.../plugins/{skills-security-check,skills-sec-audit}`（已读 plugin.json，腾讯云鼎实验室）
- 功能边界：对指定 `SKILL.md` 及其配套文档/脚本做安全审查（防供应链投毒）。**对应 F1“插件接口安全/供应链”。** 本地、无授权。

### ⑫ chainguard（plugins，官方）
- 市场/路径：`.../plugins/chainguard`（已读 README）
- 功能边界：拦截 AI 的依赖安装命令，CVE/OSV 漏洞库检测、SBOM 白名单、License 合规、拦截高危操作（Hook 触发）。**对应 F1“供应链安全”。** 本地 Hook、无授权。

### 补充候选（简列）
- **playwright-cli**（plugins）：浏览器/API 契约测试 CLI，token-efficient，需 Node18+（本地）。
- **github / gitlab MCP**（plugins，③）：`.mcp.json` 为 `http` 型，github 指向 `https://api.githubcopilot.com/mcp/`，头 `Authorization: Bearer ${GITHUB_PERSONAL_ACCESS_TOKEN}` → **需独立 PAT/OAuth**。用于源码、PR、CI 编排。
- **context7 / supabase / firebase MCP**（plugins，③）：第三方 API，需各自密钥。
- **serena / testbuddy / feature-dev / find-skills / cloudbase**（plugins）：代码语义分析、测试、功能开发、技能发现、云端。

### 明确“未发现”
- 精确名为 **model-router / billing-quota / canary-release** 的官方插件：**未发现**（相关能力由 models.json + backend-api-security + deployment-strategies 组合实现）。
- `observability-monitorin`（external_plugins）目录**存在但内容为空（0 文件）** → 实际能力未发现，列为 T4/空壳。
- 本地 **Qwen / Phi-4** 未出现在 `--model` 云端列表 → 需自建 OpenAI 兼容端点 + models.json 注册（④）。
- 本人**不持有任何 ChatGPT 账号授权**，无法验证 ChatGPT 侧连接器实际可用性（见 §3）。

---

## 3. 与 ChatGPT 可调用的同类能力比较（权限必须分开）

> 以下 ChatGPT 侧描述基于公开知识/**推断**，非本环境验证；本人无 ChatGPT 授权。

| 能力 | ChatGPT 侧（推断） | CodeBuddy 侧（本环境事实） | 同源 SaaS 必须分开的点 |
|---|---|---|---|
| GitHub | ChatGPT 通过自身 OAuth App 连接仓库 | `github` MCP（③）需独立 `GITHUB_PERSONAL_ACCESS_TOKEN` | **两套 OAuth 授权、两套 token 作用域、两套审计轨迹**，不可互认 |
| Automations（定时/自动化） | ChatGPT 自定义 GPT 定时任务 | CodeBuddy 无内建 scheduler；用 `--serve`+外部 cron/CI 编排 | 调度主体与凭据边界不同 |
| WorkBuddy MCP | 若 ChatGPT 连接“WorkBuddy MCP”则为外部连接器 | 本环境 CodeBuddy 原生运行于 WorkBuddy 主机，**非“ChatGPT 调 WorkBuddy MCP”** | 信任边界完全不同，不能混为一谈 |
| Google Drive | ChatGPT 原生连接器 | 需自行接 Drive MCP（③，需 Google OAuth） | 不同 OAuth、不同数据出口 |
| Browser | ChatGPT 浏览能力 | CodeBuddy 用 `playwright-cli`/web-mods（本地） | 执行环境与数据留存不同 |
| Firecrawl | ChatGPT 抓取技能 | 需自建/第三方 Firecrawl MCP（③，需 API key） | 密钥与配额独立 |
| Plugin Management | ChatGPT GPTs/插件市场 | `codebuddy plugin install/marketplace`（本环境两市场） | 分发源、版本、审计各自独立 |

**结论**：功能相似 ≠ 权限共享。F1 若同时用两侧，必须为每个 SaaS 单独授权、单独记录凭据、单独设最小权限，禁止跨侧复用 token。

---

## 4. 五个互不重复实战案例

### 案例 A｜多模型路由网关（覆盖：多模型路由）
- **目标**：用本地 Qwen/Phi-4（免费）+ 云端 glm-5.3-flash（低价）+ deepseek-v4-pro（高质量）按成本/质量路由。
- **组合**：models.json（②原生）+ `codebuddy --serve`（原生）+ 候选 `mcp-builder`（③→②）。
- **步骤**：① 本地起 vLLM 暴露 `/v1/chat/completions`；② 写 models.json 注册三个模型；③ `codebuddy --serve --port 8080` 起网关；④ 路由策略由上游调用方按 `/model` 或自建 router MCP 选择。
- **输入/输出**：调用请求 → 路由后模型响应（JSON/流式）。
- **验收**：`curl /api/v1/health` 返回 ok；三模型在 `/model` 可切换；单请求成本可归因到具体 `vendor`。
- **预估**：0.5–1 天（本地 GPU 就绪前提下）。
- **失败/回滚**：本地端点宕机 → 用 `--fallback-model` 指向云端；models.json 改错 → 还原文件、重启。

### 案例 B｜API 契约测试流水线（覆盖：API 契约测试）
- **目标**：对生成的 REST API 做契约测试并产出 OpenAPI。
- **组合**：`api-testing-observability`（②）+ `api-scaffolding`（②）+ `playwright-cli`（②）。
- **步骤**：① `/api-scaffolding:fastapi-templates` 生成骨架；② `/api-testing-observability:api-documenter` 生成 OpenAPI 与测试用例；③ playwright-cli 跑端到端契约校验。
- **输入/输出**：API 源码 → `openapi.json` + 测试报告。
- **验收**：OpenAPI 覆盖主要路由；契约测试 0 违约。
- **预估**：0.5 天。
- **失败/回滚**：测试失败 → 锁定契约版本，回退至上一 green OpenAPI。

### 案例 C｜限流与计费限额（覆盖：限流计费）
- **目标**：对外 API 加速率限制并按模型/租户计量成本。
- **组合**：`backend-api-security`（②，rate limiting）+ models.json 按 vendor 分离密钥（原生）+ 自建计量（mcp-builder②）。
- **步骤**：① backend-api-security 加鉴权与限流中间件；② models.json 为每租户配独立 `apiKey` 实现额度隔离；③ mcp-builder 生成计量 MCP 上报用量。
- **输入/输出**：带 key 的请求 → 限流响应头 + 用量记录。
- **验收**：超阈返回 429；每 key 用量可统计。
- **预估**：1 天。
- **失败/回滚**：限流误杀 → 调阈值；计量异常 → 关闭计量 MCP 不影响主链路。

### 案例 D｜可观测性 + 安全审计（覆盖：可观测性 + 安全审计）
- **目标**：全链路 trace + 代码/插件安全门禁。
- **组合**：OTEL 监控（原生 env）+ `security-scan`（②）+ `skills-security-check`（②）。
- **步骤**：① `CODEBUDDY_CODE_ENABLE_TELEMETRY=1` + `OTEL_EXPORTER_OTLP_ENDPOINT=...` 上报 trace；② `security-scan --auto` 做安全门禁；③ 对所有自定义 SKILL.md 跑 `skills-security-check`。
- **输入/输出**：运行期 → OTLP trace；代码/插件 → 审计报告。
- **验收**：trace 进入自有 Collector；高危漏洞阻断合并（Git Hook）。
- **预估**：0.5–1 天。
- **失败/回滚**：OTEL 端点故障 → 关闭上报不影响业务；误报 → 人工复核白名单。

### 案例 E｜密钥安全/供应链 + 灰度与持续交付（覆盖：密钥安全/供应链 + 持续交付/灰度）
- **目标**：CI 中防供应链投毒、密钥不落盘、灰度发布可回滚。
- **组合**：`chainguard`（②）+ `cicd-automation`（②，secrets-management）+ `deployment-strategies`（②）+ `github` MCP（③）。
- **步骤**：① chainguard Hook 拦截危险依赖安装并做 SBOM/CVE 检查；② cicd-automation 用 Vault 注入密钥（不硬编码）；③ deployment-strategies 做金丝雀 + 自动回滚；④ github MCP（③）触发 PR/部署。
- **输入/输出**：依赖清单/部署清单 → SBOM 报告 + 灰度部署 + 回滚事件。
- **验收**：高危依赖被拦截；密钥未写入仓库；灰度异常自动回滚。
- **预估**：1–2 天（含 Vault 搭建）。
- **失败/回滚**：Vault 不可用 → 暂停发布；回滚脚本前置验证。

---

## 5. 第一周最小可实施方案

### 5.1 依赖图
```
[本地/云端模型端点] --models.json--> [--serve 网关]
                                       |
        +-- api-scaffolding / api-testing-observability (生成+契约)
        +-- backend-api-security (限流/鉴权)
        +-- machine-learning-ops (模型服务)
        +-- cicd-automation + deployment-strategies (交付/灰度)
        +-- chainguard + security-scan + skills-security-check (安全/供应链)
        +-- OTEL env (可观测)        + github/gitlab MCP③ (源码编排)
```

### 5.2 优先安装 Top5（均为②，未安装，仅展示命令）
1. `codebuddy plugin install backend-api-security@codebuddy-plugins-official`
2. `codebuddy plugin install api-testing-observability@codebuddy-plugins-official`
3. `codebuddy plugin install cicd-automation@codebuddy-plugins-official`
4. `codebuddy plugin install security-scan@codebuddy-plugins-official`
5. `codebuddy plugin install chainguard@codebuddy-plugins-official`
（原生能力 `--serve` / models.json / OTEL 无需安装，直接启用。）

### 5.3 可重复验证命令（只读，已实测可跑）
```bash
codebuddy --version
codebuddy plugin marketplace list
codebuddy plugin list
codebuddy mcp list
cat ~/.codebuddy/plugins/installed_plugins.json   # 预期空
ls ~/.codebuddy/plugins/marketplaces/codebuddy-plugins-official/plugins | head
```

### 5.4 成本边界
- CLI/插件本身免费；费用仅来自**模型调用**（注意列表含 `minimax-m3-pay` 等付费档，具体价目以官方计费页为准，**本次未验证**）。
- 本地 GPU 推理边际成本低但需硬件；云端按 token 计费。
- 严禁递归调用、越权写入（F1 安全策略：合规>正确性>截止>成本）。

### 5.5 不能宣称已验证的事项（诚实声明）
- 未实际安装/运行任何上述插件 → 其功能边界基于**清单与 SKILL.md 文档**，非运行实测。
- 本地 Qwen/Phi-4 网关、第三方 MCP（GitHub 等）的授权与连通性**未验证**。
- ChatGPT 侧任何连接器**未验证**（无授权）。
- 各模型具体单价/限额**未验证**（需查官方计费文档）。

---

## 6. EVIDENCE_LOG 与 UNVERIFIED

### EVIDENCE_LOG
| 编号 | 事实/声明 | 证据类型 | 来源/命令 |
|---|---|---|---|
| E1 | CLI 版本 2.177.0 | 实测 | `codebuddy --version` |
| E2 | 两个市场存在（cb_teams_marketplace, codebuddy-plugins-official） | 实测 | `plugin marketplace list` |
| E3 | 无插件安装、无 MCP 配置 | 实测 | `plugin list` / `mcp list` / `installed_plugins.json` 空 |
| E4 | 官方市场插件清单与文件 | 文件存在 | `.../marketplaces/codebuddy-plugins-official/plugins/*` |
| E5 | external_plugins 含 api-scaffolding 等 | 文件存在 | `.../external_plugins/*` |
| E6 | github MCP 需 PAT | 文件存在 | `plugins/github/.mcp.json` |
| E7 | `--serve` 暴露 REST/ACP/Swagger | 官方文档 | `docs/cn/cli/http-api.md` |
| E8 | models.json 可注册自定义模型端点 | 官方文档 | `docs/cn/cli/models.md` |
| E9 | OTEL trace 上报（仅 traces） | 官方文档 | `docs/cn/cli/monitoring.md` |
| E10 | 支持模型列表（含 minimax-m3-pay） | 实测 | `codebuddy --help` |
| E11 | chainguard/security-scan 功能描述 | 文件存在 | 各自 README |
| E12 | observability-monitorin 目录为空 | 文件存在 | `find ... -type f` 计数 0 |
| E13 | ChatGPT 侧连接器描述 | 推断/公开知识 | 非本环境，无授权 |

### UNVERIFIED（明确未验证）
- U1：任何插件**安装后实际运行效果**（未安装）。
- U2：本地 Qwen/Phi-4 端点可达性与性能（④未建）。
- U3：GitHub/GitLab/Supabase/Firebase/Context7 MCP 的**授权与连通**（③未授权）。
- U4：各模型具体计费单价与配额（需官方计费页）。
- U5：ChatGPT 侧 GitHub/Automations/WorkBuddy MCP/Drive/Browser/Firecrawl/Plugin Management 的可用性（无 ChatGPT 授权）。
- U6：`--serve` 在公网反代下的完整安全表现（仅文档，未压测）。

### 命令执行声明
- 所有标注“实测”的命令均**在本环境真实运行**；标注“文件存在”的均通过 Read/ls/find 核实；标注“官方文档”的均读取自内置 `dist/web-ui/docs`。
- 所有 `plugin install` / `mcp add` 类命令**仅展示、未执行**；未触发任何网络安装、配置写入或凭据读取。

### 事实 vs 建议（对照）
- **事实**：E1–E12 所列状态与文档内容。
- **建议**：§2 优先级、§4 案例步骤、§5 Top5 安装——均为基于事实的**规划建议**，未经运行验证，落地前须按 U1–U6 补齐验证。

---

RESULT_STATUS: COMPLETE