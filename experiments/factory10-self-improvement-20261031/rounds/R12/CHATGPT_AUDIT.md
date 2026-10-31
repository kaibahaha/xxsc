# R12 F2｜CHATGPT_AUDIT（仅派单前独立预审，正式评分待报告）
## A. WORKBUDDY_SELF_REPORT
NOT_YET_RETURNED。唯一job_id=9d502bcdaf6e40bc，MCP真实submit已接受，list明确QUEUED。不可把Job ID、[running]泛状态或Git反馈提交当成研究完成。
## B. CHATGPT_INDEPENDENT_AUDIT
真实读取R02 F2原始完整报告、CHATGPT_AUDIT、ADAPTATION、FEEDBACK、STATUS，以及R11 F1状态/审计/适应、R10 F10独立审计与旧实验README/F2审计。R02正式基线76/100(21/18/14/14/9)，本轮差值NOT_EVALUABLE；R11尚无正文，跨厂迁移标DELAYED_BASELINE并采用R10的具体失败数据。
本轮Git反馈4531字符已独立回读且全文实际注入4953字符MCP prompt；三项同厂整改与两项跨厂方法均有原始证据、验收阈值、可证伪条件，实际效果待WorkBuddy结果。另通过公开官方文档独立核验F2资源机会，结果写OPPORTUNITY_RADAR.md与ACTION_CHECKLIST.md；该研究与Buddy质量门禁分开。
## 固定五维评分及同厂同比
|维度|R02正式基线|R12|Δ|
|---|---:|---|---|
|证据25|21|NOT_EVALUABLE|NOT_EVALUABLE|
|战略20|18|NOT_EVALUABLE|NOT_EVALUABLE|
|技巧20|14|NOT_EVALUABLE|NOT_EVALUABLE|
|五案例20|14|NOT_EVALUABLE|NOT_EVALUABLE|
|风险真实性15|9|NOT_EVALUABLE|NOT_EVALUABLE|
|总分100|76|NOT_EVALUABLE|NOT_EVALUABLE|
## SAME_FACTORY_REMEDIATION
|缺陷|R02具体证据|本轮已实际注入的整改|结果|
|---|---|---|---|
|P0-F2-R12-01|R02审计§二 headless -p/dontAsk/-y权限冲突、worktree非OS隔离|当前CLI help、官方版本、3类越权拒绝、不得使用通配删除|NOT_VERIFIABLE_PENDING|
|P1-F2-R12-02|R02审计§二 GPL/AGPL过宽、import即违规、CVE/secret假样本|5许可×4行为矩阵、真实规则ID、3正3负与误报/漏报|NOT_VERIFIABLE_PENDING|
|P1-F2-R12-03|R02审计§一/§五危险rm -rf、恢复状态机未跑、成本≈0|隔离MVE、安全唯一目录清理、429/TTL/孤儿状态机、真实成本公式|NOT_VERIFIABLE_PENDING|
- same_factory_baseline_round=R02; same_factory_defects_count=3 (本轮重点); resolved_count=NOT_EVALUABLE; recurred_count=NOT_EVALUABLE; same_factory_score_delta=NOT_EVALUABLE; cross_hour_transfer_verdict=INJECTED_NOT_TESTED。
## V4质量仪表盘
fact_check_sample_count=0 (Buddy报告待返回); material_fact_error_count=NOT_EVALUABLE; fact_gate_verdict=NOT_VERIFIED; case_status_counts=NOT_EVALUABLE; core_mve_status=PENDING; core_mve_independent_replay=NOT_VERIFIED; artifact_reproducibility_verdict=NOT_VERIFIED; red_team_test_count=0; red_team_pass_count=0; red_team_blocked_count=0; p0_open_count=NOT_EVALUABLE; p1_open_count=NOT_EVALUABLE; p2_open_count=NOT_EVALUABLE; claims_overstated_count=NOT_EVALUABLE; production_readiness=NOT_ASSESSED。
## C. FINAL_ACCEPTANCE
PENDING / NOT_EVALUABLE；工具提交成功不等于研究质量通过，机会规则核验不等于申请领取。等待完整原文后至少5项Buddy高影响事实独立抽核、MVE源码与冻结输入SHA复算、normal/-O安全负例、五案例状态和三缺陷复测。
## 独立官方预检：R02关键缺陷与现行文档
2026-10-31由ChatGPT实际访问CodeBuddy官方具体文档，以下5项为**前置独立事实核验**，不是尚未返回的R12 Buddy报告抽样；因此V4 Buddy fact_check_sample_count仍为0。
1. `-y` / `--dangerously-skip-permissions` 等价`bypassPermissions`，不是`dontAsk`。官方 https://www.codebuddy.cn/docs/cli/permission-modes （启动参数/非交互章节），PASS。
2. 官方同页展示 `codebuddy -p --permission-mode dontAsk`，同时Headless页 https://www.codebuddy.cn/docs/cli/headless 明确在`-p`执行需要授权的文件/命令/网络操作时须`-y`；这属于**需区分动作是否预授权及实际CLI版本的文档语境差异**，不能凭两页静态文字断言某个命令组合必定安全可运行。实际CLI命令仍NOT_TESTED。
3. `dontAsk` 对未预批准的Edit/Bash/其他操作直接拒绝；`bypassPermissions`跳过大部分审批但前置deny/ask仍可能生效。官方 https://www.codebuddy.cn/docs/cli/permission-modes ，PASS。
4. `--add-dir`把额外目录加入信任范围，不是限制读取的OS安全沙箱。官方 https://www.codebuddy.cn/docs/cli/permissions ，PASS。
5. Worktree官方 https://www.codebuddy.cn/docs/cli/worktree 描述多个工作目录/共享Git对象、修改隔离；未证明独立进程身份/网络/内核访问控制。结论“不能据此宣称防作弊OS隔离”是证据边界判断，PASS；但实际跨目录访问阻断仍NOT_TESTED。
这5项不替代R12 Buddy原始报告的≥5项战略事实抽核，也不证明MVE、权限拒绝或生产安全已通过。


