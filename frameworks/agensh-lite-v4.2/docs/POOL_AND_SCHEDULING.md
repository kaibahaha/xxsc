# V4.2 跨平台 Agent 池与独立调度（N>=2，无全局固定最大值）

## 原则
- 至少2个（包含2个）已准入的 Agent。系统总数由 AgentRegistry 动态决定，不固定 A/B/C/D/E；支持 2、3、5、6、8、12、几十个。上限来自实际各平台配额、成本、GitHub 限流和控制器吞吐，而非源码写死。
- 一个 agent_id 对应明确 provider_id、account_scope、capabilities、adapter_id、runtime_mode、身份凭证范围、allowed_paths、desired_enabled、admission_status、health、调度设置。
- 区分 REGISTERED、DESIRED_ENABLED、PROBING、ADMITTED_ACTIVE 与 UNAVAILABLE/DRAINING。配置 active_agent_ids 仅表达启用**意图**；未通过能力、鉴权、触发与 Git 读写回读探针的 Agent 不得领正式租约。

## 平台独立配额
- ChatGPT scheduled_tasks 示例预算5，用户预留2给 Work/其他用途，则最多占用3个此类计划任务槽。数字5是示例，必须核实当前配额；**不限制额外 WorkBuddy/Codex Agent 的数量**。
- WorkBuddy 定时计划数量、最小间隔、并行与云端执行环境按它自己的 provider/account_scope 登记；Codex 是否提供独立云端定时运行与外部触发必须实测。未知配额标 null/UNKNOWN，不能假定无限。
- 全局 N 是跨 provider 的成员数量；同一账号下独立身份/职责/权限可注册多个 Agent，不得仅根据模型名称去重。

## 每个 Provider 自行调度
- trigger_type 可为 scheduled/manual/external_poll/event_driven；每个 Agent 有 timezone、interval_minutes、schedule_id、planned_time、actual_fired_at、completed_at、verified_capabilities。计划 schedule≠真实唤醒，不能未经用户许可自动修改现有任务。
- **仅对 ChatGPT 同账号每小时的 K 个工位**平均错峰：K=1 :00；K=2 :00,:30；K=3 :00,:20,:40；K=4 :00,:15,:30,:45；K=5 :00,:12,:24,:36,:48。K 是该平台子池数，不是总池 N。平台若实际允许 K>5，则由 scheduler 量化分钟与校验重叠，而不是拒绝 Agent。
- WorkBuddy 可以按自己的验证周期运行；Codex 可以由手动或平台真实提供的定时任务启动。异构 Agent 同时触发由 Controller 原子授权 lease/fencing，不能指望错峰自然避免冲突。

## 扩容/退场
1. 注册 Agent identity、provider adapter、capabilities 和只写本人工件路径，进行只读+写后回读+调度能力探针。
2. 只有通过真实 probe 才可从 DESIRED_ENABLED→ADMITTED_ACTIVE；mock 测试标 MOCK_ACTIVE，不可进入生产任务池。
3. 任意 Agent 退场先 DRAINING、阻止新 CLAIM、保存 HANDOFF，由 Controller 原子撤销/过期租约并增加 fencing_epoch；其他 provider 可以重新领取任务。不得删除历史事件/ACK/cursor。
4. 读板失败 UNKNOWN 不领新单；Controller 不可用则退至 L0 静态分片、仅提议 CLAIM_PROPOSED，不能谎称拥有动态排他能力。

## 必须覆盖的测试
N=2/3/5/6/8/12，总池含 3 ChatGPT+2 WorkBuddy+1 Codex 的 N=6；单平台超预算拒绝但全局6不拒绝；模拟 provider 断线、重复 CLAIM、旧 epoch、ACK 丢失、跨平台 Git 事件回读。性能受可核验运行资源约束，不承诺无限吞吐。