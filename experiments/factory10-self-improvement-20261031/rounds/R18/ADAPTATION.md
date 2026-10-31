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

## R18 FINAL｜双反馈链实际观察（覆盖PENDING预注册但保留事件历史）
- 唯一Job e06ced6b21e84758 DONE，MCP全文35661字符；WORKBUDDY_REPORT commit e69c61b1f323a6d360350854043ee696597cbd81 / blob 26369c989c48336f7080de7182d80cdfcb51c2fc Git逐字回读PASS；ChatGPT独立审计 commit 5cad14767f467e54797646cad0478a125b70cfb7 / blob 097527791272fa469927780c33507a3a2b5d1920，独立回读PASS；新增安全探针 commit 52531b68ab31c727cb510ca7cf4115b50ced574a / blob 9d6939b0d4983a20c4a96d9387f83a4fcd95a249。MCP完整prompt实际包含4688字符FEEDBACK，不能把Git修改当成实际注入。
## CROSS_FACTORY_TRANSFER FINAL
|source_round|source_factory|target_round|target_factory|method_change|baseline_metric|target_metric|observed_metric|verdict|evidence_path|
|---|---|---|---|---|---|---|---|---|---|
|R17|F7|R18|F8|M1严格bool授权/可信来源/未知默认拒绝/相邻红队|R17 10新增探针8错误ADMIT|≥8相邻负例0 fail-open|R18 Buddy自选13负例拒绝，但ChatGPT独立逻辑复刻9新边界8 ADMITTED、1 TypeError，未做真正来源签名/nonce|PARTIAL_IMPLEMENTED_FAILED_TRUST_CHAIN|R18/INDEPENDENT_SECURITY_PROBES.md §D|
|R17|F7|R18|F8|M2源码+全部冻结输入+原始stdout/stderr/SHA|R17源码SHA不符且4 JSON缺失|≥1完整MVE字节重放0差异|R18源码2/2 SHA一致、13 JSON可重构；normal stdout报告文本SHA与自称不符，optimize和P1原始字节缺失，原始Python未独立执行|PARTIAL_IMPLEMENTED_OUTPUT_INTEGRITY_FAIL|R18/INDEPENDENT_SECURITY_PROBES.md §B|
- 研究方法改善与工具调用成功分开：R17与R18安全探针样本不同，不比较总分因果；源码哈希改善只支持工件源文本一致，不能证明完整MVE或生产安全。
## SAME_FACTORY_REMEDIATION FINAL
|defect|R08基线|R18实际变化|status|
|---|---|---|---|
|D1 P0|assert estop在-O exit0|源码改显式if/raise，自报双模阻断，原始源码未独立运行；新来源伪造仍放行|PARTIAL|
|D2 P1|ROS1引用/型号/旧价|旧三点纠正，新增OV251错、Ubuntu20.04当当前支持，7官方抽2实错|RECURRED|
|D3 P1|五案例均未E2E|C导航模拟路径数学复核PASS，其余四个未运行，原始输出hash不符|PARTIAL|
- R08 73(19/18/15/13/8)→R18 71(18/18/16/15/4)，Δ=-2（难度与证据覆盖变化）；resolved0/3, partial2/3, recurred1/3, key_error_recurrence=1/3；事实门禁FAIL、可信审批P0仍开、production NOT_READY。
## 上一小时通用改进：计划→实际注入→实际效果→下轮调整
- M1计划0 fail-open→Git+MCP全文实际注入→严格bool及assert修复，但9新相邻探针8放行→下轮升级为真实可信身份签名、nonce与防重放、严格未知字段拒绝，≥8探针0放行。
- M2计划完整源码/JSON/stdout哈希一致→Git+MCP实际注入→源码2/2一致但日志SHA失败、原始输出字节缺→下轮必须返回全部原始日志和输出文件字节并独立复算1/1。
- 机会研究线：独立官方5候选/新增去重4、用户资格0、实际领取0；不可将Buddy机会自报当已获得资源。R19 F9继承最多2项方法，不改变调度、评分、生产或插件权限。
