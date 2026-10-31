# R10 F10｜ChatGPT V4独立审计｜2026-10-31
- experiment FACTORY10-SELF-IMPROVEMENT-20261031；factory F10 小说与叙事；唯一WorkBuddy job **6899942694c048bb**，MCP list_workbuddy_jobs真实显示 **DONE/311秒/18980字符**；取得BEGIN_FULL_REPORT/END_FULL_REPORT完整报告正文18903字符，Git commit **05e78d056c41bf86b348e5e95b00f06081c62755**、blob **66c7bec9ba40386b97f13d6e13bdd73f812aa14a**，逐字回读PASS。
- 本实验F10首次，**MISSING_BASELINE**；旧实验F10 R10 job 09ede5860fdb4aaf独立76/100(18/19/15/15/9)仅HISTORICAL_REFERENCE，不作为正式同厂分差；R09 F9 65/100是跨厂，不能把总分变化当因果证据。
- 本次独立证据：实际从Git报告提取源码并计算SHA256；在ChatGPT隔离Python3.13.5上以合成输入执行15类×normal/-O两模式共30次；核对官方版权局、美国GovInfo/FTC、OpenAI定价、Twine官方代码仓库及Adobe停用公告。详细矩阵在INDEPENDENT_RED_TEAM.md。

## A. WORKBUDDY_SELF_REPORT（自述，不等于独立证明）
- Buddy称本轮MVE世界观圣经校验器已EXECUTED；6类负例×两模式全部结构化拒绝，0 fail-open；源码/8份冻结输入/run_mve.py/日志/SHA全部可复现；官方7项事实0错；五案例A执行、B/C设计、D/E文档；历史法律错误修复。
- 以上只有“完整报告真实返回、代码块可运行、原定6类负例可拒绝”等部分得到独立支持。其他自述须看以下独立核验。

## B. 固定五维100分独立评分
|维度|满分|得分|独立依据|
|---|---:|---:|---|
|证据与事实|25|**16**|官方法律/价格/许可部分准确，报告源码可提取；但Adobe Story已停用却列当前候选、所谓10条一级官方来源混入GovTrack/官网首页，源码SHA不一致、8份原始JSON及run_mve.py缺失。|
|战略契合|20|**18**|世界观圣经、章节生产、分支互动、翻译和改编四条商业路径贴合F10；缺客户、获客、收入和单位经济验证。|
|操作技巧|20|**12**|源码完整、部分负例可运行；Top5仅表格/URL，没有逐项可执行命令、真实安装/权限/输出验证；代码多处schema和边界漏洞。|
|五案例|20|**8**|A仅本地一致性验证且原始工件不齐；B/C/D/E每例仅一两句，缺完整输入/步骤/预期输出/实际输出/异常/预算/回滚和人工审稿记录；全业务闭环0/5。|
|风险与真实性|15|**8**|正确区分法案提案/版权局政策研究/实验安全策略；但授权只靠自报、失效软件候选、源码哈希错配、负例边界错误接受。|
|**合计**|**100**|**62/100**|**真实MCP与Git交付PASS；V4质量门禁FAIL；NOT_READY_FOR_PRODUCTION**。|

## C. 官方事实独立抽查（2026-10-31）
|序号|报告主张|独立权威证据|结果|严重度|
|---|---|---|---|---|
|1|TAKE IT DOWN Act=P.L.119-12，2025-05-19批准|美国政府GovInfo https://www.govinfo.gov/app/details/PLAW-119publ12 |PASS|—|
|2|平台下架义务2026-05-19生效|美国FTC https://www.ftc.gov/business-guidance/resources/complying-take-it-down-act |PASS|—|
|3|版权局Part1 Digital Replicas 2024-07-31发布，性质政策报告|美国版权局 https://copyright.gov/ai/ |PASS|—|
|4|版权局Part2 Copyrightability 2025-01-29发布|美国版权局 https://copyright.gov/ai/ |PASS|—|
|5|版权局Part3预发布2025-05-09|美国版权局 https://copyright.gov/ai/ |PASS|—|
|6|GPT-5.6 Sol标准短上下文$4输入/$20输出（每百万tokens）|OpenAI官方 https://developers.openai.com/api/docs/pricing |PASS；需注明standard/short context|—|
|7|GPT-6 Astra标准短上下文$10输入/$50输出（每百万tokens）|同上|PASS；需注明standard/short context|—|
|8|Twine开源GPL|Twine官方源码仓库 https://github.com/klembot/twinejs ，LICENSE GPL-3.0|PASS；作品商用许可≠软件GPL自动适用|—|
|9|Adobe Story作为2026年可用剧本创作工具候选|Adobe官方2018公告 https://blog.adobe.com/en/publish/2018/01/22/adobe-exits-scriptwriting-software-business-end-adobe-story-cc ：服务/离线应用2019-01-22全部停止|**FAIL**，候选已失效|P1|
- **可核验样本9项：8正确、1实质错误，fact_gate_verdict=PARTIAL**。不能把9项抽样推断为整份报告准确率。报告§3所述NO FAKES S.4591尚未成法有非官方跟踪交叉支持，但本轮直接访问congress.gov被阻断，官方实时状态**NOT_VERIFIABLE**，不计入上述9项PASS。报告“已官方核验全部7项0错”口径过宽。
- 报告“一手官方来源≥10”实际把GovTrack（二手）、congress.gov首页（不支持具体法案状态）、OpenAI API产品首页、版权局年报等混作独立精确证据；不得按10条有效独立官方事实计分。
- 法律判断：Part1是研究不是法规，Part2强调人类作者贡献；TAKE IT DOWN Act聚焦NCII而非一般声音克隆全面禁令。报告“唯一已生效的联邦deepfake成文法”范围过宽、缺排他性法律检索证据，标UNVERIFIED，不得作为法律建议。

