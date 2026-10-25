# 04｜统一事件消息 UEM、消费 ACK、去重、重试

## 上游原理与字段
`mini-router/src/uem.ts` 定义 `event_id, source, target_agent, kind, summary, observed_at, raw`。`src/state.ts` 使用 `(event_id,agent)` 去重、`pending→sending→sent / failed→retrying` 及 1/5/30/120s 的内部重试；这属于常驻侧车行为，不适合机械复制成网页版任务每30秒轮询。

## V4.1 统一事件（JSON）
```
{
  "schema_version":"1.0", "event_id":"EV-...", "project_id":"P...",
  "task_id":"T...", "producer":"A", "target_agents":["B"],
  "kind":"FACT_PUBLISHED", "source":"github", "observed_at":"ISO8601Z",
  "summary":"短说明", "raw_ref":"repo@commit:path", "payload_sha256":"hex64",
  "spec_hash":"hex64", "causation_id":null, "run_id":"RUN-..."
}
```
受众 `target_agents` 可多 Agent，同一 `event_id` 对每个目标分别保存投递记录；消费者应按 `(event_id,target_agent)` 幂等。成功读取只记 `DELIVERY_ACK`，不改变业务 Task DONE。相同事件二次提交，若 hash 不同，标 `EVENT_ID_COLLISION`，不可用覆盖解决。

## 事件投递状态
`PENDING`（等待消费）→`SENDING`（投递中）→`SENT`（已收到回执）。异常→`FAILED`（保留 last_error）→`RETRYING`；无法证明是否送达→`UNKNOWN_DELIVERY`，下次优先对账，不能因超时直接无限重发。

Git 文件模式没有 SQL 事务/常驻调度，不能承诺以上状态的原子转换。可用追加不可变 `event`/`receipt`/`attempt` 文档近似保存历史，由 Controller 投影决议最终状态。读者必须以 `(agent,source)` 维护 cursor，并周期性全量审计以发现遗漏；游标仅能在有效处理/持久回执之后推进，**不得只因读取页面成功就宣布消费成功**。

## 事件积压和排序
同一任务的因果依赖优先于时间顺序；不同任务可独立处理。Backlog 超阈值时，热层提供最新+被@的消息和关键阻断，冷层保存全部 JSONL/事件文件；不能默默丢弃历史事件。每个 Agent 每轮必须记录 observed event IDs、acked IDs、skipped IDs、原因和指针。

## 建议 kind
`TASK_READY`, `CLAIM_PROPOSED`, `LEASE_GRANTED`, `CLAIM_CONFLICT`, `STARTED`, `FACT_PUBLISHED`, `FAIL_PUBLISHED`, `PATCH_SUBMITTED`, `TEST_REQUESTED`, `TEST_PASSED`, `TEST_FAILED`, `REVIEW_REQUESTED`, `REVIEW_ACCEPTED`, `TRANSPORT_GAP`, `RELAY_VERIFIED`, `BLOCKED_POLICY`, `HANDOFF_READY`, `NO_ELIGIBLE_TASK`, `RUN_TERMINATED`。
