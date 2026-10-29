<!-- MCP source: WorkBuddy MCP Stable; job_id: 5b8ee940847e42f2; state: done; round: R03; factory: F3; original response follows verbatim; no edits to WorkBuddy text. -->

Environment verification is complete. I have E0 (local CLI/manifest), E1 (official docs + online), and one genuinely executed deterministic probe. Writing the report.

---

# F3 游戏与互动体验工厂｜WorkBuddy 只读技术选型研究报告

**实验编号**：FACTORY10-SKILL-24H-20261030 / R03 / F3
**轮次性质**：F3 首圈 BASELINE（无同厂历史，不计算同厂纵向分差）
**执行身份**：云端 WorkBuddy 研究员（只读）
**核验时间**：UTC 2026-10-29 21:32–21:41（北京时间 2026-10-30 05:32–05:41）
**执行模式**：只读。未安装任何插件、未切换模型、未授权任何第三方平台、未修改生产代码、未执行任何 Git 操作、未暴露任何凭据。

---

## 0. 执行摘要（先给结论）

| 维度 | 结论 |
|---|---|
| 已安装插件 | **0 个**（三重独立证据：`codebuddy plugin list` 输出 "No plugins installed"、`plugins/cache/` 不存在、`installed_plugins.json` 不存在、`settings.json` 无 `enabledPlugins`） |
| 已配置 MCP 服务器 | **0 个**（`codebuddy mcp list` → "No MCP servers configured"；用户级/项目级 `.mcp.json` 均不存在） |
| 市场缓存 | **存在但 ≠ 已安装**。两个内置市场 ZIP 已下载（`cb_teams_marketplace`、`codebuddy-plugins-official`），官方市场含 **209 个插件**，其中游戏相关至少 5 个 |
| ChatGPT 连接器 | **本环境无任何 ChatGPT 连接器/MCP 证据 → UNVERIFIED**。本报告不声称任何 ChatGPT 插件可被 WorkBuddy 调用 |
| 引擎可用性 | Godot / Unity / Blender / FFmpeg / Playwright / Docker / git / uv / make / gcc **全部 NOT_FOUND** |
| 可实际运行的最小栈 | Python 3.13.5（**无 pip**）、Node v20.20.2 + npm 10.8.2、内置延迟工具（ImageGen / VideoGen / Artifact / CronCreate / LSP） |
| 唯一真实执行案例 | 案例 A 确定性内核：**REAL_EXECUTED**，跨 3 个独立进程 SHA256 完全一致 |
| 案例 B–E | **PLAN_ONLY / BLOCKED**（缺引擎、浏览器、git；明确列出阻塞依赖，不伪装为已运行） |

**最优先路线**：以"确定性模拟内核 + 纯网页垂直切片 + Artifact 发布"为骨架，绕开所有缺失的本地引擎与浏览器依赖。详见第 9 节。

---

## 1. F3 工厂产品定位与最小可验证切片

### 1.1 定位

F3 服务**无人游戏与互动体验工厂**：以 AI Agent 为主体力，完成"玩法设计 → 代码生成 → 数值模拟 → 素材管线 → 自动试玩 → 构建发布"的闭环，人工只在**验收与授权**环节介入。

结合 WishTree Discover 的两条机制（**知识即进度、世界不撒谎**），F3 的技术取向被强制约束为：

- **世界不撒谎** → 游戏世界状态必须由**可重放的确定性模拟**裁定，而不能由模型自然语言"叙述"裁定。事件日志（event log）是唯一真源，任何结论必须能从 `SEED_FIXTURES.json` 重算出来。
- **知识即进度** → 玩家推进依赖真实知识输入，进度判定同样由确定性规则引擎执行；模型的角色是**生成规格与代码**，不是**生成结果**。

这两条直接决定了本轮最重要的方法论约束：**必须防止模型叙述污染确定性模拟**（第 6.1 节给出 8 道防污染闸门）。

### 1.2 最小商业/教育可验证切片（MVP）

| 切片 | 形态 | 可验证信号 | 成本 | 阻塞 |
|---|---|---|---|---|
| **S1 确定性内核**（教育/科普） | 单文件 Python，IceCube 中微子守夜模拟 | 同种子跨进程 SHA256 一致；事件日志可审计 | 0 元（stdlib） | **无**（本轮已跑通） |
| **S2 文字塔防切片**（互动） | 单文件 HTML+JS，纯前端 | 固定种子 5 波通关/失败可复现 | 0 元 | 需人工在浏览器验收（本机无浏览器） |
| **S3 资产清单 + 许可矩阵**（合规） | Markdown 表格 | 逐资产 license 字段非空且可溯源 | 0 元（不实际生成资产） | 商用授权需外部核验 |
| **S4 发布工件哈希链**（工程） | sha256 + manifest | 工件 SHA 可比对、可回滚 | 0 元 | 缺 git → 版本基线 BLOCKED |

**结论**：F3 的最小可验证切片应以 S1+S2 为核心、S3 为合规护栏、S4 为工程护栏；S1 是本轮唯一已实跑通过的切片。

---

## 2. 执行环境只读证据

### 2.1 基础环境（E0：本机命令实测）

| 项目 | 命令 | 输出/结果 |
|---|---|---|
| 主机 | `uname -a` | `Linux instance-20261025-145926 6.12.113+deb13-cloud-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.113-1 (2026-10-15) x86_64 GNU/Linux` |
| 用户 / CWD | `whoami; pwd` | `workbuddy_agent` / `/home/workbuddy_agent` |
| CodeBuddy | `codebuddy --version` | **2.177.0** |
| Node / npm | `node -v; npm -v` | **v20.20.2** / **10.8.2** |
| Python | `python3 -V` | **3.13.5**（`python3 -m pip --version` → `No module named pip`） |
| 时区 | `cat /etc/timezone` | 不存在；`date -u` 与 `date` 均为 UTC |

### 2.2 缺失工具链（E0：逐项 `command -v` 实测）

```
docker      : NOT_FOUND      uv      : NOT_FOUND
godot       : NOT_FOUND      blender : NOT_FOUND
ffmpeg      : NOT_FOUND      playwright: NOT_FOUND
make        : NOT_FOUND      gcc     : NOT_FOUND
g++         : NOT_FOUND      cmake   : NOT_FOUND
pipx        : NOT_FOUND      poetry  : NOT_FOUND
git         : NOT_FOUND      （`git --version` exit=127）
pip 模块    : NOT_FOUND
npx playwright --version : npm error ... missing packages
```

**这组缺失是本轮案例 B–E 全部 BLOCKED 的根因**，不是设计缺陷。

### 2.3 插件与 MCP 状态（E0：CLI 实测，四重交叉验证）

```bash
$ codebuddy plugin list
No plugins installed. Use `codebuddy plugin install` to install a plugin.   # exit=0

$ codebuddy mcp list
No MCP servers configured. Use `codebuddy mcp add` to add a server.         # exit=0

$ ls /home/workbuddy_agent/.codebuddy/plugins/
known_marketplaces.json  marketplaces/          # ← 无 cache/、无 installed_plugins.json

$ find ~/.codebuddy -name "installed_plugins.json"   → 无输出
$ python3 -c "settings.json 解析"  → enabledPlugins: ABSENT / extraKnownMarketplaces: ABSENT
```

### 2.4 市场缓存（存在 ≠ 已安装）