## D. 独立MVE复现、红队与SHA（详细见INDEPENDENT_RED_TEAM.md）
- WorkBuddy §5嵌入源码7092 ASCII字符。对Git精确源码块算SHA256：无末尾LF **ec14e7f26956f0b382d2acf41d8934b26f4ff295a44d2bd1df0bfec38821b617**；有末尾LF **a681c6ca4c06612d6470a5efd8f69f6fd0c3dacf45aa2e931ab48a23a105717c**；报告自报 **222568b773ab19adcf0eb5b429a07186f362d10c43a89b9527e444f979830cf4**，**均不一致**。无法据报告源码证明原始文件SHA正确。
- 报告只列8份冻结JSON的文件名和哈希，未附文件字节；run_mve.py及mve_run_summary.json也只给名字/摘要，**不能独立复算原始输入哈希或原始运行日志**。故核心MVE独立状态为 **RECONSTRUCTED_EQUIVALENT_TESTED / ORIGINAL_FROZEN_ARTIFACT_NOT_VERIFIED**，不是INDEPENDENTLY_VERIFIED。
- 实际独立运行15类×2模式=**30次**：原定6类负例×2=12/12结构化拒绝；合法正例×2=2/2接受。新增8类×2=16次，**12次错误退出0（含空/缺章节、重复ID、年龄矛盾、数值正文、布尔来源），4次未捕获AttributeError/TypeError退出1**。所以T1仅**PARTIAL_EFFECTIVE**，不能声称“0 fail-open”涵盖相邻边界。
- **P0-GATE-01**：meta.authorization.source可为true、text_usage由用户自述即可通过；这不是可信版权授权验证，不可用作生产权利门禁。**P1-SCHEMA-02**：顶层数组/引用dict触发未捕获异常，text=123被VALID。**P1-SEMANTICS-03**：空/缺章节、重复角色ID、严重年龄矛盾仍exit0。**P1-ARTIFACT-01**：报告源码SHA与自报不符且原始输入缺失。
- red_team_test_count=30；red_team_pass_count=14（合法正例2+原定负例12）；red_team_fail_count=16；red_team_blocked_count=12（正确拒绝的负例）；p0_open_count=1（生产授权门禁）；p1_open_count=5（工件、schema、语义、过期候选、证据/案例）；p2_open_count=0。安全级别针对拟议生产使用，不代表已部署或已造成真实损害。

## E. 五案例执行分级与真实业务能力
|案例|Buddy标记|ChatGPT独立判定|关键缺口|
|---|---|---|---|
|A 世界观圣经|EXECUTED|**EXECUTED_SELF_REPORTED + RECONSTRUCTED_CODE_TESTED，未独立验证原始冻结输入**|源码SHA错配、原始输入缺失、重大冲突只警告不阻断、授权自述|
|B 章节流水线|DESIGNED|DESIGNED|无实际生成、编辑diff、字数阈值、预算、人工审稿|
|C 分支互动小说|DESIGNED|DESIGNED|无可达性/死路/循环/变量状态引擎，仅简单角色引用|
|D 多语翻译|DOCUMENTED|DOCUMENTED|无授权源稿、翻译输出、术语测评、母语审稿|
|E 影视/音频改编|DOCUMENTED|DOCUMENTED|无权利链矩阵、真实交接包、成本/回滚；未调用声音克隆是合规边界|
- case_status_counts: DOCUMENTED=2, DESIGNED=2, SIMULATED=0, EXECUTED=1（Buddy自述、非完整业务）, INDEPENDENTLY_VERIFIED=0, NOT_TESTED=0；真实商业端到端闭环0/5。
- artifact_reproducibility_verdict=FAIL；core_mve_status=EXECUTED_SELF_REPORTED / RECONSTRUCTED_TESTED；core_mve_independent_replay=FALSE_FOR_ORIGINAL_FROZEN_INPUTS。

