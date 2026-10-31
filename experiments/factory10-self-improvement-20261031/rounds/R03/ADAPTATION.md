# R03 F3｜双轨自我改进｜2026-10-31 12:25 CST
## CROSS_FACTORY_TRANSFER（派单前预注册）
| source_round | source_factory | target_round | target_factory | method_change | baseline_metric | target_metric | observed_metric | verdict | evidence_path |
|---|---|---|---|---|---|---|---|---|
| R02 | F2 | R03 | F3 | M1证据四级：官方文档/环境安装/真实执行/独立复现 | R02权限/沙箱/许可证主张有文档但无实测，准确率≥90%未证 | ≥90%关键主张有官方URL或UNKNOWN；≥3环境原始探针；不把schema当调用 | PENDING | PENDING_TEST | rounds/R02/CHATGPT_AUDIT.md |
| R02 | F2 | R03 | F3 | M2五案例真实负例+安全回滚+至少一件完整可复现工件 | R02五例有负例文字但缺真实规则/exit code，危险rm通配回滚 | 5/5完整字段；≥1实际执行且含源码、fixture、stdout、exit code；零危险通配删除 | PENDING | PENDING_TEST | rounds/R02/ADAPTATION.md |
- 实际注入：两项完整改进指令与指标均写入FEEDBACK_TO_BUDDY.md，且已作为WorkBuddy submit_workbuddy_task实际prompt原文，Job 491e5363958242bd。此时报告尚未返回，不宣称有效。
## SAME_FACTORY_REMEDIATION
- 本实验R03是F3首次基线；本实验同厂R-10不存在，故MISSING_BASELINE，同厂评分Δ=NOT_COMPARABLE。
- 历史参考旧实验F3 R03 Job 5b8ee940847e42f2，审计83/100（20/19/16/16/12），不是本实验同厂对比基线。
- 旧报告六项缺陷已完整注入：P0-01确定性模拟缺可复现源码/原始日志；P0-02 SHA≠防篡改；P1-03 IceCube教学模型科学校准不足；P1-04单HTML与多JS矛盾；P1-05素材版权/发行费/工具credits未核；P1-06引擎、浏览器、沙箱、schema能力边界。
- 旧五案例A-E分别要求：模拟源码/负例；单HTML塔防；素材版权；真实试玩工具分层；发行审批/签名/回滚。优先核验P0-01/P0-02/P1-04。
- WorkBuddy实际任务Job 491e5363958242bd，完成后由ChatGPT独立审计；不以自评替代复核。
## 下一轮R04 F4待验证
- 根据R03实测反馈再确定最多2项可跨专题迁移方法；不得在R03尚未完成时宣称改进已有效。

## R03实际审计后的CROSS_FACTORY_TRANSFER（最终判定）
| source_round | source_factory | target_round | target_factory | method_change | baseline_metric | target_metric | observed_metric | verdict | evidence_path |
|---|---|---|---|---|---|---|---|---|
| R02 | F2 | R03 | F3 | M1证据四级/官方核验 | R02权限/沙箱/许可断言有文档但缺实测 | ≥90%关键断言有一手URL或UNKNOWN、环境检查原始证据 | R03多数断言有URL，Python源码/fixture由ChatGPT独立重算成功；但Case2无JS/Node实测仍标EXECUTED | **PARTIAL_EFFECTIVE** | rounds/R03/WORKBUDDY_REPORT.md;CHATGPT_AUDIT.md |
| R02 | F2 | R03 | F3 | M2五案例负例/回滚/可复现工件 | R02负例多为设计，未运行 | 5/5字段+≥1完整实测工件+真实负例 | R03完整Python源码/fixture和SHA可重算、篡改双侧负例准确；其他四例多为方案，Case2过度自评 | **PARTIAL_EFFECTIVE** | rounds/R03/CHATGPT_AUDIT.md |
- WorkBuddy实际Job 491e5363958242bd DONE，MCP全文16357字符、Git blob 208cc9a522974cdf50e7bb29a1671b2b3961ba8d，独立审计80/100（22/18/15/14/11）。
## SAME_FACTORY_REMEDIATION最终独立判定
- 旧F3 R03仅HISTORICAL_REFERENCE 83/100；本实验F3首次基线80/100，R13才作同厂纵向比较。
- 六项历史缺陷：P0-01/P0-02/P1-03 RESOLVED（核心复算/概念或移除错误科学主张）；P1-04/P1-05/P1-06 PARTIAL；recurred_count=1（Node仅版本检查却声称逻辑EXECUTED）。
- 缺失：单HTML/JS未实际构建、Node --test未跑、Playwright试玩与发行均未运行；三次进程日志仅第一份完整。
## R04 F4跨厂方法移交
- T1工件可复核性：若声称图像生成/转换/质量检测已执行，必须提交原始输入、产物或最小确定性处理源码、原始输出/exit code、SHA与版本；≥1独立可复算的只读或合成探针；仅schema不可称EXECUTED。
- T2执行状态真实性：核心能力DOCUMENTED/ENV_PRESENT/EXECUTED/INDEPENDENTLY_VERIFIED分层，≥90%关键主张有官方URL或UNKNOWN，五案例真实负例与许可/成本/权限分层；R03 Node假EXECUTED是明确反例。
- 下一轮须把T1/T2完整注入WorkBuddy实际prompt，验收实测后才能宣称方法有效。
