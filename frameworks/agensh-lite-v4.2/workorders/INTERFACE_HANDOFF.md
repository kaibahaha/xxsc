# R01｜Codex 与 WorkBuddy 的集成接口冻结门槛

1. 统一 Python 3.11+ 包根 factory/agl/。建议只引入最必要第三方库；把缺失工具/权限显式报告为 UNKNOWN 或 BLOCKED。
2. core 与 adapters 共享协议：AgentRegistry / Config、TaskSpec、Event(UEM)、ClaimProposal、LeaseGrant、StateTransition、Handoff、Ack、ArtifactEvidence，至少有 schema_version/task_id/agent_id/provider_id/run_id/spec_hash/attempt_id/fencing_epoch/commit_sha/evidence_refs（按类型可空）。Codex 负责冻结 schema 和类型；WorkBuddy 不要独立发明第二套互斥定义。
3. 跨平台 provider 的统一操作接口：probe/read/publish/reread/observe_schedule/health；按真实工具能力逐项返回 SUPPORTED/UNSUPPORTED/UNKNOWN/BLOCKED。Workbench/WorkBuddy 无真实 webhook 时只能产生 Git mailbox/测试请求，不编造自动触发。
4. Git Repository 接口：read_ref、read_file、write_immutable(path,content,idempotency_key)、readback(receipt)、cas_publish_projection。返回精确 repo/ref/path/blob_sha/commit_sha/hash/error_code。非确认写入按 UNKNOWN_WRITE 后只读 reconcile。
5. Controller 的 grantLease 只在经过原子事务或严格可证明 CAS 排他时返回 GRANTED；只有软 CLAIM 时返回 CLAIM_PROPOSED，不执行共享写入或 QA 升级。AUTH 权限校验不能仅靠字符串 agent_id。
6. 测试与模拟输入均可不依赖云端网络；真实 Git probe、shell pytest、GitHub Action 探针需独立记录。关键测试：100 并发抢租、失效 epoch、事件重放、ACK 丢失、N=2/3/5/6/10/20、provider 离线、Git API 错误与权限隔离。
7. 契约版本兼容：Codex 在自己的 dev 分支交付 contracts、schema、README；WorkBuddy 在自己的 dev 分支以本文件和文档已有合同作为首轮稳定接口，在 STUBS.md 标注其等待 Codex 冻结的名称/类型。正式跨分支集成待 PR 评审，禁止预先覆盖彼此代码。
8. 所有 deliverables 中应包含设计选择、接口差异与兼容性矩阵；不能以“无法合并”完全代替交付本职模块。
