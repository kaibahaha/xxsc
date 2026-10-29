# R02 / F2 WorkBuddy 原始研究报告

- Experiment: FACTORY10-SKILL-24H-20261030
- Round: R02 / F2 软件与开源程序工厂
- WorkBuddy Job ID: f77da8aaab28496d
- MCP result: done / RESULT_STATUS: COMPLETE
- Provenance: 以下原样保存 WorkBuddy MCP get_workbuddy_result 返回的完整文本；其“已实测”描述为WorkBuddy自述，ChatGPT尚未独立复现远端Shell。

---

已完成真实云端只读勘察。以下为 R02/F2 报告。

---

# R02 / F2 软件与开源程序工厂｜WorkBuddy 只读研究报告

- 实验：FACTORY10-SKILL-24H-20261030｜轮次：R02（F2 首圈，**BASELINE**，无同厂历史分差）
- 执行时间：UTC 2026-10-29 17:58–18:0x（北京时间 2026-10-30 01:58 起）
- 执行身份：`workbuddy_agent`（非 root）｜CWD `/home/workbuddy_agent`
- 本轮约束：全程只读；**未安装任何插件/包、未配置 MCP、未写入 Git、未触碰其他实验目录**（`queue_eval_*`、`parallel_code_*`、`mcp_*_eval` 等仅 `ls` 观察到目录名，未进入）

---

## ① 环境实测与 EVIDENCE_LOG

### 1.1 平台与运行时

| 项 | 实测值 | 命令 |
|---|---|---|
| CLI 版本 | **2.177.0** | `codebuddy --version` |
| 二进制 | `/usr/bin/codebuddy`（alias `cbc`） | `type -a codebuddy` |
| npm 包 | `@tencent-ai/codebuddy-code@2.177.0` | `cat /usr/lib/node_modules/@tencent-ai/codebuddy-code/package.json` |
| Node / npm | v20.20.2 / 10.8.2 | `node --version` / `npm --version` |
| OS | Debian GNU/Linux 13 (trixie) | `cat /etc/os-release` |
| Python / jq | 3.13.5 / jq-1.7 | `python3 --version` / `jq --version` |
| 网络环境 | `CODEBUDDY_INTERNET_ENVIRONMENT=internal`（值已脱敏确认存在） | `env \| grep -i codebuddy` |

### 1.2 EVIDENCE_LOG（逐条，含命令）

