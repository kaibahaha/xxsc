# GitHub 往返证据（真实仓库 + 本地 git 对象）

本文件只写**实际发生**的事。任何未达成项显式标 `NOT_VERIFIED`，不以"应该可以"代替证据。

## 0. 执行环境事实

| 事实 | 观测 |
|---|---|
| `api.github.com:443` | 可达（真实 API 调用成功） |
| `github.com:443`（git smart HTTP） | **不可达**（`Failed to connect ... port 443`），`git push` 不可用 |
| `raw.githubusercontent.com` | 可达（用于独立读取基线文件） |
| 凭据 | 阶段一：无 token（`gh` 未登录、无环境变量）；阶段二：拿到 `repo` scope 的 PAT（**无** `workflow` scope） |

因此分支发布使用 Git Data API（blob → 嵌套 tree → commit → fast-forward ref），语义等价于 push；已通过本地 `git hash-object` 与远端 blob SHA 双重校验。

## 1. 读取（真实仓库，冻结基线）

| 项目 | 值 |
|---|---|
| repo | `kaibahaha/xxsc` |
| baseline ref | `exp/agensh-lite-v4.2-controller-mvp-20261025` |
| 冻结 commit | `2d4c1a6fc0792a1182777262b41bfb4c09c0b5d2`（`git cat-file -t` = commit；标题 `dispatch: freeze V4.2 R01 ...`） |
| TASK.md（raw @冻结 commit） | 4087 bytes，sha256 `d47b09b99f3eded1dc8a76f22fdcd97ca1ba186d938c93314bf7553db80b1eb3` |
| INTERFACE_HANDOFF.md | 2109 bytes，sha256 `c5934de46926830dc30e08aee04cdf6a903305af3fcbe702e1ee0043893c9a4c` |
| mixed_pool.example.json | 9676 bytes，sha256 `f8ffb65b054011804b5965abdc0ae03cc6f266d9c038739bf8a87fb6...`（完整值见 `evidence/remote_probe_2.log`） |
| 无凭据 API 读取 | 首次成功；随后触发匿名限流 `403 RATE_LIMITED`（`x-ratelimit-remaining: 0`，reset `1792944492`），如实记录，不视为仓库不可用 |

## 2. 写入 + 独立回读（真实 API，2026-10-25T16:19Z）

`agl verify-roundtrip --transport api --apply`，目标 `dev/agl-v4.2-workbuddy-adapters`：

| 字段 | 值 |
|---|---|
| path | `factory/projects/AGL-R01-PROBE/_probe/ROUNDTRIP_RUN-RT-REAL-2.json` |
| base head（写入前） | `6961e58a7d85b9aeceebf006225c95893c8ececa` |
| commit_sha（写入） | `a0ae03b595f36bc7af17a72209b05cf601e3a1be` |
| blob_sha | `54276ebad59ca4da07f2d75ceecff73afb868225` |
| content_sha256 | `49ad3bbb632ba38f4a52ecfd8dbb399006e5468852b854c97c5e7b42800df19f` |
| 第二次独立读取 sha256 | `49ad3bbb632ba38f4a52ecfd8dbb399006e5468852b854c97c5e7b42800df19f` |
| 第二次读取 blob_sha | `54276ebad59ca4da07f2d75ceecff73afb868225` |
| matches | **true** |
| 写入时刻 / 回读时刻 | `2026-10-25T16:19:18Z` / `2026-10-25T16:19:22Z` |
| 传输 | `github_rest`（真实 API） |

另一次（`RUN-RT-REAL-1`）：commit `6961e58a7d85...`、blob `e8631eb17dcc...`、sha256 `53d73395a18e...`，同样 `matches=true`。

## 3. 幂等重放（同一 run_id 第二次调用）

| 项目 | 结果 |
|---|---|
| 第二次调用时刻 | `2026-10-25T16:19:25Z` |
| 返回 commit | `a0ae03b595f36bc7af17a72209b05cf601e3a1be`（**与首次相同**） |
| 分支 HEAD（两次调用后） | `a0ae03b595f36bc7af17a72209b05cf601e3a1be` —— **未产生新提交** |
| 判定 | `IDEMPOTENT_REPLAY`（内容哈希一致，未覆盖、未重复） |

## 4. 事件冲突（同 event_id，不同 payload）

