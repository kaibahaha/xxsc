# V4.2 多 Provider Agent 注册与扩容规范

## 定义
全局池 N 是 enable 的 Agent 总数，N>=2，不设协议/源码级最大人数。ChatGPT、WorkBuddy、Codex 或其他 Provider 只要通过能力与权限探针，都可以成为全局任务池的参与者。所谓不设固定上限，并不意味着跳过 GitHub API 限流、Controller 吞吐压测、各平台配额、付费预算或凭据隔离。

## AgentRegistration
每个成员：agent_id（全局唯一）、provider_id、agent_kind（scheduled / triggered / on_demand）、enabled、lifecycle_state、capabilities、preferred_roles、allowed_reads、allowed_writes、scheduler_type、schedule_id、cadence、timezone、transport_state、permission_state、max_inflight。禁止把固定 A/B/C/D/E 分支逻辑塞进 Controller。

## ProviderAdapter（插件接口，尚待代码实现）
probe()：验证实际工具与读写权限。
get_schedule_status()：核验真实 schedule_id、计划/实际触发和状态；无开放接口返回 UNSUPPORTED。
get_capabilities()：只登记已核验能力，UNKNOWN 不升级成可执行。
poll_tasks()、submit_event()、ack()：统一 TASK/UEM/HANDOFF/ACK，保持跨 Provider 的 task_id/spec_hash/attempt_id/fencing_epoch。
create_or_update_schedule()：仅在真实有此 API 且获得用户明确授权时可执行，不能假定各平台都支持。

## 权限与配额
- ChatGPT 的计划任务槽数只计算实际占用 ChatGPT 调度资源的任务。WorkBuddy、Codex 的各自原生定时器使用其各自核实的预算，不占 ChatGPT 槽位（具体集成若有共享限制，以实测为准）。
- 执行 Agent、按需触发 Agent、仅审查 Agent 可以共用看板，但不能把没有原生计划任务的成员计算成真实“每小时已唤醒”。
- 未通过调度和权限探针的成员处于 CANDIDATE/PROBING，禁止声称已经进入 ACTIVE 生产执行。
- Agent 停用先进入 DRAINING，Controller 停止发新租约并清理旧 attempt/fencing，保留 HANDOFF、RUN、Event/ACK 历史供其他已验证的 Agent 继续。

## 真实接力验收
ChatGPT A 的真实定时唤醒提交 TASK 分析并回读 → WorkBuddy 自己的真实定时/执行入口读取 TASK 与事件 → 获合法租约后运行真实测试 → 写 TEST_RESULT 原始证据 → Controller 验收，Codex 可作为另一个已接通的开发或审查成员。每步要有 commit SHA/时间/回执；没有连通就记 BLOCKED_PROVIDER，不得声称闭环成功。