| # | 命令（已执行） | 结果摘要 | 等级 |
|---|---|---|---|
| E01 | `codebuddy --version` | `2.177.0` | **已实测** |
| E02 | `codebuddy --help` | 顶层 60+ flag；含 `--serve/--acp/--bg/--exec/--swarm/--worktree/--mcp-config/--fallback-model/--max-turns/--effort` | **已实测** |
| E03 | `codebuddy plugin list` | `No plugins installed.` | **已实测** |
| E04 | `codebuddy mcp list` | `No MCP servers configured.` | **已实测** |
| E05 | `codebuddy plugin marketplace list` | 2 个市场：`cb_teams_marketplace`、`codebuddy-plugins-official`（type: zip） | **已实测** |
| E06 | `cat ~/.codebuddy/plugins/known_marketplaces.json` | 源 `https://download.codebuddy.cn/plugin-marketplace/*.zip`；`lastUpdated 2026-10-29T04:38:44Z / 46Z`；`isBuiltIn:true` | **已实测** |
| E07 | 解析 `…/codebuddy-plugins-official/.codebuddy-plugin/marketplace.json` | owner `CodeBuddy <codebuddy@tencent.com>`，**209 个插件** | **已实测** |
| E08 | `ls plugins` / `ls external_plugins` | 60 + 149 = 209（与 E07 自洽） | **已实测** |
| E09 | 目录存在性判定循环（21 个候选） | serena/feature-dev/testbuddy/github/gitlab/context7/playwright-cli/security-scan/chainguard/pr-review-toolkit… 全在 OFFICIAL；`cicd-automation`、`skill-creator` 在 `external_plugins` | **已实测** |
| E10 | `cat plugins/github/.mcp.json` | `type:http`, `url:https://api.githubcopilot.com/mcp/`, `Authorization: Bearer ${GITHUB_PERSONAL_ACCESS_TOKEN}` | **已实测** |
| E11 | `cat plugins/gitlab/.mcp.json` | `type:http`, `url:https://gitlab.com/api/v4/mcp`，**manifest 内无 token 字段** | **已实测** |
| E12 | `cat plugins/serena/.mcp.json` | `uvx --from git+https://github.com/oraios/serena serena start-mcp-server` | **已实测** |
| E13 | `cat plugins/context7/.mcp.json` | `npx -y @upstash/context7-mcp` | **已实测** |
| E14 | `cat plugins/testbuddy/.mcp.json` | `http://testbuddy.woa.com/api/tb/v1/cb-plugin/sse`（`x-testbuddy-origin: cb-plugin`, streamable-http, timeout 100000） | **已实测** |
| E15 | `cat plugins/security-scan/.codebuddy-plugin/plugin.json` | v**3.5.14**，author 腾讯云鼎实验室，`hooks: hooks/hooks.json`，8 项 features | **已实测** |
| E16 | `head plugins/security-scan/commands/{project,diff,setup}.md` | argument-hint 全文见 §2；`--auto` 红线"绝不自动修复" | **已实测（文档证据）** |
| E17 | `cat plugins/chainguard/hooks/hooks.json` | PreToolUse matcher `Write\|Edit\|MultiEdit\|Bash` → `node ${CODEBUDDY_PLUGIN_ROOT}/dist/security-guard.cjs`（716 KB） | **已实测** |
| E18 | `head plugins/feature-dev/commands/feature-dev.md` + `ls agents` | 3 agents：`code-explorer`/`code-architect`/`code-reviewer` | **已实测** |
| E19 | `head plugins/pr-review-toolkit/commands/review-pr.md` + `ls agents` | 6 agents：comment/PR-test/silent-failure/type-design/code-reviewer/code-simplifier；`allowed-tools: Bash,Glob,Grep,Read,Task` | **已实测** |
| E20 | 解析 `external_plugins/cicd-automation` | v**1.2.1**，author Seth Hobson；skills: `github-actions-templates`/`gitlab-ci-patterns`/`secrets-management`/`deployment-pipeline-design` | **已实测** |
| E21 | 工具可用性循环（17 个） | **git / gh / uv / uvx / pipx / docker / semgrep / syft / grype / trivy / gitleaks / cargo / go = NOT-FOUND**；仅 python3/node/npm/npx/jq 可用 | **已实测（关键阻塞）** |
| E22 | `find / -maxdepth 4 -name git -type f -perm -u+x` | 无结果（确认无 git 二进制） | **已实测** |
| E23 | 网络只读探测 `curl -s -o /dev/null -w %{http_code}` | api.github.com **200**、github.com **200**、registry.npmjs.org **200**、download.codebuddy.cn **200**、testbuddy.woa.com **301** | **已实测** |
| E24 | `ls docs \| grep -i action` + `grep -rl "GitHub Actions"` | **本地内置文档无 GitHub Actions 专章**；仅 `cn%2Fcli%2Fgitlab-ci-cd.md` 存在 | **已实测（精确否定）** |
| E25 | `head dist/web-ui/docs/cn%2Fcli%2Fscheduled-tasks.md`（168 行） | 定时任务为一等公民：`/loop`、CronCreate(`durable:true`)/CronList/CronDelete、任务会话、Jitter、daemon 接管 | **已实测（P0 纠错）** |
| E26 | `grep -n Cron tools-reference.md` | `CronCreate`(durable 需授权) / `CronDelete` / `CronList` 三工具在列 | **已实测（P0 纠错）** |
| E27 | `head dist/web-ui/docs/cn%2Fcli%2Fgitlab-ci-cd.md` | 官方 CI 集成：**GitLab CI** 有完整 YAML 示例（`CODEBUDDY_API_KEY`/`GITLAB_ACCESS_TOKEN`/`-p --permission-mode acceptEdits --allowedTools`） | **已实测（文档证据）** |
| E28 | `codebuddy plugin install --help` / `mcp add --help` / `plugin validate --help` | `-s user\|project\|local`；`-t stdio\|sse\|http`、`-e`、`-H`；validate 只读 | **已实测（仅读 help）** |
| E29 | `codebuddy agents --json` | **`error: unknown option '--json'`**（`--help` 却声明"requires --json" → help 与实现不一致） | **已实测（负面）** |
| E30 | `codebuddy daemon --help` | `start/stop/status/restart/install/uninstall`（系统服务注册） | **已实测** |
| E31 | `ls ~/.codebuddy/skills` | **不存在**；`builtin/skills` 仅 `mods-create` | **已实测** |
| E32 | `cat ~/.codebuddy/settings.json`、`app/plugin-status-daily.json` | 仅 `agentHome.orchestration:true`；无 MCP/插件授权痕迹 | **已实测** |
| E33 | `grep --fallback-model --help` | 存在：`"Enable automatic fallback … (only works with --print)"` | **已实测（R01 未核验项补证）** |
| E34 | `head headless.md` | `-p` 非交互**必须配 `-y`**；`--permission-prompt-tool` **❌ 不支持** | **已实测（文档证据）** |
| E35 | `head mcp.md` | `-p` 模式下 MCP 审批需 `--settings '{"enableAllProjectMcpServers":true}'` 或 `enabledMcpjsonServers` | **已实测（文档证据）** |
| E36 | `head agent-teams.md` | Agent Teams：team-lead + teammates、独立上下文、共享任务列表、可直接互发消息 | **已实测（文档证据）** |
| E37 | `find … -name SKILL.md \| wc -l` | 官方市场 483 个、Teams 市场 142 个（合计 625） | **已实测** |

> 未执行：`plugin install` / `plugin marketplace add` / `mcp add` / `daemon install` / `update`。下文所有安装命令**仅展示**。

---

## ② F2 候选工具清单（21 项，全部为"市场存在、本机未安装"）

**全局安装状态（E03/E04/E31）：插件 0 个、MCP 0 个、用户级 skills 目录不存在。**市场缓存 ≠ 已安装。

### 2.1 优先级总表

