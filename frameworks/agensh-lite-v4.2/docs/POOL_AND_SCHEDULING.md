# 开放式弹性 Agent 池与调度（全局 N>=2，无固定上限）

## 两个独立概念
全局成员池可包括 ChatGPT、WorkBuddy、Codex 等 N>=2 个 Agent；不存在硬编码的五人上限。但资源必须按 provider_id 分开核实，系统吞吐/并发/费用也受现实限制。一个 Provider 的预算不限制其他 Provider 的逻辑注册成员。ChatGPT 平台保留两个 Work/其他计划任务槽，并不限制额外加入 WorkBuddy Agent。
统一 TASK/Claim/Event/Handoff/ACK/QA 状态机在 GitHub 上跨平台复用。不同平台用独立 scheduler_id、时区、cadence、transport_status 和权限记录。配置是建议，不是实际平台已创建的定时任务。
详见 MULTI_PROVIDER_AGENT_REGISTRY.md。

## ChatGPT 内部错峰
只有在同一 Provider 上的 K 个 Agent 都以每小时一次被真实配置时，才可在时钟分钟粒度下用 floor(60*i/K) 计算推荐错峰。
K=2：:00,:30；K=3：:00,:20,:40；K=4：:00,:15,:30,:45；K=5：:00,:12,:24,:36,:48；K=6：:00,:10,:20,:30,:40,:50。
K>60 时须处理分钟精度冲突或 provider 限制，不能承诺每个触发点唯一。多个不同 Provider 或不同 cadence 的 Agent 无法按全局 N 套用 60/N。
WorkBuddy 的原生计划任务和 Codex 的可能触发模式需逐项探针验证，不能因聊天/编程界面可以调用就断定后台可调度。记录实际 schedule_id、fired_at 和 git 写后回读证据。

## 伸缩流程
扩容：登记候选 agent_id / provider_id → 只读探针 → 能力/授权/预算核对 → 沙盒 Git 写入回读 → 验证真实触发 → ACTIVE；失败则保持 BLOCKED。
缩容：停止授新 lease → DRAINING → 确认原有 attempt/lease 到期或安全撤销且 fencing_epoch 增长 → 保留 HISTORY/HANDOFF → 让其他有能力且获权 Agent 重新领取 → 验证真实停止调度。
没有原子 Controller 时只采用 L0 隔离写入和 CLAIM_PROPOSED，不把 CLAIM 当排他锁。

## 验收
单元和压力测试覆盖 N=2/3/4/5/6/10/20，至少测一次 ChatGPT+WorkBuddy 异构组合；N=1 和重复 agent_id 拒绝；已证实 Provider 配额不足拒绝；未知配额标 UNKNOWN 而非无限；24 小时真实唤醒由各 Provider 独立核对。
