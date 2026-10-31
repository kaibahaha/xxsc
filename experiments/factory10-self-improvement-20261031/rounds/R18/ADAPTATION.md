# R18 F8｜双反馈链预注册与下轮验证
- R17 F7 DONE job 4314c14e9faa4d80，独立62/100，8/10相邻边界错误ADMIT，R17原始源码SHA不符/四JSON输入和完整日志缺失；R08 F8 DONE job b76c0601c10f4d60，73/100(19/18/15/13/8)，优化模式assert急停绕过、ROS1链接当ROS2、D435价格错、五案例未端到端执行。两条反馈线不可互替。
- Git FEEDBACK 4688字符逐字回读，MCP实际prompt 4872字符全文注入，job e06ced6b21e84758；实施效果待正文及独立审计，NOT_VERIFIED。
## CROSS_FACTORY_TRANSFER
|source_round|source_factory|target_round|target_factory|method_change|baseline_metric|target_metric|observed_metric|verdict|evidence_path|
|---|---|---|---|---|---|---|---|---|---|
|R17|F7|R18|F8|M1严格bool授权/可信来源/未知默认拒绝与相邻红队|R17 8/10相邻边界错误ADMIT|≥8负例、普通与-O模式0 fail-open|PENDING|INJECTED_NOT_VERIFIED|R17/INDEPENDENT_SECURITY_PROBES.md;R18/FEEDBACK_TO_BUDDY.md §A|
|R17|F7|R18|F8|M2冻结输入/原始源码/完整stdout-stderr/实际SHA字节一致|R17源码SHA不符、4份JSON和完整日志缺失|≥1完整MVE字节独立重放、0缺文件|PENDING|INJECTED_NOT_VERIFIED|R17/CHATGPT_AUDIT.md;R18/FEEDBACK_TO_BUDDY.md §A|
- M1根因假设：字符串真值或默认放行替代可信授权；证伪条件=任一未经授权/急停指令ADMIT。M2根因假设：报告源码与执行工件不同步；证伪条件=任一原始文件缺失或SHA不一致。
## SAME_FACTORY_REMEDIATION
|defect|R08独立证据|R18验收目标|observed|status|
|---|---|---|---|---|
|D1 P0|R08/CHATGPT_AUDIT.md §Q2，python -O急停exit0|显式if/raise，普通/-O双模式拒绝，无副作用|PENDING|NOT_VERIFIABLE|
|D2 P1|R08/CHATGPT_AUDIT.md §官方来源，ROS1 Fuerte误引、TB4型号、D435 $179错误|≥5官方事实精准版本/型号/日期/现价0实错|PENDING|NOT_VERIFIABLE|
|D3 P1|R08/CHATGPT_AUDIT.md §五案例，A-E全无业务E2E|C导航安全MVE完整冻结输入→路径→拒绝→回滚可重放|PENDING|NOT_VERIFIABLE|
- same_factory_baseline_round=R08; same_factory_defects_count=3; resolved_count=PENDING; recurred_count=PENDING; same_factory_score_delta=NOT_EVALUABLE。五案例A-E逐项要求见本轮FEEDBACK §B。
## 上一小时通用改进：计划→实际注入→实际效果→下轮调整
- M1/M2计划已写入Git并逐字发送，实际效果PENDING/NOT_VERIFIED；下轮R19 F9仅继承独立核实的方法，尤其双模式fail-closed与原始工件复放，不能因R18总分变化声称跨厂有效。