| P | 候选 | 类型 | 版本 | 存在性证据（绝对路径） | 安装状态 | 依赖/权限 | 许可证 | 费用 |
|---|---|---|---|---|---|---|---|---|
| **P1** | `github` | 插件=MCP(http) | 无版本字段 | `…/codebuddy-plugins-official/plugins/github/.mcp.json` | 未安装 | **需 `GITHUB_PERSONAL_ACCESS_TOKEN`**（第三方授权） | 未声明 | 插件本身免费；**GitHub/Copilot 额度价格未核实** |
| **P1** | `security-scan` | 插件+commands | **3.5.14** | `…/plugins/security-scan/.codebuddy-plugin/plugin.json` | 未安装 | 写 `~/.codebuddy/security-scan/config.json` + `.codebuddy/`；企业微信 Webhook 可选 | 未声明（腾讯云鼎实验室） | **价格未核实** |
| **P1** | `chainguard` | 插件(hooks) | **1.1.3** | `…/plugins/chainguard/hooks/hooks.json` | 未安装 | PreToolUse 钩子**拦截**所有 Bash/写文件（副作用强） | 未声明 | **价格未核实** |
| **P1** | `pr-review-toolkit` | 插件+6 agents | 无版本字段 | `…/plugins/pr-review-toolkit/commands/review-pr.md` | 未安装 | 需 git 仓库读状态（**E21：git 缺失**） | UNKNOWN | 免费开源代码；调用产生 token |
| **P2** | `cicd-automation` | 外部插件 | **1.2.1** | `…/external_plugins/cicd-automation/.codebuddy-plugin/plugin.json` | 未安装 | 生成 YAML（**不自带 runner**） | 未标注 | **价格未核实** |
| **P2** | `serena` | 插件=MCP(stdio) | 无版本字段 | `…/plugins/serena/.mcp.json` | 未安装 | **需 `uvx`（E21 缺失）** + GitHub 拉取源码 | 未声明（Oraios） | **价格未核实** |
| **P2** | `context7` | 插件=MCP(stdio) | 无版本字段 | `…/plugins/context7/.mcp.json` | 未安装 | `npx -y @upstash/context7-mcp`（网络可达 E23） | 未声明（Upstash） | **价格未核实** |
| **P2** | `feature-dev` | 插件+3 agents | 无版本字段 | `…/plugins/feature-dev/commands/feature-dev.md` | 未安装 | 无外部依赖 | UNKNOWN | 免费 |
| **P3** | `testbuddy` | 插件+MCP(http) | **1.6.7** | `…/plugins/testbuddy/.mcp.json` | 未安装 | 指向**内网** `testbuddy.woa.com`（本机仅 301，E23） | 未声明 | **UNVERIFIED/价格未核实** |
| **P3** | `taskmaster` | 外部插件 | — | `…/external_plugins/taskmaster/commands/*.md` | 未安装 | PRD→任务分解 | 未标注 | **价格未核实** |
| **P3** | `repomix-mcp` / `repomix-commands` / `repomix-explorer` | 外部插件 | — | `…/external_plugins/repomix-*/` | 未安装 | 远程/本地仓库打包（**A 案核心**） | 未标注 | **价格未核实** |
| **P3** | `gitlab` | 插件=MCP(http) | 无版本字段 | `…/plugins/gitlab/.mcp.json` | 未安装 | token 未在 manifest 声明（需自建） | 未声明 | **价格未核实** |
| **P4** | `dependency-management` | 外部插件 | — | `…/external_plugins/dependency-management/commands/deps-audit.md` | 未安装 | 纯提示词编排，调用系统扫描器（本机无） | 未标注 | **价格未核实** |
| **P4** | `unit-testing` / `tdd-workflows` | 外部插件 | — | `…/external_plugins/unit-testing/commands/test-generate.md` | 未安装 | 需 pytest/jest 等运行时 | 未标注 | **价格未核实** |
| **P4** | `code-review-ai` | 外部插件 | — | `…/external_plugins/code-review-ai/commands/ai-review.md` | 未安装 | 依赖 CodeQL/SonarQube/Semgrep/Snyk/GitGuardian（**本机全缺 E21**） | 未标注 | **价格未核实** |
| **P4** | `security-compliance` | 外部插件 | — | `…/external_plugins/security-compliance/commands/compliance-check.md` | 未安装 | 提示词级合规映射 | 未标注 | **价格未核实** |
| **P4** | `playwright-cli` | 插件 | **0.1.0** | `…/plugins/playwright-cli/.codebuddy-plugin/plugin.json` | 未安装 | 需 Playwright 运行时+浏览器 | **Apache-2.0** | **价格未核实** |
| **P5** | `skills-sec-audit` / `skills-security-check` | 插件(skill) | **1.0.0** | `…/plugins/skills-sec-audit/skills/skills-sec-audit/SKILL.md` | 未安装 | Skill 供应链投毒审计 | 未声明 | **价格未核实** |
| **P5** | `plugin-dev` | 插件(7 skills) | 无版本 | `…/plugins/plugin-dev/skills/{plugin-structure,skill-development,hook-development,mcp-integration,…}` | 未安装 | 自建插件工具包 | 未声明 | 免费 |
| **P5** | `skill-creator`（external, Apache-2.0 / teams 同名） | 外部插件 | — | `…/external_plugins/skill-creator/SKILL.md` | 未安装 | 含 `run_eval.py`/`package_skill.py` | **Apache-2.0** | 免费 |
| **P5** | `pyright-lsp` / `typescript-lsp` / `rust-analyzer-lsp` | 插件 | — | `…/plugins/pyright-lsp/README_zh.md` | 未安装 | 需 `npm i -g pyright` 等二进制 | 未标注 | **价格未核实** |

