# CLAIM RECEIPT｜AGL-WB-ADAPTERS-R01 / WORKBUDDY

- RUN_ID: `RUN-20261025T1541Z-WB-ADAPTERS-R01-A1`
- TASK_ID: `AGL-WB-ADAPTERS-R01`
- AGENT_ID: `WORKBUDDY`（provider_id=`workbuddy`，account_scope=`workbuddy-main`）
- 认领方式: 手动认领（**非租约**）。当前无 Controller，`CLAIM_PROPOSED` 不代表排他。
- 状态: `CLAIMED` → `IMPLEMENTED` → `DELIVERED_DRAFT_PR`
- 开始时间: 2026-10-25T15:41:25Z（clone 时刻）
- 认领记录写入时间: 2026-10-25T16:45Z

## 基线

| 项目 | 值 |
|---|---|
| repo | `kaibahaha/xxsc` |
| 工单基线分支 | `exp/agensh-lite-v4.2-controller-mvp-20261025` |
| 冻结基线 SHA | `2d4c1a6fc0792a1182777262b41bfb4c09c0b5d2` |
| 校验方式 | `git cat-file -t` = commit；标题 `dispatch: freeze V4.2 R01 Codex core and WorkBuddy adapters workorders, branches and QA gates`；分支名未作为 SHA 替代 |
| 开发分支 | `dev/agl-v4.2-workbuddy-adapters`（创建前 `git ls-remote` 确认远端不存在同名分支，无覆盖历史） |
| 分支起点 | 直接 `switch -c` 于冻结 SHA |

## 权限探针（按时间顺序，如实记录）

| # | 探针 | 结果 |
|---|---|---|
| 1 | `git clone`（HTTPS，无凭据） | 成功，公开仓库可读 |
| 2 | `git fetch origin` | 首次超时（TLS terminated），重试仍超时 → 归类为环境网络抖动，不影响本地对象完整性 |
| 3 | 冻结提交存在性 | `commit`（本地对象，克隆所得） |
| 4 | `raw.githubusercontent.com` 读取 TASK.md / INTERFACE_HANDOFF.md | 成功；sha256 `d47b09b9…` / `c5934de4…` |
| 5 | `api.github.com` 无凭据读 ref | 首次成功；随后 `403 RATE_LIMITED`（剩余 0） |
| 6 | `api.github.com` 无凭据写 | `401 NO_PERMISSION`（未产生提交） |
| 7 | `git push`（有 token 后） | **失败**：`github.com:443` 不可达（135s 超时） |
| 8 | `git push`（网络可用时） | **被拒**：PAT 无 `workflow` scope，无法创建 `.github/workflows/*` |
| 9 | 有 token 后 API 读 | 成功，`scopes=repo`，配额 5000/h |
| 10 | 有 token 后 API 写（隔离路径 + 自有 dev 分支） | 成功；commit/blob/sha256 与二次读取一致 |
| 11 | 执行环境（本地 subprocess runner） | 可用；真实 pytest exit 0 |

结论：**读 = SUPPORTED；写 = SUPPORTED（仅限自有 dev 分支、自有路径，且无 workflow scope）；平台触发 = UNSUPPORTED；平台排班 = UNKNOWN。**

## 文件边界承诺（实际遵守）

允许：`factory/agl/{storage,adapters,poll.py,execution.py,cli.py,support/}`、`factory/tests/{adapters,integration}/`、`factory/{pyproject.toml,README.md,config,ci,tools,.gitignore}`、`factory/commands` 无、本 claims 与 `deliveries/WORKBUDDY_ADAPTERS_R01/`。

未触碰：`factory/agl/{config,schemas,events,controller,leases,task_state,memory,context,handoff,audit,replay,registry}.py`（Codex 专属）、`main`、盲测分支、`frameworks/agensh-lite-v4.1/`、微软原仓库。

## 事故记录（认领期间）

2026-10-25T16:24:16Z 一个联网测试因环境 token 自动生效，向**基线分支**写入 `factory/_probe/should-not-exist.json`（提交 `5c5e95c`）。已确认父链仅有 `2d4c1a6`、未覆盖他人提交，随后 `force` 恢复基线至 `2d4c1a6`，文件 404。根因已修并加回归测试。详见 `deliveries/.../GITHUB_ROUNDTRIP_EVIDENCE.md` §8。

## 交付

- 本地提交：`0cf0237`（实现）、`1fdf4d1`（CI 暂存）、`6055f2e`（凭据/worktree 修复）
- 远端发布：`02566162b99b1bd0711e321ae55b714efbad9346`（代码，38 文件）+ 探针提交链（见 `REPORT.md` §2）
- PR：#2 <https://github.com/kaibahaha/xxsc/pull/2>（draft，指向工单基线分支，未合并）
- 交付目录：`frameworks/agensh-lite-v4.2/deliveries/WORKBUDDY_ADAPTERS_R01/`
