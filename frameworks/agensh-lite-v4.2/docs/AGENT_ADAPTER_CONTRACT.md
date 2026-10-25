# V4.2 跨平台 AgentRegistry / Adapter 合同

目标：ChatGPT、WorkBuddy、Codex、ChatGPT Work 以及将来新的平台的 Agent，至少2个且系统总数无固定上限，共享 GitHub Task、Board、Event、Claim、Lease、Handoff、Ack 和证据记录。

## 统一身份
AgentRecord 必有 agent_id、provider_id、account_scope、adapter_id、runtime_mode、capabilities、allowed_reads、allowed_writes、desired_enabled、admission_status、health、max_inflight 和经过验证的鉴权范围。Agent ID 不固定 A-E。Task 匹配依能力与范围，不以 provider 名称固定分工。

## 统一运行接口（设计合同，非已运行代码）
\`\`\`python
class AgentAdapter(Protocol):
    def probe(self, principal, scope) -> CapabilityProbe: ...
    def read(self, work_ref, cursor) -> ReadResult: ...
    def publish(self, immutable_event, idempotency_key) -> WriteReceipt: ...
    def reread(self, receipt) -> VerifiedReadback: ...
    def observe_schedule(self, agent_id) -> ScheduleObservation: ...
    def health(self, agent_id) -> HealthObservation: ...
\`\`\`
调用真实平台工具需确认权限。某平台只有手动触发或 Git 文件读写，也可实现其支持的接口；不支持就明确 UNSUPPORTED/UNKNOWN，不编造云端 webhook 或可自动创建任务的 API。新增 provider 添加 Adapter，不改 Controller 核心。

## Admission 状态机
REGISTERED→DESIRED_ENABLED→PROBING→ADMITTED_ACTIVE；不可用→UNAVAILABLE/DRAINING。最低准入：认证主体、GitHub repo/ref 实际可读、专属 outbox 写入和 SHA/hash 回读、Run_ID 与真实触发/执行证据、权限白名单；缺失能力仅可作为草案或 MOCK_ACTIVE 测试角色。配置 active_agent_ids 是**计划启用意图**，不代表已上线。

## 跨平台调度与容量
ProviderScheduler 独立保存 trigger_type、interval_minutes、timezone、schedule_id、due/fired/completed、quota 与账户作用域。ChatGPT 计划任务示例总额5、预留2，只允许3个此类 ChatGPT 工位，但不限制增加其他 WorkBuddy/Codex Agent。WorkBuddy 独立定时节拍，Codex 有无定时运行必须真实测量。定时任务创建/停用需要用户授权，不得凭配置宣称已生效。

## 安全与事件
所有 provider 使用 V4.1 通用 UEM/Claim/Lease/Handoff/ACK/SHA 证据，per-target (event_id, agent_id) 幂等，per-agent cursor。CLAIM 不等于排他；Controller 原子 grant + fencing。WorkBuddy DEV、WorkBuddy QA、WorkBuddy Runner 是不同权限身份；ChatGPT Work Relay 不自动具有开发/验收权限。旧 epoch 产物仅留档，不推进状态。禁止外部 Agent 绕过平台安全。

## 配置与验收
agent_pool.example.json 启用意图3 ChatGPT（预留2个示例 ChatGPT 槽），同时登记2个 WorkBuddy 和1个 Codex（禁用待探针）。mixed_pool.example.json 计划启用全部6个，**所有 admission=PENDING_PROBE，非真实运行证据**。验收 N=2/3/5/6/8/12 的配置、多平台并发、独立预算和断线接力。