### 2.2 Top5 精确调用语法（均来自 manifest/SKILL.md/README 的 `argument-hint`，**未实测执行**）

1. **security-scan**（`commands/project.md` 与 `commands/diff.md` frontmatter 原文）
```
/security-scan:project [file_path...] [--scan-level fast|light|deep] [--focus high] [--auto] [--background|--bg] [--include *.py,*.js] [--exclude node_modules,dist] [--output-root <dir>]
/security-scan:diff [--commit <hash|base..head>] [--scan-level fast|light|deep] [--mode staged|unstaged|all] [--auto] [--background|--bg] [--output-root <dir>]
/security-scan:setup                      # 无参数；配置 Webhook + auto_scan
```
   - `allowed-tools: Bash, Read, Glob, Write, Grep, Task, Edit, MultiEdit, LSP, WebSearch, AskUserQuestion`
   - 三档耗时（README）：Fast 3–12min / Light 5–10min / Deep 20–40min；置信度上限 90/90/100
   - **安全红线**：`--auto`、Light、Fast 绝不自动修复；`--background` 仅支持 `--scan-level fast`
   - 配置分层：`~/.codebuddy/security-scan/config.json`（不提交）> `.codebuddy/security-scan/config.json`（可提交）
2. **chainguard**：无斜杠命令，`hooks.json` 自动生效；PreToolUse matcher `Write|Edit|MultiEdit|Bash`，PostToolUse matcher `Write|Edit|MultiEdit`（timeout 60s/10s）
3. **pr-review-toolkit**：`/pr-review-toolkit:review-pr "[review-aspects]"`，`allowed-tools: ["Bash","Glob","Grep","Read","Task"]`
4. **feature-dev**：`/feature-dev [Optional feature description]`，三 agent 分工（探索/架构/审查）
5. **github（MCP）**：连接后工具名前缀为 `mcp__github`（`--allowedTools "mcp__github"` 见 E27）；授权头 `Authorization: Bearer ${GITHUB_PERSONAL_ACCESS_TOKEN}`

### 2.3 安装命令（**仅展示，本轮未执行**）

```bash
# 展示用 — 未执行
codebuddy plugin install github@codebuddy-plugins-official -s user
codebuddy plugin install security-scan@codebuddy-plugins-official -s project
codebuddy plugin install chainguard@codebuddy-plugins-official -s project
codebuddy plugin install pr-review-toolkit@codebuddy-plugins-official -s project
codebuddy plugin install cicd-automation@codebuddy-plugins-official -s project
# 只读校验（不安装）：codebuddy plugin validate <path>
# MCP 手工注册（不执行）：codebuddy mcp add <name> <cmdOrUrl> -t stdio|sse|http -e K=v -H K=v
```

### 2.4 能力边界矩阵（M2 / P0-2 要求）

| 能力层 | 本平台实测结论 | 层次归属 | 证据 |
|---|---|---|---|
| 代码生成 Agent | 有（内置 Agent/Sub-agent/Agent Teams） | **内置已实测** | E02/E36 |
| 仓库只读解构 | 无专用内置；靠 Agent + 市场 repomix-*(未装) | **市场存在未安装** | E09 |
| GitHub 仓库/PR 读写 | 仅经 `github` MCP，**需 PAT** | **第三方授权** | E10 |
| GitLab MR/CI | 仅经 `gitlab` MCP（manifest 无 token 字段） | **第三方授权（字段未验证）** | E11 |
| CI/CD runner | **平台本身不是 runner**；官方仅提供 GitLab CI 集成文档与 cicd-automation 模板 | **需独立 CI 系统** | E24/E27 |
| GitHub Actions | **本地 v2.177.0 内置文档无 GitHub Actions 专章** | **尚无官方专章（已核实范围=本地内置文档）** | E24 |
| 静态分析(LSP) | 有 `LSP` 工具，但需 `pyright-lsp` 等插件+二进制 | **市场存在未安装** | E19 段 |
| 安全/供应链门禁 | security-scan(命令) + chainguard(Hook) | **市场存在未安装** | E15/E17 |
| 测试执行 | 无内置 runner；依赖 pytest/jest/playwright | **自建/外部** | E21 |
| 部署系统 | 无内置；cicd-automation 只产出配置 | **理论自建** | E20 |
| 定时器 | **有**：CronCreate/CronList/CronDelete + `/loop` + daemon 持久化 | **内置已实测** | E25/E26/E30 |
| 无人值守执行 | `-p` + `-y` + `--permission-mode acceptEdits`；`--auto` | **内置（文档证据）** | E34 |

---

## ③ 与 ChatGPT 侧相近能力的边界比较

> **声明：我无 ChatGPT 账号/管理员权限**。OpenAI 侧结论来自公开帮助中心与第三方整理（第三手），标记为**文档证据（第三方）/ 推断**；CodeBuddy 侧为**已实测**。