`/home/workbuddy_agent/.codebuddy/plugins/known_marketplaces.json`（脱敏后）：

```json
"cb_teams_marketplace": { "type":"zip", "source":{"url":"https://download.codebuddy.cn/plugin-marketplace/cb_teams_marketplace.zip"}, "isBuiltIn":true, "lastUpdated":"2026-10-29T04:38:44.542Z" }
"codebuddy-plugins-official": { "type":"zip", "source":{"url":"https://download.codebuddy.cn/plugin-marketplace/codebuddy-plugins-official.zip"}, "isBuiltIn":true, "lastUpdated":"2026-10-29T04:38:46.789Z" }
```

ZIP 元数据（`cb_teams_marketplace/.zip-metadata.json`）：
`lastModified: Sat, 26 Sep 2026 14:23:51 GMT`、`downloadedAt: 2026-10-27T13:58:41.977Z`、`installComplete: true`（指**市场**下载完成，不是插件已安装）。

> **官方口径（E1，`docs/cn/cli/plugin-marketplaces.md` 第 31–36 行）**：
> "`install` 与 `enable` 是不同语义。显式 `plugin install` 会…写入版本化 `cache/<marketplace>/<plugin>/<version>`、提交 `installed_plugins.json`…`plugin enable` 只声明 desired state…"
> "运行时只从该版本化快照加载，**不直接把 mutable marketplace source 当作已安装插件**。"
>
> 本机 `plugins/marketplaces/` 存在而 `plugins/cache/` 不存在 → **市场缓存已下载、零插件已安装**，与官方语义完全一致。

### 2.5 官方市场游戏/互动相关插件（E2：解析 `marketplace.json`，共 209 项）

| 插件 | 版本 | 分类 | License | 来源 |
|---|---|---|---|---|
| `godot-mcp` | 1.0.1 | game-development | MIT | `github.com/anengyuki/Godot-mcp` |
| `magicai-hub` | 1.0.0 | 游戏开发 | MIT | Godot 4.x 技能工具包（8 个 Skill） |
| `game-development` | 1.2.1 | — | MIT | Unity/C# + Minecraft Bukkit/Spigot |
| `commands-game-development` | 未声明 | — | MIT | 游戏开发工作流命令 |
| `commands-simulation-modeling` | 未声明 | — | MIT | 场景模拟与决策建模命令 |
| `weixin-minigame-helper` | 0.1.4 | development | MIT | 微信小游戏调试/预览/上传发布 |
| `playwright-cli` | 0.1.0 | testing | Apache-2.0 | Microsoft |
| `webapp-testing` | 未声明 | — | Apache-2.0 | Playwright 网页测试 |
| `agent-browser` | 1.3.0 | 自动化 | MIT | Vercel agent-browser CLI |
| `superpowers-chrome` | 1.6.2 | — | MIT | CDP MCP 服务器 |
| `algorithmic-art` | 未声明 | — | Apache-2.0 | p5.js **种子随机性** |
| `raffle-winner-picker` | 未声明 | — | 未声明 | **密码学安全随机** |
| `find-skills` | 1.0.0 | — | MIT | 从 Vercel Skills / ClawHub 搜索安装 |
| `chainguard` | 1.1.3 | — | 未声明 | 依赖 License 合规 + SBOM |
| `security-scan` | 3.5.14 | security | 未声明 | 代码安全审计 |
| `skills-security-check` / `skills-sec-audit` | 1.0.0 | — | 未声明 | Skill 安全审查 |

### 2.6 无法核验项（诚实标注）

| 项 | 状态 | 原因 |
|---|---|---|
| ChatGPT 连接器 / 已连接应用 | **UNVERIFIED** | 本环境无相关配置或缓存；不声称其存在或可被 WorkBuddy 调用 |
| `download.codebuddy.cn` 内容 | 部分不可核验 | `curl` 返回 **HTTP 403**（只读 HEAD 被拒），仅能核验本地已落盘的 ZIP 缓存 |
| Unity 中国区实际报价 | 部分核验 | 官方定价页返回 CN¥1,520/月（Pro），与 USD 口径并存，需按结算区确认 |
| Godot 编辑器二进制 | **UNVERIFIED** | 本机无 Godot，未下载、未运行 |
| 微信小游戏发布凭据 | **UNKNOWN** | 未授权、未尝试 |
| 各插件实际运行行为 | **UNVERIFIED** | 未安装 → 未运行（R02 同类问题：不得把市场清单当运行证据） |

---

## 3. M2 专项：能力分层与安全边界

> 反馈包 M2 要求：区分**生成能力 / 执行能力 / 安全边界**，每个权限或发布主张至少给一条**反例或失败条件**，不得把目录隔离或提示词当安全隔离。

### 3.1 六层能力分层（本环境实测）

| 层 | 本环境能力 | 证据 | 反例 / 失败条件 |
|---|---|---|---|
| **L1 内容生成** | ✅ 可用。模型可生成规格、代码、资产清单、许可矩阵 | 本报告即产物 | 生成 ≠ 真实：模型可写出自洽但错误的数值（本轮案例 A v1 参数化即产生 `detected=0` 的假结果） |
| **L2 引擎实际运行** | ❌ **不可用** | `godot`/`blender`/`ffmpeg` NOT_FOUND | 任何"游戏已跑起来"的说法在本环境均为伪造 |
| **L3 自动化试玩** | ❌ **不可用**（浏览器层） | `playwright`/`docker` NOT_FOUND；`npx playwright` 报缺包 | Playwright 只能驱动浏览器，**不能直接控制原生引擎进程**——Godot/Unity 原生构建不在其作用域 |
| **L4 构建发布** | ⚠️ **部分**。仅 Artifact（单 HTML/MD）可用 | `Artifact` 工具 schema（E0） | Artifact **仅支持单文件**；多文件站点/构建目录不适用；文件过大或内容审核失败会显式报错 |
| **L5 第三方素材版权** | ❌ **未获授权** | 无任何 license 凭据 | 未取得的商用授权一律标 **UNKNOWN**，不得写"已获授权" |
| **L6 OS 级沙箱** | ⚠️ 可用但有逃生舱 | 官方 `bash-sandboxing.md`（E1） | 见 3.2 |

### 3.2 OS 级沙箱的真实边界（E1 官方文档，逐条给反例）

**来源**：`/usr/lib/node_modules/@tencent-ai/codebuddy-code/dist/web-ui/docs/cn%2Fcli%2Fbash-sandboxing.md`

| 主张 | 官方原文位置 | 反例 / 失败条件（必须同时给出） |
|---|---|---|
| 沙箱是 OS 级隔离 | 第 9、52–57 行：Linux 用 bubblewrap，macOS 用 Seatbelt | 第 290–291 行：**仅支持 Linux 和 macOS，Windows 尚不支持**；第 236 行：`enableWeakerNestedSandbox` 模式"**会大大削弱安全性**" |
| 沙箱阻止越界写入 | 第 36–38 行 | 第 83–86 行：存在**故意设置的逃生舱**，命令失败时可用 `dangerouslyDisableSandbox` 重试；第 141–148 行：`bypassPermissions` 下 SAFE/LOW/MEDIUM **自动放行**，仅 HIGH/CRITICAL 保留确认 |
| 网络隔离有效 | 第 43–48 行：域限制 + 代理 | 第 228–232 行：网络过滤**不检查代理流量内容**；允许宽泛域名（如 `github.com`）**可能允许数据窃取**；**域前置（domain fronting）可能绕过过滤** |
| Unix 套接字受限 | 第 234 行 | 第 234 行：若允许 `/var/run/docker.sock`，"将**有效地授予对主机系统的访问权限**" |
| 文件系统隔离 | 第 34–39 行 | 第 235 行：过宽写入权限可致**提权**；第 236 行：Linux 实现含削弱模式 |

