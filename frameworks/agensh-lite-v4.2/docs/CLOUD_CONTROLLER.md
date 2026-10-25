# GitHub 云端协作机制的可实现边界

## 1. Git 是共享事实载体，不是内存消息队列
事件、任务、认领、运行、证据以不可变文件为主，唯一 Controller 投影的 BOARD.md/CURRENT.json 才允许 CAS 更新。每条写入记录 repo/ref/path、event_id、producer、commit_sha、blob_sha、readback_hash、observed_at 和 ACK。Git ref HEAD 变更必须显式处理 optimistic concurrency。

## 2. 三种运行层
L0（可立即测试）：Agent 仅写独立 outbox 和认领提议，任务分区/互斥靠静态白名单，Controller 的权威租约尚不存在。适合双 Agent 接力验证消息通路。
L1（MVP 目标）：单主 Controller 云端短事务；可以是经真实验证的 GitHub Actions 串行 Controller + Git CAS 状态发布，或持久 DB 支撑的轻服务。必须证明不会在并发/重试情况下产生两个有效 GRANT。不把 GitHub API create-file 当跨多文件事务。
L2（未来）：事件驱动通知与持续 Runner，Webhook/WS/MCP 嵌入当前 turn，仅在云端桥实际存在后启用。ChatGPT 定时 Agent 自身仅保证在下次真实唤醒读取新状态，不能承诺收到中途通知。

## 3. CLAIM 协议
Agent 先提交单独 CLAIM_PROPOSED，控制器在锁/事务下核对资格和 Task 状态，生成 LEASE_GRANTED(fencing_epoch,attempt_id,lease_deadline)。Agent 必须回读租约权威发布，再进行影响共享状态的任务。单次工作 RUN 结束时通过 HANDOFF 记录续作意图，不能默认将排他租约跨小时延长；下轮请求新授权。任何超时/迟到结果不得以旧 epoch 晋升业务状态。

## 4. 五种事实
INTENT / WRITTEN / READBACK_VERIFIED / ACK / BUSINESS_ACCEPTED 各自独立。Controller 合并 BOARD 时聚合 ACCEPTED 事件，不接受未经验证的输入；被审查/测试对象必须绑定具体 commit/spec_hash。推送成功但独立读取失败时状态 UNKNOWN_COMMIT，优先对账而非盲重试。

## 5. 没有本机电脑也能运行的条件
仅当真正存在云端运行器 + 持久状态存储 + 鉴权凭据 + 当前任务工具权限，并通过冷启动验证，才能宣称云端运行。GitHub 共享文件本身不等于云端 compute；ChatGPT 的网页计划任务不保证可以调用任意 Webhook。WorkBuddy/ Codex 的云端执行是否可桥接须独立探针。

## 6. 控制器停机
Board 读/写异常即 UNKNOWN；暂停新增高风险认领，已完成成果保存到本人 outbox；Controller 恢复从事件账本回放；连续拒绝/安全拦截立即熔断该通路。不要替用户自行开启新部署或付费运行。
## 多 Provider 扩容修订
Controller 使用统一 AgentRegistration/ProviderAdapter，而非五个 ChatGPT 固定角色。工作领取由 capability、权限、状态和 epoch 决定；调度由各平台独立管理。ChatGPT、WorkBuddy、Codex 总体 N>=2 无固定协议上限，实际容量受各平台配额、计算成本和 GitHub 限流约束；Provider 失联时安全移交已有工单而非丢历史。

## 7. 总数与平台解耦（最新需求）
Controller 通过 AgentRegistry 与标准化 Task/Lease/UEM/ACK 接口接收 2个及以上跨平台 Agent，不存在全局固定5个工位。ChatGPT/WorkBuddy/Codex 的调度预算、连接器、运行方式由各自 Adapter 负责探针和健康状态。注册与启用意图不等于运行准入。详见 docs/AGENT_ADAPTER_CONTRACT.md。
