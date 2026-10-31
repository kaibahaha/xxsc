# R01 F1 WorkBuddy完整原始报告｜只读补交成功

- Original research job: aab758d7c33d4631 (DONE, 696s)
- Read-only recovery job: 93de654703984b20 (retrieved original existing remote file; no re-research)
- Original remote path: /tmp/factory10-self-improvement-20261031/R01/WORKBUDDY_REPORT.md
- Source: actual MCP recovery response between BEGIN_R01_ORIGINAL_REPORT and END_R01_ORIGINAL_REPORT, 382 lines, 21275 characters; original R01 MCP summary preserved in WORKBUDDY_SUMMARY_ORIGINAL.md.
- No independent execution validation of remote CLI claimed; independent audit in CHATGPT_AUDIT.md.

---

# R01 / F1 — WorkBuddy 云端执行代理研究报告（FACTORY10-SELF-IMPROVEMENT-20261031）

> 实验：FACTORY10-SELF-IMPROVEMENT-20261031 · 轮次：R01（新实验 BASELINE，不与旧实验 R00/旧 R01 混号）
> 主题：F1 API 与模型服务工厂，结合 ChatGPT→MCP 桥接器→CodeBuddy 单槽队列→Git 归档架构
> 审计视角：独立云端只读研究；严禁修改生产桥接器 / 服务 / 模型 / Git 仓库 / 任务调度 / 插件配置 / 凭据；严禁安装、授权、切模型、读凭据、创建子定时任务。
> 历史基线标记：NO_PREVIOUS_HOUR（无 R00）。旧实验 `factory10-skill-plugin-24h-20261030/rounds/R01` 的评分 70/100 仅作历史参考，不代表本环境事实。

---

## ① 日期 / 环境 / 命令原始关键输出（只读，未做任何写操作）

### 1.1 时间与环境（本机只读采集）

```
$ date
Sat Oct 31 02:25:34 UTC 2026            # 北京时间约 2026-10-31 10:25，与派单计划一致

$ echo $HOME
/home/workbuddy_agent
$ pwd
/home/workbuddy_agent
$ uname -a
Linux <host> #1 SMP PREEMPT_DYNAMIC Debian 6.12.113-1 (2026-10-15) x86_64
```

### 1.2 关键环境变量（已脱敏，仅显示键名，值一律 `<redacted>`）

```
CODEBUDDY_SESSION_ID=<redacted>   CODEBUDDY_TOKEN=<redacted>
CODEBUDDY_GATEWAY_PASSWORD=<redacted>   CODEBUDDY_SERVICE_PROXY_URL=<redacted>
CODEBUDDY_BASE=<redacted>   CODEBUDDY_IS_SANDBOX=<redacted>
CODEBUDDY_INTERNET_ENVIRONMENT=<redacted>   CODEBUDDY_CURRENT_MODEL_ID=<redacted>
```
> 说明：本报告全程未读取、未打印任何凭据明文；以上为变量名清单，证明运行于受管沙箱且网关默认带密码。

### 1.3 已安装 CLI 版本与子命令（只读 `--help` / `--version`）

```
$ codebuddy --version
2.177.0

$ codebuddy --help        # 顶层子命令（节选）
Commands:
  config      Manage configuration
  mcp         Configure and manage MCP servers
  sandbox     Manage sandboxes
  plugin      Manage CodeBuddy Code plugins
  project     Manage CodeBuddy Code project state
  doctor      Check the health of your CodeBuddy Code auto-updater
  update      Check for updates and install if available
  install     Install CodeBuddy Code native build
  cleanup     Clean up expired local CodeBuddy data
  daemon      Manage the daemon supervisor process
  ps / logs / attach / kill / stop / rm / respawn / agents / auto-mode
```
> 观察：顶层 **没有** 名为 `scheduler` 的子命令；原生调度能力以**会话内工具**（`CronCreate`/`CronList`/`CronDelete`）与 **`/loop` 斜杠命令**形式存在，并经 `--serve` 后的 REST `/api/v1/scheduled-tasks` 暴露（见 §② 官方文档证据）。这与旧报告“无内建 scheduler”的论断直接矛盾（详见 §⑤ SF01）。

```
$ codebuddy mcp --help     # 只读子命令清单（未列/未增任何 MCP 服务器）
Commands: add / remove / list|ls / get / add-json / help

$ codebuddy plugin --help  # 插件管理（未安装任何插件）
Commands: add / validate / init / build

$ codebuddy config --help  # 配置查询（未改任何配置）
Commands: get / set / remove|rm / list|ls
```

### 1.4 关于“`codebuddy --serve` 是否为多模型推理网关”的只读核验结论

对随包分发的官方文档 `http-api.md`（v2.177.0）全量端点列表做检索，**未发现任何 `/v1/chat/completions` 或 OpenAI 兼容推理端点**。该网关暴露的是：
`/api/v1/runs`、`/api/v1/jobs`、ACP（`/api/v1/acp`）、sessions、PTY、files、process、plugins、scheduled-tasks、traces、stats 等**智能体控制面**端点。
而 `/chat/completions` 仅作为 `models.json` 中**上游模型 `url` 字段**出现（即 CodeBuddy 去调用的下游，而非它对外提供的服务）。