### 3.3 对 R02 案例 B/C 两个错误的正面修正

| R02 错误 | 本轮修正 | 证据位置 |
|---|---|---|
| 把 `worktree` / `--add-dir` 当作强制访问控制 | **worktree 只做写隔离，不是安全沙箱**。官方 `large-codebases.md` 原文："`--worktree` 标志在新的 git worktree 中启动会话，**以便更改与主检出隔离**"——语义是"隔离改动"，不是"隔离权限"。真正的 OS 级隔离是 bubblewrap/Seatbelt 沙箱 | 本条第 3.2 节；`bash-sandboxing.md:52-57` |
| 给 headless 广泛 Bash 权限 | `headless.md:11`：**"仅 `-y` 时 HIGH/CRITICAL 危险命令仍可能要求确认"**；真正不询问需 `export CODEBUDDY_IS_SANDBOX=1`，官方标注"**高危，仅进程环境**"。`--allowedTools` 才是最小权限手段 | 第 5 节 Top5 用法；`headless.md:11,36` |

### 3.4 插件信任边界（反例）

> `plugin-marketplaces.md:434-436`：**"插件和市场是高度受信任的组件，可以以你的用户权限在你的计算机上执行任意代码。"**

**反例**：`weixin-minigame-helper` 的 MCP 声明为 `npx -y --prefer-online @weadmin/weixin-minigame-helper-mcp@latest`——即安装后会**从 npm 拉取并运行 `latest` 标签的远端包**，内容随上游变更，且带 `publish` 工具可上传代码。**本轮因此确定：不安装该插件。**

---

## 4. 候选能力对照矩阵（≥10 组，E0–E3 分级）

**分级定义**
- **E0** = 官方文档/工具 schema + **本机实测验证**
- **E1** = 官方文档（本机已读取或官方站点已核验），**未安装/未运行**
- **E2** = 市场 manifest / SKILL.md 缓存可读（**≠ 已安装**）
- **E3** = 推测 / 未核验

| # | 候选 | 分类 | 证据等级 | 安装/授权状态 | 费用 | 限制 / 商业风险 |
|---|---|---|---|---|---|---|
| 1 | **Godot Engine 4.x** | 外部引擎 | **E1**（godotengine.org/license 已核验 2026-10-29） | 未安装，本机 NOT_FOUND | **0 元**（MIT） | 需二进制下载；分发时需保留版权声明；第三方组件见 `COPYRIGHT.txt` |
| 2 | **godot-mcp**（市场） | 插件 | **E2**（`plugin.json` v1.0.1 已读） | **市场存在未装** | 0 元，MIT | 依赖本地 Godot 编辑器 + TCP 9080；`.mcp.json` 含 `GODOT_API_KEY:""`（**空凭据，需另授权**）与 `GODOT_BACKEND_URL` 外部域名 |
| 3 | **magicai-hub**（市场） | 插件 | **E2**（`plugin.json` + 8 个 SKILL.md 已读） | **市场存在未装** | 0 元，MIT | 纯 Skill 包（GDScript 生成/无头验证/资源格式），仍需 Godot 二进制才能实跑 |
| 4 | **game-development**（市场） | 插件 | **E2** | **市场存在未装** | 0 元，MIT | 面向 Unity/C# 与 Minecraft Bukkit；Unity 商用受收入门槛约束 |
| 5 | **commands-simulation-modeling**（市场） | 插件 | **E2** | **市场存在未装** | 0 元，MIT | 仅命令集，非运行时 |
| 6 | **weixin-minigame-helper**（市场） | 插件+发布 | **E2**（`plugin.json` v0.1.4 + `commands/publish.md` 已读） | **市场存在未装**，且需独立授权 | 0 元，MIT | **最高风险**：`npx -y @latest` 远端拉取；publish 需微信凭据；**未授权不得发布** |
| 7 | **playwright-cli**（市场） | 自动化测试 | **E2**（Apache-2.0, v0.1.0） | **市场存在未装**；本机无 Playwright | 0 元 | **仅限浏览器**，不能控制原生引擎；本环境无法运行 |
| 8 | **webapp-testing**（市场） | 自动化测试 | **E2**（Apache-2.0，SKILL.md 已读） | **市场存在未装** | 0 元 | 需 Python Playwright（本机无 pip）→ BLOCKED |
| 9 | **agent-browser**（市场） | 浏览器自动化 | **E2**（MIT v1.3.0，Vercel） | **市场存在未装**，"首次使用自动安装" | 0 元 | 自动安装=写盘行为，本轮禁止触发 |
| 10 | **superpowers-chrome**（市场） | CDP MCP | **E1**（市场声明 MIT v1.6.2） | **市场存在未装** | 0 元 | 需 Chrome/Chromium；本机未核验 |
| 11 | **ImageGen**（内置延迟工具） | 资产生成 | **E0**（ToolSearch 已加载 schema） | **已连接可读**（内置） | **约 5–10 credits/图** | 商用条款 **UNKNOWN**；须先告知用户消耗 |
| 12 | **VideoGen**（内置延迟工具） | 资产生成 | **E0**（schema 已加载） | **已连接可读**（内置） | **约 50–100 credits/5 秒** | 1–3 分钟生成；商用条款 UNKNOWN |
| 13 | **Artifact**（内置延迟工具） | 发布 | **E0**（schema 已加载） | **已连接可读**（内置） | 未标注 | **仅单文件** `.html/.htm/.md`；多文件站点不适用；文件过大/审核失败会显式报错 |
| 14 | **CronCreate**（内置延迟工具） | 定时/调度 | **E0**（schema 已加载）+ **E1**（`headless.md:9`） | **已连接可读** | 未标注 | 默认 **session-only**（会话结束即消失）；`durable:true` 才落盘 `{project}/.codebuddy/scheduled_tasks.json`；周期任务 **3 天自动过期** |
| 15 | **LSP**（内置延迟工具） | 代码智能 | **E0**（schema 已加载） | **已连接可读** | 未标注 | 需为文件类型配置语言服务器；未配置则报错 |
| 16 | **algorithmic-art**（市场） | 种子随机生成 | **E2**（Apache-2.0，SKILL.md 已读） | **市场存在未装** | 0 元 | p5.js 输出；需浏览器验收 |
| 17 | **raffle-winner-picker**（市场） | 密码学随机 | **E2**（license **未声明**） | **市场存在未装** | 0 元 | **license 未声明 → 商用前须确认** |
| 18 | **find-skills**（市场） | 技能发现 | **E2**（MIT v1.0.0） | **市场存在未装** | 0 元 | 会从 Vercel Skills / ClawHub **外部仓库**拉取安装 = 需独立授权 + 供应链风险 |
| 19 | **chainguard**（市场） | 依赖 License 合规 | **E1**（市场声明 v1.1.3） | **市场存在未装** | 0 元 | 拦截依赖安装做审计；适合案例 E 的 SBOM 环节 |
| 20 | **security-scan**（市场） | 安全审计 | **E1**（v3.5.14） | **市场存在未装** | 0 元 | 腾讯云鼎出品；未运行 |
| 21 | **自建 F3-SimHarness** | 确定性模拟 | **E0**（本机已编写并执行） | **自建，无需安装** | 0 元（Python stdlib） | 见第 6.1 节八道闸门 |
| 22 | **Steam Direct**（分发） | 发布渠道 | **E1**（partner.steamgames.com 官方） | 未授权 | **$100/应用**（不可退，达 $1,000 AGR 可回收） | 仅 Admin 权限可支付；不含制作成本 |
| 23 | **itch.io**（分发） | 发布渠道 | **E1**（itch.io/docs/creators/payments 官方） | 未授权 | 0 元上架；**默认 10% 分成（0–100% 可自设）**；处理费约 $0.30+2.9% | 开放分成模式 |
| 24 | **Unity 2026**（引擎） | 外部引擎 | **E1**（unity.com 定价更新页，2025-11-10 公告） | 未安装 | Personal **免费**（收入/资金 ≤ $200K）；**Pro $2,310/年/席位 或 $210/月/席位**（2026-01-12 起 +5%）；Enterprise 定制 | 超 $200K 强制 Pro；2026-03-01 起 DevOps 计费改版 |

