# V4.2 最小验收矩阵（NOT_TESTED，需真实执行）

## C0 配置与调度（必须）
- C0-01 N=2、3、4、5 自动错峰分别为 [0,30]、[0,20,40]、[0,15,30,45]、[0,12,24,36,48]。
- C0-02 agent_id 可选择非连续子集 A/C/E，启用 3、预留 2；所有业务逻辑从 active_agent_ids 获取，不对数组第5项做越界引用。
- C0-03 N=1、N=6、重复 ID、off/未声明的 ID、保留名额超预算、无效时区均 fail-closed。
- C0-04 停用 B、D 时原有 HANDOFF、ACK 与历史保留；不可领取新任务，原有租约按安全流程撤销、旧结果不得晋升。
- C0-05 修改 pool N 后不改源码即可重排；实际 ChatGPT 计划任务状态必须独立探针证明，不以打印时间表当创建成功。
- C0-06 并行两个运行实例重叠时，单任务只有一份有效 lease；错峰不是锁。

## C1 Git 与事件（必须）
- C1-01 创建后用第二次 API 请求回读准确 repo/branch/path/commit/blob/content。
- C1-02 同 event_id+hash 重试不重复业务事件；同 event_id 不同 payload → COLLISION。
- C1-03 写入成功但 ACK 丢失，重启仅补 ACK 不重复投递。
- C1-04 ACK 记录 per-target agent；A 已消费不能影响 C 的 cursor。
- C1-05 Git 读板失败被标 UNKNOWN；不得当 EMPTY 接新单。
- C1-06 不写 main、其他 Agent outbox、旧盲测路径、冻结原稿。

## C2 Controller / 任务（必须）
- C2-01 双重 CLAIM 同一任务只有一个权威授租，100 个并发 claim 压测仍成立。
- C2-02 迟到旧 fencing epoch 不能更新当前任务状态；新 epoch 可以正常完成。
- C2-03 依赖未满足时不领取下游任务，历史错过轮次不造成业务状态跳过。
- C2-04 非法/未知任务状态变更拒绝并留审计。
- C2-05 重放事件与投影恢复一致，漏单/孤儿任务有证据链。
- C2-06 CLAIM_PROPOSED 不等于 LEASE_GRANTED；没有 Controller 严格退到 L0。

## C3 交接/验收（必须）
- C3-01 A 出成果，C 在真实后续独立定时唤醒读取并继续，数据不靠 A 对话历史。
- C3-02 保存 Task/Spec SHA/HANDOFF，新模型错过两次唤醒后可合法续作或被安全接手。
- C3-03 假称测试 passed 的 Markdown 不得升为 QA_GREEN；需真实 Runner + exit code + commit SHA。
- C3-04 禁止 Work Relay 在 native grace 尚未到期或 source 未验证时抢节拍。
- C3-05 测试执行器不存在→BLOCKED_EXECUTOR，而非 PASS。

## C4 运行可靠性（上线前）
- C4-01 2 Agent shadow 真实往返 Git + ACK，带各自真实 run_id/commit。
- C4-02 3 Agent shadow、4 Agent shadow、5 Agent shadow 配置切换与退场再加入。
- C4-03 断开 Controller / Board / Git / Executor 故障注入，状态 fail-closed。
- C4-04 24 小时影子真实计划轮次 vs 实际唤醒/结果/延迟/故障审计。
- C4-05 任何成功均有 Git 链接+commit SHA+hash/测试原始日志；缺一项不报告为通过。

阶段签发：P0/P1/P2 全绿且 CI 实验通过，再由用户授权调度器变更。本文是验收计划，不是已通过证据。