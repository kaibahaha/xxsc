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
