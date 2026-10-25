# 发给 WorkBuddy｜Agensh-Lite V4.2 GitHub 云端适配与集成代码任务

你是工程执行与集成负责人。任务是把 Codex 的控制逻辑接成能真正运行、测试、审计的 GitHub 协作控制系统，不是只写漂亮 Markdown。

## Git 精确位置
REPO kaibahaha/xxsc
START_BASE exp/agensh-lite-v4.2-controller-mvp-20261025（先核对 HEAD SHA）
READ_ONLY_REFERENCE frameworks/agensh-lite-v4.1/ + frameworks/agensh-lite-v4.2/
READ_ONLY_MICROSOFT microsoft/Agensh@0468a3e6a58b51dc2b84871fcaa0df22b0d1033e
OWN_DEV_BRANCH dev/agl-v4.2-workbuddy-adapters
OWN_SOURCE factory/agl/{storage,poll,execution,cli}.py, factory/tests/adapters/, build/test/docs
NO TOUCH main、既有盲测分支、Codex 专属代码路径、真正定时任务配置。

## 必须查微软源码的工程模式
mini-router/src/state.ts（event_id 去重/ACK/retry）、src/board_client.ts（增量和 UNKNOWN）、src/group_messages.ts（积压）、board-service/main.py（投影与 cursor）、prompts/{kickoff,idle,deadline-45m,deadline-5m}.txt。只迁移适用于 Python/GitHub cron 的思路，禁止虚构可以直通 ChatGPT schedule 的 ACP 事件通知。

## M02 GitHub Adapter
使用可用的 GitHub API/CLI/SDK，只在隔离 dev 分支下提交独立事件/结果、读回 commit/blob/hash。创建与更新必须区分，CAS 冲突须重读并判断重复还是冲突；重试必须带原 event_id/operation_id。敏感凭据不进仓库日志。附真实读写探针成功/失败矩阵。

## M06 Dynamic Poll Adapter
一个定时工位对应一个 active agent id，每轮从最新状态冷启动；生成 N=2/3/4/5 的建议错峰窗口（N=2→30m，3→20m，4→15m，5→12m）。启停 Agent 只需改 JSON 配置+用户批准的调度器登记，不允许把启用数硬编码成5。本人旧任务仍有效先续，否则按 READY 选单；无租约时 fail-closed。打印计划时间与真实执行时间独立字段。

## M08 Executor Bridge
把代码测试设计为 GitHub TEST_REQUEST + authorized runner + TEST_RESULT/TEST_ACK。优先实现本环境内可实际验证的 shell/Python 假数据测试，随后评估 WorkBuddy 云端运行实例/ChatGPT Webhook 的真实调用能力。若没连接则产出 BLOCKED_EXECUTOR，不能宣称 webhook 跑通。严禁新建付费 API、无批准部署对外服务。

## M10 CLI/CI
提供一条 CLI 完成 local/isolated Git test；命令包括 validate-config、plan-schedules、dry-run-poll、submit-event、reconcile、rebuild-board、audit、run-sample-test。命令默认 read-only 或 dry-run，写入必须显式 --apply --repo --branch --project 并通过白名单检查。CI 测试不需要启动用户本机电脑。

## 要求交付
源码、依赖锁、pytest、集成测试真实输出、操作手册、权限/网络探针、测试结果文件、每阶段 Git commit/PR 链接、尚未连接的能力清单。先两 Agent 自循环实验成功再扩到 N=5，不要在未经实际验证时报告上线。完整读取 tests/ACCEPTANCE_MATRIX.md。

## 严格分工
Codex 主责 M01/M03/M04/M05/M07/M09；你主责 M02/M06/M08/M10。不要重复实现 Controller。两个开发分支由单一集成者审计与合并，不修改生产 main。无法真实提交远程仓库时保存 patch 与日志，标 NOT_PUSHED，不伪造 Git 成功。