```
检索证据（随包文档，只读 grep）：
  http-api.md 全文端点表中无 "chat/completions" 作为本服务对外端点；
  models.md 中 "chat/completions" 仅出现于自定义模型 url 示例（如
  https://api.openai.com/v1/chat/completions）——属于“上游供给”，非“本服务暴露”。
```

---

## ② 官方一手 URL 及证据等级、未验证清单

| # | 官方一手来源（URL） | 主题 | 证据等级 | 用于整改项 |
|---|-------------------|------|---------|-----------|
| U1 | https://www.codebuddy.cn/docs/cli/http-api | CodeBuddy Code HTTP API（含 scheduled-tasks、runs、ACP、plugins） | 官方在线文档（本轮 Web 检索命中，2026-10-31） | SF01, SF02 |
| U2 | http://www.codebuddy.ai/docs/cli/http-api | 同上英文版 | 官方在线文档（Web 命中） | SF01, SF02 |
| U3 | https://intl.cloud.tencent.com/document/product/1316/84458 | Scheduled Tasks 官方说明（CronCreate/`/loop`/cron、会话级 vs 外部调度） | 官方在线文档（Web 命中） | SF01 |
| U4 | https://www.codebuddy.cn/docs/cli/models （随包 `models.md` v2.177.0 同源） | models.json 配置（字段、环境变量引用、密钥安全） | 官方随包文档（本机读取，与在线同源） | SF03, SF04 |
| U5 | https://www.codebuddy.cn/docs/cli/plugins （随包 `plugins.md` 同源） | 插件创建/市场/安全提示 | 官方随包文档（本机读取） | SF05 |
| U6 | https://docs.litellm.ai/ | LiteLLM 开源 AI 网关（keys/budgets/costs、虚拟密钥、路由） | 官方在线文档（Web 命中） | SF02, SF03 |
| U7 | https://litellm.vercel.app/docs/proxy/users | LiteLLM Budgets / Rate Limits（**无数据库时预算 fail-open**） | 官方在线文档（Web 命中，含原文引述） | SF03 |
| U8 | https://agentclientprotocol.com/ （及 /protocol/v2/overview） | Agent Client Protocol（ACP）规范：JSON-RPC 2.0、session/prompt、远程 agent over HTTP | 官方在线文档（Web 命中） | SF02 |
| U9 | https://e2b.dev/docs/sandbox/secured-access | E2B Secured Access（默认开启、X-Access-Token、ID 不是凭据） | 官方在线文档（Web 命中） | SF02（安全类比） |

**证据等级定义**：`官方随包文档`＝随 CLI 安装包分发、与官方在线同源、本机直接读取；`官方在线文档`＝本轮 Web 检索命中、可公开访问；`本环境只读CLI实测`＝仅 `--help/--version` 等无副作用命令；`设计建议/UNVERIFIED`＝需生产环境或写入/授权才能验证，本报告仅给出方案。

### 未验证清单（UNVERIFIED，明确不做断言）

- U-1：LiteLLM Proxy 在本工厂是否实际部署、版本、数据库连接状态 —— **未实测**（禁止安装/改生产）。
- U-2：CodeBuddy CLI / 插件 / Skill 的**商业订阅定价** —— 随包文档与在线文档**均未标注价格**，标记为 UNVERIFIED（仅知企业 OAuth 需购买“旗舰版”，见 iam.md 引用 Tencent Cloud 购买页，但具体金额未核实）。
- U-3：ChatGPT 侧插件 / Skill / MCP 的具体安装入口与费用 —— 属 OpenAI 平台范畴，**未核实具体入口与定价**，UNVERIFIED。
- U-4：桥接器（ChatGPT→MCP→单槽队列→Git）内部实现与当前运行态 —— 属冻结生产组件，**禁止读取/修改**，仅按派单描述与上下文描述，未做内部核验。
- U-5：`/api/v1/scheduled-tasks` 在**运行中 `--serve` 实例**上的真实返回 —— 未启动服务（避免副作用），仅以文档为据。
- U-6：多租户预算账本、OIDC 直通、SBOM/签名流水线的**端到端跑通** —— 设计建议，UNVERIFIED。

---

## ③ ChatGPT 侧 / WorkBuddy 侧：插件 · Skill · MCP 的可用性、安装、授权、费用严格区分

> 旧报告亮点之一是区分了“插件市场缓存 / 实际安装 / 第三方 MCP 授权 / 理论自建”。本轮在**不安装、不授权**前提下，仅依据官方文档与只读 CLI 做分类，并严格区分**谁安装、谁授权、谁付费**。

