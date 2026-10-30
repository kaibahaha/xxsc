# R08 / F8 机器人感知与动作工厂｜STATUS
- 实验：FACTORY10-SKILL-24H-20261030；计划Phoenix 2026-10-29 17:00 / 北京2026-10-30 08:00；按计划时间归R08；首圈F8 BASELINE，R18才同厂纵向复测。
- README交付契约：已从指定Git分支真实读取README.md（含V2.0）；先核对本轮STATUS/REPORT/AUDIT/FEEDBACK不存在，防止重复派单。
- 历史同厂材料：R08首圈，无F8前次轮次，不适用同厂评分差；读取R03 83/100审计、R07状态和ADAPTATION及总账。跨厂反馈只继承研究方法，未把F7科学研究当作F8同厂基线。
- 上轮R07 Job `1941bb3a79e84c7f`：已通过真实get_workbuddy_result回读，服务端返回DONE、约1309字摘要，声称完整正文在WorkBuddy私有路径 `/home/workbuddy_agent/f7_r07_baseline/F7_R07_REPORT.md`，附12工件。Git本实验R07的WORKBUDDY_REPORT.md和CHATGPT_AUDIT.md尚不存在；摘要不等于完整正文，故R07目前仍NOT_EVALUABLE，不伪造报告或评分。R04–R06先前确认为429失败，不重复派单。
- 本轮反馈：已真实创建 `rounds/R08/FEEDBACK_TO_BUDDY.md`，commit `15e180939fa9c3de89dd76e6d106b12841bd83c2`，blob `d27d636981fb523731c5c76ef3f3616399e52884`，2793字符，Git逐字回读PASS。反馈包全部实际内嵌MCP prompt（3217字符），不只是Git链接。
- WorkBuddy本轮唯一研究派单：实际调用 `submit_workbuddy_task` 一次，conversation_id `FACTORY10-SKILL-24H-20261030-R08-F8`，Job ID **`fc588db4b904442c`**；首次get_workbuddy_result返回[running]、约7秒、0字。状态 **PENDING/RUNNING**，研究正文尚未取得，独立审计 **NOT_EVALUABLE**，不得假造分数或WORKBUDDY_REPORT.md。
- 研究任务：F8机器人感知与动作；15+插件/Skill候选、Top5技巧、五案例WishTree桌面俯拍、机械臂仿真、移动导航、手势遥操作、多传感器评测；必须区分仿真/真机、E0/E1/E2/E3证据、工具已安装/缓存/授权/自建、费用、安全急停与回滚。
- 本轮方法调整：M1官方来源与可重放工件双轨；M2物理安全与仿真真实性分层；M3五案例负例、费用、停机及RUN/BLOCKED状态。效果待正文。
- Git提交与回读：本STATUS、ADAPTATION、ITERATION_LEDGER分别写后独立回读，成功与否以实际Git结果为准，不把提交回执等同回读。前述FEEDBACK已确认PASS。
- 下一轮R09/F9 AIoT智能硬件：先追R08 Job，完整报告到手后才独立评分；R07完整正文未取回时保持NOT_EVALUABLE。继承最多三项经核实的研究方法，突出设备协议、固件、隐私、网络隔离、断网恢复及成本。
- 边界：未安装插件、未切换模型、未授权付费、未控制实体机器人、未改其他分支/实验/自动化任务、未创建新任务。
## R08同轮晚间复查（Phoenix 2026-10-29 17:56，约北京时间2026-10-30 08:56）
- 本次再次真实读取实验README.md并核对R08 STATUS/FEEDBACK/ADAPTATION/REPORT/AUDIT和R09 STATUS：R08唯一派单已存在，R09计划时段尚未开始，不新增R08或R09派单。
- WorkBuddy MCP bridge_health：HTTP 200，版本v3.3，active_jobs=5，max_concurrent_jobs=1；这证明桥接在线，但不证明任务已实际执行。
- list_workbuddy_jobs(limit=30)：R08唯一Job `fc588db4b904442c` 显示 **QUEUED**、约3220秒、0字；共享队列另有复杂编程实验任务正在RUNNING。随后get_workbuddy_result(job_id,wait_seconds=0)返回通用 `[running]`、已3230秒、0字。两种接口状态文字不完全一致；以“**未返回正文、仍未完成/队列受阻**”作为可靠共同结论，不擅称已开始计算或已完成。
- 本轮WORKBUDDY_REPORT.md和CHATGPT_AUDIT.md经Git fetch_file均404；故R08 **PENDING / NOT_EVALUABLE**，五维评分、同厂Δ均不可计算。保留原Job ID，后续只追单不重复submit；不创建伪研究报告。
- R07 Job `1941bb3a79e84c7f` 仍是DONE_SUMMARY_ONLY，Git原报告与审计404；没有完整正文可供评分。R04–R06此前429失败，不将桥接done误认为研究完成。
- 继承到R09的方法要求（尚未派单）：M1官方证据+完整可复核工件，M2模拟/真机与安全权限分层，M3五案例负例/费用/回滚和RUN/BLOCKED标签；R09须按预定时段且先查Git防重。没有改RRULE、模型、插件授权或其他实验。
- 本段为本轮真实状态增量；写入和回读SHA在本次Git工具调用回执及随后独立fetch_file中验证，不预先宣称成功。

## R09追单核实｜Phoenix 2026-10-29 18:56后
- 实际调用WorkBuddy MCP get_workbuddy_result(job_id=fc588db4b904442c,wait_seconds=0)，返回：`[task failed] 任务尚未提交到 CodeBuddy。job_id=fc588db4b904442c status=None`。随后 list_workbuddy_jobs(limit=25)显示该Job **failed、0字**，桥接器health HTTP200/v3.3，max_concurrent_jobs=1；此前QUEUED状态已过期。
- 最新可信结论：**FAILED_NOT_SUBMITTED_TO_CODEBUDDY / NO_REPORT / NOT_EVALUABLE**。不把failed当完成研究；不能断言具体失败根因，需服务端日志进一步排查。R08 WORKBUDDY_REPORT.md和CHATGPT_AUDIT.md仍未出现，不创建伪报告。
- R09/F9已按计划另行唯一派单，Job `a178c0e82f10461d`；不重复提交R08，不切换模型、不取消他人Job。此段追加保留原始队列历史，非覆盖旧记录。
