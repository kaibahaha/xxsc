# 给 WorkBuddy / R02 Integrator 的交接

> P1 Review 后续已修复：请优先读取 REVIEW_FIX_R01_REPORT.md 与 contracts/README.md 的当前阶段授权/版本化注册表约定；本文件其余内容保留首轮交付记录。

PR：https://github.com/kaibahaha/xxsc/pull/1 （Draft，勿合并）。目标分支 `exp/agensh-lite-v4.2-controller-mvp-20261025`。源码/测试/最终合同提交 `001a7f2db4ea9d1ef3c6e164456d900a0cb7d41c`；交付证据另有后续提交，最终 head 由 PR 回读取得。

1. 先读取 factory/agl/contracts/README.md、core.schema.json 和 INTERFACES.md，核对 SOURCE_ARTIFACTS.json 的精确哈希。沿用 AgentRegistration/ProviderSession/TaskSpec/Event/UEM/Ack/ClaimProposal/LeaseGrant/StateTransition/TaskTransition/MemoryNote/Handoff/ArtifactEvidence；Config 在 config.py、AgentRegistry 在 registry.py。
2. M02 接 GitRepository Protocol：不可变写/readback/真实 blob+commit+hash、UNKNOWN_WRITE 只读对账、projection CAS。Core `reconcile_board` 只是本地 CAS，只有真实 Git 读写回读确认后才由受信 admin 调用。不得把本地 GRANTED 当跨云执行授权。
3. 接入受信认证/probe：credential -> 已核验 Session，provider/account/principal 均绑定；ADMITTED_ACTIVE 所引用 probe 的真实性必须由集成服务核验；不要开放客户端直接构造 Session/设置准入。按路径在实际 Git 接口强制读写范围。
4. M08 接证据 verifier 和外部 Runner，校验 stdout/stderr 原字节、command、exit、environment、task/spec/commit；QA 身份组独立于作者。没有 bridge 继续 BLOCKED_EXECUTOR，ACK 不触发 DONE。
5. 事件目标处理以 `digest([event_id,agent_id])` 为 sink 幂等键。副作用目标先证明处理结果，再 record_processing；丢 ACK 重启看 pending_deliveries 的 ACK_ONLY，补 ACK，不重跑外部副作用。源事件 ID/hash 冲突不可覆盖。先发布因果前置事件。
6. 持久日志通过 backend.records() 导出不可变 JSON；验证 Git 回执的 journal head hash 后用 restore(new_empty_path,records,expected_head_hash=...) 冷恢复，再 Board 对账。SQLite/WAL/SHM 不入仓库，也不由多个主机共享。
7. R02 先合并到独立集成分支，跑核心 90 项及 Adapter 的真实隔离 Git 测试、100-way 争租、旧 epoch、API 失联、权限拒绝、重启和跨目标 ACK；再真实双 Agent shadow，后续按门槛进入 24h。没有本单授权的调度/生产部署变更不要启动。
8. 独立 QA/Integrator 审查 PR 最终 head、MANIFEST.sha256、TEST_RESULTS.txt、pytest-results.xml 和 BLOCKERS.md。先完成合同差异矩阵，确认同一事务模型，不引入另一个互斥状态机。

可复现：仓库根 `python -m pip install pytest jsonschema`；`PYTHONDONTWRITEBYTECODE=1 python -m pytest factory/tests/core -v -ra`；`PYTHONDONTWRITEBYTECODE=1 python -m factory.agl.contracts.demo`。本单未编辑 WorkBuddy storage/adapters/poll/execution/cli、其 tests 或 deliveries。