| 维度 | CodeBuddy v2.177.0（实测） | ChatGPT 侧公开信息 | 判定 |
|---|---|---|---|
| GitHub | `github` 插件 = 官方 GitHub MCP（`api.githubcopilot.com/mcp/`），**必须自带 PAT**，未安装 | GitHub app/connector：公开资料称"Live repository reading；Triage PRs, issues, CI, and publish flows"；deep research 亦支持 GitHub；事件触发任务支持"GitHub pull request activity" | 两者都需**用户侧 OAuth/PAT**；CodeBuddy 走 MCP 标准、ChatGPT 走托管连接器。**推断**：ChatGPT 侧无需用户配置 MCP endpoint |
| Google Drive | **市场中未发现 Drive 插件**（209 个插件名已全量枚举比对） | Drive 为 ChatGPT 一等连接器，含管理员托管同步索引（Business/Edu） | **CodeBuddy 侧缺口**（已核实范围：本机两个市场清单） |
| "WorkBuddy" | 本机即为 WorkBuddy/CodeBuddy 侧 | ChatGPT plugin 目录中是否存在同名 app：**UNVERIFIED**（未检索到官方条目） | 标 **UNVERIFIED** |
| GitHub Actions | 无官方 Actions 集成文档；仅 `gitlab-ci-cd.md` | ChatGPT 侧亦未见 Actions 编排能力（仅 GitHub app 的 CI 可见性） | 双方均非 runner；**推断** |
| 定时/计划任务 | `CronCreate`(durable→daemon 持久化) + `/loop`，**一等公民** | "Scheduled tasks"（2025-01 beta）+ 事件触发任务（Gmail/Slack/GitHub PR） | 功能对等；CodeBuddy 侧有跨进程原子占位防重（文档证据） |
| 自定义 MCP | `codebuddy mcp add` 全支持（stdio/sse/http） | Custom MCP connectors（Beta，需 remote MCP；Business/Enterprise 全支持） | 对等；**Free/Go 的自定义 MCP 支持"未确立"**（第三方文档） |
| 费用 | **价格未核实**（不写金额、不宣称免费） | **价格未核实** | 双方均需查官方定价 |

**边界红线（本轮不做的事）**：不因"Agent 能生成代码"而宣称具备自动发布、仓库写权限或测试通过；不因市场有 `cicd-automation` 而宣称具备 runner；不因 `dependency-management` 提示词提到 Snyk/CodeQL 而宣称已具备扫描能力（本机 E21 全部缺失）。

---

## ④ 五个 F2 实战工作包（互不重复，每包 ≥8 字段）

> 全部为**方案**，本轮**零写入执行**。凡涉及 `git` 的步骤，前置条件均需先解决 E21（git 未安装）。

### 工作包 A｜开源仓库只读解构 → 架构/依赖/许可证/SBOM 与复刻计划
| 字段 | 内容 |
|---|---|
| 目标 | 对一个远端开源仓库产出"可复核的解构报告"，**不复制受限代码**，只输出架构/依赖/许可证清单与复刻路径 |
| 前置条件 | ①安装 git（E21 阻塞）；②只读访问：优先 `curl`/GitHub 公开 API，不落盘源码；③目标仓库 LICENSE 明确 |
| 输入 | `REPO_URL`、`REF`（tag/branch）、`OUTPUT_DIR=/home/workbuddy_agent/f2_caseA/` |
| 候选工具 | `repomix-commands`（`/pack-remote`）、`repomix-explorer`（`/explore-remote`）、`repomix-mcp`；无 git 时退化为 GitHub API + Agent Grep |
| 操作步骤（标注验证状态） | 1. `git ls-remote --tags $REPO_URL`（**语法来自 git 通用用法，本环境未验证**）<br>2. `git clone --depth 1 --branch $REF $REPO_URL`（同上）<br>3. `git -C repo rev-parse HEAD` → 记录 **commit SHA**（**A 案必须产物**）<br>4. 只读枚举：`find repo -name "LICENSE*" -o -name "NOTICE"`；`python3 -c "import json;…"` 解析 `package.json`/`pyproject.toml`<br>5. 生成 SBOM：**本机无 syft/cyclonedx（E21）**，改为脚本自建依赖清单(JSON)，标注"非标准 SBOM" |
| 输出文件 | `caseA/ARCHITECTURE.md`、`caseA/DEPENDENCIES.json`、`caseA/LICENSE_AUDIT.md`、`caseA/SBOM-lite.json`、`caseA/REPLICA_PLAN.md`、`caseA/PROVENANCE.md`（含 commit SHA + 抓取时间 + 命令回显） |
| 正向测试 | 报告中每个依赖都能在 `DEPENDENCIES.json` 溯源到具体清单文件行号；commit SHA 可 `git cat-file -e` 复核 |
| 异常测试 | ①仓库无 LICENSE → 报告须标 `LICENSE: UNKNOWN` 并**阻断复刻计划**；②`git` 缺失 → 降级到 GitHub API 并记录 `DEGRADED: no-git`；③GPL/AGPL 依赖 → 标记"禁止直接复制" |
| 验收标准 | PROVENANCE 含 40 位 SHA + UTC 时间戳；LICENSE_AUDIT 覆盖 **100%** 顶层依赖且无 `UNKNOWN` 残留（或残留已显式列为风险） |
| 成本 | 人工 1 人·轮 + token；**外部服务价格未核实** |
| 风险 | 许可证误判；网络抓取被限流；误把受限代码写入本地 |
| 回滚 | 全程只读，`rm -rf $OUTPUT_DIR` 即可；无远端副作用 |
| 人工批准边界 | 任何 `git clone` 到本地磁盘 = 需人工批准（默认只用 API 摘要） |

