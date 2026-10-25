# V4.2 最小验收矩阵（NOT_TESTED，需真实执行）

## C0 跨平台开放式成员配置（必须）
- C0-01 总 N=2/3/4/5/6/10/20 均被配置/业务逻辑接受，N=1 拒绝；不得硬编码固定五个 Agent。
- C0-02 3 ChatGPT A/C/E + 7 WorkBuddy 的逻辑混合池支持 10 人；ChatGPT 自身预留两个平台计划任务槽，WorkBuddy 预算独立（前提为真实平台可用）。
- C0-03 Agent ID 重复、失效权限、已核实平台预算超限、无效时区必须 fail-closed；UNKNOWN 额度不得冒充 unlimited。
- C0-04 ChatGPT 本平台每小时 K=2/3/4/5/6 建议错峰为 [0,30]/[0,20,40]/[0,15,30,45]/[0,12,24,36,48]/[0,10,20,30,40,50]；不同 Provider 不能对总 N 简单套用 60/N。
- C0-05 禁用或退出任一 ChatGPT/WorkBuddy/Codex Agent 保留 HANDOFF、ACK 和历史，吊销旧租约，新 Agent 只有在能力匹配且授权时接手。
- C0-06 动态扩容只改配置/登记，不改核心源码；实际真实 schedule_id、fired_at、Git 写后回读独立验证。
- C0-07 未验证 Provider 返回 PROBE_PENDING/BLOCKED_PROVIDER，而非宣称跨平台已连通。
- C0-08 多 Provider 并行抢同一 Task，Controller 只授出一个有效 lease。
- C0-09 压测 N=20 时不宣称无限吞吐，记录 API/并发/成本阈值。

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
- C4-02 3/4/5/6/10 Agent shadow（含跨 Provider） 配置切换与退场再加入。
- C4-03 断开 Controller / Board / Git / Executor 故障注入，状态 fail-closed。
- C4-04 24 小时按 Provider 统计影子真实计划轮次 vs 实际唤醒/结果/延迟/故障审计。
- C4-05 任何成功均有 Git 链接+commit SHA+hash/测试原始日志；缺一项不报告为通过。

阶段签发：P0/P1/P2 全绿且 CI 实验通过，再由用户授权调度器变更。本文是验收计划，不是已通过证据。