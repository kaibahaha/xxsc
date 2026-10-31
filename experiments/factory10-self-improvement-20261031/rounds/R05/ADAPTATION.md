# R05 F5｜双轨预注册：先于WorkBuddy派单
## CROSS_FACTORY_TRANSFER
| source_round | source_factory | target_round | target_factory | method_change | baseline_metric | target_metric | observed_metric | verdict | evidence_path |
|---|---|---|---|---|---|---|---|---|---|
| R04 | F4 | R05 | F5 | U1结构/解码/内容三层证据隔离，至少1个合成WAV独立复算 | R04 PNG 8494B独立重算，商业案例5/5 NOT_TESTED | 1个WAV可独立复算，5/5标L1/L2/L3状态，0错误升级 | PENDING | PENDING_TEST | rounds/R04/CHATGPT_AUDIT.md; rounds/R05/FEEDBACK_TO_BUDDY.md |
| R04 | F4 | R05 | F5 | U2逐模型价格、许可、权限核验 | R04图像模型混价、素材权利混淆 | ≥90%可查价格主张有型号/单位/官方URL，未知UNKNOWN | PENDING | PENDING_TEST | rounds/R04/CHATGPT_AUDIT.md; rounds/R05/FEEDBACK_TO_BUDDY.md |
## SAME_FACTORY_REMEDIATION
- 新实验R05 F5为首轮正式BASELINE；同厂R15才作正式纵向比较。
- 旧实验F5 R05 Job 6f4057fc78094c63 = FAILED_RATE_LIMIT_429，无研究正文或评分。旧五案例仅计划。formal old content defects_count=0，historical gaps=4，不计算同厂分差/复发率。
- 四项历史交付/证据缺口及五案例A–E逐项整改指令全文见FEEDBACK_TO_BUDDY.md，实际prompt必须包含全文，不能只传Git链接。
## AFTER_RESULT
- 只根据真实MCP返回与Git回读填写U1/U2 observed_metric和verdict；独立核查官方URL与价格版本，不以WorkBuddy自评认定修复。
- R06跨小时只继承本轮审计选出的最多2项通用研究方法，避免直接复制F5市场结论。
