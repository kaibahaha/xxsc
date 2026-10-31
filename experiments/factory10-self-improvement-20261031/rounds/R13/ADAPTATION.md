# R13 F3｜ADAPTATION 双反馈链预注册
## A 跨小时R12 F2→R13 F3
R12真实DONE，原报告17388字符Git独立回读；R12当时独立质量审计尚待完成。以下基线指标仅R12自述，不能当独立通过。已在Git反馈全文先行回读，随后逐字注入R13唯一WorkBuddy prompt。
|source_round|source_factory|target_round|target_factory|method_change|baseline_metric|target_metric|observed_metric|verdict|evidence_path|
|---|---|---|---|---|---|---|---|---|---|
|R12|F2 软件开源|R13|F3 游戏互动|T1 fail-closed+相邻负例双模式|R12自述9类×2=18/18拒绝，独立验证待定|F3≥5类×normal/-O，≥10次拒绝、0 fail-open|PENDING|INJECTED_NOT_VERIFIED|rounds/R12/WORKBUDDY_REPORT.md;rounds/R13/FEEDBACK_TO_BUDDY.md|
|R12|F2 软件开源|R13|F3 游戏互动|T2源码/输入/输出原始SHA三联与证据级别|R12自报SHA但Git仅报告，未独立复算；R03 Node执行等级错误|≥1完整HTML/JS+Node核心MVE，5例0假EXECUTED|PENDING|INJECTED_NOT_VERIFIED|rounds/R12/WORKBUDDY_REPORT.md;rounds/R03/CHATGPT_AUDIT.md|
## B 同厂R03→R13
正式R03 80/100 (22/18/15/14/11)，同厂三项重点：Node执行过度声称、单HTML缺失、三进程原始日志及源码SHA缺失。其他素材许可、引擎/浏览器界限与可信锚持续复核；五案例A–E逐项重测要求在FEEDBACK完整给出。
## 假设、证伪、下一轮
H1：增加真实负例可减少fail-open；任一非法exit0即证伪。H2：源码+冻结输入+输出完整工件能避免ENV_PRESENT→EXECUTED误报；任一无运行日志却称EXECUTED即证伪。
本轮Buddy未返回前效果NOT_VERIFIED；下一轮R14优先追R13，再按同口径跨厂质量指标观察，不用F3/F4总分作因果推断。