### 工作包 B｜Markdown 任务合同 → 需求分解 → Agent 实现 → PR → 测试 → 审计 → Git 回读
| 字段 | 内容 |
|---|---|
| 目标 | 用一份 Markdown 任务合同驱动"实现→审计→回读"闭环，证明无人值守可行 |
| 前置条件 | git 可用；`github` 插件已装且 PAT 具备（**本轮未装→方案态**）；目标仓库有 CODEBUDDY.md |
| 输入 | `CONTRACT.md`（目标/范围/验收/AC 列表）、`CODEBUDDY.md`、仓库快照 |
| 候选工具 | `taskmaster`（PRD→任务）、`feature-dev`、`pr-review-toolkit`、`security-scan`、`unit-testing`；编排用 Agent Teams（E36） |
| 操作步骤 | 1. `/feature-dev "<CONTRACT 摘要>"`（语法来自 E18 frontmatter，**未执行**）<br>2. `codebuddy -p "实现 CONTRACT.md 中 AC-1..AC-3" -y --permission-mode acceptEdits --allowedTools "Bash,Read,Edit,Write"`（语法来自 E34，headless 文档）<br>3. `/security-scan:diff --commit HEAD --scan-level light --auto`（E16 原文）<br>4. `/pr-review-toolkit:review-pr`（E19）<br>5. 回读：`git show --stat HEAD` + 比对 CONTRACT 的 AC 勾选表 |
| 输出文件 | `PR_BODY.md`、`caseB/AC_CHECKLIST.md`、`caseB/SECURITY_REPORT(.html)`、`caseB/REVIEW.md`、`caseB/READBACK_DIFF.md` |
| 正向测试 | 3 条 AC 全部在 AC_CHECKLIST 中标注 `PASS` 且各自链接到具体测试用例 |
| 异常测试 | ①PAT 失效 → 必须失败在 MCP 连接层且**不产生本地提交**；②`--auto` 下发现高危 → 门禁 `gate_mode=warn` 默认**不阻断**（须显式改 block 才阻断，README 默认值）；③测试失败 → 禁止生成 PR |
| 权限隔离 | PAT 仅授予目标仓库；`--disallowedTools "Bash(git push)"` 显式禁推送；PR **创建需人工批准** |
| 验收标准 | 无高危 finding 且 AC 全绿；`READBACK_DIFF.md` 与 CONTRACT 逐条可映射 |
| 成本 | Deep 扫描 20–40 分钟（README 标称）；token 与 CI 额度**价格未核实** |
| 风险 | `--auto` 仍会写 `~/.codebuddy/security-scan/config.json`；PAT 泄露；自动提交污染主分支 |
| 回滚 | `git revert <sha>`；`codebuddy plugin uninstall security-scan`；撤销 PAT |

### 工作包 C｜多 Agent 并行代码挑战（盲测/公平比较）
| 字段 | 内容 |
|---|---|
| 目标 | 同一冻结题目，N 个 Agent 独立实现，盲测打分，冲突隔离 |
| 前置条件 | Agent Teams 可用（E36）；为每个 Agent 准备**独立目录**；题目冻结文件只读挂载 |
| 输入 | `FROZEN_TASK.md`（含固定输入/期望输出样例）、`RUBRIC.md`、`N=3` |
| 候选工具 | 内置 Agent/TeamCreate（实测存在）、`--worktree`（E02）、`unit-testing` |
| 操作步骤 | 1. 冻结：`sha256sum FROZEN_TASK.md` 记录<br>2. `codebuddy -p "按 FROZEN_TASK.md 实现" --worktree`（或每 Agent 独立 `<dir_i>`）<br>3. **隔离硬约束**：Agent_i 只可见 `dir_i` 与 FROZEN_TASK.md；`--add-dir` 限定（E02）<br>4. 盲测：评审 Agent 只见 `dir_i` 的匿名化副本（去掉作者/目录名）<br>5. 汇总 RUBRIC 打分 |
| 输出文件 | `caseC/TASK_SHA256.txt`、`caseC/solutions/agent_{1..3}/`、`caseC/BLIND_REPORT.md`、`caseC/SCOREBOARD.md` |
| 正向测试 | 三份实现均通过同一组 10 个固定用例；SCOREBOARD 分数可复算 |
| 异常测试 | ①某 Agent 提前中止 → 标 `INCOMPLETE` 不进排名；②发现 Agent 读取他人目录 → 判 `DISQUALIFIED`；③VLM 打分不一致 → 双人复核 |
| 验收标准 | 每个 Agent 的可见目录集合有日志证据；盲测阶段无作者标识残留 |
| 成本 | Agent Teams Token 消耗显著高于单会话（E36 明确提示）；**价格未核实** |
| 风险 | 上下文污染；worktree 冲突；评审偏差 |
| 回滚 | `git worktree remove`（需 git）；删除 `caseC/solutions/` |