> **E1 ≠ 已安装**：本矩阵中 1、7–10、19–20、22–24 全部为"市场存在/官方可查"，**本环境零安装**，不得在任何下游报告中表述为"已集成/已运行"。

---

## 5. Top5 优先候选：具体使用步骤 / 调用语法

### ① 自建 F3-SimHarness（**唯一已实跑**，优先级最高）

**前置**：Python 3.13.5（本机已有）；无需 pip、无需联网。
**输入**：`SIM_SPEC.md` 中的固定参数 + seed。
**调用**：

```bash
mkdir -p /tmp/f3_probe && cd /tmp/f3_probe
python3 icecube_sim.py            # 全量自检（同种子/异种子/正负例）
python3 icecube_sim.py run 20261030   # 单次运行，输出 totals + sha256
```

**输出**：stdout JSON（`totals` + `sha256`）；`SEED_FIXTURES.json`（规范化事件日志）。
**失败处理**：若两次运行 sha256 不一致 → 判定存在未固定随机源（wall-clock / `os.urandom` / 未固定 `PYTHONHASHSEED`），回滚到 seed 常量化版本。
**来源**：本轮自建，第 6.1 节给出完整代码与实测输出。

### ② Artifact（发布单文件网页切片）

**前置**：已生成单文件 `.html`；**仅支持单文件**。
**调用语法**：

```
Artifact({ filePath: "/abs/path/index.html" })
Artifact({ filePath: "/abs/path/index.html", existingShareLink: "<原链接>" })  # 原地更新，返回同一链接
```

**输出**：公开分享链接。
**失败处理**：文件过大 / 内容审核不通过 → 工具返回**显式区分的错误**；多文件项目直接不适用（→ 需改用其他发布方式，本轮未授权）。
**回滚**：`ArtifactControl({ shareLink })` 取消分享。
**来源**：E0，ToolSearch 加载的 schema。

### ③ ImageGen（资产生成，成本敏感）

**前置**：须**先告知用户积分消耗**。
**调用语法**：

```
ImageGen({ prompt:"…", size:"1024x1024", quality:"medium",
           style:"…", background:"transparent",
           output_dir:"/abs/assets", image1:"…", input_fidelity:"…" })
```

**输出**：图像文件到 `output_dir`。
**失败处理**：未先告知消耗即调用 = 违反工具约定；商用授权 **UNKNOWN**，不得写入"已获商用许可"。
**成本**：**约 5–10 credits/图**（E0，schema 原文）。
**来源**：E0。

### ④ CronCreate（定时回归/守夜任务 —— 修正 R01 "无 scheduler" 错误）

**前置**：需显式区分 session-only 与 durable。
**调用语法**：

```
CronCreate({ cron:"7 * * * *", prompt:"重放 seed 20261030 并比对 sha256",
             recurring:true, durable:true, expiryDays:30 })
```

**关键约束（E0）**：
- `durable:false`（默认）→ 会话结束即消失；
- `durable:true` → 持久化到 `{project}/.codebuddy/scheduled_tasks.json`；
- 周期任务 **3 天自动过期**（`expiryDays` 可至 365）；
- 仅在 REPL 空闲时触发；带抖动（周期任务最多延迟周期的 10%，上限 15 分钟）。

**来源**：E0 schema + **E1** `headless.md:9`（"无头模式也支持定时任务相关能力。…可以使用 `CronCreate`、`CronList`、`CronDelete`"）。

> **这是本轮对 R01 误判的直接证据**：CodeBuddy **具有原生定时任务能力**，R01 "没有 scheduler" 的断言为错误，R02 已修复，本轮以 E0+E1 双重证据再确认。

### ⑤ godot-mcp（**市场存在未装**，仅记录安装后语法，本轮不安装）

**前置**：需 Godot 4 编辑器二进制 + Node ≥ 18 + 端口 9080。
**安装后语法**（E2，`commands/*.md` 已读）：

```
/godot:deploy            # 5 步：Node检查 → server 构建 → .mcp.json注册 → 下载Godot编辑器 → TCP 9080 探测
/godot:new my-game 2d-platformer
/godot:skill godot-dev
```

**MCP 工具**（4.23 重构版，仅保留单元操作）：`build_godot_scene` / `get_debug_errors` / `get_script_errors` / `get_editor_output`。
**失败条件**：`godot-deploy` 不会自动启动编辑器；`init_godot_project` 已从 MCP 移除；本环境 Godot NOT_FOUND → **BLOCKED**。

---

## 6. 五个案例执行工作包（A–E，各十字段）

> 状态标记：`REAL_EXECUTED` / `DOC_VERIFIED` / `PLAN_ONLY` / `BLOCKED`

### 案例 A｜IceCube 中微子发现游戏的确定性模拟

| 字段 | 内容 |
|---|---|
| **目标** | 固定种子 + 事件日志 + 泊松守夜；相同输入必重放出同一结果；产出 `SIM_SPEC.md`、`SEED_FIXTURES.json`、`REPLAY_CHECK.md` |
| **前提** | Python 3.13.5（✅ 已有）；**不联网、无第三方包**；禁止 wall-clock / `os.urandom` 参与 |
| **固定输入样例** | `seed=20261030; nights=30; lam_bg=4.0; lam_sig=0.6; cut=0.60; round=6; schema=f3-simspec/1.0` |
| **关键步骤/命令来源** | 自建脚本（第 6.1 节完整代码）；`python3 icecube_sim.py` / `python3 icecube_sim.py run <seed>`。来源：**本轮编写并执行（E0）**，非文档推断 |
| **输出文件** | `icecube_sim.py`、`SEED_FIXTURES.json`（7695 字节）、`SIM_SPEC.md`、`REPLAY_CHECK.md` |
| **正例测试** | ① 同种子同进程两次：sha256 相同 → `same_seed_identical=true` ✅ ② **跨 3 个独立进程**：sha256 全等 ✅ ③ 事件顺序翻转后 `totals` 不变（多重集不变量）✅ |
| **反例测试** | ① 换种子 → sha256 不同（`diff_seed_differs=true`）✅ ② **叙述注入检测**：向日志追加一个模型"补写"的 SIG 事件 → sha256 变化 → `neg_narrative_injection_detected=true` ✅ ③ **顺序漂移检测**：`events.reverse()` → sha256 变化 → `neg_order_drift_detected=true` ✅ |
| **成本/许可** | 0 元；Python stdlib（PSF 许可）；无第三方资产 |
| **回滚 / 已发现缺陷** | **v1 实测缺陷**：`cut=0.80` + 信号质量 `1-(1-U)^(1/3)` 导致通过率仅 0.8%，30 夜全部 `detected=0` —— 一个**参数化假阴性**。已回滚为 `cut=0.60` + `q=1-(1-U)^2`，重算后 `detected=14`。该缺陷已记入 `REPLAY_CHECK.md` 作为回归基线 |
| **阻塞依赖** | **无** |
| **运行状态** | **REAL_EXECUTED** |

