# AGL-CODEX-CORE-R01｜Codex 手动认领开发工单

STATUS: READY_FOR_MANUAL_CLAIM
OWNER_PREFERENCE: CODEX
SCOPE: M01/M03/M04/M05/M07/M09（纯 Controller 核心及兼容 schema）
PR_TARGET: exp/agensh-lite-v4.2-controller-mvp-20261025
DEV_BRANCH: dev/agl-v4.2-codex-controller
DELIVERY_DIR: frameworks/agensh-lite-v4.2/deliveries/CODEX_CORE_R01/
CODE_ROOT: factory/agl/
CLAIM_RECEIPT: frameworks/agensh-lite-v4.2/workorders/claims/AGL-CODEX-CORE-R01/CODEX/<RUN_ID>.md

## 必读（先读再开发）
1. frameworks/agensh-lite-v4.2/README.md
2. frameworks/agensh-lite-v4.2/docs/AGENT_ADAPTER_CONTRACT.md
3. frameworks/agensh-lite-v4.2/docs/MULTI_PROVIDER_AGENT_REGISTRY.md
4. frameworks/agensh-lite-v4.2/docs/PROJECT_MODULES.md
5. frameworks/agensh-lite-v4.2/docs/CLOUD_CONTROLLER.md
6. frameworks/agensh-lite-v4.2/tests/ACCEPTANCE_MATRIX.md
7. frameworks/agensh-lite-v4.2/dispatch/CODEX_MASTER_TASK.md
8. frameworks/agensh-lite-v4.1/03_TASK_CLAIMS_AND_LEASES.md、04_UEM_EVENTS_AND_DELIVERY.md、07_QA_GATES_AND_PROVENANCE.md
9. frameworks/agensh-lite-v4.2/workorders/INTERFACE_HANDOFF.md
10. 微软 https://github.com/microsoft/Agensh 固定 commit 0468a3e6a58b51dc2b84871fcaa0df22b0d1033e 中 prompts/agents.txt、board-service/shared_lessons.py、board-service/main.py、mini-router/src/uem.ts、mini-router/src/state.ts、相关 SQL。实际源码未读到应记录 UNKNOWN_SOURCE，不要假装复制运行过。

## 施工步骤
P0：真实记录基线 HEAD、Git clone/fetch 能力、源码参考与 MIT 许可，写本工单 CLAIM_RECEIPT（仅在自己的开发分支）。
P1：先冻结 factory/agl 的 AgentRegistry / Task / UEM / Ack / Handoff / Lease / Event 合同，要求 N>=2，provider-agnostic；与 WorkBuddy 接口见 INTERFACE_HANDOFF.md。
P2：实现可运行的纯 Python M01/M03/M04/M05/M07/M09：动态配置校验、Task 状态机和 DAG、事件去重/重放、多目标 ACK、冷热记忆索引、handoff 恢复、并发 lease/fencing/过期强拒绝、Controller board projection 的确定性计算核心。
P3：优先提供“安全可证明”的原子 lease 后端（可先 SQLite 本地/测试用持久事务模型，再提供云端 deployment 要件与 GitHub Actions 单主或外部 DB 方案）；**不能把 SQLite 文件放 Git 当跨云事务数据库**。若云端后端无法证明，报告 BLOCKED_ATOMIC_LEASE，不假装 L1 已生产上线。
P4：pytest/压力测试/攻击性测试，全量 run logs、手动重放和清晰部署缺口。
P5：提交 dev 分支，创建 PR 指向工单基线分支，写后回读成果与 PR 状态。不可合并 main。

## 专属代码边界
可以创建/修改 factory/agl/{config,schemas,events,controller,leases,task_state,memory,context,handoff,audit,replay,registry}.py、factory/agl/contracts/、factory/tests/core/、本工单 claims 和 CODEX_CORE_R01 delivery。
不可编辑 factory/agl/{storage,adapters,poll,execution,cli}.py 或 WorkBuddy 对应 tests/、deliveries 及他人 docs。

## 必须实际交付（不可只写设计）
源码 + tests；deliveries/CODEX_CORE_R01/ 内至少：
REPORT.md、ARCHITECTURE_DECISIONS.md、INTERFACES.md、MICROSOFT_SOURCE_ADOPTION.md、TEST_RESULTS.txt（含真实运行命令与 exit code）、RUN_LOG.md、MANIFEST.sha256、BLOCKERS.md、NEXT_HANDOFF.md。
REPORT 汇总源码路径、接口、测试数量/结果、禁用的危险路径、实际 Git SHA、PR URL；MANIFEST 每个哈希需经执行工具计算，缺失就写 NOT_GENERATED。
最低验收：N=2/3/5/6/10/20 配置；100 并发 claim 只1有效 lease；旧 epoch 拒绝；重复事件/ACK 幂等；Controller 重放一致；Board unknown 不新领单；真实没有 Runner 时不写 QA_GREEN；pytest 退出码真实可回读。
如果任何条件无法执行，则给局部代码+明确 BLOCKED/NOT_TESTED，不得空手交漂亮报告。