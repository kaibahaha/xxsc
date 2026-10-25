# R01 冻结接口与兼容性

> P1 Review 后续已修复：请优先读取 REVIEW_FIX_R01_REPORT.md 与 contracts/README.md 的当前阶段授权/版本化注册表约定；本文件其余内容保留首轮交付记录。

权威版本：源码提交 `001a7f2db4ea9d1ef3c6e164456d900a0cb7d41c`；Python 3.11+；schema_version=2.0。首轮合同提交 `4728f69` 为早期骨架，集成请固定最终源码提交及 SOURCE_ARTIFACTS.json 中 schema hash。

所有 DTO 为 keyword-only dataclass，支持 `.to_dict()`/`.from_dict()`，拒绝未知字段及不支持的版本。结构 schema：factory/agl/contracts/core.schema.json。语义校验仍在 Python；schema 不承担身份认证。

| 类型/模块 | 集成约定 |
|---|---|
| AgentRegistration / registry.AgentRegistry | 全局 agent_id；独立 provider/account/principal/adapter/运行模式；准入/健康/能力/读写/action/max_inflight/independence_group/probe_refs。N>=2 意图池，无固定上限 |
| config.Config / load_config / validate_config | 校验 repo/ref/root/timezone、active ID、enabled 别名和独立 provider_quotas；缺失权限为空，示例 outbox 不推导写权限 |
| TaskSpec | task/spec/project/revision/dependencies/allowed_agents/capabilities/read_paths/write_paths/priority/base commit；批量 add_tasks 原子校验 DAG |
| ClaimProposal | task/agent/provider/run/spec/attempt/expected_version/ttl；只是请求，未授租不可执行共享写入 |
| LeaseGrant | 上述身份+fencing_epoch/expires_at/task_version；必须以返回 status 和 authority 判定，不靠存在某文件推断权威 |
| StateTransition / TaskTransition | 两者为同一类型别名；expected_version、attempt、epoch、spec、commit 逐项检查；gate evidence 单独核验 |
| Event / UEM | 同一类型别名；event_id/producer/provider/多 target/task/kind/summary/time/raw_ref/run/source/payload；sha256 由 core 对完整 canonical envelope 计算 |
| Ack | event/agent/provider/run/event_sha256/evidence_refs；必须匹配已持久处理证据，不能代替业务验收 |
| MemoryNote | FACT/OBSERVED/FAIL/CLAIM/PATCH_SUMMARY，summary<=160；FAIL/PATCH 绑定 commit/test；CLAIM 带 expires_at |
| Handoff | task/spec/attempt/epoch/commit/run、decision_log/open_issues/next_action/evidence_refs；允许迟到历史存档，不授权继续旧 lease |
| ArtifactEvidence | 测试 command、exit、stdout/stderr SHA256、environment、runner、task/spec/commit、原始日志 refs；受信 EvidenceVerifier 独立验证 |
| ProviderSession | 仅 Authenticator 输出；不可直接接受客户端自报身份 |

核心调用为 `Controller(backend, registry, authenticate, clock=..., evidence_verifier=...)`。写方法统一 `(credential, command_id, DTO)`；`add_tasks` 接受 specs 列表；`update_health` 接受目标 ID 和降级状态；`reconcile_board` 接受 expected_digest；`record_processing` 接受 event_id/effect_ref；`recover` 扫描到期任务。结果含 status；拒绝含 error_code；不确定写入含原 command_id/reconcile_request。

首版受信诊断/API：`snapshot()`、`board()`、`board_digest()`、`ready_tasks(credential)`；backend `records()/reconcile()/restore()`；纯函数 `rebuild()/board_projection()/audit()/build_context()/resume()/knowledge()/pending_deliveries()`。不要把含所有身份和任务的诊断快照直接暴露给外部 Agent。实际读写权限必须在 Adapter 再实施。

| 边界 | 签名/行为 |
|---|---|
| Authenticator | credential -> ProviderSession；默认无生产实现，不能把 `lambda` 信任客户端身份当真实鉴权 |
| EvidenceVerifier | ArtifactEvidence -> bool；核验不可变原日志、hash、执行命令/退出状态和 SHA；默认 None -> BLOCKED_EXECUTOR |
| ProviderAdapter Protocol | probe(principal,scope)、read(work_ref,cursor)、publish(event,idempotency_key)、reread(receipt)、observe_schedule(agent_id)、health(agent_id) |
| GitRepository Protocol | read_ref(repo,ref)、read_file(repo,ref,path)、write_immutable(path,bytes,key)、readback(receipt)、cas_publish_projection(expected_commit_sha,bytes) |

Adapter 能力返回 SUPPORTED/UNSUPPORTED/UNKNOWN/BLOCKED；Git receipt 返回 repo/ref/path/blob_sha/commit_sha/hash/error_code；UNKNOWN_WRITE 后只读对账。本实现未调用或覆盖 WorkBuddy 的 storage/adapters/poll/execution/cli。

| 原合同/版本 | 兼容处理 | 实际验证 |
|---|---|---|
| V4.1 Task | `import_v41('task',data)` 校验原 schema，仅 READY 可导入，revision 保留 | 已测示例及额外字段拒绝 |
| V4.1 Event | 显式绑定 provider；旧 payload_sha256 保留为 provenance，不冒充 canonical envelope hash | 已测 |
| V4.1 Receipt/Note | 只返回已校验旧字典；缺 recipient/test scope 不自动生成可执行 ACK/FAIL | 已测 |
| 配置 schema 1.0 | enabled/max_inflight_tasks 显式别名，其他旧调度字段不升级准入 | 已测；冻结示例重复 ID 被拒绝 |
| WorkBuddy 首版签名 | Protocol 保留 probe/read/publish/reread/observe_schedule/health、GitRepository 边界 | INTEGRATION_PENDING，未跨分支运行 |
| 真实跨云 Grant/Git projection | 本地 status 不代表公开授租；要求事务 authority + Git 回读 | BLOCKED_ATOMIC_LEASE |

标准错误包括：BOARD_UNKNOWN、VERSION_CONFLICT、LEASE_CONFLICT、LATE_STALE_ATTEMPT、AUTH_SCOPE_MISMATCH、ACTION_DENIED、PATH_DENIED、READ_PATH_DENIED、SPEC_MISMATCH、COMMAND_ID_COLLISION、EVENT_ID_COLLISION、ACK_UNVERIFIED、CAUSATION_NOT_ACKED、CLOCK_REGRESSION、BLOCKED_EXECUTOR、CANDIDATE_RECHECK_REQUIRED。CLI exit-code 映射由 WorkBuddy 冻结，core 不抢占 cli.py。