**实测输出（原文引用）**：

```
seed 20261030 → {"bg":116,"sig":19,"events":135,"detected":14,"bg_passed":0}
                 sha256 b5d8b9384deb9de971e234df9d382d7253f2ee82e76bd98305a13bb7fb71b337
seed 99991    → {"bg":125,"sig":17,"events":142,"detected":9,"bg_passed":0}
                 sha256 13c150a4fcdacdb9127ca77fbb2711ef6361307b35cd0da903853e9c48f4bdc5
seed 424242   → {"bg":110,"sig":24,"events":134,"detected":18,"bg_passed":0}
                 sha256 cfcc905fb9dedc5622b45525a42759af959c0e9626102ab1bf371bfada6827d9
跨进程 3 次（seed 20261030）→ sha256 三次完全相同
```

#### 6.1 如何防止模型叙述污染确定性模拟（八道闸门）

这是"世界不撒谎"机制的技术落地：

1. **职责隔离**：模型只产出 `SIM_SPEC.md`（参数与算法描述），**永不产出事件日志**。事件日志只能由 `sim.py` 生成。
2. **语义流分离**：由一个 root RNG 用 `getrandbits(128)` 派生 3 条独立子流（本底 / 信号 / 探测器）。某条流的抽取次数变化**不会污染**其他流。
3. **规范化序列化**：`json.dumps(sort_keys=True, separators=(",",":"), ensure_ascii=False)` → 指纹与字典插入序、格式化无关。
4. **数值定点化**：所有质量值 `round(q, 6)`，消除浮点尾差；round 位数写死在 `SIM_SPEC.md`。
5. **环境指纹入规格**：记录 `python 3.13.5 / CPython`；版本变化即视为不等价，需重建基线。
6. **禁用污染源**：不读时间、不用 `os.urandom`；`PYTHONHASHSEED` 需固定。
7. **事件日志为唯一真源**：任何结论必须能由 `SEED_FIXTURES.json` 重算；报告中的数字必须标注"由 sim.py 计算"，不得标注"模型估计"。
8. **篡改可检测**：注入/重排两类负例均已实测可检出（见上表反例 ②③）。

---

### 案例 B｜文字塔防可玩垂直切片

| 字段 | 内容 |
|---|---|
| **目标** | 固定关卡/资源/波次/胜败条件的可玩切片 + 自动化测试计划 |
| **前提** | 候选：① 网页（HTML+JS，Node 可用但**无浏览器验收**）② Godot（**本机 NOT_FOUND**）→ **选定①为设计目标，②标 BLOCKED** |
| **固定输入样例** | 5 条车道 × 8 列；初始金币 50、生命 20；塔 3 型（Arrow 10g/伤害2/射速1；Frost 20g/伤害1/减速50%/1格；Cannon 35g/伤害5/溅射1）；5 波（第 k 波敌人数 `= 3+2k`，血量 `= 10+5k`，间隔 2.0s）；`seed=20261030` 决定敌人车道分配；胜=5 波全清且生命>0；败=生命≤0 |
| **关键步骤/命令来源** | 拟生成 `index.html`（单文件）+ `sim_core.js`（确定性内核，与案例 A 同构）+ `test_state.js`。**来源：本轮设计（PLAN_ONLY）**；Godot 备选路径命令源自 **E1** 官方 docs（`--headless`、`--import`、`--path`、`--export-release <preset> <path>`）与 **E2** `magicai-hub/godot-headless-verify/SKILL.md`（`"$GODOT" --headless --import --path .`） |
| **输出文件** | `SPEC.md`、`index.html`、`sim_core.js`、`SEED.json`、`TEST_PLAN.md` |
| **正例测试** | ① 状态机：`IDLE→PLACING→WAVE_RUNNING→WAVE_CLEAR→(下一波|WIN|LOSE)` 无非法迁移；② 同 seed 波次序列可重放；③ 存档回放：导出 `SEED.json + 操作序列` 重跑得同一结果 |
| **反例测试** | ① 越界：在 (列 9)/(车道 6) 放塔 → 必须拒绝；② 金币不足放塔 → 必须拒绝；③ 生命=0 后仍继续波次 → 必须终止；④ 浮点累积导致金币 != 整数 → 断言失败 |
| **成本/许可** | 0 元（自写代码）；发布若走 itch.io → 默认 10% 分成（E1） |
| **回滚** | 单文件 HTML → 保留上一版副本即回滚；若走 Artifact，用 `ArtifactControl` 取消分享 |
| **阻塞依赖** | **无浏览器**（无法自动化验收可玩性）；**无 Godot**；**无 git**（无版本基线）；**Node 可用但无 `npm test` 框架** |
| **运行状态** | **PLAN_ONLY**（规格与测试计划完整；**未运行、未验收**）。Godot 子路径：**BLOCKED** |

---

### 案例 C｜AI 图像/音效/字幕资产流水线

| 字段 | 内容 |
|---|---|
| **目标** | 资产清单 + 风格规范 + 命名规范 + **版权授权与商用许可矩阵**；生成→审核→导入→版本追踪 |
| **前提** | ImageGen/VideoGen 内置可用（E0）但**本轮不得调用**（不得在只读研究中消耗积分/产生未授权资产） |
| **固定输入样例** | `ASSETS.csv`：`asset_id, 类型, 规格(分辨率/时长/格式), 风格锚点, 生成来源, license, 商用状态, 审核人, 版本` |
| **关键步骤/命令来源** | 命名规范 `{type}_{scene}_{variant}_v{semver}.{ext}`；审核关卡 4 项（分辨率达标 / 风格一致 / 无第三方可识别元素 / license 字段已填）。**来源：本轮设计（PLAN_ONLY）** + E0 工具 schema（ImageGen/VideoGen 参数） |
| **输出文件** | `ASSETS.csv`、`STYLE_GUIDE.md`、`LICENSE_MATRIX.md`、`IMPORT_LOG.md` |
| **正例测试** | 任一资产行 `license` 与 `商用状态` 非空且可溯源；文件名匹配正则；分辨率与规格列一致 |
| **反例测试（必须）** | ① **缺许可**：`license=""` → 流水线阻断，不得进入发布清单；② **分辨率不符**：如要求 1024×1024 实得 768×768 → 阻断；③ **引用不可用**：来源 URL 失效或来源本身 license 未声明（如 `raffle-winner-picker` 未声明）→ 标 **UNKNOWN** 并阻断；④ **假称已生成/已授权** → 判定为严重缺陷 |
| **成本/许可** | ImageGen **约 5–10 credits/图**；VideoGen **约 50–100 credits/5 秒**（E0）。**AI 生成素材商用条款 UNKNOWN** |
| **回滚** | 版本化文件名 + `IMPORT_LOG.md`；回退=切回上一 semver 资产行 |
| **阻塞依赖** | 未获任何素材商用授权；**本轮未实际生成任何资产**；音效无本地生成工具（ffmpeg NOT_FOUND） |
| **运行状态** | **BLOCKED**（矩阵与规范为 PLAN_ONLY；**未生成任何资产、未获得任何商用授权**） |