| 项目 | 值 |
|---|---|
| event_id | `EV-R01-COLLIDE-1` |
| 首次投递 | `CREATED`，commit `0954f21521ca`，manifest sha256 `2bd34b1b622755f99e9bc449d83f7986c7b57e0296825054b3f6647aa909eada` |
| 目标文件 sha256 | `ba1b261bf620c1356eba40bbce190b7dea0ba09daba596b0eb30251da52bcd36` |
| 第二次（payload B） | `EVENT_ID_COLLISION`，CLI 退出码 **6** |
| 原文件 | 未被修改（`reconcile` 显示事件仍在、sha256 未变） |

## 5. 端到端：任务 → 看板 → 认领 → ACK → 游标（真实 API）

| 步骤 | 证据 |
|---|---|
| 种子任务 | `34f316bd965a`，blob `f23a03e0b8d6`，回读 `matches=True` |
| BOARD CAS 发布 | `c5d5dcdd4f83`，sha256 `e2c88f044ca7...` |
| 轮询 | `RUN-R01-REAL-POLL`：`CLAIM_PROPOSED`，task `TASK-R01-PROBE`，planned `16:21:42Z` / actual `16:22:05Z`，`CONTROLLER_UNAVAILABLE` |
| 认领事件 | `e5b099a5ed19`（outbox），run record `86bc60c3c115`，meta `ade2bc27ba34` |
| ACK | `08e0b542d343`（`07_receipts/WORKBUDDY_01/EV-R01-COLLIDE-1.json`），`reconcile` 显示 `ack_present=true`, `ack_result=DELIVERY_ACK` |
| cursor 前进 | `ef19faa19196` |
| cursor 回退尝试 | `MONOTONIC_NOOP`，仍为 `2026-10-25T16:20:00Z` |

## 6. 本地 bare 仓库（真实 git 对象，无网络）

`bash factory/tools/local_evidence.sh`，日志 `evidence/local_evidence.log`：

| 字段 | 值 |
|---|---|
| ref | `exp/test`（由当前 checkout 克隆出的裸库） |
| 写入前 head | `98c09e6ad386928aa0e2b924db5fa6c76080e60b` |
| commit_sha | `cc1c49440f60cbcd8ea8f24a001c13183e61dd7d` |
| blob_sha | `5527bd0bdeb9d6b09ae61e1994539eb77f7cb683` |
| content / readback sha256 | `0782ece97eaa3c69f44d7b8af537ff9e803e6895b31328a1bdba2e3368e36955` / 同值 |
| matches | true |
| 时间 | `2026-10-25T16:29:07Z` |

同一脚本还给出：N=2/3/5/6/10/20 全部 `PASS`；`offsets --k 1..6` 与规范表逐字一致；`run-sample-test` 真实 pytest `PASS`（exit 0，commit `6055f2e`）；错误 SHA → `STALE_TEST`（exit 5）；无 runner → `BLOCKED_EXECUTOR`（exit 3）。

## 7. NOT_VERIFIED（明确未达成）

| 项目 | 原因 |
|---|---|
| 通过 `git push` 发布分支 | `github.com:443` 不可达；已用 Git Data API 等价替代并双向校验 SHA |
| GitHub Actions 实际运行 | 推送 `.github/workflows/*` 被拒（token 无 `workflow` scope）；定义改为 `factory/ci/` 交付，未激活 |
| ChatGPT 定时任务自动唤醒并读取 | 无平台 API/Webhook，无法在本环境实测 |
| 跨平台（ChatGPT→WorkBuddy→Codex）实时接力 | 同上；只能提供 Git 信箱 + 各自节拍机制 |
| Codex 云端执行器 | 无已验证端点 |

## 8. 事故与恢复（必须留档）

- `2026-10-25T16:24:16Z`：联网测试「未认证写入必须失败」因环境新增 `GITHUB_TOKEN` 而被 `RestTransport` 自动采用，**真实写入基线分支**，产生提交 `5c5e95c5de8239623556071003aa79bbec93171f`（父提交 `2d4c1a6`，仅新增 `factory/_probe/should-not-exist.json`；该提交 tree `7ac91b51...`，基线 tree `3fcb1c95...`）。
- 处置：确认该提交父链只有 `2d4c1a6`（没有覆盖他人的提交）后，用 `PATCH /git/refs/heads/<baseline> {"sha":"2d4c1a6...","force":true}` 将基线**精确恢复**到冻结提交；随后 `contents/factory/_probe/should-not-exist.json` 返回 **404**。
- 根因修复：`RestTransport(token="")` 语义改为"显式未认证"，不再回退环境变量；联网测试断言 `authenticated is False`，写目标限定 dev 分支。
- 影响：基线分支现为 `2d4c1a6fc0792a1182777262b41bfb4c09c0b5d2`，内容与冻结基线一致；事故提交已不可达，SHA 保留在此供审计。