## R12最终独立审计（2026-10-31，取代上文PENDING预审，原预审保留为审计历史）
### A. WORKBUDDY_SELF_REPORT
唯一job=9d502bcdaf6e40bc，DONE/905秒；MCP返回BEGIN_FULL_REPORT/END_FULL_REPORT之间17388字符原始正文，协调者通过GitHub连接器写入WORKBUDDY_REPORT.md，commit=4f011748557a242c87094f70d295cb0d09ca9180，blob=218ae196b108033f37539e92455f02f211d4131a，**全文回读exact PASS**。Buddy自述两MVE各22/22、红队7项、官方8事实0错；其自述不等于独立验证。
### B. CHATGPT_INDEPENDENT_AUDIT：发现P0安全拒绝失效
ChatGPT从R12报告§A.1内联源码重建同一validate函数，在独立Python 3.13内存执行，另用compile(...,optimize=2)复核优化模式（并非远端CLI原始进程，也未取得远端实际源码文件字节）。冻结基线：version="1", allowed_root="/tmp/scope", rules=[{id:"r1",path:"/tmp/scope/game",action:"write"}], budget_tokens=100, mode="dontAsk"。以下是新增相邻边界的**真实函数返回**（normal/-O一致），非法应REJECTED但实际ACCEPTED/ok=True：
|独立负例|实际normal|实际-O|根因|
|---|---|---|---|
|relative_path_outside: rules.path="sensitive_file"（相对路径不在allowed_root内）|ACCEPTED True|ACCEPTED True|仅对os.path.isabs(path)做范围校验，所有相对路径未绑定根|
|unknown_mode: mode="anything"|ACCEPTED True|ACCEPTED True|mode只验证字符串，不校验枚举|
|negative_budget: budget_tokens=-999|ACCEPTED True|ACCEPTED True|只检查上限，不检查非负|
|sandbox_string_true: mode="bypassPermissions", sandbox="false"|ACCEPTED True|ACCEPTED True|bool("false")为True，未强制布尔类型/OS隔离证明|
|empty_rules: rules=[]|ACCEPTED True|ACCEPTED True|未校验最小规则数或默认拒绝策略|
|control abs_outside: rules.path="/tmp/outside"|REJECTED False|REJECTED False|原有绝对路径规则有效|
|control valid|ACCEPTED True|ACCEPTED True|合法基线通过|
- 共5种新非法边界×2=10/10 **错误接受**；2种控制×2=4/4符合预期。此为函数级独立执行；根据main()对ok=True返回0的代码可推断CLI会错误exit0，但本轮独立子进程调用曾阻塞/中断，**不把推断exit0冒充真实CLI退出码**。无真实文件修改，安全测试隔离。
- P0-NEW-R12-01：将用户自报sandbox字符串当可信安全边界、相对路径未约束导致策略校验fail-open；生产安全门禁立即FAIL/NOT_READY，禁止部署。
- P1-NEW-R12-02：未知mode、负预算、空规则可放行；需schema枚举/数值下限/默认拒绝，并复测相邻边界。
- P1-NEW-R12-03：MVE-2 simulate()未调用validate_contract()、cleanup()把合同中自报_created_files当文件归属证据；只能称合成模拟，不能当真实租约/删除安全。
- 源码/冻结fixture/log实际远端文件未通过Git交付；报告内联文本虽可重建逻辑，远端SHA表没有原始文件独立重算；artifact_reproducibility=PARTIAL_NOT_INDEPENDENTLY_HASH_VERIFIED。
### 五项以上高影响官方事实独立抽查（访问2026-10-31）
|原主张|官方具体来源|适用范围|结论|
|---|---|---|---|
|-y等价bypassPermissions|https://www.codebuddy.cn/docs/cli/permission-modes|CodeBuddy CLI现行文档|PASS|
|dontAsk未预批准直接拒绝|https://www.codebuddy.cn/docs/cli/permission-modes|CLI模式|PASS|
|Headless需-y执行授权操作，但不等于安全full pass|https://www.codebuddy.cn/docs/cli/headless|CLI非交互|PASS（需保留语境）|
|worktree不是OS安全边界|https://www.codebuddy.cn/docs/cli/worktree|文件工作区隔离|PASS（不可推断进程/网络强隔离）|
|Copilot Free每月2000补全|https://docs.github.com/en/copilot/get-started/plans|个人Free计划|PASS（该文档个人计划§Inline suggestions明确2000）|
|JetBrains个人非商业OSS IDE免费、成熟OSS单独申请|https://www.jetbrains.com/community/opensource/|产品/个人或成熟维护者不同资格|PASS|
|Copilot Free“商用需Pro/Business”|https://docs.github.com/en/enterprise-cloud@latest/billing/concepts/product-billing/github-copilot-licenses|个人与组织许可需区分|NOT_VERIFIABLE/P1：官方只称Free供个人、非组织；不能据此断言个人商业项目一律必须付费，撤销强制付费结论|
- fact_check_sample_count=7；verified_pass_count=6；material_fact_error_count=0已证实错误，unsupported_material_claim_count=1；fact_gate_verdict=NOT_VERIFIABLE（因关键商用许可断言缺具体条款；不能宣称7/7 PASS）。源码P0是安全实现缺陷，不计入“官方事实错误”分母。
### SAME_FACTORY_REMEDIATION
|旧问题|独立结果|证据|
|---|---|---|
|R02 P0权限/OS边界混淆|PARTIAL：官方CLI矩阵较清晰，但MVE中sandbox="false"可绕拒绝、live权限拒绝未跑|R12源码§A.1 + 本次独立边界|
|R02 P1 GPL/AGPL与供应链假阳性|PARTIAL：文字上修正import≠违法，semgrep缺失，3正3负扫描未真实执行|R12 §B2/C/D|
|R02 P1危险清理/状态机/成本|PARTIAL：不再建议rm -rf通配，状态机仅SIMULATED；模拟归属由合同自报，成本仍UNKNOWN|R12 §A.2/B3/C|
- same_factory_baseline_round=R02; same_factory_defects_count=3; resolved_count=0; partial_count=3; recurred_count=1（安全边界仍有fail-open同类风险）; strict_resolved_rate=0/3；新发现3组缺陷。
### 固定五维评分（真实报告+独立反例后）
|维度|R02|R12|Δ|
|---|---:|---:|---:|
|证据25|21|19|-2|
|战略20|18|18|0|
|操作技巧20|14|11|-3|
|五案例20|14|12|-2|
|风险及真实性15|9|5|-4|
|合计100|76|65|-11|
理由：两份源码/边界矩阵/机会资料比基线更详，但真实扫描/PR/OS隔离未跑，五案例仅E模拟；独立新增5类fail-open击穿核心安全声明，故研究安全质量下降。R02与R12任务难度及审计深度不同，-11不代表所有研究能力退化，也不能用跨厂总分推断方法因果。
### V4质量仪表盘最终
fact_check_sample_count=7; material_fact_error_count=0 confirmed, unsupported_material_claim_count=1; fact_gate_verdict=NOT_VERIFIABLE; case_status_counts={DOCUMENTED:0,DESIGNED:2,SIMULATED:1,EXECUTED:0,INDEPENDENTLY_VERIFIED:0,NOT_TESTED:2}; core_mve_status=SIMULATED_WITH_P0_FAIL_OPEN; core_mve_independent_replay=PARTIAL_FUNCTION_LEVEL; artifact_reproducibility_verdict=PARTIAL; red_team_test_count=14 independent function calls (7 fixtures×2 modes), red_team_pass_count=4 controls, red_team_blocked_count=0, red_team_unexpected_accept_count=10; p0_open_count=1,p1_open_count=2,p2_open_count=0; claims_overstated_count=2 (安全fail-closed完整性、Copilot商用强制付费无依据); production_readiness=NOT_READY。
### C. FINAL_ACCEPTANCE
**FAIL**（P0安全fail-open；禁止生产部署）。Git报告交付PASS、官方事实抽核大部分PASS、研究质量FAIL、业务就绪NOT_READY是四个不同结论。R13跨厂迁移T1/T2的prompt在R12独立审计完成前已提交，故R13后续审计必须加入本P0反例作为新的相邻边界检验；不能说R12方法已证明有效。
