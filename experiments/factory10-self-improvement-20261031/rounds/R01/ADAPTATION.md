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


## R01实际结果与R02可验证改进
- WorkBuddy已DONE，报告声称382行；MCP仅返回1517字摘要。**实际新发现P0-DELIVERY-01：远端正文没有进入Git或ChatGPT审计视野**；不能评分。
- H1: SF01/SF02/SF03的官方事实纠偏已经ChatGPT核对，但报告全文缺失导致“关键主张证据覆盖≥90%”无法统计，verdict=EVIDENCE_INSUFFICIENT。
- H2: 摘要自称五案例含失败注入，但没有具体案例正文，verdict=EVIDENCE_INSUFFICIENT。
- R02必须将以下两项具体方法改进完整注入WorkBuddy prompt：M1交付完整研究正文到MCP/Git（避免只有远端路径与摘要），M2版本差异审计与5/5案例负例+回滚。
- 版本冲突提示：CodeBuddy v2.168.3发布说明提及默认30天，通用scheduled-tasks文档称循环任务3天；应按任务类型与版本拆分，不可泛化。
## CROSS_FACTORY_TRANSFER — 已观察
| source_round | source_factory | target_round | target_factory | method_change | baseline_metric | target_metric | observed_metric | verdict | evidence_path |
|---|---|---|---|---|---|---|---|---|
| R01 | F1 | R02 | F2 | M1全文可审计交付 | 本轮仅摘要，全文缺失 | 100%正文可回读；关键主张≥90%有官方依据 | 待R02 | PENDING_TEST | rounds/R01/CHATGPT_AUDIT.md |
| R01 | F1 | R02 | F2 | M2版本冲突+负例回滚 | R01案例正文不可读 | 版本明确、5/5案例有负例与回滚 | 待R02 | PENDING_TEST | rounds/R01/CHATGPT_AUDIT.md |

## R01延迟审计结论与R02时序证据
- 原研究job aab758d7c33d4631 DONE；只读补交job 93de654703984b20 DONE，完整382行报告现已Git回读；新实验R01正式评分79/100，五维22/18/14/14/11。
- M1跨厂交付方法：R01在R02派单时仅摘要→R02全文直回→R01原文后续追回，交付链路改进有效，但R01研究准确性与R02不同工厂分数不能直接比较。
- R11 F1同厂深挖：`--fallback-model`真实CLI语法/模式；多租户fail-closed故障注入；cosign/Sigstore与OIDC；五案例实际验收。
