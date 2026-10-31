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

## R05完成后的CROSS_FACTORY_TRANSFER（取代上表PENDING，保留预注册）
| source_round | source_factory | target_round | target_factory | method_change | baseline_metric | target_metric | observed_metric | verdict | evidence_path |
|---|---|---|---|---|---|---|---|---|---|
| R04 | F4 | R05 | F5 | U1结构/解码/内容三层证据 | R04合成PNG 8494B哈希可复算，5商业案例NOT_TESTED | ≥1个WAV独立重算，5案例标L1/L2/L3，0越级 | WAV16044B、SHA 5fc01c0f096e4def771d173852278fe14fbd9240326d4461394af901e9be4a65，ChatGPT独立Python重算与wave读取8000帧一致；5商业案例仍未运行 | EFFECTIVE_FOR_DETERMINISTIC_PROBE / PRODUCTION_NOT_PROVEN | rounds/R05/WORKBUDDY_REPORT.md §§0-1,5; CHATGPT_AUDIT.md §§2,4 |
| R04 | F4 | R05 | F5 | U2逐产品价格/许可/权限 | R04跨模型报价混用与授权过度概括 | ≥90%可核价格断言逐型号+官方URL+计费单位 | R05 13候选矩阵但Opus$14.5/年误写（实际$14.5/月年付$174）、Runway Gen4.5 $15/min算错（应$7.20/min API基础价）、Suno 500曲/无Content ID风险无证据；官方核验目标不成立 | PARTIAL_FORMAT / FAILED_FACT_ACCURACY | rounds/R05/CHATGPT_AUDIT.md §§3-4 |
- WorkBuddy unique Job 09ea81a5a538420a DONE 460s，完整MCP 13721字符，Git报告blob 2758bf8630378dd70ce0ebbdc7e6532dbb467577、审计blob a0f78bf15afa53be67d3a9061de0be6d7e7d0b9d，均逐字回读PASS。
- 独立评分**73/100（18/17/15/14/9）**；R04 F4 77分不同厂不可作质量因果比较。
## SAME_FACTORY_REMEDIATION 完成状态
- 旧实验F5 Job 6f4057fc78094c63 FAILED_RATE_LIMIT_429，无报告、无评分；formal_same_factory_defects_count=0，historical_gaps_count=4，delivery_resolved=1，gaps_partial=3，same_factory_score_delta=NOT_COMPARABLE，recurred_count=NOT_COMPARABLE。新实验R05正式F5基线73/100，R15与本轮比较。
- R15优先修正：P0 Opus计费周期错误、P0 Runway单分钟费用算术、P1 Suno商业权与下载额度、P1 平台政策逐项官方核验、Case A视频宽高比拉伸风险。
## R06 F6跨小时移交（最多2项，必须实际注入下一轮WorkBuddy prompt）
- **V1价格/数值算术门禁**：R05 Opus年付/月付误读、Runway 12cr/s×$0.01×60=$7.20/min却报$15、Suno下载量与credits混淆。F6研究/报告工厂要求至少5项数值主张逐项列公式、单位、官方来源、核验日期、算术复核；错误则FAIL，未知标UNKNOWN。
- **V2结构校验≠语义事实/版权合法**：R05合成WAV可独立复算但不能证实真实听感/商用权。F6对DOI/元数据格式、论文全文及撤稿/更正状态、研究结论语义准确与版权/数据权限分层；至少1个可复核DOI/引用探针，五案例均标EXECUTED/NOT_TESTED；不得将格式通过当成科学事实通过。
