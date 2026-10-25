# 验收及故障注入清单（全是待执行，不是已测试）

| ID | 注入条件 | 应看到的结果 | 真实执行状态 |
|---|---|---|---|
| TC-01 | A/B 同时对同一 TASK 提 CLAIM | 只有 Controller 授权的一份 LEASE_GRANTED 有效 | NOT_TESTED |
| TC-02 | A 已消费事件 B 仍未消费 | B 不受 A 的 cursor 影响 | NOT_TESTED |
| TC-03 | Board 读失败 | BOARD_UNKNOWN，不能抢新单 | NOT_TESTED |
| TC-04 | Git create 成功但 ACK 超时 | 只读发现已有源并补 ACK，不另生新事件 | NOT_TESTED |
| TC-05 | FAIL 后已验收候选 | 定位同 SHA/Spec 复核，不全局禁用 | NOT_TESTED |
| TC-06 | 前一个 Agent 迟到交付 | 旧 epoch 拒绝状态晋升 | NOT_TESTED |
| TC-07 | 30+ 历史消息/长上下文 | Hot 提要+Cold 索引，无丢失原记录 | NOT_TESTED |
| TC-08 | C 产出代码但没运行 | CODE_DRAFT / TEST_REQUESTED，而非 QA_GREEN | NOT_TESTED |
| TC-09 | Work 抢节拍争议 | 由源就绪、原生尝试、grace、Work 时间分开核对 | NOT_TESTED |
| TC-10 | 五任务 :00/:12/:24/:36/:48 | 记录真实触发时间与并发区间，不能假定无重叠 | NOT_TESTED |
| TC-11 | 同一 evidence 由同一模型转述三次 | 不认作三份独立 QA | NOT_TESTED |
| TC-12 | 真实本机 API 关机 | BLOCKED_EXECUTOR，不伪造 webhook 成功 | NOT_TESTED |
