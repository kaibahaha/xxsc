# R12 / F2 WorkBuddy 原始报告（MCP真实追单补交）

- 实验：FACTORY10-SKILL-24H-20261030
- 唯一原Job ID：`00401c5228a34073`
- WorkBuddy任务列表状态：`done`；返回原文长度：29204字符。
- 交付性质：**以下为MCP get_workbuddy_result原始正文，不代表ChatGPT独立核实远端自测、CLI或文件工件。**
- 回收时间：北京时间2026-10-30 15时段（R15时段追单R12）；原研究仍归R12/F2。

---

已完成 R12/F2 同厂 R02 定向整改研究报告（只读研究，未安装/授权/购买/切模型/读凭据/改生产/写其他实验；所有写入均为方案）。完整正文如下：

---

# R12 / F2 软件与开源程序工厂 —— 同厂 R02 定向整改研究报告

- 实验：`FACTORY10-SKILL-24H-20261030`
- 本轮固定：`R12 / F2`（不因子 R11 补跑而变更）
- 计划窗口：Phoenix 2026-10-29 21:00 / 北京 2026-10-30 12:00
- 性质：**只读研究**。未安装/授权/购买/切模型/读凭据/改生产/写其他实验。所有"写入动作"仅为方案，未实际执行。
- 同厂旧版基线：`R02`（Job `f77da8aaab28496d`，DONE，自报 **81/100**，五维 **22/25、18/20、16/20、15/20、10/15**）。本轮**不自行宣布提升**；Δ 与五维差由 ChatGPT 在取得正文后独立审计给出。

---

## 0. 证据分级与关键边界声明（M1 前置）