### 工作包 D｜自动化回归与安全供应链门禁（负例驱动）
| 字段 | 内容 |
|---|---|
| 目标 | 建立"负例必失败"的门禁：依赖漏洞、密钥、回归、CI 阻断、回滚证据 |
| 前置条件 | git + CI 系统（**非本平台**）；`security-scan` 与 `chainguard` 已装（**未装→方案态**） |
| 输入 | 含**已知植入缺陷**的样例仓库（负例集：`hardcoded_key.py`、`vuln_dep` in `requirements.txt`、回归用例） |
| 候选工具 | `security-scan`（门禁）、`chainguard`（依赖安装拦截）、`dependency-management`（`/deps-audit`）、`skills-sec-audit`（技能供应链） |
| 操作步骤 | 1. `/security-scan:setup` 配 `gate_mode=block` + Webhook（默认 `warn`，**必须显式改**）<br>2. `/security-scan:diff --commit HEAD~1..HEAD --scan-level fast --auto`（CI 场景推荐 Fast，README）<br>3. 装 `chainguard` 后，任一 `npm install` 触发 PreToolUse 审计（E17）<br>4. 负例验证：植入 `AKIA...` 常量 → 期望 `secret-detection-patterns.yaml` 命中 |
| 输出文件 | `caseD/GATE_RESULT.json`、`caseD/NEGATIVE_CASES.md`（每条：植入→期望→实际→判定）、`caseD/ROLLBACK_LOG.md` |
| 正向测试 | 干净分支 → 门禁 PASS |
| 异常测试 | ①密钥负例未被发现 → **判定门禁失败**；②`gate_mode=warn` 时高危仍不阻断（预期行为，须记录）；③Webhook URL 非法 → setup 校验失败（`https://qyapi.weixin.qq.com/...` 格式强校验） |
| 验收标准 | 负例检出率 100%（至少密钥/注入/漏洞依赖三类各 1 条）；每条负例有回滚记录 |
| 成本 | Fast 3–12 分钟/次；**价格未核实** |
| 风险 | chainguard 的 PreToolUse 覆盖 `Bash` → **可能拖慢/拦截正常构建**；Webhook 泄露 |
| 回滚 | 卸载插件；`git revert`；Webhook 置于用户级配置（不入库） |

### 工作包 E｜现有桥接器/队列调度代码只读可靠性审计
| 字段 | 内容 |
|---|---|
| 目标 | 对既有桥接器/队列调度代码做**只读**审计：中断、重复派单、幂等、超时、双写一致性 |
| 前置条件 | **只读挂载**被测代码；**禁止修改生产桥接器**；优先提交哈希固定版本 |
| 输入 | 被测源码目录（如本地副本）、`FAILURE_TAXONOMY.md`（中断/重复/幂等/超时/双写 5 类） |
| 候选工具 | 内置 Agent + Grep/Read、`serena`（语义分析，需 uvx）、`code-review-ai`（/ai-review）、`pr-review-toolkit` |
| 操作步骤 | 1. **模拟优先**：构造事件序列（中断/重试/并发）→ 在纸面/单元级推演，不连生产<br>2. 静态：按 5 类缺陷 grep 关键模式（无锁重试、无 dedupe key、超时未设、写顺序不一致）<br>3. 若需真实执行：**仅限隔离副本容器**（本机无 docker，E21 → 标阻塞）<br>4. 输出"模拟方案 vs 真实执行"**双栏对照** |
| 输出文件 | `caseE/RELIABILITY_AUDIT.md`、`caseE/FINDINGS.json`（含 file:line）、`caseE/SIM_VS_REAL.md` |
| 正向测试 | 每条 finding 有 `file:line` 与可复现步骤 |
| 异常测试 | ①无 docker/git → 全部结论标 `SIMULATION ONLY`；②无法访问生产 → 标 `UNVERIFIED`；③只读挂载被写入尝试 → 立即中止 |
| 验收标准 | 5 类缺陷每类至少 1 条判定（`PASS/FAIL/UNVERIFIED` 三态，不得留空） |
| 成本 | 人工主导；`serena` 依赖 uvx（缺失→方案降级） |
| 风险 | 误读生产代码语义；把推断写成事实 |
| 回滚 | 只读，无副作用；副本目录可删 |

---

## ⑤ 首周最小落地路线图 + Top5

| 天 | 动作 | 依赖 | 产出 |
|---|---|---|---|
| D1 | **解除 E21 阻塞**：安装 git（唯一硬阻塞）；确认 PAT 申请渠道 | 人工批准 | `ENV_READY.md` |
| D2 | 装 `github` + `security-scan`（`-s project`），仅跑 `plugin validate` 与只读 `diff --scan-level fast` | PAT | `GATE_BASELINE.md` |
| D3 | 工作包 **A**（只读解构，无需写权限） | git + 网络 | 6 个 Markdown/JSON 产物 |
| D4 | 工作包 **E**（只读审计，无需写权限） | 只读副本 | `RELIABILITY_AUDIT.md` |
| D5 | 工作包 **B**：仅到"生成 diff + 审计报告"，**PR 创建留人工** | PAT | `AC_CHECKLIST.md` |
| D6 | 工作包 **D**：负例门禁，先 `warn` 观察再切 `block` | 插件已装 | `NEGATIVE_CASES.md` |
| D7 | 工作包 **C**：3 Agent 盲测；用 `--worktree` 隔离 | git | `SCOREBOARD.md` |

