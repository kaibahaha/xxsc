# R01 F1 研究方法预注册与跨工厂交接
- Baseline: 新实验R01，上一小时R00不存在，故本轮跨小时改善效果 NOT_EVALUABLE。
- Same-factory historical reference: 旧实验R01 70/100，已在派单前把六项历史缺陷SF01-SF06与五案例整改逐项注入WorkBuddy。不能把本轮改善预先宣称成功。
- Hypothesis H1: 将“Agent REST/ACP vs OpenAI Chat Completions推理网关”协议分层并提供官方接口证据，减少概念混淆；验证：关键API主张中明确协议、版本、来源的占比≥90%，未核验项显式标记。
- Hypothesis H2: 对五个案例逐一补负例、量化验收、回滚条件，降低不可复现案例比例；验证：5/5案例均有失败注入和可执行回滚判据。
- Actual injection: FEEDBACK_TO_BUDDY.md 全文包含在 submit_workbuddy_task prompt；Job aab758d7c33d4631。
- Effect: PENDING; wait for WorkBuddy report and ChatGPT independent audit.
## CROSS_FACTORY_TRANSFER
| source_round | source_factory | target_round | target_factory | method_change | baseline_metric | target_metric | observed_metric | verdict | evidence_path |
|---|---|---|---|---|---|---|---|---|---|
| R01 | F1 | R02 | F2 | 关键主张三级证据标签+负例回滚 | 待R01审计 | ≥90%证据覆盖、5/5案例负例 | PENDING | NOT_EVALUABLE | rounds/R01/CHATGPT_AUDIT.md（待完成） |

## SAME_FACTORY_REMEDIATION
- Source: old experiment R01 (historical reference, not new R01 baseline).
- Defect register: SF01-SF06, details in FEEDBACK_TO_BUDDY.md.
- Result: PENDING; do not invent resolved/recurred counts.
