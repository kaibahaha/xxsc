# 阻断与未达成项（R01）

按影响排序。每一项都给出"现在的行为"和"解除条件"，避免下一位把未验证当已完成。

## B1｜`github.com:443` 不可达，`git push` 无法使用（已绕过，仍属环境阻断）

- 现象：`Failed to connect to github.com port 443 after 135956 ms`；`api.github.com` 正常。
- 现状：分支通过 Git Data API 发布（`factory/tools/publish_branch.py`），blob/tree/commit 均由 GitHub 生成，并用本地 `git hash-object` 对每个 blob 做双向校验。远端提交链见 `REPORT.md` §2。
- 影响：远端历史是压缩提交 + 探针提交，本地 3 个语义提交无法以对象形式推送；已附 `git-bundle/workbuddy-adapters.bundle` 保留本地历史。
- 解除：在可访问 `github.com:443` 的环境执行 `git push origin dev/agl-v4.2-workbuddy-adapters`；若对象不一致需先 `git fetch` 后 rebase，禁止强推。

## B2｜令牌缺少 `workflow` scope，CI 定义无法推送到 `.github/workflows/`

- 现象：`refusing to allow a Personal Access Token to create or update workflow .github/workflows/agl-adapters-tests.yml without workflow scope`。
- 现状：CI 定义以 `factory/ci/agl-adapters-tests.yml` 交付，并附 `factory/ci/README.md` 说明激活步骤；**未激活、未运行**。
- 解除：使用带 `workflow` scope 的 token/App，经用户批准后 `git mv` 到 `.github/workflows/` 再推送。

## B3｜Controller / Lease / Event 核心缺失（Codex 负责）

- 现状：`poll` 只产出 `CLAIM_PROPOSED`，`controller_state=CONTROLLER_UNAVAILABLE`；`ExecutorBridge.ensure_business_acceptance()` 在缺 `agl.controller` 时抛 `CONTROLLER_UNAVAILABLE`，`TEST_RESULT.business_acceptance` 恒为 `PENDING_CORE`。
- 影响：没有排他租约、没有 fencing、没有权威 BOARD；`rebuild-board` 只生成"适配器投影"，文件头明确写明不得据此授租。
- 解除：Codex 交付 `agl.controller`/`agl.leases`/`agl.events` 后，在本分支接 `grantLease` 与 ACK 回执（见 `STUBS.md`）。

## B4｜ChatGPT / WorkBuddy / Codex 无可用触发通道

- 现状：`trigger=UNSUPPORTED`（三平台），`schedule=UNKNOWN`（三平台）。跨平台接力只有 Git 信箱 + 各自节拍；`plan-schedules` 产出的是待人工登记清单，`verified=false`、`creates_real_schedule=false`。
- 影响：无法声称"ChatGPT 定时任务会自动触发 WorkBuddy"。任何此类说法都不成立。
- 解除：平台提供可验证的唤醒/排班 API，并实测一次真实触发（记录 request id、时间、接收日志）。

## B5｜云端执行器未接通

- 现状：只有本机 `LocalSubprocessRunner`（真实 subprocess、真实 exit code、原始日志）。无 runner 时 `BLOCKED_EXECUTOR`。
- 影响：CI/云端 Runner 的跨机执行未被验证；`environment_id` 仅描述本机（`linux-x86_64-py3.11`）。
- 解除：提供带鉴权的远程 Runner 端点，并在 `TEST_RESULT` 中回传可核验的环境与 commit。

## B6｜示例配置自身不合规（已发现，未改动上游文件）

- `config/agent_pool.example.json` 与 `mixed_pool.example.json` 各自出现两次 `WORKBUDDY_DEV_01`（一次 `provider_id=chatgpt`，一次 `workbuddy`），`WORKBUDDY_QA_01` 同样重复；`active_agent_ids` 因此语义歧义。
- 现状：`validate-config` 对这两个文件返回 `DUPLICATE_AGENT_ID`（`tests/adapters/test_registry_pool.py::test_shipped_example_configs_have_duplicate_ids`）。未修改上游示例（避免与 Codex 冲突），另在 `factory/config/` 提供合规的 N=6 配置。
- 解除：由规范维护者去重并明确每个 agent 的 provider 归属。

## B7｜配额全部未验证

- 现状：ChatGPT 的 5 槽/预留 2 是示例值；WorkBuddy/Codex 配额为 `null`。`capacity_verified=false` 时只告警，不硬拒。
- 影响：无法据此断言"最多可跑 N 个"。`N=20` 只证明配置与调度逻辑成立，不代表平台容量。
- 解除：逐平台实测配额与限流后置 `capacity_verified=true` 并填实测值。

## B8｜基线分支误写事故（已恢复）

- 2026-10-25T16:24:16Z 一个联网测试因环境 token 被自动采用，向基线分支写入 `factory/_probe/should-not-exist.json`（提交 `5c5e95c5de82`，父提交即 `2d4c1a6`）。
- 已确认该提交只含此文件、未覆盖他人工作；用 `PATCH ref force=true` 将基线恢复为 `2d4c1a6fc0792a1182777262b41bfb4c09c0b5d2`，文件现为 404。
- 根因已修（`RestTransport(token="")` 显式未认证；测试断言 `authenticated is False`；写目标限定 dev 分支）。留档于 `GITHUB_ROUNDTRIP_EVIDENCE.md` §8。
