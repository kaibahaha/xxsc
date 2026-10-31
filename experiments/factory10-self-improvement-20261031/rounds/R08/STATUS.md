# R08 F8｜状态预登记
- planned_at: 2026-10-31 17:25 Asia/Shanghai；preflight_at: 2026-10-31 17:24 Asia/Shanghai；新实验R08 F8 BASELINE。
- preflight bridge_health: HTTP200，version=3.4-candidate，codebuddy_reachable=true，running_jobs=0，queued_jobs=0，unresolved_orphan_count=0；list_workbuddy_jobs最近15条R07 c20368ab43794a78 DONE/372秒/19114字，未见本实验R08任务。
- Git rounds/R08/STATUS.md 首次读取404，防重复通过；旧实验R08 Job fc588db4b904442c failed/0字，不得混淆为本实验R08。
- R07四文件STATUS/WORKBUDDY_REPORT/CHATGPT_AUDIT/ADAPTATION均已Git读取，68/100(17/17/13/13/8)，迁移Q1字节一致性和Q2官方标识+真实负例。旧F8仅历史交付缺口，无可比正文/评分。
- job_id: NOT_SUBMITTED；state: PREPARED；report: NOT_EVALUABLE；score: NOT_EVALUABLE；same_factory_delta: NOT_COMPARABLE；cross_hour_effect: PENDING_TEST。
- 只允许本轮唯一submit，计划时刻17:25后执行；先写FEEDBACK并回读，完整正文注入WorkBuddy prompt；不得改生产、模型、插件授权、旧实验或其他定时任务。
## R08唯一真实派单（2026-10-31 17:25 Asia/Shanghai）
- pre-submit bridge_health HTTP200，version 3.4-candidate，codebuddy_reachable=true，running_jobs=0，queued_jobs=0，unresolved_orphan_count=0；list_workbuddy_jobs最近20条无本实验R08，防重复PASS。
- FEEDBACK_TO_BUDDY.md commit 7f7df00f0e20d0d33d610de57d7fe0a82ef21c87 / blob f4ca36d529a7461e5cb95c559d211a6034ec42b6，3945字符，派单前Git逐字回读PASS；ADAPTATION.md commit bb608766474e645ac4ff6d54734e506fc249df52，Git回读PASS。
- 实际MCP submit prompt 4354字符，完整内嵌3945字符FEEDBACK原文（Q1/Q2跨小时整改及HIST-F8-01~05同厂历史交付缺口，五案例A-E均注入）。
- conversation_id FACTORY10-SELF-IMPROVEMENT-20261031-R08-F8；**job_id: b76c0601c10f4d60**；submit_workbuddy_task返回“已提交”，未返回研究正文。
- state: **PENDING**；report: PENDING；audit/score: NOT_EVALUABLE；same_factory_score_delta: NOT_COMPARABLE；cross_hour_effect: INJECTED/PENDING_TEST。
- 后续仅get_workbuddy_result(b76c0601c10f4d60)追取，绝不重派；完整报告回来后再独立评分、写报告与双轨审计。

## R08最终验收（覆盖PENDING，保留原始事件）
- planned_at: 2026-10-31 17:25 Asia/Shanghai；actual submit_at: 2026-10-31 17:25 Asia/Shanghai；WorkBuddy运行489秒（约8.15分钟）；independent audit completed约2026-10-31 17:35 Asia/Shanghai。
- unique job_id **b76c0601c10f4d60**，WorkBuddy list_workbuddy_jobs **DONE / 489秒 / 14517字符**；get_workbuddy_result返回BEGIN_FULL_REPORT/END_FULL_REPORT完整正文；未重复派单。
- FEEDBACK_TO_BUDDY.md commit 7f7df00f0e20d0d33d610de57d7fe0a82ef21c87 / blob f4ca36d529a7461e5cb95c559d211a6034ec42b6，3945字符，派单前Git逐字回读PASS，完整注入4354字符MCP prompt。
- WORKBUDDY_REPORT.md commit **af138af32037bec1c145236137c8cd939906234e** / blob **853cbb7dc1c574d0653f8318969c3e64bdeb0d56**，14517字符Git逐字回读PASS。
- CHATGPT_AUDIT.md commit **54471709deaf5141b14e9b8b3363f58cc61da226** / blob **e38e48bb3a3f1f452c3ce84103d8bb19ee143592**，独立评分 **73/100（19/18/15/13/8）**，Git逐字回读PASS。
- 独立Python3.13.5标准库重放：两源码SHA256与Buddy报告一致2/2，正常stdout字节SHA一致1/1，exit0，stderr空；五负例普通Python exit1/1/1/1/3。但急停assert在python -O模式exit0绕过（P0），不能声称生产安全通过。
- 官方抽核：ROS2 Range引用错误ROS1 Fuerte版本（单位正确但版本链接错误）；TurtleBot4标准摄像头为OAK-D-Pro；RealSense D435当前官网$314而非报告$179。五案例A-E未端到端运行。
- SAME_FACTORY: 旧F8只有历史failed/0字，无正文评分，historical_gaps=5，resolved_delivery_only=1，partial=4，same_factory_score_delta=NOT_COMPARABLE，old_error_recurrence=NOT_COMPARABLE；本轮73是R18正式基线。
- CROSS_HOUR: Q1 EFFECTIVE_FOR_DETERMINISTIC_REPRODUCTION；Q2 PARTIAL_EFFECTIVE/SAFETY_AND_VERSION_FACT_ERRORS_RECUR。R09 F9移交S1可复放+双模式不可绕过安全门禁，S2官方版本/型号/价格精确核验。
- final_state: **DONE / FULL_REPORT_GIT_VERIFIED / INDEPENDENT_AUDIT_GIT_VERIFIED / CONDITIONAL_ACCEPT_FOR_RESEARCH / NOT_READY_FOR_PRODUCTION**。不修改生产、其他分支、旧实验、模型、插件授权或定时任务。