## F. SAME_FACTORY_REMEDIATION（旧实验历史参考，不是本次R-10）
|旧问题|Buddy自评|ChatGPT独立判定|证据|
|---|---|---|---|
|HIST-F10-01 NO FAKES误作现行法|RESOLVED|**RESOLVED_NARROWLY / 官方最新状态NOT_VERIFIABLE**|正确改为提案，Part1政策研究；但congress.gov官方状态未直接取得，不能宣称完全法律核验|
|HIST-F10-02 RUN无可复放工件|RESOLVED|**RECURRED**|报告嵌入源码但SHA错配、8份JSON及runner原文缺失|
|HIST-F10-03 官方来源/插件状态混淆|RESOLVED|**RECURRED**|GovTrack被列一手、Adobe Story失效候选、Top5缺实测|
|HIST-F10-04 五案例闭环缺失|PARTIAL|**PARTIAL**|A原型改善，B/C/D/E未执行、字段仍缺|
- 历史参考4项：窄义已解决1、复发2、部分1；不计算本实验正式同厂解决率/评分Δ。本轮**62/100**成为R20正式基线。

## G. CROSS_FACTORY_TRANSFER（R09 F9→R10 F10）
|source_round|source_factory|target_round|target_factory|method_change|baseline_metric|target_metric|observed_metric|verdict|evidence_path|
|---|---|---|---|---|---|---|---|---|---|---|
|R09|F9|R10|F10|T1 缺字段/空输入/类型负例fail-closed|R09三类缺字段/空命令错误接受|R10≥5类拒绝、0相邻fail-open|原定6类×2全部拒绝；新增8类×2中12次错误接受、4次非结构化异常|**PARTIAL_EFFECTIVE**|rounds/R10/INDEPENDENT_RED_TEAM.md|
|R09|F9|R10|F10|T2 官方事实+RUN工件双门禁|R09 5项事实3错，CaseB缺源码/输入|R10≥5事实0错，1/1原始工件SHA一致|抽核9项1错；源码SHA不符、8输入缺失|**FAILED_ARTIFACT / PARTIAL_FACT**|rounds/R10/CHATGPT_AUDIT.md;rounds/R10/WORKBUDDY_REPORT.md|
- 跨厂不比较65→62的分数因果；只比较同类证据门禁。下一轮R11继承最多2项方法：**T1 完整schema与fail-closed相邻负例**；**T2 原始工件三联SHA核验+官方当前产品存续状态核验**。将本轮实际失败输入、预期退出码、SHA冲突及Adobe停用公告具体注入R11实际MCP prompt。

## H. V4质量仪表盘与最终验收
- fact_check_sample_count=9; material_fact_error_count=1; fact_gate_verdict=PARTIAL; case_status_counts={DOCUMENTED:2,DESIGNED:2,SIMULATED:0,EXECUTED:1,INDEPENDENTLY_VERIFIED:0,NOT_TESTED:0}; core_mve_status=EXECUTED_SELF_REPORTED/RECONSTRUCTED_TESTED; core_mve_independent_replay=FALSE_FOR_ORIGINAL_INPUTS; artifact_reproducibility_verdict=FAIL; red_team_test_count=30; red_team_pass_count=14; red_team_blocked_count=12; red_team_fail_count=16; p0_open_count=1; p1_open_count=5; p2_open_count=0; claims_overstated_count=3 (全工件可复放、官方事实0错、一级官方来源≥10); production_readiness=NOT_READY。
- A WORKBUDDY_SELF_REPORT: 6/6负例、7/7官方事实、完整工件自评通过；B CHATGPT_INDEPENDENT_AUDIT: 原定负例通过，但新负例16次未满足，SHA错配、官方候选过期；C FINAL_ACCEPTANCE: **FAIL（V4质量门禁）**，不影响“真实MCP完成、Git原文交付成功”的独立结论。
- R10交付状态 **DONE / FULL_REPORT_GIT_VERIFIED / INDEPENDENT_AUDIT_GIT_VERIFIED / V4_QUALITY_FAIL / NOT_READY_FOR_PRODUCTION**。下一轮R11仍按固定计划推进F1，不重复派R10，不更改其他任务或生产。
