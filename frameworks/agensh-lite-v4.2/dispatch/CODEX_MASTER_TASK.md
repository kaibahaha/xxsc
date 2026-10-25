# 发给 Codex｜Agensh-Lite V4.2 总架构 + Controller 代码任务

你是 Controller/协议/并发一致性技术负责人，不是本任务的调度器。请在云端可用的 Codex 开发环境完成可运行的工程改造，并保留所有终端/测试证据。

## Git 精确位置
REPO kaibahaha/xxsc
START_BASE exp/agensh-lite-v4.2-controller-mvp-20261025（先记录 HEAD 的真实 SHA）
READ_ONLY_REFERENCE frameworks/agensh-lite-v4.1/
READ_ONLY_MICROSOFT microsoft/Agensh@0468a3e6a58b51dc2b84871fcaa0df22b0d1033e
OWN_DEV_BRANCH dev/agl-v4.2-codex-controller（存在则核对后复用，禁止 force）
OWN_SOURCE factory/agl/{config,schemas,events,controller,leases,task_state,memory,context,handoff,audit,replay}.py
NO TOUCH main、既有盲测分支、其他 Agent outbox、用户既有定时任务。

## 必须先看源代码
Microsoft: prompts/agents.txt；board-service/shared_lessons.py / main.py / verifier.py / gquery.py；mini-router/src/{uem.ts,state.ts,board_client.ts,dispatcher.ts}；mini-router/sql/01-events-schema.sql。
逐文件登记：直接移植/按接口改写/只借鉴设计/明确排除。不要搬 Copilot ACP、Gitea、Mattermost、secret-service 作为 MVP 必要运行依赖。直接复制微软源代码必须保留 MIT 许可/原版权文本。

## 开发与交接
1) 冻结 Python 接口和 schema：ClaimProposal、LeaseGrant、TaskTransition、UEM、Ack、MemoryNote、Handoff、Config、AgentRegistration、ProviderAdapter、ProviderSession；写 contracts/ 和 schema compatibility tests。
2) 实现 M01/M03/M04/M05/M07/M09，配最小可运行 CLI 协议；只认 active_agent_ids 的启用成员，N>=2 运行无需源码修改。
3) 设计可实际部署的单主 Controller 实现：Git CAS + 持久事务 / GitHub Actions 方案与备用 DB 方案对比，选最小真实可验方案并明确依赖；不可用时 fail-closed L0。
4) 写重点 adversarial tests：100-way same Task CLAIM、旧 epoch 延迟、故障重放、无 Board、数据越权、ACK 丢失、多 Agent cursor、N 动态变更。
5) 提交完整源码、tests、DESIGN_DECISIONS.md、TEST_RESULTS.txt、RUN_LOG.md、MANIFEST.sha256、DEMO_STEPS.md。展示真实命令退出码；没有跑的测试写 NOT_RUN。

## 接口协作
在 coding 前先将 interfaces/contracts 与 WorkBuddy 可实现适配器签名明确写在 dev 分支；另一执行者以这份接口开发 M02/M06/M08/M10。不得同时编辑同一个文件。向集成者提交 PR，不直接合并 main。无法跨分支共享时用稳定冻结 spec SHA 和 PR 信息交接。

## 合格标准
必须满足 tests/ACCEPTANCE_MATRIX.md 所有 P0/P1/P2 项；尤其任意启用 N=2/3/4/5/6/8/12 及多 provider/6/10/20 的跨平台池；停用角色的未完任务会重新进入待接手队列（保留原审计链），无双租约、无丢事件、无假 QA。输出实测证据；遇到云端权限/额度障碍明确 STOP 而不伪造。
## 追加的强制设计要求（本节覆盖之前的五 Agent 假设）
跨 Provider AgentRegistry（ChatGPT/WorkBuddy/Codex/后续插件），总 N>=2 不设最大值；分平台调度/配额、统一 Git UEM/HANDOFF/lease/fencing/QA；核心 Controller 不能枚举固定五人，需证明 N=6/10/20 与异构故障恢复。先读 docs/MULTI_PROVIDER_AGENT_REGISTRY.md。

## 最优先：实现异构 Provider Adapter 合同
用户明确要求至少2个（含2），以后可能加入大量 WorkBuddy/Codex 或自定义 Agent。禁止将 ChatGPT 最多5个计划任务写成全局最大成员数。先冻结 registry/schema/admission/lease 的 provider-neutral 接口，测试跨平台并发 claim、N=6/8/12、掉线转交和按平台 budget 限流；必读 docs/AGENT_ADAPTER_CONTRACT.md、config/mixed_pool.example.json。