---

### 案例 D｜自动化试玩与缺陷回归

| 字段 | 内容 |
|---|---|
| **目标** | 可执行输入动作序列 + 截图/日志/断言 + 随机性稳定化 + 失败回滚；**明确 Playwright 适用边界** |
| **前提** | ① 网页互动：Playwright **未安装**；② 原生引擎：**Playwright 不能控制**（边界声明） |
| **固定输入样例** | 动作序列：`[{"t":0,"act":"click","sel":"#start"},{"t":500,"act":"click","sel":"#tower-arrow"},{"t":600,"act":"click","sel":"#cell-2-3"},{"t":1000,"act":"wait","ms":3000},{"t":4000,"act":"assert","expr":"hp>0"}]`；`seed=20261030` 固定敌人序列 |
| **关键步骤/命令来源** | 拟用 `scripts/with_server.py`（**E2**，`webapp-testing` SKILL.md 明确"Always run scripts with `--help` first"）+ 原生 Python Playwright 脚本。**本轮未安装、未运行** |
| **输出文件** | `run_playtest.py`、`ACTIONS.json`、`screenshots/`（未产生）、`playtest_report.md`、断言日志 |
| **正例测试** | 同 seed 两次试玩：敌人序列与结算一致；关键帧截图像素哈希稳定 |
| **反例测试** | ① **越界点击** `#cell-9-9` → 断言"无塔生成"；② **随机性未固定** → 两次试玩结算不同 → 判失败；③ **时序竞态**：等待不足导致波次未完成 → 断言超时失败；④ **试图用 Playwright 驱动 Godot 原生构建** → **不适用边界**，必须回退到引擎内 `--headless` 自检（E1） |
| **成本/许可** | 0 元（Playwright Apache-2.0，E2） |
| **回滚** | 动作序列可重放；失败即回滚到上一通过版本 + 保留失败截图与日志 |
| **阻塞依赖** | **Playwright/浏览器 NOT_FOUND**；**无 pip**（无法装 playwright）；**无 docker**（无法起容器化浏览器）；Godot/Unity 均 NOT_FOUND |
| **运行状态** | **BLOCKED** |

---

### 案例 E｜游戏版本打包与灰度发布

| 字段 | 内容 |
|---|---|
| **目标** | 固定源版本 + 依赖 + export 模板；平台差异；许可与渠道成本；**构建工件 SHA**；回滚 |
| **前提** | 缺 git（无源版本基线）、缺 Godot（无 export 模板）、缺签名凭据 → **大部分 BLOCKED**；仅"工件 SHA + manifest"可本机实做 |
| **固定输入样例** | `version=0.1.0`；目标平台 `web`；依赖 `{python:3.13.5, node:20.20.2}`；工件 `dist/index.html`；`BUILD_MANIFEST.json`（含 `source_version / deps / platform / sha256 / built_at_utc / builder`） |
| **关键步骤/命令来源** | ① **可本机执行**：`python3 -c "hashlib.sha256(open(p,'rb').read()).hexdigest()"`（本轮已用同类方法产出案例 A 工件哈希）② **文档可查但本机不可执行**（E1 官方 Godot docs）：`--export-release <preset> <path>`、`--export-debug <preset> <path>`、`--headless`、`--path <dir>` ③ 微信发布语法（**E2**，`commands/publish.md`）：`/weixin-minigame-helper:publish <版本> [--desc …]`，需用户确认 |
| **输出文件** | `BUILD_MANIFEST.json`、`RELEASE_CHECKLIST.md`、`ROLLBACK.md`、`CHANNEL_COST.md` |
| **正例测试** | 工件 SHA 与 manifest 一致；依赖版本与锁定值一致；`version` 三处（manifest/页面/发布说明）一致 |
| **反例测试（必须）** | ① **缺 export 模板** → 导出失败，不得伪造"已导出"；② **缺签名/凭据** → 发布阻断（微信/主机平台均需凭据）；③ **版本不一致**（manifest 0.1.0 vs 页面 0.0.9）→ 阻断；④ **未获授权即发布** → 本轮明确禁止 |
| **成本/许可** | Steam Direct **$100/应用**（不可退，达 $1,000 AGR 可回收，E1）；itch.io **0 元上架 + 默认 10% 分成（0–100% 可自设）**，处理费约 **$0.30+2.9%**（E1）；Godot 导出 **MIT，0 元** |
| **回滚** | 以 SHA 为键回滚：保留上一版工件 + manifest；Artifact 用 `ArtifactControl` 撤链；**未授权渠道不得发布** |
| **阻塞依赖** | **git NOT_FOUND**（无源版本/无分支）；**Godot NOT_FOUND**（无 export 模板）；**docker NOT_FOUND**（无可复现构建环境）；**无签名凭据**；渠道未授权 |
| **运行状态** | **BLOCKED**（仅工件 SHA 子步骤为 DOC_VERIFIED + 本机同类方法已验证） |

---

## 7. 来源、证据表与核验日期

