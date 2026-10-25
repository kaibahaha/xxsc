# 08｜故障注入、恢复、事故判因

| 场景 | 正确动作 | 禁止行为 |
|---|---|---|
| Git/Board 读取失败 | 标 BOARD_UNKNOWN；读取自己的有效 HANDOFF；不抢新共享任务 | 把未知当空板、覆盖 BOARD |
| 两 Agent 同时 CLAIM | 写 CLAIM_CONFLICT，Controller 按 epoch 原子授租；输者改选其他任务 | 两者都直接更改同个文件 |
| 任务已被别人完成 | 核验同 `task_id/spec_hash/commit` 与验收状态，放弃旧执行 | 按计划时间重做一遍 |
| Git 写后调用超时 | 对同分支/同路径只读核对 hash+event，确认后补 ACK | 未核对即二次创建同名事件 |
| event ACK 丢失 | `(event_id,agent)` 去重恢复，记录 UNKNOWN/RECOVERED | 当作新任务重复执行 |
| 旧 worker 迟到 | fencing_epoch 不符→LATE_STALE_ATTEMPT | 覆盖最新正常成果 |
| 测试失败/FAIL | 附日志及失败输入；只使同版本候选复核或失效 | 宣布全局永久失效，或者隐藏失败 |
| Work 抢节拍争议 | 按 source_ready/native_attempt/grace/relay 时间作逐笔分析 | 以“Work 最终提交”推断原 worker 没尝试 |
| 定时任务未运行 | 用真实 run 与预期 schedule 差集记录 MISSED_TRIGGER | 仅凭任务 enabled 认定成功运行 |
| 安全权限拒绝 | 原路径熔断；保留源和只读审计；等待授权 | 更换端点、身份或工具绕过检查 |
| Context 太大 | HOT/WARM/COLD 分层 + cold 索引；保留安全 P0 | 直接截断权限约束/测试证据 |
| 设备关机且本地 bridge 不可达 | BLOCKED_EXECUTOR；完成云端许可的研究/代码草稿 | 声称云端已经调通本地 WorkBuddy |

## 七类可计量指标
唤醒真成功率、唯一有效任务交付率、双端 readback 验证率、CLAIM 撞车率、重试导致重复率、从 ready 到 QA_GREEN 的 P50/P95、每次有效成果的 API/模型调用成本。至少记录三次冲突/重试注入和24小时 shadow 才考虑晋升。

## 事后恢复约束
历史 append-only，纠错新建 `CORRECTION_EVENT`，不改旧事件；单轮内只有 Controller 有权裁决最终 Task 状态；跨目标传输恢复必须逐目标独立处理。引用源事件 ID 和目标实际回执，不把聊天自报作为外部写入证明。
