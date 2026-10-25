# R01 架构决定

1. **本地证明模型选 SQLite，权威边界写入回执。** `BEGIN IMMEDIATE` 内回放账本、校验权限/版本/依赖、创建 lease 与 epoch，再把变化和结果一起提交。WAL + synchronous=FULL；每次请求独立连接。只有 commit 后才返回 GRANTED，回执明确 `LOCAL_SQLITE_ONLY`。生产 backend 未交付。
2. **单一追加账本，不引入第二套可分叉权威表。** 记录含 seq、command_id、请求 hash、受鉴别身份、时间、domain changes、结果、previous_hash、record_hash。UPDATE/DELETE trigger 拒绝修改历史。投影由纯 reducer 重建；拒绝的已鉴别请求也有审计。根权限或整库替换不在本地 trigger 的防护边界内；恢复必须用受信 Git 回执固定 head hash。
3. **请求幂等与业务事件去重分开。** `(authenticated_agent, command_id)` 固定请求和原始结果；内容变化拒绝 COMMAND_ID_COLLISION。事件 event_id 对全 payload 比较，内容冲突不覆盖。被拒绝请求已终结，修正后用新 command_id；不确定写入先 reconcile 原 ID。历史 lease/renew 回执再次返回前检查当前 epoch、期限、Board 和时钟。
4. **过期和退场安全收敛。** 准入/能力/读写路径/WIP 检查在同一事务内。到期或 DRAINING/OFFLINE 使 lease 失效、epoch/version 增加、候选回到 READY，保留全部事件和交接。旧 attempt 只能留下历史，不得晋升业务状态。心跳不改变 epoch，失效后不可复活。
5. **Board UNKNOWN 默认阻止权威推进。** 每个新 Controller 实例先只读对账；本地 digest CAS 通过才允许 claim/renew/transition。显式未知、存储错误关闭实例 fence；不把空队列和读取失败混同。远端 Git projection CAS/回读仍由 WorkBuddy 实现，本地 CAS 不能代替它。
6. **ACK 不等于 DONE。** 处理证据先持久化；缺 ACK 时只补 ACK。按目标独立去重，按 Agent/source 维护连续水位，ACK 不得跳过前面的未确认事件；因果前置事件未 ACK 时拒绝后续 ACK。外部副作用必须在目标系统按相同 key 去重。本地日志和远端 HTTP 不能靠本实现组成分布式原子事务。
7. **身份由可替换受信 Authenticator 验证。** 服务接受 credential，经验证得到 ProviderSession，再绑定 agent/provider/account/principal。客户端 JSON 不可冒充 Session。测试使用假凭证映射；生产 OAuth/JWT/GitHub App 认证及 probe 核验是集成阻断。诊断 snapshot/backend 接口仅供受信进程，不能直接暴露给客户端。
8. **验收门禁不解析自然语言判断通过。** SUBMITTED 必须绑定 commit；QA 必须有同 task/spec/commit 的真实运行结构证据、exit=0、独立身份组和受信 verifier 对原日志核验。REVIEW/INTEGRATE/ACCEPT 分权限；ACK 和知识不会自动推进。匹配 FAIL 阻止后续验收，不影响其他 commit。FAIL 撤回/同提交重验策略和身份重新准入需后续显式审查。
9. **跨会话采用可检索交接，不依赖浏览器会话。** HANDOFF 保存 task/spec/attempt/epoch/commit/decision/open issues/next action/evidence；恢复时对当前 lease 检查，过期只读重新认领。热层裁剪不删除冷历史。
10. **云端选型与部署门槛。** 最小路径是受保护的单主轻服务+持久本地卷（同一主机，禁止把 SQLite 放 Git/NFS）；生产更推荐事务 DB（如 Postgres 行锁+唯一约束），事务内持久 lease/epoch/journal/outbox。GitHub Actions concurrency 仅能串行工作流，不能单独证明跨工作流/重试/Runner 消失时的持久 fencing，且取消不能等同撤销。外部 DB 和云端 Runner 均未配置/启动/验证，因此 BLOCKED_ATOMIC_LEASE。云端适配必须复用本套契约和不变量，而不是另造第二状态机。

成本边界：当前每个事务完整回放历史，单请求 O(history)，长运行总成本可能为 O(n²)；无并发读投影优化、快照截断或云吞吐承诺。N=20 是功能验收规模，不是无限容量实测。真实重启后时钟/持久卷/备份与 Git 出站日志都必须再验。控制器不执行模型推理、不启动任何调度器。