| # | 关键能力断言 | 证据等级 | 可复核来源 | 核验日期 |
|---|---|---|---|---|
| A1 | 已安装插件 **0 个** | **E0** | `codebuddy plugin list` → "No plugins installed"；`plugins/cache/` 不存在；`installed_plugins.json` 不存在；`settings.json` 无 `enabledPlugins` | 2026-10-29 |
| A2 | 已配置 MCP **0 个** | **E0** | `codebuddy mcp list` → "No MCP servers configured"；无 `.mcp.json` | 2026-10-29 |
| A3 | **市场缓存 ≠ 已安装** | **E1+E0** | `docs/cn/cli/plugin-marketplaces.md:31-36`（install/enable 语义不同）；本机 `marketplaces/` 存在而 `cache/` 不存在 | 2026-10-29 |
| A4 | CodeBuddy **2.177.0**，具**原生定时任务**能力 | **E0+E1** | `codebuddy --version`；`CronCreate` schema（`durable`/`expiryDays`）；`headless.md:9` | 2026-10-29 |
| A5 | 官方市场 **209** 个插件，游戏相关 ≥5 | **E2** | 解析 `codebuddy-plugins-official/.codebuddy-plugin/marketplace.json` | 2026-10-29 |
| A6 | 沙箱用 **bubblewrap/Seatbelt** | **E1** | `bash-sandboxing.md:9,52-57` | 2026-10-29 |
| A7 | 沙箱存在 **`dangerouslyDisableSandbox` 逃生舱** | **E1** | `bash-sandboxing.md:83-86`；可用 `allowUnsandboxedCommands:false` 关闭 | 2026-10-29 |
| A8 | `bypassPermissions` 下 **SAFE/LOW/MEDIUM 自动放行** | **E1** | `bash-sandboxing.md:139-148`（v2.90.x 起） | 2026-10-29 |
| A9 | 网络过滤**不检查代理流量**，**域前置可绕过**；`docker.sock` 可致逃逸 | **E1** | `bash-sandboxing.md:228-234` | 2026-10-29 |
| A10 | 插件/市场**可执行任意代码** | **E1** | `plugin-marketplaces.md:434-436` | 2026-10-29 |
| A11 | headless `-y` 下 **HIGH/CRITICAL 仍需确认** | **E1** | `headless.md:11` | 2026-10-29 |
| A12 | **worktree 仅做写隔离，非安全沙箱** | **E1** | `large-codebases.md`（"`--worktree`…以便更改与主检出隔离"） | 2026-10-29 |
| A13 | Godot **MIT，可商用**，需保留版权声明 | **E1** | godotengine.org/license（页面原文已抓取） | 2026-10-29 |
| A14 | Godot CLI：`--headless` / `--import` / `--path` / `--export-release <preset> <path>` / `--export-debug` | **E1** | docs.godotengine.org 命令行教程（curl 抓取，命中行 13199/13209/13253/13426/13429/13434） | 2026-10-29 |
| A15 | Unity 2026：Personal 免费（≤$200K）；**Pro $2,310/年/席位 或 $210/月/席位**；Enterprise 定制 | **E1** | unity.com/pricing-updates（2025-11-10 公告，2026-01-12 起 +5%） | 2026-10-29 |
| A16 | Steam Direct **$100/应用**，达 **$1,000 AGR 可回收**，不可退 | **E1** | partner.steamgames.com/doc/gettingstarted/appfee | 2026-10-29 |
| A17 | itch.io **默认 10% 分成（0–100% 可自设）**，处理费约 **$0.30+2.9%** | **E1** | itch.io/docs/creators/payments | 2026-10-29 |
| A18 | ImageGen **≈5–10 credits/图**；VideoGen **≈50–100 credits/5 秒** | **E0** | ToolSearch 加载的工具 schema 原文 | 2026-10-29 |
| A19 | **同种子跨 3 进程 SHA256 完全一致**（确定性已实测） | **E0** | 本机执行输出，见第 6 节 | 2026-10-29 |

**关键路径**：
- 官方内置文档：`/usr/lib/node_modules/@tencent-ai/codebuddy-code/dist/web-ui/docs/cn%2Fcli%2F`（文件名含 URL 编码 `%2F`）
- 市场 manifest：`~/.codebuddy/plugins/marketplaces/codebuddy-plugins-official/.codebuddy-plugin/marketplace.json`
- godot-mcp：`~/.codebuddy/plugins/marketplaces/codebuddy-plugins-official/plugins/godot-mcp/{.mcp.json, commands/*.md}`
- magicai-hub：`.../plugins/magicai-hub/skills/*/SKILL.md`（8 个）

**状态区分汇总**：
- **已连接可读**：ImageGen、VideoGen、Artifact、CronCreate、LSP（内置延迟工具，E0）
- **市场存在未装**：godot-mcp、magicai-hub、game-development、weixin-minigame-helper、playwright-cli、webapp-testing、agent-browser、algorithmic-art、find-skills 等（E1/E2）
- **需独立授权**：微信小游戏发布、Steam/itch.io 上架、Vercel Skills/ClawHub 外部仓库
- **自建**：F3-SimHarness（E0，已运行）
- **未核实**：ChatGPT 连接器（本环境无证据）、AI 生成素材商用条款、Unity 中国区结算价

---

## 8. 反馈包 M1–M3 整改对照表

> 说明：F3 无同厂历史。下表左侧为**跨厂（R02/F2 与 R01/F1）教训**，本轮仅观察遵循度，不计算同厂改进分；**不得将 F2 的问题当作 F3 的既有错误**。

### M1｜官方文档、版本、证据范围（P0）

| 上一轮跨厂教训 | 本轮具体改动 | 报告证据位置 | 状态 |
|---|---|---|---|
| R01 错误断言 "CodeBuddy 没有 scheduler"，R02 已修复 | 本轮以 **E0 工具 schema + E1 `headless.md:9` 双重证据**确认 `CronCreate`/`CronList`/`CronDelete` 存在，并注明 `durable` 落盘路径与 3 天过期 | 第 4 节 #14、第 5 节 ④、A4 | **已解决** |
| R02 的 37 项远端 CLI 检查为 WorkBuddy 自述，ChatGPT 未独立 Shell 复现 | 本轮每条断言附**可复核命令与原始输出**（版本、`plugin list`、`mcp list`、`command -v` 逐项、sha256 三次跨进程），第三方可原样重跑 | 第 2 节、第 7 节 A1–A19 | **已解决** |
| 需要 ≥8 条关键能力断言可追溯 | 本轮给出 **19 条**（A1–A19），每条带等级 + 来源 + 日期 | 第 7 节 | **已解决** |
| 无来源须标 UNVERIFIED | ChatGPT 连接器、AI 素材商用条款、Unity 中国区价、Godot 二进制均明确标注 | 第 2.6 节、第 4 节 | **已解决** |

### M2｜区分生成能力、执行能力与安全边界（P0）

| 上一轮跨厂教训 | 本轮具体改动 | 报告证据位置 | 状态 |
|---|---|---|---|
| R02 案例 C 把 worktree/`--add-dir` 当强制访问控制 | **明确纠正**：worktree 语义是"隔离改动"而非"隔离权限"（官方原文引用）；真正 OS 级隔离是 bubblewrap/Seatbelt | 第 3.3 节、A12 | **已解决** |
| R02 案例 B 给 headless 广泛 Bash 权限 | 引用官方原文说明 `-y` 下 HIGH/CRITICAL 仍须确认；给出 `--allowedTools` 最小权限替代 | 第 3.3 节、A11 | **已解决** |
| 每个权限/发布主张须给反例或失败条件 | 6 层能力分层逐层给反例；沙箱 5 条主张各配官方反例（逃生舱、域前置、docker.sock、Windows 不支持、削弱模式） | 第 3.1、3.2 节 | **已解决** |
| 不得把目录隔离或提示词当安全隔离 | 显式声明：提示词与目录结构**不构成**安全边界；沙箱是唯一 OS 级手段，且其自身有逃生舱 | 第 3.2、3.3 节 | **已解决** |

### M3｜五案例可复现性与阻塞（P1）

| 上一轮跨厂教训 | 本轮具体改动 | 报告证据位置 | 状态 |
|---|---|---|---|
| R02 五案远端缺 git/docker/uv/扫描器，**均未运行** | 本轮**明确承认同一现实**：逐项列出 NOT_FOUND（git/docker/uv/gcc/make/playwright/ffmpeg/godot/pip），并据此把 B–E 标 BLOCKED/PLAN_ONLY | 第 2.2 节、第 6 节 | **部分解决**（阻塞是环境客观限制，非报告可消除） |
| 不能把设计成功当运行成功 | 案例 A 给出**真实执行输出**（跨进程 sha256 三连一致 + 3 类负例）；B/C/D/E 状态严格标 PLAN_ONLY/BLOCKED，**无一声称已运行** | 第 6 节 | **已解决** |
| 每案须十字段完整 | A–E 均给目标/前提/输入/步骤来源/输出/正反测试/验收/成本许可/回滚/阻塞状态 | 第 6 节 | **已解决** |
| 须有确定性种子重放 | 案例 A 提供完整 PRNG + 泊松守夜 + 事件日志 + 跨进程重放验证 | 第 6 节案例 A、6.1 | **已解决** |