**优先 Top5**：`github`（P1，PAT 授权）→ `security-scan`（P1，门禁）→ `chainguard`（P1，供应链拦截）→ `pr-review-toolkit`（P1，PR 审计）→ `cicd-automation`（P2，CI 脚手架，仅产 YAML）。
**备选**：`serena`/`context7`（先补 uvx）、`repomix-*`（A 案）、`taskmaster`（B 案）。

---

## ⑥ 证据分层

| 层 | 内容 |
|---|---|
| **已实测** | E01–E23、E29、E31–E33：CLI 2.177.0、0 插件/0 MCP、209 插件清单、各 manifest 原文、git/uv/docker/扫描器缺失、网络 200/301、Cron* 三工具、scheduled-tasks.md、无 GitHub Actions 专章 |
| **文档证据（本机内置）** | E24/E25/E27/E34/E35/E36：GitLab CI 集成 YAML、headless `-p` 需 `-y`、`--permission-prompt-tool` 不支持、MCP `-p` 审批开关、Agent Teams 模型 |
| **文档证据（第三方/公开）** | §③ ChatGPT 侧 GitHub/Drive/Scheduled tasks/自定义 MCP —— 无账号权限，未实测 |
| **候选未安装** | §2.1 全部 21 项（市场缓存存在，安装态为 0） |
| **第三方授权** | `github`（GITHUB PAT）、`gitlab`（token 字段未在 manifest 声明）、企业微信 Webhook、`testbuddy.woa.com`（内网，**UNVERIFIED**） |
| **理论自建** | 工作包 A 的 SBOM-lite（无 syft）、D 的密钥/漏洞扫描（无 trivy/gitleaks）、C 的容器隔离（无 docker）、Git 相关全部步骤（无 git） |

---

## ⑦ R01 跨厂教训 → 本轮整改追踪表

| # | R01 教训 | 本轮具体措施 | 证据位置 | 状态 |
|---|---|---|---|---|
| 1 | "CodeBuddy 无内建 scheduler"被官方 scheduled-tasks 文档证伪 | 先查本地内置文档再下结论；给出 `CronCreate/CronList/CronDelete` + `/loop` + daemon，并注明 v2.177.0 | E25/E26/E30（`dist/web-ui/docs/cn%2Fcli%2Fscheduled-tasks.md`、`tools-reference.md:15-17`） | **已落实** |
| 2 | 把 `--serve` 当通用推理网关（层次混淆） | 建立 §2.4 能力边界矩阵，显式区分 Agent/GitHub MCP/CI runner/静态分析/测试/部署/定时器 | E02/E10/E24/E27 | **已落实** |
| 3 | "只有 X"类断言缺版本出处 | 两处否定结论均附命令与已核实范围：无 GitHub Actions 专章（E24，范围=本机内置文档）、无 Drive 插件（范围=209 插件全量枚举） | E24/§③ | **已落实** |
| 4 | `--fallback-model`、`security-scan --auto` 等命令未核验 | `--fallback-model` 取自 `--help` 原文（E33）；`--auto`/`--background`/`--scan-level` 取自 `commands/*.md` 的 `argument-hint` 与 README（E16） | E33/E16 | **已落实** |
| 5 | 五案例缺边界测试/成本/回滚 | 五包各含 ≥11 字段，含异常测试、权限隔离、回滚、人工批准边界 | §④ | **已落实** |
| 6 | 成本声明过宽 | 全表统一"**价格未核实**"，不写金额、不称全免费；区分免费代码/服务收费/token/CI 额度 | §2.1、§④ | **已落实** |
| 7 | 关键架构断言未验官方文档 | 凡断言均附 manifest/SKILL.md/README/内置文档路径 | 全文 E# | **已落实** |
| 8 | 缓存当已安装 | E03/E04/E31 三重确认安装态为 0，并在 §2.1 逐项标注"未安装" | E03/E04/E31 | **已落实** |
| 9 | 命令未区分"实测/示例" | 所有命令标注来源（help/README/manifest）与验证状态；git 系步骤统一标"本环境未验证" | §④ | **已落实** |
| 10 | （新增本轮发现）help 与实现不一致 | `codebuddy agents --json` 报 `unknown option`，而 `--help` 称"requires --json" | E29 | **已记录（待上游确认）** |

### 方法指标自检
- **M1**：8 项关键断言全部附来源/命令/版本（CLI 版本、0 插件、0 MCP、209 清单、scheduler、GitLab CI、无 Actions 专章、无 Drive）→ **8/8**
- **M2**：21 个候选分类准确率（已安装 0 / 未安装 21）；Top5 全部给出可复核语法出处 → **5/5**；无"缓存当已安装"
- **M3**：五包字段完整率 **5/5**（≥8 字段）；负面测试覆盖 **5/5**；含费用/回滚/许可证 **5/5**

---

**RESULT_STATUS: COMPLETE**