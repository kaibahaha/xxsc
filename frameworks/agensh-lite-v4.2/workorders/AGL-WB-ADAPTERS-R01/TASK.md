# AGL-WB-ADAPTERS-R01｜WorkBuddy 手动认领开发工单

STATUS: READY_FOR_MANUAL_CLAIM
OWNER_PREFERENCE: WORKBUDDY
SCOPE: M02/M06/M08/M10（GitHub Adapter、跨 provider 引导、CLI/CI、可真实测试的接力）
PR_TARGET: exp/agensh-lite-v4.2-controller-mvp-20261025
DEV_BRANCH: dev/agl-v4.2-workbuddy-adapters
DELIVERY_DIR: frameworks/agensh-lite-v4.2/deliveries/WORKBUDDY_ADAPTERS_R01/
CODE_ROOT: factory/agl/
CLAIM_RECEIPT: frameworks/agensh-lite-v4.2/workorders/claims/AGL-WB-ADAPTERS-R01/WORKBUDDY/<RUN_ID>.md

## 必读
1. frameworks/agensh-lite-v4.2/README.md
2. frameworks/agensh-lite-v4.2/docs/AGENT_ADAPTER_CONTRACT.md
3. frameworks/agensh-lite-v4.2/docs/MULTI_PROVIDER_AGENT_REGISTRY.md
4. frameworks/agensh-lite-v4.2/docs/POOL_AND_SCHEDULING.md
5. frameworks/agensh-lite-v4.2/docs/PROJECT_MODULES.md
6. frameworks/agensh-lite-v4.2/tests/ACCEPTANCE_MATRIX.md
7. frameworks/agensh-lite-v4.2/dispatch/WORKBUDDY_BUILD_TASK.md
8. frameworks/agensh-lite-v4.1/02_GITHUB_LAYOUT_AND_WRITES.md、04_UEM_EVENTS_AND_DELIVERY.md、06_LIFECYCLE_AND_HANDOFF.md、07_QA_GATES_AND_PROVENANCE.md
9. frameworks/agensh-lite-v4.2/workorders/INTERFACE_HANDOFF.md
10. Microsoft microsoft/Agensh@0468a3e6a58b51dc2b84871fcaa0df22b0d1033e 中 mini-router/src/{state.ts,board_client.ts,group_messages.ts}、board-service/main.py、prompts/{kickoff,idle}.txt。

## 施工步骤
P0：核对 branch HEAD、Git read/write/readback 权限和云端执行环境；在自己的 dev 分支留下 CLAIM_RECEIPT。未连接记录 BLOCKED_PROVIDER。
P1：实现可运行 M02 GitHub Storage Adapter，Git API 只读、单事件不可变写入、分支限定、冲突后回读/幂等 reconcile、Commit/Blob SHA 验证、token 遮蔽与 Git 错误分类。
P2：实现 M06 Dynamic Poll + AgentAdapter：不同 provider/account_scope/trigger_type/cadence/quota；ChatGPT 每小时 K 工位错峰，不把跨平台 N 套入 60/N；固定权限目录、健康/准入 probe；不能注册未实际可用的 Webhook。
P3：M08 测试请求/Runner 结果协议、环境限制、Git证据回写与测试日志；优先本环境可执行的 Python/shell Runner 与离线 mock，其他云桥有真实授权再接。每个平台探针逐项说明。
P4：M10 CLI 与基本 CI（默认 --dry-run）；支持 validate-config、plan-schedules、poll、submit-event、reconcile、rebuild-board、audit、run-sample-test；CLI 对尚未实现的 Codex 核心功能输出清晰 PENDING_CORE 而不是伪造可用。
P5：真机/云端隔离 branch 的 Git roundtrip 探针至少一次（若权限允许）+ pytest；提交到本 dev 分支并创建 PR 指向工单基线。不能改 main。

## 专属代码边界
可以创建/修改 factory/agl/{storage/,adapters/,poll.py,execution.py,cli.py}、factory/tests/adapters/、factory/tests/integration/、打包依赖和 CLI/CI 相关入口（避免覆盖他人合同）、本工单 claims 和 WORKBUDDY_ADAPTERS_R01 delivery。
不得修改 Codex 的 config/events/controller/leases/registry 等核心源码，不能以修适配器为由自行覆盖 Controller。

## 必交文件
源码 + tests；deliveries/WORKBUDDY_ADAPTERS_R01/ 至少：
REPORT.md、PROVIDER_CAPABILITY_MATRIX.md、GITHUB_ROUNDTRIP_EVIDENCE.md、INTEGRATION_TEST_RESULTS.txt、RUN_LOG.md、MANIFEST.sha256、BLOCKERS.md、NEXT_HANDOFF.md。
PROVIDER_CAPABILITY_MATRIX 按 ChatGPT/WorkBuddy/Codex 的 read/write/reread/trigger/execute 列出 VERIFIED/UNSUPPORTED/UNKNOWN，不得因 GPT 连接器存在就推断 WorkBuddy 也有此权限。
GITHUB_ROUNDTRIP_EVIDENCE 记录真实 repo/ref/path/commit_sha/blob_sha/第二次回读 hash/time；如果隔离测试未成功，标 NOT_VERIFIED 而非 PASS。
验收：Git 三方比对、重复 event id 幂等与不同内容冲突；配置 N=2/3/5/6/10/20；ChatGPT K 的时槽计算；provider 容量独立；未准入者 fail closed；不允许假 QA、越权写和无批准 schedule 修改。
如果 Codex 合同尚未在 Git 交付，可按 INTERFACE_HANDOFF 规范建 mock/stub、注明待合并项，独立适配器与 GitHub 测试仍应先完成。