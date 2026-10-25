# V4.2 开发工作分解（WBS）与模块接口

目标：云端可运行的、可测试的 Python 3.11+ 小型控制系统。首版控制面与执行面分开，不绑定任何模型 API；GitHub/Markdown 是消息面，Controller 负责短事务，独立 Runner/QA 负责真实执行。必要时可用外部 SQLite/Postgres 单主事务后端，但单机 SQLite 不等于云端持久化。

## M01 配置与协议验证 / Codex（P0）
代码 factory/agl/config.py, schemas.py；载入 agent_pool.json；验证 N>=2、active IDs 唯一、能力、配额、allowed_paths、schema_version、绝对 repo/ref 以及安全默认值；兼容 V4.1 Task/Event/Receipt JSON Schema；非法配置明确退出无写入。
完成：N=2/3/4/5/6/10/20 配置通过；1、重复 ID、已核实的 Provider 额度超限和权限错误失败；增加 WorkBuddy/Codex 不需修改核心源码。

## M02 GitHub 存储适配 / WorkBuddy（P0/P1）
factory/agl/storage/github.py；严格 repo/branch/path 映射；读 branch SHA、提交不可变事件、Git blob+commit SHA 回读、超时后只读 reconciliation、CAS 更新专职 projection；规范事件唯一名；细分 NO_PERMISSION/NOT_FOUND/CONFLICT/UNKNOWN_WRITE。
完成：用隔离测试路径验证提交/读取/相同事件重试/不同内容冲突；不可覆盖现有分支；禁止日志泄漏 token。

## M03 统一事件账本 / Codex（P1）
factory/agl/events.py；UEM event_id、producer、target_agents、task_id、causation_id、created_at、source_ref；(event_id,target_agent) 幂等处理，ACK 不等于业务 DONE；消费指针只有在证据 ACK 被核对后推进。
完成：重复事件不会形成重复的业务确认；模拟写后丢 ACK 不重做副作用；cursor 故障可回补，所有历史不可变。

## M04 任务与租约 Controller / Codex（P2）
factory/agl/controller.py, leases.py, task_state.py；状态推进、依赖 DAG、任务优先级、公平队列、AtomicGrant(task+expected_version+owner+attempt+epoch+expires)；失效令牌拒绝；read-only fence；处理任务孤儿。
完成：100 次并发双抢仅有 1 个有效 lease；旧 epoch 不能提交；同一任务同一时刻无双主；未经审批不能推进到 DONE。Controller 短事务不负责调用模型思考。

## M05 类型化共享知识 / Codex（P1/P2）
factory/agl/memory.py；FACT、OBSERVED、FAIL、CLAIM、PATCH_SUMMARY 五类，按 task/spec/commit/test 精准影响；短摘要/详情链接；保守去重；全文历史不消失；读失败 UNKNOWN。
完成：新增 FAIL 使受影响候选待复核，而不误伤其他 commit；不把字符串“passed”当实际测试通过；热摘要容量可配置。

## M06 定时工位轮询包 / WorkBuddy（P1/P3）
factory/agl/poll.py；按跨 Provider 注册表动态生成运行指令上下文，先看旧 HANDOFF/任务状态，再领取一项 READY；按各 Provider 的原生 cadence/预算独立计算建议错峰和真实 schedule_id，生成 schedule manifest 供用户在真实平台登记；记录计划与实触发分离。
完成：任意已验证的 ACTIVE agent_id 可冷启动；N=6/10 及异构 Provider 不需修改 Python；disabled/unverified/draining Agent 不可领共享写入任务。

## M07 交接与断点恢复 / Codex（P1/P3）
factory/agl/handoff.py, context.py；每次保存 TASK_ID/SPEC_HASH/DECISION_LOG/OPEN_ISSUES/NEXT_ACTION/EVIDENCE_REFS，HOT/WARM/COLD 和逐 Agent cursor；个人上下文不依赖浏览器对话长度；上轮失败可恢复。
完成：断开/错过两个小时后仍能从 Git 证据正确续作，若 lease 已失效不能继续对旧 attempt 推进。

## M08 外部 ProviderAdapter 与测试接口 / WorkBuddy（P4）
factory/agl/execution.py；TEST_REQUEST → 外部获权 Runner → stdout/stderr、exit_code、test_summary、environment_id、commit_sha、sha256 → TEST_RESULT/ACK；WorkBuddy 和 Codex 适配器需通过可用性探针，云端 webhook/API 未实测前状态 DISCONNECTED。
完成：真实执行端对固定测试程序给出 PASS/FAIL 证据，错误 SHA 的测试不能验收；关闭云端执行器返回 BLOCKED_EXECUTOR 不伪造。

## M09 审计、事件重放与恢复 / Codex（P2/P5）
factory/agl/audit.py, replay.py；重建 BOARD、孤儿工单、投递差异、Work Relay grace、C/D 补交对账、失效时钟、读写未知、独立 run ledger。
完成：随机崩溃注入可从 Git 事件重新计算相同权威状态；Work 补交不能抹除 native 失败/未知；历史不覆盖。

## M10 CLI/CI/镜像与手册 / WorkBuddy（P0–P5）
factory/agl/cli.py、pyproject.toml、tests、README；命令 validate-config, plan-schedules, poll, claim, reconcile, rebuild-board, audit, test-runner；所有写操作须支持 --dry-run；隔离 workflow 与日志归档。
完成：pytest 单元/集成测试、类型检查、静态检查；全新云端环境在无本机电脑条件下独立执行并显示版本/Commit/回读证据。不能假设 GitHub Actions 或外部任务调度权限已开启。

## 任务顺序与边界
M01+M02 可并行；M03+M05+M07 依赖 Schema；M04 必须在 M02/M03 后集成；M06 依赖 M01/M03，M08 依赖成熟的 M04 任务授权；M09/M10 从首个切片开始开发，不能最后才补测试。
先实现端到端垂直薄切片：CONFIG→TASK→CLAIM_PROPOSED→Controller GRANT→RESULT→ACK→HANDOFF→BOARD；再扩展高级检索/执行桥。所有模块用稳定 Python 接口并在冻结 CONTRACT 后交付，禁止多套数据库/多套状态机。

## 预期代码体量（估计，不作为验收硬门槛）
约 10 模块、20–35 源码文件、20–40 测试文件、若干配置与文档。按最小可用切片实施，严禁为了凑数量造文件。

## 开发权责
Codex = 设计/状态机/并发正确性/难点实现/代码复核；WorkBuddy = GitHub 云端通路/CLI/流水线/真实隔离测试/交付。两边只在自己的开发分支写，统一 Integrator 通过 PR + QA 合并。用户批准前不改 main、不创建真实 ChatGPT 定时任务、不接入付费 API。
## V4.2 跨平台强制修订
所有 M01–M10 模块必须支持 N>=2、无固定最大人数的异构 registry 和 per-provider 调度/配额/运行权限。优先阅读 docs/MULTI_PROVIDER_AGENT_REGISTRY.md，不允许依赖固定 ChatGPT A–E 顺序或全局 60/N 排班。首次真实接入 WorkBuddy 只能在凭据、云端触发、Git 回读、QA 全部实测成功后宣布通过。