| 维度 | ChatGPT 侧（上游调用方 / 审计方） | WorkBuddy 侧（CodeBuddy CLI / 智能体） |
|------|--------------------------------|----------------------------------------|
| **插件可用性** | ChatGPT 生态含 Custom GPT / Actions（API）、桌面端 MCP connector；具体入口随版本变动，**本轮未核实具体入口**（U-3）。 | 文档确认存在插件市场 + 本地 `--plugin-dir` 测试 + `codebuddy plugin add/validate/build`（`plugins.md`、`plugin --help` 已实测）。 |
| **Skill 可用性** | ChatGPT 侧对应“指令/自定义 GPT 指令”类能力；非本侧重点，**UNVERIFIED**。 | CodeBuddy 插件内含 `skills/`（带 `SKILL.md`），`/plugin-name:skill` 命名空间化；`--plugin-dir` 可本地加载（`plugins.md` 已读）。 |
| **MCP 可用性** | ChatGPT 桌面端支持连接 MCP 服务器（作为 client）；具体配置路径 UNVERIFIED。 | `codebuddy mcp add/list/get/add-json` 管理；MCP OAuth 回调用内部 RPC 代理（`release-notes v2.125.4`）；`mcp --help` 已实测，未增删任何服务器。 |
| **安装动作（谁做）** | 在 OpenAI 平台侧由用户/组织管理员安装 GPTs/Actions 或配置 MCP 连接。 | 在 CodeBuddy 侧由 `codebuddy plugin add`（市场/包）或 `--plugin-dir`（本地）完成；**本轮未安装任何插件**。 |
| **授权（信任边界）** | OpenAI 平台侧的 OAuth / 组织策略；不在本环境管控内。 | 插件可**执行命令、访问文件系统**（`plugins.md` 明确安全提示）；需审查代码；受 CodeBuddy 权限系统约束（`iam.md`：allow/ask/deny、permission-mode）。**本轮未对任何插件授权**。 |
| **费用（谁付费）** | ChatGPT 订阅 / API 用量由 OpenAI 计费（具体 UNVERIFIED）。 | ①CLI/插件/Skill/MCP **安装与使用本身文档未标价→免费但 UNVERIFIED 商业订阅**；②**模型推理费用**由 `models.json` 指向的**上游 provider**（OpenAI/DeepSeek 等）按其定价承担；③企业 OAuth 需购“旗舰版”（`iam.md` 引用腾讯云购买页，金额 UNVERIFIED）。 |

**严格结论**：
- “CLI/插件免费”**不可作为已核实的商业结论**——文档未标价 ≠ 免费；正确表述为“文档未提供价格，UNVERIFIED”。
- 模型调用成本与“CLI/插件是否收费”是**两件事**：前者是上游 provider 的费用，后者是 CodeBuddy 平台计费，必须分开陈述。
- 本侧（WorkBuddy）在本轮**未安装、未授权、未启用**任何插件/Skill/MCP 额外组件；所有判断均来自只读文档与 `--help`，未产生任何费用，未触碰凭据。

---

## ④ F1 模块化架构 + 五个案例（每案含输入 / 最小命令 / 输出 / 失败注入 / 回滚 / 权限与成本 / 可量化验收）

### 4.0 F1 模块化架构（建议蓝图，区分被旧报告混淆的各层）

```
┌──────────────────────────────────────────────────────────────────────┐
│  接入层（冻结生产，禁止改动）                                          │
│  ChatGPT ──MCP 桥接器──▶ WorkBuddy 单槽队列（串行）──▶ Git 归档       │
└──────────────────────────────────────────────────────────────────────┘
            │ 单槽队列把请求投入 CodeBuddy Agent
            ▼
┌──────────────────────────────────────────────────────────────────────┐
│  L1  Agent 控制面（CodeBuddy --serve 网关，非推理网关）                │
│   REST /api/v1/runs · /api/v1/jobs · ACP /api/v1/acp                  │
│   会话/PTY/文件/进程/插件/定时任务(traces,stats)  — 见 U1/U2           │
│   认证：默认密码(gateway_session)；CORS 白名单；X-CodeBuddy-Request    │
└──────────────────────────────────────────────────────────────────────┘
            │ Agent 执行模型调用时，按 models.json `url` 发往：
            ▼
┌──────────────────────────────────────────────────────────────────────┐
│  L2  推理网关 / 策略路由层（建议：LiteLLM Proxy 或等价，U6/U7）        │
│   OpenAI 兼容 /v1/chat/completions · 虚拟密钥 · 预算/账本(RPM/TPM)    │
│   模型路由 / 回退 / 限流 —— 这一层才是“多模型推理网关”                │
└──────────────────────────────────────────────────────────────────────┘
            │
            ▼
┌──────────────────────────────────────────────────────────────────────┐
│  L3  模型供给层（上游 provider，models.json `url` 实际指向处）         │
│   OpenAI / DeepSeek / 本地 Ollama …（按 vendor 与 url 区分）          │
└──────────────────────────────────────────────────────────────────────┘
            ▲
┌──────────────────────────────────────────────────────────────────────┐
│  L4  工厂级治理（横切）：身份/OIDC · 预算账本 DB · 插件治理            │
│   SBOM/签名 · 灰度闸门 · 可观测(trace_id/job_id 贯通)                  │
└──────────────────────────────────────────────────────────────────────┘
```

