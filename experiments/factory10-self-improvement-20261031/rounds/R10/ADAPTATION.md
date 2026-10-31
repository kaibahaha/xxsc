# R10 F10｜V4双轨反馈与动态研究策略
- 实际前轮：R09 F9 75e17092ec644e6c DONE，65/100，Git四文档可读；本实验F10首次，SAME_FACTORY_BASELINE_MISSING；旧实验F10 76/100仅历史参考。
- 实际注入：FEEDBACK_TO_BUDDY.md 3422字符，blob 6e2c53e26f6394da2df09483c7027ddd6c646e8d；MCP prompt 3705字符完整嵌入，唯一job 6899942694c048bb。报告尚未返回，实施效果不得先验宣称。
## CROSS_FACTORY_TRANSFER
|source_round|source_factory|target_round|target_factory|method_change|baseline_metric|target_metric|observed_metric|verdict|evidence_path|
|---|---|---|---|---|---|---|---|---|---|
|R09|F9|R10|F10|T1 缺字段/空输入/非法引用真正拒绝|R09 3类缺字段/空命令fail-open；预设10/10故障被拒|F10核心MVE≥5类负例、0 fail-open，适用时普通/-O双模式|PENDING|INJECTED/PENDING_TEST|rounds/R09/CHATGPT_AUDIT.md;rounds/R10/FEEDBACK_TO_BUDDY.md|
|R09|F9|R10|F10|T2 官方事实与可复放工件双门禁|R09 官方事实抽核5项3错，Case B RUN无源码/输入|F10官方事实抽核≥5、0实质错；RUN工件1/1可复放|PENDING|INJECTED/PENDING_TEST|rounds/R09/CHATGPT_AUDIT.md;rounds/R10/FEEDBACK_TO_BUDDY.md|
- T1根因假设：只覆盖预设异常而未覆盖缺字段、空集合与非法类型；可证伪：任一无效输入被exit0接受。T2根因假设：来源时间/型号/法律状态未锁定，执行日志与工件未同步；可证伪：官方原文冲突或RUN缺工件。
## SAME_FACTORY_HISTORICAL_REFERENCE（非本实验正式R-10）
- 旧实验R10 F10 job 09ede5860fdb4aaf，独立76/100(18/19/15/15/9)。缺陷HIST-F10-01法律地位误判、02 RUN缺源码输入、03官方来源与缓存混算、04五案例闭环缺失；整改指令与验收条件已在本轮反馈全文注入。
- 本实验F10尚无上次报告；不能计算同厂Δ、历史解决率或错误复发率。待R10完成后成为R20的正式可比基线。
## V4预注册质量门禁
- fact_check_sample_count≥5；material_fact_error_count目标0；五案例逐项标DOCUMENTED/DESIGNED/SIMULATED/EXECUTED/INDEPENDENTLY_VERIFIED/NOT_TESTED。
- core_mve_status目标EXECUTED并有完整源码/冻结输入/原始日志/SHA；core_mve_independent_replay目标TRUE；red_team_test_count≥5，red_team_pass_count目标≥5，p0_open_count目标0。
- 若报告仍排队：所有observed_metric=PENDING、verdict=NOT_VERIFIED；若报告返回，ChatGPT逐项独立抽核，记录证据及有效/无效/不足，不能凭自评判PASS。
- 下一轮R11 F1必须读取R01同厂报告和R10跨小时通用审计；跨厂只能迁移方法，不能拿F10法律/叙事业务结论替代F1 API专项整改。

## R10最终观测与V4闭环（覆盖上方PENDING占位，不抹去预注册）
- WorkBuddy唯一job 6899942694c048bb DONE/311秒/18980字符，完整正文Git回读PASS；独立评分62/100(16/18/12/8/8)；同厂正式基线缺失，62成为R20基线。
- **CROSS_FACTORY_TRANSFER最终结果**：T1实际注入并实现6类原定负例×普通/-O=12/12结构化拒绝；但独立新增8类×2=16次中12次错误exit0、4次非结构化异常，verdict=**PARTIAL_EFFECTIVE**，不能说fail-closed整体通过。T2实际注入并引用法律/价格来源；独立事实9项1错（Adobe Story 2019停用），报告源码SHA与自报不符且8份冻结JSON/runner/原始输出未交付，verdict=**FAILED_ARTIFACT/PARTIAL_FACT**。
- **SAME_FACTORY_HISTORICAL_REFERENCE**：旧F10 76分仅历史参考；4项旧缺陷：NO FAKES提案地位窄义修正1、RUN原始工件缺失复发1、官方来源/产品候选混淆复发1、五案例部分改善1。不可计算本实验同厂分差或正式旧缺陷解决率。
- **V4质量仪表盘**：fact_check_sample_count=9; material_fact_error_count=1; fact_gate_verdict=PARTIAL; case_status_counts={DOCUMENTED:2,DESIGNED:2,SIMULATED:0,EXECUTED:1,INDEPENDENTLY_VERIFIED:0,NOT_TESTED:0}; core_mve_status=EXECUTED_SELF_REPORTED/RECONSTRUCTED_TESTED; core_mve_independent_replay=FALSE_FOR_ORIGINAL_INPUTS; artifact_reproducibility_verdict=FAIL; red_team_test_count=30; red_team_pass_count=14; red_team_blocked_count=12; red_team_fail_count=16; p0_open_count=1; p1_open_count=5; p2_open_count=0; claims_overstated_count=3; production_readiness=NOT_READY。
- **下一小时R11跨厂通用改进（最多2项）**：①把根对象/缺字段/空集合/非法类型/不可哈希输入/异常恢复统一纳入fail-closed矩阵，任何无效输入exit0或异常无结构即失败；②真实源码+原始输入+输出/runner的SHA三联复核，且从官方确认候选产品仍运营、API版本价格许可当前有效。R11另必须读取同厂R01 F1报告并落实≥3项同厂专项整改；不得用R10 F10行业内容替代F1业务研究。
- **可证伪条件**：下一轮只要有一个非法输入被接受、一个原始SHA不匹配、一个停用产品当现行推荐，方法改进判未通过；不得凭报告自述提升状态。证据见 rounds/R10/INDEPENDENT_RED_TEAM.md、CHATGPT_AUDIT.md、EXECUTIVE_QUALITY_GATE.md。
