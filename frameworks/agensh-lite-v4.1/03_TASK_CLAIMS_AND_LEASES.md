# 03｜自主任务认领、冲突消解与正式租约

## 微软来源
`prompts/agents.txt` 要求 CLAIM、碰撞通知和合并前同步；`board-service/shared_lessons.py` 默认 CLAIM 有效 3600 秒，过期从 live view 隐藏但历史保留。这是**软协作声明**，不是数据库排他锁。

## 本系统两层认领
- `CLAIM_PROPOSED`：Agent 看到了 READY、依赖满足的任务后创建不可变认领提案。任何人可能同时提出相同 task。提案不能授予写共享代码的权利。
- `LEASE_GRANTED`：Controller 事务确认 `task_id + expected_version + owner + attempt_id + expires_at + fencing_epoch`；冲突时仅一个生效。**如果没有在线 Controller 原子授租，所有 CLAIM 只能在预分区的只读/独立 outbox 范围内执行。**
- `LEASE_RENEWED`：同一 epoch 的合法心跳才能续期；`LEASE_REVOKED`/`EXPIRED` 之后迟到结果标 `LATE_STALE_ATTEMPT`，只能保存供审计，不可推进权威状态。

## 选择任务算法（每次定时唤醒）
先检验自己尚未结束的旧任务 lease；若有效，优先继续，不因跨过其他 Agent 的多轮而丢失状态。无有效 lease 时读取最新 BOARD 投影和未消费事件，按 `READY`、依赖满足、权限、最新版本、WIP 限额过滤；排序优先 blocked dependency、priority、age，避免一直抢最新任务。候选冲突则写 COLLISION 并选择另一个。没有合适工作写 `NO_ELIGIBLE_TASK`，不是失败。

## 五 Agent 错峰不是排他锁
A :00、B :12、C :24、D :36、E :48 为每小时五条均匀计划触发，**并不能保证实例恰好启动或在12分钟内结束**；若 A 的单次执行持续20分钟，与 B 的任务存在重叠。冲突由权威租约和专属写目录解决，不依赖排班。若只有四条 Agent + 一条 Work 占用账号槽，不能凭文档把 Work 改造成 E。

## 多层回退
租约服务缺失→转 L0 静态领域分区，仅做研究/审核并提交提案；Agent 无仓库写权限→本地/Library 暂存并标 NOT_GIT_DELIVERED；Git 冲突→只读复核后重提合法候选；明确无权限→熔断该写通路，不能绕平台安全。