**关键边界（纠正旧报告）**：`codebuddy --serve` 是 **L1 Agent 控制面**，不是 L2 推理网关；真正的多模型推理网关是 L2（需 LiteLLM 之类组件，本环境未部署＝U-1 UNVERIFIED）。`models.json` 的 `url` 把 L1 指向 L3 的上游，若要统一鉴权/预算，应在 L2 收口。

### 案例 A — 多模型路由（保留多模型价值，拆 Agent 入口与 LLM Gateway）

- **目标**：在不宣称 `--serve` 是推理网关的前提下，验证 L2 多模型路由、429/超时/敏感数据行为、计费与回退。
- **输入**：一个标准 OpenAI 格式请求 `{model:"openai/gpt-4o", messages:[...]}` 经 L2 网关发出；Agent 侧通过 `/api/v1/runs`（Gateway Protocol）下派任务。
- **最小命令（只读/设计）**：
  ```bash
  # L2 网关（设计，未部署）：路由到多模型
  curl -s http://localhost:4000/v1/chat/completions \
    -H "Authorization: Bearer $LITELLM_VK" -H "Content-Type: application/json" \
    -d '{"model":"openai/gpt-4o","messages":[{"role":"user","content":"ping"}]}'
  # L1 Agent 入口（文档真实存在）：
  curl -X POST http://127.0.0.1:8080/api/v1/runs \
    -H "X-CodeBuddy-Request: 1" -H "Authorization: Bearer $GW_PWD" \
    -d '{"id":"r1","type":"message","payload":{"text":"分析这段代码"}}'
  ```
- **预期输出**：L2 返回 `choices[].message`；L1 返回 `{"data":{"runId":...,"status":"accepted"}}` 后由 SSE `/runs/:runId/stream` 取结果。
- **失败注入（≥10 条可手工复现，设计为可复跑）**：
  1. 模型不存在 → L2 返回 400/404；2. provider 429 → L2 退避并重试（`CODEBUDDY_MAX_RETRIES`）；
  3. provider 500 → 同上；4. 上游超时 → 设 `CODEBUDDY_FIRST_TOKEN_TIMEOUT_MS`；
  5. 虚拟密钥超额 → L2 返回 429 + 预算拦截；6. 数据库不可用 → **L2 fail-open**（见 SF03，预算不生效）；
  7. L1 缺 `X-CodeBuddy-Request` 头 → 403；8. L1 缺 Bearer → 401；
  9. L1 `?password=` 用于 API → 401（设计如此）；10. 敏感数据出域 → 需在 L2/桥接层做脱敏（见案例 D）；
  11. 路由切人工 vs 策略自动：人工切换用 `/model`，策略自动由 L2 router 决定，二者必须区分记录。
- **回滚**：L2 路由规则以版本化 `config.yaml` 管理，回滚＝还原上一版并重载；L1 模型回退用 `relatedModels`/备用模型（`models.md` 已载）。
- **权限与成本**：L2 虚拟密钥最小权限（仅授权模型）；成本＝上游 provider 按 token 计费（UNVERIFIED 单价）+ L2 自身免费（UNVERIFIED）。
- **可量化验收**：上述 11 条中 ≥10 条有确定性预期响应码与日志；预算超额用例在“数据库在线”时 100% 拦截，在“数据库离线”时明确记录为 fail-open 告警（不谎称拦截）。

### 案例 B — API 契约（OpenAPI 差异 + 负例 + 破坏性变更 CI 阻断）

- **目标**：为 L1 `/api/v1/*` 建立契约测试，覆盖 401/403/409/429/500 负例与版本破坏性变更门禁。
- **输入**：`/api/openapi.json`（网关自带，U1）作为契约基线；L2 `/v1/chat/completions` OpenAPI 作为第二契约。
- **最小命令**：
  ```bash
  curl http://127.0.0.1:8080/api/openapi.json -o l1-openapi.json   # 取得 L1 契约
  # 负例：缺安全头
  curl -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8080/api/v1/sessions   # 期望 403
  curl -o /dev/null -w "%{http_code}\n" -H "X-CodeBuddy-Request: 1" http://127.0.0.1:8080/api/v1/sessions  # 期望 401
  ```
- **预期输出**：`/api/openapi.json` 给出完整端点；负例返回对应错误码 + `{"error":{"code":...,"message":...}}`（错误码表见 http-api.md：AUTH_REQUIRED=401, AUTH_INVALID=401, SIGNATURE_INVALID=403, RATE_LIMITED=429, BAD_REQUEST=400, INTERNAL_ERROR=500, NOT_FOUND=404, session 类 404/400 等）。
- **失败注入**：① 未带 `X-CodeBuddy-Request`→403；② 带头无 Bearer→401；③ 重复幂等 id 冲突→409（设计）；④ 高频→429；⑤ 网关内部故障→500；⑥ 路径不存在→404；⑦ 删除当前会话→400 SESSION_DELETE_CURRENT。
- **回滚**：契约存 Git；CI 比对新 openapi 与基线，破坏性变更（删除/改语义）阻断合并。
- **权限与成本**：只读端点免费；无上游推理成本。
- **可量化验收**：≥7 个负例各有断言；CI 门禁在“删除端点/改响应结构”时 100% 失败并阻断；样例请求/输出写入契约仓库。

