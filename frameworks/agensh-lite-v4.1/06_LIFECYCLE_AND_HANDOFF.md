# 06｜定时 Agent 生命周期、断点恢复与任务交接

## 每次真实唤醒的 9 步
1. 生成 `RUN_ID`，记录计划时间、实际唤醒时间、Agent ID；无法取得真实时间则标 UNKNOWN。
2. 读取冻结的 POLICY、能力清单及自己上次 HANDOFF；检查是否已经截止、禁写或额度不足。
3. 从 Git 读取 Controller BOARD 投影与自己消费水位；失败标 `BOARD_UNKNOWN`，不得“空板=没有任务”。
4. 检查自己的未完成 TASK、lease 与 epoch；仍有效则继续；失效则只读保存旧证据，不得继续向权威状态提交。
5. 对新任务按可执行性选一个主任务；CLAIM 只是提议，没有 Controller 租约不做共享写冲突风险动作。
6. 读必要原件（`spec_hash`, `base_commit`）和相关 FACT/FAIL；确认前序交付真实存在。
7. 做本轮允许的设计、编码草案、评审、测试请求或文档研究；不声称无法实际执行的工具/测试能力。
8. 逐项输出不可变产物，核对 Git commit/readback，写 PATCH 或 FAIL 和 HANDOFF；如有变更请求写 REQUEST 而不是修改规范基线。
9. 最后写 RUN_REPORT（已做/未做/工具证据/下一步），记录 `next_action`、依赖、目标 agent；截止前预留回读与 ACK 时间。

## 启动消息（微软 kickoff.txt 改写）
你是 `AGENT_ID`。本轮只执行仓库冻结协议与被授权任务。优先读取最新权威状态和自己 HANDOFF，处理仍有效的原任务后再自选 READY 任务。所有行动必须留下 run_id、任务 ID、证据 URI，未知权限时只读停止。

## 空闲提醒（微软 idle.txt 改写）
当没有活跃任务时优先选择未覆盖、可独立推进的新 READY 任务。若没有满足依赖、版本和权限要求的任务，写 `NO_ELIGIBLE_TASK` 并结束本轮。**不得编造任务或自动扩大用户批准的项目范围。**

## 截止/软停止（微软 deadline 文件改写）
距离本轮可用执行时间不足指定安全余量时停止认领新任务；先回写 progress、验证已经写入的目标、记录未完问题和下一工位交接。硬截止后停止所有业务写入；仅在授权范围内完成只读核对、审计和报告。

## 无原生 session 恢复时
每个浏览器定时任务都视为“可能冷启动的新会话”。保留 `TASK_ID + CURRENT_COMMIT + SPEC_HASH + DECISION_LOG + OPEN_ISSUES + NEXT_STEP + EVIDENCE_REFS`，不能假设上轮未压缩上下文自然继承。Microsoft ACP `loadSession` 不等价于我们的网页版定时会话功能。

## 上次任务跨三轮怎么办
A 下一次唤醒先看任务 ID 的版本与最新状态，再看自己是否仍有有效 lease，不能按“第三轮/第四轮”推导任务顺序；只要前面 C/D/E 已完成并通过验证，A 可跳过旧阶段；反之旧任务若被别人合法接管，A 不能继续以过期身份写入。