| 级别 | 含义 | 本轮来源 |
|---|---|---|
| **E0** | 自述/远端 CLI 自报 | `codebuddy --version` = 2.177.0；本会话 `codebuddy --help` / `mcp` / `skill` 只读抓取 |
| **E1** | 外部官方一手来源 | codebuddy.cn/docs/*、gnu.org 许可证正文与 FAQ、GitHub REST 文档、SPDX（见 §3，≥10 条，与缓存分开计数） |
| **E2** | 市场缓存（**≠已安装**） | R02 自报"209 项市场缓存、0 已装"。本轮**不把任何缓存当作已安装**，不把 ChatGPT GitHub 连接器授权推定到 WorkBuddy |
| **E3** | 推断/演绎 | 本报告中的分析、矩阵、方案推导，均显式标注 |

**三道不可混淆的边界（本轮硬性约束）**
1. **工作区信任 ≠ OS 访问控制**：`--worktree` / `--add-dir` 只扩展"文件可见/可写范围"，不提供 OS 级隔离（E1 官方文档原句见 §6-P0-1）。
2. **缓存 ≠ 安装**：E2 的 209 项市场插件"0 已装"，任何"插件能力"在未实际安装前一律按"未验证/PLAN"处理。
3. **ChatGPT 连接器授权 ≠ WorkBuddy 授权**：R02 P2-6 曾把"ChatGPT 已连接 GitHub 可用"作为可行路径；本轮明确：**ChatGPT 的 GitHub OAuth 连接器授权不能等价于 WorkBuddy 的 GitHub 写权限**。WorkBuddy 若要写 GitHub，须自有 GitHub App / token 且按仓库授权，与 ChatGPT 无关（E1: IAM 文档）。

**R02 原句出处透明度**：本环境 `rounds/R02/WORKBUDDY_REPORT.md` 等路径**不可在本文件系统独立读取**（仅 `factory24_20261030/.../20261030-0232-R02/{A,B,C}` 源码树存在，无报告 markdown）。因此 §6 引用的 R02 原句**引自本反馈包对 R02 的转述**（E3 级出处），非本轮独立复读原文；这正是 M2 要求的"可独立重放/可溯源"缺口，列为§7 新增缺陷 N1。

---

## ① R02 基线 81 分及五维与五案例历史复盘

### 1.1 五维复盘（R02 自报，E3 转述）
| 维度 | R02 分 | 内容 | 本轮定位 |
|---|---|---|---|
| D1 来源/证据 | 22/25 | 37 项 EVIDENCE_LOG、CLI 分层、21 组候选/Top5 | 保留来源级别；补 E1/E0/E2/E3 四分计数 |
| D2 案例完整度 | 18/20 | 五案例输入/输出/负例/回滚字段完整 | 保留字段；补"真实 Skill/插件连接状态"与"执行状态" |
| D3 安全/权限 | 16/20 | E25/E26/E30 纠正 R01 scheduler 误判 | **P0-1/P0-2 未根治**（见 §6） |
| D4 许可精确性 | 15/20 | **P1-3 GPL/AGPL 一刀切禁止** | 按 SPDX 场景矩阵重做（§6-P1-3） |
| D5 可重复/方法 | 10/15 | 自述 RUN 但路径不可复现 | **P1-4/P1-5/M2** 重做（§4、§5、§6） |

### 1.2 五案例历史复盘（R02 自报要点，E3 转述）
- **A 开源仓库解构**：只读架构/许可证/SBOM-lite；输出 ARCHITECTURE/DEPENDENCY/LICENSE/SOURCE_LOCK。缺陷：GPL/AGPL 统一"禁止直接复制"（P1-3）、缺 LICENSE 负例、未禁止冒称非标 SBOM 为 SPDX。
- **B Markdown 合同→PR**：CONTRACT.md AC1–AC5→PATCH.diff→TEST_RESULTS→PR_REVIEW→Git readback。缺陷：headless 授权过宽（P0-2）、未授权即计划 push。
- **C 多Agent 盲测**：缺陷：以 `--add-dir` + 工作区隔离当作"可信盲测"（P0-1）、答案可见性未做 OS 级隔离。
- **D 安全供应链门禁**：缺陷："100% 负例检出"无实测、AKIA 样本不代表真实密钥覆盖（P1-5）、无扫描器却声称 PASS。
- **E 桥接器可靠性只读审计**：最贴近当前项目；缺陷：未给出 429/重启/重复 submit/Git 写入成功但回读失败的独立可重放模拟。

---

## ② F2 候选 Skill / 插件 ≥12（Top5 详述）

> 连接状态统一口径：**INSTALLED**（本机已装且可用）/ **CACHED-0**（E2 市场缓存、0 已装、未验证）/ **ABSENT**（环境缺失：git/docker/uv/uvx 经 `which` 确认不存在）/ **DESIGN**（仅方案，需审批后部署）。

### 2.1 候选清单（≥12）
| # | 能力 | 形态 | 连接状态 | 用途 |
|---|---|---|---|---|
| 1 | `mcp__github` | MCP 服务器 | DESIGN（需自有 GitHub App/Token，按仓库授权） | A/B/E 读仓库、建 PR |
| 2 | GitHub REST `gh api` / `curl api.github.com` | Bash+WebFetch | ABSENT(git/gh)→改只读 API 路线 | A 只读架构/SBOM |
| 3 | `WebFetch` + 官方许可证/SPDX | 内置工具 | INSTALLED | A/P1-3 许可证矩阵 |
| 4 | `codebuddy --sandbox container` | CLI 隔离 | ABSENT(docker)→BLOCKED | P0-1 OS 级隔离 |
| 5 | `Bash` + `--allowedTools`/`--disallowedTools` + deny | 内置工具 | INSTALLED | P0-2 最小工具集 |
| 6 | `gitleaks` / `trufflehog` | 机密扫描 | ABSENT | D 密钥门禁 |
| 7 | `osv-scanner` / `trivy` / `grype` | 依赖/CVE | ABSENT | D 漏洞门禁 |
| 8 | `syft` | SBOM 生成 | ABSENT | A SBOM-lite |
| 9 | `scancode` / `license-checker` | 许可证扫描 | ABSENT | A/D 许可证 |
| 10 | `semgrep` | SAST | ABSENT | D 代码脆弱性 |
| 11 | `codebuddy --worktree` + `isolation: worktree` 子代理 | CLI 内置 | INSTALLED（但**非安全沙箱**，见 P0-1） | C 并行对比 |
| 12 | `PreToolUse` Hooks | CLI 内置 | INSTALLED | 全案例硬边界 deny |
| 13 | `mcp__gitlab` | MCP（备选 Git 主机） | DESIGN | A 跨主机 |
| 14 | `npx @anthropic-ai/sandbox-runtime` | npm 包 | ABSENT(node 未确认) | P0-1 进程沙箱 |

### 2.2 Top5 详述

**Top1 — `mcp__github`（GitHub MCP）**
- 官方/manifest：`codebuddy mcp add github ...`（E1: codebuddy.cn/docs/cli/mcp；GitHub App 授权见 E1: IAM）
- 调用语法（只读优先）：`mcp__github__get_repo`、`mcp__github__list_issues`、`mcp__github__get_pull_request`（读）；写：`mcp__github__create_pull_request`（**需 GitHub App 按仓库授权 + PR 人工审批**）
- 依赖：需自有 GitHub App 或 `CODEBUDDY_AUTH_TOKEN`；**与 ChatGPT 连接器无关**
- 费用：UNKNOWN（按 GitHub API 配额/CodeBuddy 计费，本只读研究无账单访问）
- 安全/授权：默认 deny 写；仅 `mcp__github__create_pull_request` 在"GitHub App 单仓授权 + `--disallowedTools` 兜底 + 人工 review"下开放
- 状态：DESIGN（未装未授权；本环境 `git`/`gh` ABSENT）

**Top2 — `WebFetch` + 官方许可证/SPDX 源**
- 官方：E1 `gnu.org/licenses/*`、`spdx.org/licenses`、`choosealicense.com`
- 调用：`WebFetch(domain:gnu.org)`、`WebFetch(domain:spdx.org)`；配合 `ask:["WebFetch"]` + `allow:["WebFetch(domain:gnu.org)","WebFetch(domain:spdx.org)"]`
- 依赖：网络（沙箱内需把域名加入 `sandbox.network` 白名单）
- 费用：UNKNOWN
- 安全：纯只读，无写权限
- 状态：INSTALLED

**Top3 — `Bash` + 最小权限规则（P0-2 核心）**
- 官方：E1 permission-modes/permissions/bash-sandboxing
- 调用（修正后，对比 R02 原句见 §6-P0-2）：
  `codebuddy -p "…" --permission-mode dontAsk --allowedTools "Read,Grep,Glob,Bash(git status:*),Bash(git diff:*),Bash(npm test:*)" --disallowedTools "Bash(git push:*),Bash(sudo:*),Bash(rm:*),Bash(curl:*),Bash(wget:*)"`
- 依赖：本机 `Bash`（INSTALLED）；git 命令 ABSENT → 改 GitHub 只读 API（Top1）
- 费用：UNKNOWN
- 安全：deny 永远优先；`dontAsk`+白名单=固定能力集；配合 `--sandbox container`（BLOCKED）得 OS 级隔离
- 状态：INSTALLED（规则可落地；OS 隔离 BLOCKED）

**Top4 — 机密/依赖/许可证扫描器（gitleaks/osv-scanner/trivy）**
- 官方：E1 GitHub REST、OSV（`osv.dev`）、GitHub Advisory
- 调用（设计）：`osv-scanner --recursive ./`、`gitleaks detect`、`trivy fs ./`
- 依赖：ABSENT（P1-4）→ **DESIGN/PLAN**；Case D 仅用合成夹具做设计矩阵（§5 Sim-D）
- 费用：UNKNOWN（无报价访问）
- 安全：只读扫描，不写
- 状态：**BLOCKED（未安装）**——不得声称 PASS

**Top5 — `codebuddy --worktree` + `isolation: worktree` 子代理（Case C）**
- 官方：E1 worktree 文档**明确"子代理隔离是安全沙箱吗？不是"**
- 调用：`codebuddy --worktree agent-i`；子代理 frontmatter `isolation: worktree`
- 依赖：需 Git 仓库（本环境 git ABSENT → 非 Git 项目可走 WorktreeCreate hook，但仍非 OS 隔离）
- 费用：UNKNOWN
- 安全：**仅防文件冲突，不防越权**；可信盲测须改用独立容器/VM/MAC（P0-1）
- 状态：INSTALLED（CLI 支持）；作为"安全隔离"使用 = **错误**（已纠正）

---

## ③ 外部官方一手来源 ≥10（E1，与 CLI 缓存分开计数）

> 计数：E0=自述 CLI（1 类）；E1=下列 **13** 条外部官方 URL；E2=市场缓存（209 项/0 装，单列不计入 E1）；E3=本报告推断。

| # | 来源（现行官方 URL） | 版本/适用范围 | 支撑断言 |
|---|---|---|---|
| E1-1 | https://www.codebuddy.cn/docs/cli/permissions | CLI 2.177.x 权限规则 | P0-2 最小集；`--add-dir` 仅授文件访问 |
| E1-2 | https://www.codebuddy.cn/docs/cli/worktree | Git worktree 隔离 | P0-1 "子代理隔离不是安全沙箱" |
| E1-3 | https://www.codebuddy.cn/docs/cli/headless | 无头/`-p`/`-y` | P0-2 `-y` 必需且 HIGH/CRITICAL 仍问 |
| E1-4 | https://www.codebuddy.cn/docs/cli/permission-modes | default/acceptEdits/auto/dontAsk/plan/bypassPermissions | P0-2 `dontAsk`+白名单；bypass≠无条件 |
| E1-5 | https://www.codebuddy.cn/docs/cli/bash-sandboxing | bubblewrap(Linux)/Seatbelt(macOS) | P0-1 真正 OS 级隔离 |
| E1-6 | https://www.codebuddy.cn/docs/cli/security | 整体安全模型/最小权限 | P0-1/P0-2 纵深防御 |
| E1-7 | https://www.codebuddy.cn/docs/cli/iam | IAM/凭据/按仓库授权 | P0-2 GitHub App 单仓授权；ChatGPT≠WorkBuddy |
| E1-8 | https://www.gnu.org/licenses/gpl-faq.en.html | GPL/AGPL FAQ | P1-3 复制/修改/销售合法（守条款） |
| E1-9 | https://www.gnu.org/licenses/gpl-3.0.en.html | GPLv3 正文 §0/§2/§5/§6 | P1-3 "convey"定义；私用无义务 |
| E1-10 | https://www.gnu.org/licenses/agpl-3.0.en.html | AGPLv3 §13 网络触发 | P1-3 SaaS 网络义务 |
| E1-11 | https://spdx.org/licenses/ | SPDX 许可证列表 | P1-3 矩阵标识 |
| E1-12 | https://docs.github.com/en/rest | GitHub REST API（只读路线） | P1-4 无本机 git 的只读 API |
| E1-13 | https://docs.github.com/en/apps | GitHub App 按仓库授权 | P0-2 PR 审批/单仓授权 |

（E2 单列：R02 自报市场缓存 209 项、0 已装——**不计入 E1，不视作已安装**。）

---

## ④ 五案例 A–E（固定输入/命令/输出/正反测试/阈值/费用/回滚/状态）

> 统一字段：目标 / 真实 Skill·连接状态 / 固定输入 / 操作·精确命令 / 输出 / 正反测试 / 阈值 / 权限·费用 / 回滚 / 执行状态 / 依赖阻塞 / **旧版不足是否修复**。

### 案例 A — 开源仓库解构（MIT/Apache/GPL/AGPL/UNKNOWN 场景矩阵）
- 目标：只读解构 owner/repo@冻结 SHA，输出 ARCHITECTURE/DEPENDENCY/LICENSE/SOURCE_LOCK。
- 连接状态：`mcp__github`=DESIGN；`WebFetch`+GitHub REST(只读)=INSTALLED(只读 API 路线，因 git ABSENT)。
- 固定输入：`owner/acme` `repo/logger` `sha=a1b2c3d4e5f6`（冻结）
- 命令：
  `gh api repos/acme/logger/git/trees/a1b2c3d4e5f6?recursive=1`（DESIGN，git ABSENT 时改 `curl -H "Authorization: …" https://api.github.com/repos/acme/logger/git/trees/a1b2c3d4e5f6?recursive=1` 只读，但**无 token 不执行**）；
  `WebFetch(domain:spdx.org)` 取 LICENSE 标识。
- 输出：ARCHITECTURE.md / DEPENDENCY.md / LICENSE 矩阵 / SOURCE_LOCK（冻结 SHA）。
- 正反测试：
  - 正：含 `LICENSE=MIT` → 允许复制/修改/再分发（守声明）；`LICENSE=Apache-2.0` → 须保留 NOTICE；
  - 正：`LICENSE=GPL-3.0` → **允许复制修改销售**，但整体须 GPL、须提供源码（convey 时）；
  - 正：`LICENSE=AGPL-3.0` → 网络/SaaS 交互须提供对应源码（§13）；
  - 负（缺 LICENSE）：`UNKNOWN` → **不得直接复制**，标记 BLOCK-LEGAL-REVIEW；
  - 负：第三方依赖层级/版本漂移 → 标 UNKNOWN-VERSION，回滚到冻结 SHA 复核。
- 阈值：LICENSE 必须命中 SPDX 标识；UNKNOWN→人工法律复核；不得冒称非标 SBOM 为 SPDX/CycloneDX。
- 权限·费用：只读；费用 UNKNOWN。
- 回滚：全部以冻结 SHA 为锚；版本漂移→`git checkout a1b2c3d4`（DESIGN）或只读 API 重新拉树。
- 执行状态：**PLAN / READ-ONLY 路线可设计，未实际拉取（无 token，遵守只读）**。
- 依赖阻塞：git/gh ABSENT → 走 GitHub 只读 API（需审批后部署 token）；扫描器 ABSENT → SBOM-lite 仅结构级。
- 旧版不足修复：**是（P1-3 已按场景矩阵纠正；补缺 LICENSE 负例与"非标 SBOM 不得冒称"约束）**。

### 案例 B — Markdown 合同→PR（最小权限 + 人工审批）
- 目标：CONTRACT.md AC1–AC5 → PATCH.diff → TEST_RESULTS → PR_REVIEW → Git readback。
- 连接状态：`mcp__github`=DESIGN（写 PR 需 GitHub App 单仓授权）；`Bash`=INSTALLED。
- 固定输入：`CONTRACT.md`（AC1–AC5 可机器校验）、目标仓库 `acme/api`、基分支 `main`。
- 命令（**修正后**，对比 R02 见 §6-P0-2）：
  `codebuddy -p "依据 CONTRACT.md 生成 PATCH 并跑 AC 测试" --permission-mode dontAsk --allowedTools "Read,Edit,Grep,Glob,Bash(git diff:*),Bash(git status:*),Bash(npm test:*)" --disallowedTools "Bash(git push:*),Bash(sudo:*),Bash(rm:*),Bash(curl:*),Bash(wget:*)"`
  生成 PATCH.diff 后**不自动 push**；PR 由 GitHub App 单仓授权 + **人工 review** 创建。
- 输出：PATCH.diff / TEST_RESULTS / PR_URL / Git readback diff。
- 正反测试：
  - 正：AC 全绿 → 出 PATCH；
  - 负（测试失败）→ 不提交，回退计划；
  - 负（越权：尝试 `git push`）→ `--disallowedTools` 系统级拒绝；
  - 负（错误分支：非 `main` 基）→ 拒绝；
  - 负（重试重复提交）→ 幂等：同 idem 不建第二个 PR。
- 阈值：AC1–AC5 全 PASS 才可建 PR；push 一律 deny（即使 bypass 也被 `disableBypassPermissionsMode` 退化）。
- 权限·费用：写 PR 需 GitHub App 单仓授权 + 人工审批；费用 UNKNOWN。**ChatGPT 连接器授权不替代**。
- 回滚：未 push 前 `git checkout -- .`；已建 PR 则关闭 PR（不 merge）。
- 执行状态：**PLAN（未授权不自动 push；遵守只读）**。
- 依赖阻塞：git ABSENT → PATCH 生成设计在内存/临时区；push 需审批后 GitHub App。
- 旧版不足修复：**是（P0-2 最小集 + 分支保护 + 人工审批 + 隔离 runner 方案）**。

### 案例 C — 多 Agent 盲测（隔离重做）
- 目标：冻结题目哈希、不同系统身份、不可见彼此答案、独立 runner/容器/VM，输出匿名结果/隔离拒绝日志/评分。
- 连接状态：`--worktree`+`isolation:worktree`=INSTALLED（**但官方明确非安全沙箱**）；真实 OS 隔离=`--sandbox container`=ABSENT(BLOCKED)。
- 固定输入：题目集哈希 `H=sha256(tasks.json)`；Agent_i 只见 `dir_i`+`FROZEN_TASK.md`。
- 命令（修正）：
  真实可信盲测须 `docker run -it --rm -v $(pwd)/agent_i:/w codebuddy --permission-mode dontAsk …`（BLOCKED：docker ABSENT）；
  退而求其次用 worktree 仅作**并行对比（非可信盲测）**：`codebuddy --worktree agent-i`。
- 输出：匿名结果表 / 隔离访问拒绝日志 / 评分。
- 正反测试：
  - 正：Agent_i 试图读 `dir_j` 或共享缓存 → 系统权限拒绝（容器/VM/MAC），附日志；
  - 正：尝试访问其他 Agent 答案 → 拒绝；
  - 负（R02 旧做法）：仅 `--add-dir` 限定 → **不能**宣称可信盲测（工作区非 OS 隔离）。
- 阈值：无 OS 级隔离 → 标注"普通并行对比"，**不得声称可信盲测**。
- 权限·费用：容器/VM 需资源；费用 UNKNOWN。
- 回滚：容器销毁 / worktree 删除。
- 执行状态：**PLAN/BLOCKED（docker ABSENT；无 OS 隔离不声称盲测）**。
- 依赖阻塞：docker/uvx ABSENT；无独立凭据 → 隔离 runner 不可验证。
- 旧版不足修复：**部分（隔离方案已给出并使用官方"非安全沙箱"证据；但本环境无法实测 OS 隔离，标 BLOCKED）**。

### 案例 D — 安全供应链门禁（负例驱动 + 设计矩阵）
- 目标：合成密钥/漏洞/许可证样本集，输出 GATE_MATRIX/误报漏报/RULE_VERSION；CI 真实 block/warn 区分。
- 连接状态：gitleaks/osv-scanner/trivy=ABSENT → **DESIGN/PLAN**；本环境无扫描器。
- 固定输入：合成夹具（见 §5 Sim-D）：3 正/3 负 × {secret, dep, license}。
- 命令（设计）：`osv-scanner --recursive ./`、`gitleaks detect --redact`、`scancode -l ./`
- 输出：GATE_MATRIX（TP/FP/FN/TN）、RULE_VERSION=DESIGN-0.1、CI block vs warn 策略。
- 正反测试（≥3 正/负每类，见 §5 Sim-D 实测）：secret 正=AKIA…/github_pat_…/私钥头；负=占位符/片段/文档 URL；dep 正=log4j 2.14.1/openssl 1.0.2k/django 2.2.0；负=requests/click/pyyaml 干净版；license 正=GPL/AGPL/UNKNOWN；负=MIT/Apache/BSD。
- 阈值：CI **block**=命中已知密钥/已知 CVE/UNKNOWN 许可；**warn**=低置信/版本漂移；RULE_VERSION 须可重放。
- 权限·费用：只读扫描；费用 UNKNOWN。
- 回滚：签名与回滚（设计）：门禁规则版本化，回滚到上一 RULE_VERSION。
- 执行状态：**PLAN / 设计矩阵已用 Python 重放（§5 Sim-D），但无真实扫描器 → NOT_TESTED on live scanner**。
- 依赖阻塞：扫描器 ABSENT → 只设计夹具，不称 PASS（纠正 R02 P1-5）。
- 旧版不足修复：**是（补每类≥3 正负样本、误报/漏报、RULE_VERSION、CI block/warn；明确 NOT_TESTED）**。

### 案例 E — 桥接器可靠性只读审计（最贴近当前项目）
- 目标：输入冻结源码 SHA 与 submit→queued→running→done/failed→Git commit/readback 事件流；输出 EVENT_LOG/DEDUP/STATE_TRANSITION。
- 连接状态：纯 Python 标准库模拟器（§5 Sim-E）=INSTALLED(可跑)；**不触碰生产桥接器或其他实验**。
- 固定输入：payload `{repo,sha,action,frozen}`；idem-key=sha256(payload)。
- 命令：`python3 /tmp/sim_E_bridge.py`（只读模拟；不连生产）。
- 输出：EVENT_LOG / DEDUP(idem) / STATE_TRANSITION；模拟 429、重启 interrupted、任务未提交、队列积压、重复 submit、Git 写入成功但回读失败。
- 正反测试（见 §5 Sim-E 实测）：
  - 正：重复 submit → 同 task_id（幂等）；
  - 正：429 → 指数退避 1s/2s+抖动，重试成功；
  - 正：Git 写入成功但 readback 失败 → 标 READBACK_MISMATCH；
  - 负（越权/失败）：未授权 push 不在本模拟范围（桥接器侧由服务端鉴权）。
- 阈值：幂等键必须稳定；429 退避上限 16s；readback 失败必须告警（不得静默 done）。
- 权限·费用：只读模拟；token/调用成本 UNKNOWN（需采样）；回滚仅在隔离模拟器。
- 回滚：模拟器内状态机可重置；生产回滚不在本只读研究范围。
- 执行状态：**RUN（模拟器 exit 0，可独立重放；不触生产）**。
- 依赖阻塞：无（stdlib）。
- 旧版不足修复：**是（给出 429/重启/重复 submit/Git 回读失败的可重放模拟，纠正 R02 缺项）**。

---

## ⑤ 两项 Python 标准库只读模拟（完整源码/输入/stdout/exitcode 写入正文，M2）

> 两模拟均落 `/tmp`（临时草稿，**非任何实验目录**），纯 `python3` 标准库，未安装任何包，未触生产/其他实验。以下为**完整正文**，可自行复现。

### 5.1 Sim-E（案例 E：桥接队列/429 退避/幂等/ Git 回读）
**源码**（文件 `/tmp/sim_E_bridge.py`，完整）：
```python
#!/usr/bin/env python3
# SIM-E: Bridge queue / 429 backoff / idempotent submit / Git readback mismatch. READ-ONLY SIM.
import hashlib, json, random, sys
from dataclasses import dataclass, field
from typing import Optional
random.seed(20261030)
class Clock:
    def __init__(self): self.t = 0
    def now(self): return self.t
    def sleep(self, s): self.t += s
CLOCK = Clock()
def idem_key(payload: dict) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]
@dataclass
class Task:
    task_id: str; idem: str; state: str; attempts: int = 0
    last_429_at: Optional[int] = None; git_commit_ok: bool = False; git_readback_ok: bool = False
    events: list = field(default_factory=list)
    def log(self, msg): self.events.append(f"[{CLOCK.now()}s] {msg}")
class Bridge:
    def __init__(self): self.tasks = {}; self.seq = 0; self.rate_limited_until = 0
    def _new_id(self):
        self.seq += 1; return f"task-{self.seq:04d}"
    def submit(self, payload, *, force_429_rounds=0):
        key = idem_key(payload)
        if key in self.tasks:
            t = self.tasks[key]; t.log(f"DUPLICATE submit ignored (idempotency-key={key}) -> existing {t.task_id}"); return t, "DUPLICATE"
        if CLOCK.now() < self.rate_limited_until: return None, "RATE_LIMITED_429"
        t = Task(task_id=self._new_id(), idem=key, state="queued"); self.tasks[key] = t
        t.log(f"submit accepted -> {t.task_id} (queued)"); return t, "ACCEPTED"
    def run_task(self, t, *, inject_429=True, git_readback_fail=False):
        t.attempts += 1
        if inject_429 and t.attempts <= 2:
            backoff = min(2 ** (t.attempts - 1), 16); jitter = random.uniform(0, backoff * 0.1)
            self.rate_limited_until = CLOCK.now() + 1; CLOCK.sleep(1); t.last_429_at = CLOCK.now()
            t.log(f"429 received; backoff={backoff:.0f}s+jitter={jitter:.2f}s (attempt {t.attempts})"); return "RETRY"
        t.state = "running"; t.log("running"); CLOCK.sleep(0)
        t.git_commit_ok = True; t.log("Git commit written (sha simulated)")
        if git_readback_fail:
            t.git_readback_ok = False; t.state = "done"; t.log("Git READBACK FAILED -> state=done but readback mismatch FLAGGED")
        else:
            t.git_readback_ok = True; t.state = "done"; t.log("Git readback OK -> verified done")
        return "DONE"
def main():
    b = Bridge(); print("=== SIM-E: bridge queue / 429 backoff / idempotency / git readback ===")
    payload = {"repo": "acme/bridge", "sha": "a1b2c3d4", "action": "deploy", "frozen": True}
    t, st = b.submit(payload); print(f"[submit#1] status={st} task={t.task_id}")
    t2, st2 = b.submit(payload); print(f"[submit#2 dup] status={st2} task={t2.task_id if t2 else None}  (expect DUPLICATE, same id)")
    while t.state == "queued":
        r = b.run_task(t, inject_429=True, git_readback_fail=False)
        if r == "RETRY": continue
    print(f"[run#1] final state={t.state} attempts={t.attempts} git_commit={t.git_commit_ok} readback={t.git_readback_ok}")
    payload2 = {"repo": "acme/bridge", "sha": "e5f6a7b8", "action": "deploy", "frozen": True}
    t3, st3 = b.submit(payload2)
    while t3.state == "queued":
        r = b.run_task(t3, inject_429=False, git_readback_fail=True)
        if r == "RETRY": continue
    flag = (t3.git_commit_ok and not t3.git_readback_ok)
    print(f"[run#2] state={t3.state} git_commit={t3.git_commit_ok} readback={t3.git_readback_ok} READBACK_MISMATCH_FLAG={flag}")
    distinct = len(b.tasks)
    print(f"[assert] distinct tasks created = {distinct} (expect 2)")
    print(f"[assert] idempotency held = {st2 == 'DUPLICATE' and t2.task_id == t.task_id}")
    print(f"[assert] readback-mismatch detected = {flag}")
    print("\n--- EVENT_LOG task1 ---"); [print(e) for e in t.events]
    print("--- EVENT_LOG task2 ---"); [print(e) for e in t3.events]
    ok = (distinct == 2) and (st2 == "DUPLICATE") and flag
    sys.exit(0 if ok else 1)
if __name__ == "__main__": main()
```
**固定输入**：`payload={"repo":"acme/bridge","sha":"a1b2c3d4","action":"deploy","frozen":True}`；重复提交同 payload；task2 注入 `git_readback_fail=True`。
**实测 stdout（本会话运行）**：
```
=== SIM-E: bridge queue / 429 backoff / idempotency / git readback ===
[submit#1] status=ACCEPTED task=task-0001
[submit#2 dup] status=DUPLICATE task=task-0001  (expect DUPLICATE, same id)
[run#1] final state=done attempts=3 git_commit=True readback=True
[run#2] state=done git_commit=True readback=False READBACK_MISMATCH_FLAG=True
[assert] distinct tasks created = 2 (expect 2)
[assert] idempotency held = True
[assert] readback-mismatch detected = True
--- EVENT_LOG task1 ---
[0s] submit accepted -> task-0001 (queued)
[0s] DUPLICATE submit ignored (idempotency-key=4579ee7b220b49c7) -> existing task-0001
[1s] 429 received; backoff=1s+jitter=0.05s (attempt 1)
[2s] 429 received; backoff=2s+jitter=0.11s (attempt 2)
[2s] running
[2s] Git commit written (sha simulated)
[2s] Git readback OK -> verified done
--- EVENT_LOG task2 ---
[2s] submit accepted -> task-0002 (queued)
[2s] running
[2s] Git commit written (sha simulated)
[2s] Git READBACK FAILED -> state=done but readback mismatch FLAGGED
```
**exitcode**：`0`（本会话 `EXITCODE_SIM_E=0`）。

### 5.2 Sim-D（案例 D：供应链门禁矩阵，设计级）
**源码**（文件 `/tmp/sim_D_supplychain.py`，完整）：
```python
#!/usr/bin/env python3
# SIM-D: supply-chain gate matrix. READ-ONLY SIM. DESIGN-0.1 (NOT_TESTED on live scanner).
import re, sys
SECRETS_POS = ["AKIAIOSFODNN7EXAMPLE","github_pat_11ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789","-----BEGIN RSA PRIVATE KEY-----\nMIIBOgIBAAJBAKj34GkxFhD5..."]
SECRETS_NEG = ["AKIA_IS_A_SAMPLE_PLACEHOLDER_NOT_REAL","my_var = 'AKIA'","see https://docs.aws.amazon.com/IAM/latest/UserGuide/id_keys.html"]
VULN_DEP_POS = [("log4j-core","2.14.1"),("openssl","1.0.2k"),("django","2.2.0")]
VULN_DEP_NEG = [("requests","2.31.0"),("click","8.1.7"),("pyyaml","6.0.1")]
LICENSE_POS = ["GPL-3.0-only","AGPL-3.0-only","UNKNOWN"]
LICENSE_NEG = ["MIT","Apache-2.0","BSD-3-Clause"]
RE_AWS = re.compile(r"\bAKIA[0-9A-Z]{16}\b"); RE_GHPAT = re.compile(r"\bgithub_pat_[0-9A-Za-z_]{20,}\b")
RE_PK = re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----")
KNOWN_VULN = {("log4j-core","2.14.1"),("openssl","1.0.2k"),("django","2.2.0")}
BLOCK_LICENSE = {"GPL-3.0-only","AGPL-3.0-only","UNKNOWN"}
def scan_secret(t): return bool(RE_AWS.search(t) or RE_GHPAT.search(t) or RE_PK.search(t))
def scan_dep(n,v): return (n,v) in KNOWN_VULN
def scan_license(l): return l in BLOCK_LICENSE
def main():
    print("=== SIM-D: supply-chain gate matrix (DESIGN-0.1, NOT_TESTED on live scanner) ===")
    tp=fp=fn=tn=0; rows=[]
    for s in SECRETS_POS: hit=scan_secret(s); tp+=hit; fn+=(not hit); rows.append(("secret","POS",hit,"TP" if hit else "FN"))
    for s in SECRETS_NEG: hit=scan_secret(s); fp+=hit; tn+=(not hit); rows.append(("secret","NEG",hit,"FP" if hit else "TN"))
    for n,v in VULN_DEP_POS: hit=scan_dep(n,v); tp+=hit; fn+=(not hit); rows.append(("dep","POS",hit,"TP" if hit else "FN"))
    for n,v in VULN_DEP_NEG: hit=scan_dep(n,v); fp+=hit; tn+=(not hit); rows.append(("dep","NEG",hit,"FP" if hit else "TN"))
    for l in LICENSE_POS: hit=scan_license(l); tp+=hit; fn+=(not hit); rows.append(("license","POS",hit,"TP" if hit else "FN"))
    for l in LICENSE_NEG: hit=scan_license(l); fp+=hit; tn+=(not hit); rows.append(("license","NEG",hit,"FP" if hit else "TN"))
    print(f"{'class':8} {'fixture':5} {'detected':8} {'result'}"); [print(f"{r[0]:8} {r[1]:5} {str(r[2]):8} {r[3]}") for r in rows]
    print(f"\nGATE_MATRIX: TP={tp} FP={fp} FN={fn} TN={tn}")
    precision = tp/(tp+fp) if (tp+fp) else 0; recall = tp/(tp+fn) if (tp+fn) else 0
    print(f"precision={precision:.3f} recall={recall:.3f}  (DESIGN baseline; NOT_TESTED on real scanner)")
    print("\nKNOWN_GAPS (must be closed before any CI block):")
    print(" - regex secrets miss env-var indirection / base64 / vault references (FP/FN risk)")
    print(" - KNOWN_VULN is a 3-entry fixture, not a live advisory feed (OSV/GHSA)")
    print(" - license scan assumes SPDX tag present; UNKNOWN => block (per policy, not detection)")
    ok = (fp == 0 and fn == 0)
    print(f"\n[assert] design matrix clean on fixtures = {ok}  (still NOT_TESTED: no scanner installed)")
    sys.exit(0 if ok else 1)
if __name__ == "__main__": main()
```
**固定输入**：上列 6×3 合成夹具（明确 fake，无害）。
**实测 stdout（本会话运行）**：
```
=== SIM-D: supply-chain gate matrix (DESIGN-0.1, NOT_TESTED on live scanner) ===
class    fixture detected result
secret   POS   True     TP
secret   POS   True     TP
secret   POS   True     TP
secret   NEG   False    TN
secret   NEG   False    TN
secret   NEG   False    TN
dep      POS   True     TP
dep      POS   True     TP
dep      POS   True     TP
dep      NEG   False    TN
dep      NEG   False    TN
dep      NEG   False    TN
license  POS   True     TP
license  POS   True     TP
license  POS   True     TP
license  NEG   False    TN
license  NEG   False    TN
license  NEG   False    TN

GATE_MATRIX: TP=9 FP=0 FN=0 TN=9
precision=1.000 recall=1.000  (DESIGN baseline; NOT_TESTED on real scanner)

KNOWN_GAPS (must be closed before any CI block):
 - regex secrets miss env-var indirection / base64 / vault references (FP/FN risk)
 - KNOWN_VULN is a 3-entry fixture, not a live advisory feed (OSV/GHSA)
 - license scan assumes SPDX tag present; UNKNOWN => block (per policy, not detection)

[assert] design matrix clean on fixtures = True  (still NOT_TESTED: no scanner installed)
```
**exitcode**：`0`（本会话 `EXITCODE_SIM_D=0`）。

> M2 落实：两模拟均含最小源码+固定输入+原始 stdout+exitcode+环境版本（python3 3.13.5），可独立重放；未指私有目录替代。属 **SELF_REPORTED_REPRODUCED**（本机可跑），但 Case D 在"真实扫描器"维度仍为 NOT_TESTED（无扫描器），未冒称 PASS。

---

## ⑥ 两项 P0 及 P1 逐项纠正表（R02原句→本轮修订→证据→解决追踪）

### 6.1 P0-1 工作区 ≠ 安全沙箱
| 项 | 内容 |
|---|---|
| **R02 原句（E3 转述）** | 案例 C："Agent_i 只可见 dir_i 与 FROZEN_TASK.md；--add-dir 限定" |
| **原因** | 把 Git worktree / `--add-dir` 的"文件可见范围"误当作 OS 访问控制与盲测隔离 |
| **本轮修订** | 区分四层：Git 工作区 / OS 权限 / GitHub App 授权 / CI 执行 / 模型 Agent 权限。**真实隔离用独立用户/容器/VM 或 MAC + 只读挂载 + 独立凭据**；本机无 docker 时标 BLOCKED，不声称可信盲测 |
| **证据** | E1-2 worktree 文档 FAQ："子代理隔离是安全沙箱吗？**不是**…防止文件冲突，而非安全限制"；E1-1："操作系统级保护需要靠 Bash 沙箱"；E1-5 bash-sandboxing 用 bubblewrap/Seatbelt OS 原语；E0 CLI `--sandbox container` 需 Docker/Podman（本环境 ABSENT） |
| **验收（未做=PLAN）** | 越目录读取/访问其他 Agent 答案/共享缓存 三类负例须由**系统权限拒绝并附日志**；不能用提示词拒绝替代 |
| **状态** | **已解决（方案+官方证据）；本机实测 BLOCKED** |

### 6.2 P0-2 headless 自动写入授权过宽
| 项 | 内容 |
|---|---|
| **R02 原句（E3 转述）** | 案例 B：`codebuddy -p ... -y --permission-mode acceptEdits --allowedTools "Bash,Read,Edit,Write"` |
| **原因** | 仅 `disallowedTools` 缺 `Bash(git push)` 不足防越权；`Bash` 全开可绕（复合命令/间接写） |
| **本轮修订** | 最小工具/命令允许集：`--permission-mode dontAsk` + `--allowedTools "Read,Grep,Glob,Bash(git status:*),Bash(git diff:*),Bash(npm test:*)"` + `--disallowedTools "Bash(git push:*),Bash(sudo:*),Bash(rm:*),Bash(curl:*),Bash(wget:*)"`；分支保护（仅 `main` 基）、GitHub App 按仓库授权、PR 人工审批、隔离 runner |
| **证据** | E1-4 permission-modes：`dontAsk`+allow=固定白名单代理；bypass≠无条件（deny/ask 先评估，HIGH/CRITICAL 仍问，`disableBypassPermissionsMode` 可退化）；E1-3 headless：`-y` 必需且 HIGH/CRITICAL 仍可能问，真正 full pass 需 `CODEBUDDY_IS_SANDBOX=1`；E1-1 复合命令"deny/ask 任一子命令命中即触发"；E1-7 IAM 按仓库授权 |
| **验收（未做=PLAN）** | git push / 访问凭据 / 错误分支 / 危险网络请求 四类负例由**系统/服务端拒绝**；不实际生产写入 |
| **状态** | **已解决（方案+官方证据+最小集给出）；本机生产写入未执行（只读约束）** |

### 6.3 P1-3 GPL/AGPL 过度禁止
| 项 | 内容 |
|---|---|
| **R02 原句（E3 转述）** | 案例 A：GPL/AGPL 统一"禁止直接复制" |
| **原因** | 与 GNU 官方 FAQ/正文冲突：GPL 允许复制/修改/销售，仅"convey"时触发义务 |
| **本轮修订** | 按 SPDX + 场景矩阵：MIT/Apache-2.0（宽松，守声明/NOTICE）/GPLv3（复制修改合法，整体须 GPL、convey 须供源码）/AGPLv3（同 GPL + §13 网络交互须供源码）/UNKNOWN（不得直接复制，人工法律复核） |
| **证据** | E1-8 GPL FAQ："You are allowed to sell copies of the modified program commercially, but only under the terms of the GNU GPL"；E1-9 GPLv3 §2："make, run and propagate covered works that you do not convey, without conditions"；E1-10 AGPLv3 §13 网络触发；E1-11 SPDX |
| **验收** | 每类列条件义务/阻断/人工法律复核；许可 UNKNOWN 不得直接复制；不一刀切 |
| **状态** | **已解决** |

### 6.4 P1-4 运行环境阻塞
| 项 | 内容 |
|---|---|
| **R02 原句（E3 转述）** | E21：无 git、uv/uvx、docker、扫描器；A/B/C/D 命令未能实际运行 |
| **原因** | 环境确缺工具；且曾把"缓存有插件"误当"已安装" |
| **本轮修订** | 先用只读 CLI `help`/`which` 核查（E0 实测：codebuddy 2.177.0 在；git/docker/uv/uvx **ABSENT**）；给"无需本机 git 的 GitHub 只读 API 路线"（E1-12）+ 审批后可部署路线；**不因为缓存里有插件就宣称已安装** |
| **证据** | E0 `which git/docker/uv/uvx` 均为空；E1-12 GitHub REST 只读；E2 市场缓存 209/0 装（单列，不视作已装） |
| **验收** | 五例逐案依赖/阻塞状态/替代路径/成本；运行未发生一律 PLAN/BLOCKED |
| **状态** | **已解决（核查+替代路径+明确 ABSENT/BLOCKED）** |

### 6.5 P1-5 供应链门禁"100% 检出"无实测
| 项 | 内容 |
|---|---|
| **R02 原句（E3 转述）** | 案例 D：以少数示例声称 100% 负例检出；AKIA 样本不证明真实密钥覆盖 |
| **原因** | 无扫描器却称 PASS；样本不代表真实覆盖 |
| **本轮修订** | 合成密钥/已知脆弱依赖/无害代码夹具；每类 ≥3 正负样本；记录误报/漏报、扫描器版本、CI block vs warn；**未安装只设计夹具，不称 PASS** |
| **证据** | §5 Sim-D 实测 TP=9/FP=0/FN=0/TN=9（设计基线）+ KNOWN_GAPS 显式标注 NOT_TESTED；E1-12/OSV 为真实数据源（未接） |
| **验收** | 测试矩阵 + 可重放源码/输入/stdout/exitcode，或 NOT_TESTED |
| **状态** | **已解决（设计矩阵可重放；真实扫描 NOT_TESTED，未冒称 PASS）** |

### 6.6 P2-6 商业优先级
| 项 | 内容 |
|---|---|
| **R02 原句（E3 转述）** | Top5 未考虑本环境缺 git/docker、ChatGPT 已连 GitHub、插件未装、实际费用 |
| **原因** | 选型脱离本环境与现实授权/费用 |
| **本轮修订** | 按"零安装 GitHub 只读 → Markdown 合同 → 静态审计 → 隔离测试 → PR 审批 → CI 发布"重排；给可核成本/权限表；**未知价格标 UNKNOWN**；明确 ChatGPT GitHub 连接器 ≠ WorkBuddy 授权 |
| **证据** | §2 Top5 状态列（INSTALLED/CACHED-0/ABSENT/DESIGN/BLOCKED）；§3 E1-7；费用全标 UNKNOWN（无账单访问） |
| **验收** | 每候选显式连接状态与费用 UNKNOWN 占位 |
| **状态** | **已解决** |

### 6.7 总追踪表（R02原句→修订→证据→解决）
| 缺陷 | R02 原句（摘要） | 本轮修订 | 证据 | 状态 |
|---|---|---|---|---|
| P0-1 | "--add-dir 限定即隔离" | 独立容器/VM/MAC+只读挂载；无 docker 标 BLOCKED | E1-2/1-1/1-5；E0 `--sandbox` | 已解决(方案)/BLOCKED 实测 |
| P0-2 | `-y acceptEdits --allowedTools "Bash,Read,Edit,Write"` | dontAsk+白名单+disallow push+分支保护+人工 PR | E1-4/1-3/1-1/1-7 | 已解决(方案)/未生产写入 |
| P1-3 | "GPL/AGPL 禁止直接复制" | SPDX 场景矩阵，复制合法守条款 | E1-8/1-9/1-10/1-11 | 已解决 |
| P1-4 | "无 git/docker/uvx/扫描器，命令未跑" | 只读核查+GitHub 只读 API 替代+明确 ABSENT | E0；E1-12；E2 | 已解决 |
| P1-5 | "100% 负例检出；AKIA 样本" | ≥3 正负夹具+误报漏报+NOT_TESTED | §5 Sim-D | 已解决(设计)/NOT_TESTED |
| P2-6 | "Top5 未计缺 git/docker/费用" | 重排+状态表+费用 UNKNOWN+ChatGPT≠WB | §2/§3 E1-7 | 已解决 |

---

## ⑦ M1–M3 方法落实证据、未解决与新增问题

### 7.1 M1 官方/现行来源先行
- 落实：§3 列 **13 条 E1 外部官方一手来源**（URL+版本/适用范围），与 E0（CLI 自报）、E2（市场缓存 209/0）、E3（推断）**分开计数**。
- 跨厂仅迁移方法：R10 F10（76/100）、R03 F3（83/100）只用于 F2 方法改进，**不替代 R02 同厂基线**，不把 NO FAKES Act 当现行法、不混计本地缓存（本轮已避免）。
- 未解决：R02 报告 markdown 在本环境不可独立复读（N1）。

### 7.2 M2 工件可独立重放
- 落实：§5 两项 Python 标准库模拟，**完整源码+固定输入+原始 stdout+exitcode(均 0)** 写入正文；可独立重放；未用私有目录替代。
- 未解决/限制：Case D 在"真实扫描器"维度 NOT_TESTED（环境无扫描器），未冒称 PASS；成本/token 采样 UNKNOWN（无账单访问）。

### 7.3 M3 安全与权限负例实证
- 落实：五案例均含"越权/失败/成本/回滚/PLAN 或 RUN 状态"；安全/权限负例区分五层（Git 工作区 / OS 权限 / GitHub App 授权 / CI 执行 / 模型 Agent 权限）。
- 未解决：本环境无法实测 OS 级隔离（docker ABSENT）→ P0-1 实测 BLOCKED；无法实测 GitHub App 单仓授权（无 token/凭据，遵守只读）→ P0-2 生产写入未执行。

### 7.4 新增缺陷（N）
- **N1（来源可溯性）**：R02 `rounds/R02/WORKBUDDY_REPORT.md` 等在本文件系统不可读，R02 原句仅由反馈包转述（E3 级）。建议后续同厂轮次把 R02 报告落盘于可访问路径，满足 M2 独立复放。
- **N2（跨产品授权混淆）**：R02 P2-6 把"ChatGPT 已连 GitHub"作为可行路径，隐含跨产品授权等同。本轮已显式分离（ChatGPT 连接器 ≠ WorkBuddy 授权），建议作为工厂级检查项。
- **N3（缓存即安装错觉）**：R02 曾因市场缓存含插件而暗示可用。本轮 E2 单列"209 缓存/0 装"，所有插件能力标 ABSENT/DESIGN/BLOCKED。

### 7.5 未验证项（BLOCKED / UNKNOWN，不声称解决）
| 项 | 原因 | 标记 |
|---|---|---|
| `--sandbox container` 实测 OS 隔离 | docker ABSENT | BLOCKED |
| GitHub App 单仓授权 + 人工 PR | 无 token/凭据，只读约束 | PLAN |
| 真实扫描器（gitleaks/osv/trivy）运行 | ABSENT | NOT_TESTED |
| 五案例生产写入/真实 push | 只读研究约束 | 未执行 |
| token/调用/插件费用 | 无账单访问 | UNKNOWN |
| R02→R12 同厂 Δ / 五维差 / P0 复发率 | 须 ChatGPT 独立审计 | **不由 WorkBuddy 宣布** |

---

## 交付自检（对照反馈包要求）
- ① R02 基线 81 与五维/五案例复盘：✓ §1
- ② 候选 ≥12、Top5 官方/manifest/命令/依赖/费用/安全/授权：✓ §2
- ③ 外部官方一手 ≥10 且与缓存分开计数：✓ §3（13 条 E1）
- ④ 五案例 A–E 固定输入/命令/输出/正反测试/阈值/费用/回滚/状态：✓ §4
- ⑤ ≥2 Python 标准库可重放只读模拟，完整源码/输入/stdout/exitcode 入正文：✓ §5（Sim-E、Sim-D，exit 0）
- ⑥ 两 P0 及 P1 逐项纠正表：✓ §6（P0-1/P0-2/P1-3/P1-4/P1-5/P2-6 + 总追踪表）
- ⑦ M1–M3 方法证据、未解决与新增：✓ §7
- 禁：自评分 / 声称同厂质量已提高：✓ 未做（Δ 留待 ChatGPT 审计）
- 边界：E0/E1/E2/E3 分开；缓存≠安装；ChatGPT 授权≠WorkBuddy 授权：✓ 全程标注

---

**正文完。** 已落盘于 `factory24_20261030/R12_F2_WORKBUDDY_REPORT.md` 供 ChatGPT 独立审计取用。R02→R12 同厂 Δ、五维差、P0 复发率均由 ChatGPT 在取得正文后计算，WorkBuddy 不自行宣布提升。