### 案例 C — 多租户限流计费（可信身份 + 原子预算账本 + fail-closed）

- **目标**：纠正旧报告“models.json 配 apiKey 即额度隔离”的错误；给出真正的多租户设计。
- **输入**：租户 T 的请求带身份声明（在 L2 虚拟密钥元数据 `metadata.client` 或 JWT `tenant_id`）。
- **最小命令（设计，基于 U7）**：
  ```bash
  # L2 为租户发虚拟密钥（带预算，需数据库）
  curl -X POST http://localhost:4000/key/generate \
    -H "Authorization: Bearer $MASTER" -H "Content-Type: application/json" \
    -d '{"max_budget":50.0,"models":["openai/gpt-4o"],"metadata":{"client":"tenant-T"},"duration":"30d"}'
  ```
- **预期输出**：返回 `sk-...` 虚拟密钥 + 预算；每次调用记入账本（spend）。
- **失败注入**：① 预算耗尽 → L2 返回 429 并停止计费（数据库在线时）；② **数据库故障 → L2 fail-open**（预算检查被跳过，请求继续）——必须 fail-closed 设计：在 L2 之外加一层“账本不可达即拒绝（fail-closed）”或把硬限额下沉到 provider 侧；③ 重试导致重复计费 → 用幂等 `id`/`request_id` + 账本去重；④ 并发超额 → 原子 RPM/TPM（Redis 共享，U6 多副本需 `router_settings`）。
- **回滚**：账本以数据库事务保证；对账作业每日比对 provider 账单与本地 spend，差异超阈值告警。
- **权限与成本**：L2 虚拟密钥最小权限；成本＝上游按 token；账本 DB 有运维成本（UNVERIFIED）。
- **可量化验收**：数据库在线时预算超额 100% 拦截；数据库离线时**明确以 fail-closed 或 provider 侧限额兜底**并记录，绝不声称“软限额已生效”；对账差异 < 1%。
- **重要更正**：`models.json` 仅含模型定义（id/name/vendor/apiKey/url/...），**无租户身份、无 RPM/TPM 预算、无账本字段**，不能实现多租户硬配额（见 §⑤ SF03）。

### 案例 D — 可观测性（ChatGPT→MCP→CodeBuddy→Git 的 job_id/trace_id 贯通）

- **目标**：跨四段链路关联标识，30 条 trace 抽样、脱敏检查、遥测中断降级。
- **输入**：一次用户请求生成 `trace_id`，经桥接器→单槽队列→`/api/v1/runs`(runId)→Git commit 全程携带。
- **最小命令（L1 真实存在）**：
  ```bash
  curl "http://127.0.0.1:8080/api/v1/traces?limit=50" -H "X-CodeBuddy-Request: 1" -H "Authorization: Bearer $GW_PWD"
  curl "http://127.0.0.1:8080/api/v1/jobs"  -H "X-CodeBuddy-Request: 1" -H "Authorization: Bearer $GW_PWD"
  # 导出 OTLP（env: OTEL_EXPORTER_OTLP_ENDPOINT 自动补 /v1/traces，monitoring.md）
  ```
- **预期输出**：`/api/v1/traces` 列表含 span；`/api/v1/jobs` 含 `sessionId`/`runId`；通过 `?session_id=`/`?worker_pid=` 过滤。
- **失败注入**：① trace 缺失 → 抽样发现率 < 100% 告警；② 敏感字段（密钥/PII）落入 span → 脱敏规则命中；③ OTLP Collector 不可达 → 本地仍落 `telemetry` 日志（`/api/v1/workers/:id/logs?type=telemetry`），降级不丢数据；④ Git 归档失败 → 队列重试并标记。
- **回滚**：遥测配置（`CODEBUDDY_*`/otel env）经 settings 管理；Collector 故障不影响主链路。
- **权限与成本**：只读查询免费；OTLP 出口无上游成本。
- **可量化验收**：连续 30 条 trace 抽样中 job_id↔trace_id↔git_commit 关联率 ≥ 95%；脱敏规则对已知密钥模式召回率 100%；Collector 中断期间本地 telemetry 落盘率 100%。

### 案例 E — 供应链 / 灰度（SBOM、签名、OIDC、PR 门禁、5%→20%→100%、回滚 SLO、无密钥泄漏）

- **目标**：插件/镜像供应链与灰度发布治理，OIDC 信任边界。
- **输入**：一个新插件包或模型路由配置变更。
- **最小命令（设计）**：
  ```bash
  codebuddy plugin validate ./my-plugin     # 校验清单（真实存在，未安装）
  # SBOM 生成（设计）：syft ./image -o spdx-json > sbom.spdx.json
  # 签名校验（设计）：cosign verify --key oidc ...
  ```