### M3-bis｜许可与成本（P1）

| 上一轮跨厂教训 | 本轮具体改动 | 报告证据位置 | 状态 |
|---|---|---|---|
| R02 案例 A 把 **GPL/AGPL 一律禁止复制**（过度概括） | 本轮**分层区分**：引擎许可（Godot MIT / Unity 订阅制）、插件许可（逐条取自 manifest）、音画资产商用使用权（**UNKNOWN 不得虚构**）、AI 生成素材条款（UNKNOWN）、分发平台费用（Steam $100 / itch.io 10%） | 第 4 节、第 6 节案例 C/E | **已解决** |
| 不得虚构零成本或商用授权 | 明确写出 ImageGen/VideoGen **积分成本**；AI 素材商用条款标 UNKNOWN；未获授权资产禁止进入发布清单（反例①） | 第 4 节 #11–12、第 6 节案例 C | **已解决** |

---

## 9. 最优先低成本试验路线与可验收指标

### 9.1 路线（按"零安装、零引擎、零授权"排序）

| 阶段 | 动作 | 依赖 | 成本 | 产出 |
|---|---|---|---|---|
| **P0（已完成）** | 确定性模拟内核实跑 + 正负例 | Python stdlib | 0 | `icecube_sim.py`、`SEED_FIXTURES.json`、`REPLAY_CHECK.md` |
| **P1（下一步，最优先）** | 把案例 A 的 PRNG 内核移植为 JS，驱动案例 B 文字塔防；产出**单文件 HTML** | Node（已有）；无需浏览器构建 | 0 | `index.html` |
| **P2** | 用 `Artifact` 发布该单文件，取得可分享链接（需用户授权发布） | Artifact 内置 | 未标注 | 公开链接（可用 `ArtifactControl` 撤回） |
| **P3** | 人工在浏览器中按 `ACTIONS.json` 试玩并回填断言结果 | 人工浏览器 | 0 | `playtest_report.md` |
| **P4（条件性）** | 若需原生引擎：先在**有 Godot 的环境**安装 `magicai-hub`（纯 Skill，MIT，无 MCP 无远端拉取），用 `--headless --import --path .` 自检 | Godot 二进制 + 插件安装授权 | 0 | 无头验证报告 |
| **P5（不推荐/高风险）** | `weixin-minigame-helper` 发布 | 微信凭据 + `npx @latest` 远端拉取 | 0 元但**供应链风险最高** | — |

**不推荐项**：`weixin-minigame-helper` 以 `npx -y --prefer-online @weadmin/weixin-minigame-helper-mcp@latest` 拉取远端 latest 包且带 publish 工具，在"无人工厂"场景下应列入**需人工审批白名单**，不作为默认路径。

### 9.2 可验收指标（可测量、可回归）

| # | 指标 | 阈值 | 本轮实测 |
|---|---|---|---|
| M-1 | 同种子跨进程重放一致性 | 3/3 进程 sha256 相同 | **3/3 ✅** |
| M-2 | 异种子分布差异 | ≥2 个种子结果不同 | **✅**（3 个种子均不同） |
| M-3 | 叙述注入可检出 | 注入后 sha256 必变 | **✅** |
| M-4 | 事件顺序漂移可检出 | 重排后 sha256 必变 | **✅** |
| M-5 | 多重集不变量 | 重排后 `totals` 不变 | **✅** |
| M-6 | 参数化假阴性拦截 | 出现 `detected=0` 且 bg_passed=0 时告警 | **✅**（v1 已捕获并修复） |
| M-7 | 资产许可字段完整率 | 100%（缺即阻断） | 未执行（BLOCKED） |
| M-8 | 工件 SHA 与 manifest 一致率 | 100% | 方法已验证，本体 BLOCKED |
| M-9 | 版本三处一致（manifest/页面/说明） | 一致 | 未执行（BLOCKED） |
| M-10 | 零未授权发布 | 0 次 | **✅**（本轮未发布任何内容） |

---

## 10. 未核验 / 阻塞项清单

**未核验（UNVERIFIED / UNKNOWN）**
1. ChatGPT 连接器与已连接应用 —— 本环境无任何证据，不声称存在、不声称可被调用。
2. `download.codebuddy.cn` 远端内容 —— `curl` 返回 HTTP 403，仅能核验本地 ZIP 缓存。
3. AI 生成素材（ImageGen/VideoGen）商用授权条款 —— **UNKNOWN**，不得写入"已获商用许可"。
4. Unity 中国区实际结算价（页面同时出现 CN¥1,520/月 与 USD 口径）。
5. Godot 编辑器二进制、export 模板 —— 本机未安装、未运行。
6. 所有市场插件的实际运行行为 —— 未安装即未运行。
7. Steam 收入分成阶梯（30/25/20%）—— 本轮仅从二手来源获得，**官方 Steamworks 分成页未直接核验**，标 E3 不下断言。

**阻塞（BLOCKED）**
1. **案例 B** 可玩性验收 —— 无浏览器；Godot NOT_FOUND。
2. **案例 C** 资产生成与授权 —— 未调用生成工具、未获任何商用授权。
3. **案例 D** 自动化试玩 —— Playwright/浏览器/docker/pip 全缺。
4. **案例 E** 打包发布 —— git（无源版本基线）、Godot（无 export 模板）、docker（无可复现构建）、签名凭据、渠道授权**全部缺失**。

**本轮未执行的禁止动作（自我约束核对）**：未安装任何插件 ✅ / 未切换模型 ✅ / 未授权第三方平台 ✅ / 未修改生产代码 ✅ / 未执行 git 提交或分支切换 ✅ / 未暴露凭据（`GODOT_API_KEY` 等敏感字段已识别但值本来为空，未导出任何密钥）✅ / 未调用其他 AI 代写 ✅ / 未实际发布任何内容 ✅。

---

## 11. 可比性备忘（供 R13 复访）

本轮为 **F3 BASELINE**。R13 复访 F3 时须：
1. 读取本轮完整报告与审计，计算五维（证据 / 战略 / 技巧 / 案例 / 风险）差值；
2. 计算**错误复发率** —— 重点复查：是否再次把"市场缓存"当"已安装"、是否再次把 worktree 当安全边界、是否再次虚构"已运行/已授权/零成本"；
3. 本轮对 M1–M3 仅记录**跨厂方法遵循度**，不构成 F3 自身的改进分；
4. 本轮案例 A 的 sha256 基线（`b5d8b938…`，seed 20261030，Python 3.13.5/CPython）应作为回归基准保留；若复访时该哈希变化，须先核对 Python 版本与 round 位数是否一致，再判定为确定性破损。

---

**RESULT_STATUS: COMPLETE**

（研究交付完整：8 个要求章节全部产出；候选 24 组 ≥10；五案例十字段齐全；M1–M3 逐项对照；可追溯能力断言 19 条 ≥8；确定性种子重放已真实跨进程执行。运行态诚实标注：案例 A = REAL_EXECUTED，案例 B = PLAN_ONLY，案例 C/D/E = BLOCKED，原因均为环境缺依赖且已在第 10 节逐项列出。）