- **预期输出**：`plugin validate` 通过；SBOM 含所有依赖；签名可验；OIDC（企业 OAuth Client Credentials，`iam.md`）签发短期 token。
- **失败注入**：① 插件含未声明命令/危险 hook → `validate` 或评审拦截；② 签名不符 → 拒绝加载；③ OIDC token 过期 → 重新 `client_credentials` 换发（`iam.md` 脚本，TTL 5min）；④ 灰度 5% 出现错误率突增 → 自动回滚到上一稳定版；⑤ 密钥误入镜像/日志 → SBOM/扫描告警。
- **回滚**：灰度闸门 5%→20%→100% 每阶 SLO（错误率 < 0.5% 且 P95 延迟不劣化才晋级）；回滚时限 < 5min（配置即代码，Git 还原）。
- **权限与成本**：OIDC 需企业旗舰版（UNVERIFIED 金额）；SBOM/签名工具免费（UNVERIFIED）。
- **可量化验收**：100% 发布物带 SBOM+签名；OIDC 无长期静态密钥（仅 5min TTL 短期 token）；灰度每阶有明确 SLO 闸门；密钥泄漏扫描 0 漏报。
- **OIDC 信任边界澄清**：L1 `--serve` 网关的认证是**自带密码**（`gateway_session`），与平台**企业 OAuth**（`iam.md`）是两套独立信任域；MCP OAuth 回调走内部 RPC 代理（`release-notes v2.125.4`）。二者不可混淆。

---

## ⑤ 历史缺陷 SF01–SF06 整改对照表 + A–E 逐案复盘

### 5.0 总体原则
- 本轮为**新实验 BASELINE**，历史旧报告 70/100 仅作参考；不混号。
- “旧问题”指旧审计/旧报告指出的缺陷；“修复动作”为本轮依据**官方文档+只读CLI** 的纠正；“新证据”给出可溯源出处；“验收结果”区分**已据官方文档核验**与**设计建议/UNVERIFIED**。

### 5.1 SF01（P0）— 原生调度存在性

| 项 | 内容 |
|----|------|
| 旧问题 | 旧报告 §3 称“CodeBuddy 无内建 scheduler”。 |
| 修复动作 | 查官方文档，精确区分**会话任务**（默认，退出即清）、**持久任务**（`durable:true` 写盘、重启后由 daemon 承接，v2.156.0）、**自动到期**（v2.168.3 默认 30 天；`/loop` 上限 3 天 v2.131.0）与**桥接单槽环境是否实际支持**（需 `--serve` 运行，未启动＝未实测）。给出只读验证命令与反例。 |
| 新证据 | ① `tools-reference.md`：`CronCreate`/`CronList`/`CronDelete` 为内建工具；② `scheduled-tasks.md` 与在线 U3：`/loop` 与 cron 任务；③ `http-api.md` + 在线 U1/U2：`GET/POST/PATCH/DELETE /api/v1/scheduled-tasks` 及 `:id/executions`；④ 发布说明 v2.57.0（首次引入）、v2.156.0（daemon 接管持久任务）、v2.166.0（持久任务不再 3 天删）、v2.168.3（30 天有效期）；⑤ 禁用开关：`CODEBUDDY_DISABLE_LOOP` 类环境变量（scheduled-tasks.md:153-159）。 |
| 验收结果 | **已据官方文档核验**：CodeBuddy 确有原生调度（自 v2.57.0 起）。**不得再称无原生调度**。反例：`codebuddy --help` 顶层无 `scheduler` 子命令 ≠ 无调度（能力在会话工具与 REST API）。**本环境未创建任何定时任务**（遵守禁止项）；持久任务是否在本桥接单槽环境实际可用＝U-5 UNVERIFIED（需运行 `--serve`）。 |

### 5.2 SF02（P0）— `--serve` 不是通用多模型推理网关

| 项 | 内容 |
|----|------|
| 旧问题 | 旧报告 §2 候选①及案例 A 把 `codebuddy --serve` 的 Agent REST/ACP 服务称作“通用多模型推理网关”。 |
| 修复动作 | 从官方 `http-api.md` 与 LiteLLM Proxy 官方架构拆出四层（见 §4.0）：Agent 控制面(L1) / OpenAI 兼容推理面(L2) / 策略路由层(L2) / 鉴权账本层(L2)。给出端点协议对照、最小请求样例、未验证边界。 |
| 新证据 | ① `http-api.md` 全量端点表中**无 `/v1/chat/completions`**（§1.4 只读检索）；`/api/v1/runs`（Gateway Protocol，异步返回 runId）与 ACP（`/api/v1/acp`，JSON-RPC over SSE）均为**控制/会话**语义，非推理语义；② `models.md` 中 `/chat/completions` 仅作**上游 `url`** 出现；③ ACP 规范 U8：session/new、session/prompt 等；④ LiteLLM U6/U7：真正的 OpenAI 兼容 `/v1/chat/completions` + 虚拟密钥 + 预算。 |
| 端点协议对照 | `/api/v1/runs`：REST、Gateway Protocol、异步、返回 runId；`/api/v1/acp`：有状态 JSON-RPC over SSE；`/v1/chat/completions`(L2)：无状态 OpenAI 格式、同步/流式、返回 `choices`。**三者不可等同**。 |
| 验收结果 | **已据官方文档核验**：`--serve` 是 Agent 控制面，**不是**多模型推理网关；路由切换须区分“人工（`/model`）”与“策略自动（L2 router）”。L2 是否部署＝U-1 UNVERIFIED。 |

### 5.3 SF03（P0）— models.json 不能实现多租户硬配额

| 项 | 内容 |
|----|------|
| 旧问题 | 旧报告案例 C 称 `models.json` 为每租户配独立 `apiKey` 即可实现额度隔离。 |
| 修复动作 | 明确 `models.json` 仅模型配置；补**可信身份映射 + 服务端授权 + 原子 RPM/TPM + 数据库预算账本 + 幂等计费 + 重试 + 429**。查 LiteLLM 官方预算数据库依赖与 fail-open 风险，设计 fail-closed 故障注入与账本对账。 |
| 新证据 | ① `models.md` 字段表：id/name/vendor/apiKey/url/maxInputTokens/maxOutputTokens/temperature/supports*；**无租户身份、无 RPM/TPM 预算、无账本**；② LiteLLM U7 原文：“Budgets are not enforced without a database”“litellm_settings.max_budget fails open there rather than erroring”“virtual keys themselves need a database (requests carrying one fail with No connected db.)”。 |
| 验收结果 | **已据官方文档核验**：`models.json` 仅模型定义，不能宣称多租户硬配额。多租户需在 L2（LiteLLM）用虚拟密钥 + 预算 DB 实现；**必须 fail-closed**（DB 不可达即拒绝或 provider 侧限额兜底），否则预算 fail-open。L2 实际部署与账本跑通＝U-1/U-6 UNVERIFIED。 |

### 5.4 SF04（P1）— apiKey 明文存储优先用环境变量

| 项 | 内容 |
|----|------|
| 旧问题 | 旧报告称 `models.json` 的 `apiKey` 明文存储，未优先给出官方支持的环境变量引用。 |
| 修复动作 | 核对官方 `models.md` 安全配置：展示仅用**虚拟占位符**的安全样例、最小权限、秘密轮换；明确不建议密钥提交 Git。 |
| 新证据 | `models.md` §安全配置：apiKey 与 url 支持 `${ENV_VAR}` 引用（示例 `"apiKey":"${OPENAI_API_KEY}"`）；建议 `chmod 600`；明确“不要将包含实际密钥的配置文件提交到版本控制系统”；并支持 macOS Keychain 与 `apiKeyHelper`（`iam.md`）。 |
| 验收结果 | **已据官方文档核验**：官方支持环境变量引用，且给出安全建议。本报告所有样例均用占位符 `sk-xxx`/`${VAR}`，**无真实 token**，未提交任何 Git。 |

### 5.5 SF05（P1）— 插件/Skill/MCP 状态与费用区分

| 项 | 内容 |
|----|------|
| 旧问题 | 旧报告若干插件只见 manifest/README 未实装；`--fallback-model`、`security-scan --auto` 等语法未证明；“CLI/插件免费”未核官方价格。 |
| 修复动作 | 区分“命令已在本机只读实测 / 仅文档支持 / 待安装 / 需授权”；提供 `--help` 或官方 URL 及日期；未核价格标 UNVERIFIED。 |
| 新证据 | ① 本机只读实测：`mcp --help`/`plugin --help`/`config --help`/`--version`（§1.3）；② 文档：`plugins.md`（插件可运行命令/访问文件系统，需审查）、`models.md`（含 `relatedModels` 与回退，`--fallback-model` 类由 L2/relatedModels 承担，非 `--serve` 参数——旧报告语法未在官方 CLI 出现）；③ 价格：文档均未标价 → UNVERIFIED（§③）。 |
| 验收结果 | **已据只读CLI+文档核验**：插件/Skill/MCP 能力真实存在但**未安装/未授权**；`--fallback-model`、`security-scan --auto` 在官方 CLI 文档中**未找到对应项**（UNVERIFIED 是否真实语法）；费用严格区分（§③）。未虚构执行与成本。 |

### 5.6 SF06（P1）— 案例 B/D/E 补契约负例与量化验收

| 项 | 内容 |
|----|------|
| 旧问题 | 旧案例 B/D/E 缺契约负例、端到端 trace 关联、脱敏、灰度阈值、回滚时限、OIDC 信任边界。 |
| 修复动作 | 在 §4 案例 B/D/E 中给出可复跑的输入/预期输出/失败注入/量化验收；案例 E 明确 OIDC 信任边界（网关自带密码 ≠ 企业 OAuth）。 |
| 新证据 | `http-api.md` 错误码表（401/403/404/400/429/500 等）；`monitoring.md`（OTEL 导出）；`iam.md`（企业 OAuth Client Credentials，TTL 5min）；`release-notes v2.125.4`（MCP OAuth 内部 RPC 代理）。 |
| 验收结果 | 案例 B/D/E 已给出 ≥7 负例（B）、≥95% 关联率（D）、5%→20%→100% SLO（E）等可量化验收；**端到端跑通与签名/灰度流水线＝设计建议/UNVERIFIED**（未部署）。 |

### 5.7 五个历史案例 A–E 逐案复盘（旧问题→修复动作→新证据→验收结论）

**案例 A（多模型路由）**
- 旧问题：把 `--serve` 等同于推理网关，路由/429/超时/敏感数据测试缺失或错位。
- 修复动作：保留多模型价值，拆 L1（Agent 入口）与 L2（LLM Gateway）；给出 11 条可手工复现测试（§4 案例 A）。
- 新证据：§4.0 架构；U6/U7/U8；`models.md` 回退与 `CODEBUDDY_MAX_RETRIES`（release-notes v2.134.0）。
- 验收结论：架构边界已纠正；11 条测试中 L1/L2 协议差异已厘清；实测部分仅限只读文档与 `--help`，端到端跑通 UNVERIFIED。

**案例 B（API 契约）**
- 旧问题：缺 OpenAPI 差异、401/403/409/429/500 负例、破坏性变更 CI 阻断。
- 修复动作：以 `/api/openapi.json` 为契约基线，列 7+ 负例与 CI 门禁（§4 案例 B）。
- 新证据：`http-api.md` 错误码表与端点表；`/api/openapi.json`、`/api/docs` 为网关自带。
- 验收结论：负例与门禁已设计；契约文件需运行 `--serve` 取得（U-5 UNVERIFIED 实际抓取，但端点/错误码已据文档固化）。

**案例 C（多租户限流计费）**
- 旧问题：“models.json 配 apiKey 即额度隔离”。
- 修复动作：可信身份 + 原子预算账本 + fail-closed + 对账 + 幂等计费（§4 案例 C）。
- 新证据：`models.md` 字段表（无账本）；U7 fail-open 原文。
- 验收结论：旧说法被证伪；正确方案依赖 L2 + DB；DB 离线 fail-closed 为硬要求；实际跑通 UNVERIFIED。

**案例 D（可观测性）**
- 旧问题：缺跨 ChatGPT→MCP→CodeBuddy→Git 的 job_id/trace_id 关联、脱敏、遥测降级。
- 修复动作：30 条 trace 抽样、脱敏召回 100%、Collector 中断本地落盘（§4 案例 D）。
- 新证据：`http-api.md`（traces/jobs 端点、过滤参数）；`monitoring.md`（OTEL 自动补 `/v1/traces`）。
- 验收结论：关联与降级方案已设计；实时抽样需在运行实例上执行（U-5 UNVERIFIED）。

**案例 E（供应链/灰度）**
- 旧问题：缺 SBOM/签名/OIDC/PR 门禁/灰度阈值/回滚 SLO/无密钥泄漏验证。
- 修复动作：SBOM+签名+`plugin validate`+OIDC+TTL 5min+5%→20%→100%+回滚 SLO（§4 案例 E）。
- 新证据：`plugins.md`（validate/结构）；`iam.md`（企业 OAuth Client Credentials）；release-notes v2.125.4（MCP OAuth）。
- 验收结论：OIDC 信任边界已澄清（网关密码 ≠ 企业 OAuth）；SBOM/签名/灰度流水线为设计建议，UNVERIFIED。

---

## ⑥ 适用于下个不同工厂的 2 个通用方法改进候选及指标（下轮 R02 预注册）

> 仅作“候选”预注册；只有 R01 报告与独立审计完成后，据实际结果决定是否采用，不预先宣称有效。

**候选 M1：每条关键能力同时列“官方证据 / 本环境执行证据 / 未验证项”三段式**
- 动机：本轮 SF01–SF06 的误判多源于把“文档设想”当“本环境事实”。三段式强制区分。
- 指标：关键主张（如“存在原生调度”“非推理网关”“无硬配额”）的证据覆盖 ≥90%（即 ≤10% 关键主张仅有未验证项）；审计对“证据可信度”评分提升。
- 适用：F2 及任意新工厂的架构/能力陈述。

**候选 M2：每个案例必须含至少一个负面测试 + 回滚判据**
- 动机：旧案例 B/D/E 缺负例与回滚时限，导致不可验收。本轮 5 案例均强制“失败注入 + 回滚 + 量化验收”。
- 指标：案例负面测试覆盖率 5/5（100%）；每个案例具备可量化验收阈值（如错误码、关联率、SLO）；审计对“案例可复跑性”评分提升。
- 适用：F2 及任意新工厂的验收型案例设计。

---

## 结论与 RESULT_STATUS

本轮在**只读、不安装、不授权、不改生产、不读凭据、不创建子定时任务**约束下，依据 CodeBuddy 随包官方文档（v2.177.0）、官方在线文档（U1–U9，2026-10-31 Web 检索命中）与只读 CLI（`--version`/`--help`）完成 F1 API 与模型服务工厂研究。三个 P0（SF01/SF02/SF03）均已用官方一手证据纠正旧报告错误；SF04/SF05/SF06 亦给出文档级核验与费用/状态严格区分。所有未能亲自实测的内容均明确标注 UNVERIFIED，未宣称已安装或已授权。

**RESULT_STATUS: COMPLETE**
