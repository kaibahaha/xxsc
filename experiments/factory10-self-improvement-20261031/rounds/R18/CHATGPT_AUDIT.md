# R18 F8｜独立审计预注册（真实报告尚未返回）
- WorkBuddy unique job e06ced6b21e84758 = PENDING；只有submit回执不代表执行成功；WORKBUDDY_SELF_REPORT=PENDING；CHATGPT_INDEPENDENT_AUDIT=NOT_EVALUABLE；FINAL_ACCEPTANCE=PENDING。
- same_factory_baseline_round=R08，R08 73/100 (19/18/15/13/8)；R18五维/总分=NOT_EVALUABLE；same_factory_score_delta=NOT_EVALUABLE；D1急停-O绕过、D2官方型号/价格/版本、D3五案例无端到端三项整改已完整注入4872字符实际MCP prompt，结果待审。
- CROSS_FACTORY_TRANSFER：R17 F7 8/10相邻授权边界fail-open及源码SHA不符/4JSON缺失，M1严格授权双模式红队、M2字节完整性均已注入；效果NOT_VERIFIED，不跨厂比总分因果。
- fact_check_sample_count=0; material_fact_error_count=NOT_EVALUABLE; fact_gate_verdict=NOT_EVALUABLE; case_status_counts=NOT_EVALUABLE; core_mve_status=PENDING; core_mve_independent_replay=NOT_VERIFIED; artifact_reproducibility_verdict=NOT_VERIFIED; red_team_test_count=0; red_team_pass_count=0; red_team_blocked_count=0; p0_open_count=UNKNOWN; p1_open_count=UNKNOWN; p2_open_count=UNKNOWN; claims_overstated_count=NOT_EVALUABLE; production_readiness=NOT_ASSESSED。
- OPPORTUNITY_RADAR独立官方初筛5候选、4新增去重台账、资格确认0、注册/领取0；机会不纳入五维研究质量加分。


## R18 FINAL｜三方分离的独立审计（2026-11-01）
**WORKBUDDY_SELF_REPORT**：唯一job e06ced6b21e84758 DONE，完整BEGIN_FULL_REPORT/END_FULL_REPORT 35661字符，声称官方6事实0错误、14个红队案例全过、双模式急停不可绕过、2源码/13JSON/全部stdout和输出SHA一致，C导航MVE SIMULATED执行，D1/D2修复、D3部分修复；无真机/摄像头/登录/付费。MCP原文Git commit e69c61b1f323a6d360350854043ee696597cbd81、blob 26369c989c48336f7080de7182d80cdfcb51c2fc，独立逐字回读PASS。
**CHATGPT_INDEPENDENT_AUDIT**：真实读取Git报告及R08/R17，官方独立7项事实抽查2实质错误1不可确认；独立V8 SHA256标准向量核对后，2/2源码哈希一致，10个多行JSON原文字节SHA一致、3内联JSON按2空格格式重建匹配；报告展示的normal.out日志SHA与自称SHA不符，optimize.out和P1原始文件未给完整字节。15件提取/重建工件在本轮artifacts/通过GitHub 15/15独立回读，但不是原始运行时文件。独立Python3按报告A*逻辑重实现，冻结6x6路径10节点与自报完全一致，代价9.414213562373096；按原代码门禁逻辑重实现9个新增相邻安全探针，8项ADMITTED、1项非受控TypeError。完整证据见INDEPENDENT_SECURITY_PROBES.md（Git commit 52531b68ab31c727cb510ca7cf4115b50ced574a / blob 9d6939b0d4983a20c4a96d9387f83a4fcd95a249，独立回读PASS）。**没有直接在ChatGPT环境运行原始f8_contract.py/f8_redteam.py文件，禁止称INDEPENDENTLY_VERIFIED。**
**FINAL_ACCEPTANCE=FAIL**（FACT_GATE_FAIL、SAFETY_TRUST_CHAIN_FAIL、ARTIFACT_OUTPUT_INTEGRITY_FAIL），工具调用和Git交付成功不等于研究质量通过；production_readiness=NOT_READY，绝不可连接真实机器人。

### 固定五维100分与R08同厂比较
|维度|R08基线|R18独立评分|Δ|主要证据|
|---|---:|---:|---:|---|
|证据25|19|18|-1|源码SHA2/2、13JSON可重建；7官方事实2实错，normal stdout SHA不一致，优化日志/P1原始字节缺失|
|战略20|18|18|0|导航安全契约与机器人开源试点价值明确，但无真实客户/硬件/签名认证|
|操作技巧20|15|16|+1|A*、严格bool/estop、双模红队源码完整，提取工件可供后续重放；但源码原件未独立执行|
|五案例20|13|15|+2|C导航SIMULATED_SELF_REPORTED，独立路径数学重实现吻合；A/B/D/E仍DESIGNED/NOT_TESTED，商业E2E=0|
|风险真实性15|8|4|-4|source标签可伪造、approver未验、无签名/nonce/防重放、未知字段和非整数网格可被接受；自报安全全通过过度外推|
|**总分**|**73**|**71**|**-2**|覆盖与难度不同，分数变化不是模型能力因果结论；P0与事实门禁仍FAIL|

### 官方事实门禁
- fact_check_sample_count=7; material_fact_error_count=2; not_verifiable_count=1; fact_gate_verdict=FAIL。F1 ROS2 Range PASS；F2 TB4标准OAK-D-Pro/IMX378 PASS；F3 OAK-D-Lite双目写“OV251”实为OV7251 **P1错误**；F4当前平台写Ubuntu20.04+ROS2而官方当前预装Ubuntu24.04/Jazzy、20.04/Galactic已EOL **P1错误**；F5 D435 $314等公开价PASS（不含税运费）；F6 Nav2 OccupancyGrid API概括仅项目链接NOT_VERIFIABLE；F7 FOSDEM机器人CFP 11/23截止PASS。具体官方URL与版本见INDEPENDENT_SECURITY_PROBES.md §A。

### SAME_FACTORY_REMEDIATION｜R08→R18
|defect|R08事实缺陷|R18变化|独立状态|
|---|---|---|---|
|D1 P0 assert急停-O绕过|R08 -O estop exit0|R18源码改显式if/raise，Buddy自报双模DENY，独立静态可确认不再依赖assert|**PARTIAL**：特定漏洞逻辑已修，但原始源码双模未独立直接运行，可信授权链仍有P0缺口|
|D2 P1官方版本/型号/价格|ROS1 Fuerte误当ROS2、TB4相机泛化、D435 $179|这三项表面纠正；却新错OV251/OV7251、Ubuntu20.04当前EOL，7抽2实错|**RECURRED**：版本/型号事实核验质量仍未过门禁|
|D3 P1五案例无E2E|R08 A-E均未端到端|R18 C冻结网格A*路径数学独立复算一致，SIMULATED；其他4个仍未跑，原始stdout SHA不符|**PARTIAL**：完成1个模拟案例的部分证据，非商业E2E或原始文件独立重放|
- same_factory_baseline_round=R08; same_factory_defects_count=3; resolved_count=0; partial_count=2; recurred_count=1; same_factory_score_delta=-2; key_error_recurrence_rate=1/3；new_p0>=2（可信审批/签名与重放），new_p1>=5（型号/OS、工件日志、字段/坐标类型等）。相邻9探针8个逻辑ADMITTED，1个TypeError，不能把Buddy自选13个负例PASS外推为全部安全边界PASS。

### CROSS_FACTORY_TRANSFER｜R17 F7→R18 F8
- M1严格bool/可信授权/默认拒绝：**实际注入**R18 FEEDBACK 4688字符及MCP 4872字符；源码确实拒绝str("false")/estop，并用显式if/raise；但新9个相邻逻辑探针8个被放行，可信来源仅字符串白名单无签名，**PARTIAL_IMPLEMENTED / FAILED_TRUST_CHAIN**。R17 8/10与R18 8/9是不同攻击集，不能称错误率改善。
- M2完整原始工件：**实际注入**同上；源码2/2 SHA匹配、13 JSON可重建，优于R17源码SHA不符；但R18 normal.out展示SHA不符、优化/P1原始字节未交，**PARTIAL_IMPLEMENTED / OUTPUT_INTEGRITY_FAIL**。跨厂仅比较源码SHA匹配率与证据缺口，不比较总分因果。

### 五案例与质量仪表盘
- case_status_counts={DOCUMENTED:0,DESIGNED:4,SIMULATED:1,EXECUTED:0,INDEPENDENTLY_VERIFIED:0,NOT_TESTED:0}（A/B/D/E DESIGNED但执行NOT_TESTED，C SIMULATED self-reported + independent algorithmic reimplementation）。
- core_mve_status=SIMULATED_SELF_REPORTED_WITH_ALGO_RECALC_PASS_BUT_SECURITY_FAIL; core_mve_independent_replay=LOGIC_REIMPLEMENTATION_ONLY_NOT_ORIGINAL_FILE; artifact_reproducibility_verdict=PARTIAL_SOURCE_SHA_2_OF_2_OUTPUT_SHA_MISMATCH; red_team_test_count=9（ChatGPT独立新增逻辑探针）; red_team_pass_count=0; red_team_blocked_count=0; red_team_failopen_count=8; red_team_unhandled_exception_count=1; buddy_red_team_self_report=13_NEGATIVES_PASS_PLUS_1_POSITIVE（双模式自述）；p0_open_count>=2; p1_open_count>=5; p2_open_count>=1; claims_overstated_count>=3; production_readiness=NOT_READY。
- opportunities_found=5（ChatGPT独立官方初筛），officially_verified_count=5（仅公开规则），currently_open_count=3，eligibility_confirmed_count=0，P0=0/P1=2/P2=3，actionable_count=0，registration_attempted=0，registration_completed=0，resource_claimed=0，expired_or_invalid_count=1（排除ARM2026）；NVIDIA Inception按URL去重，新增全球台账4项；机会准确性独立于100分。

### 下一轮R19 F9验证重点
①P0可信身份/审批签名、nonce防重放、未知字段/整数栅格严格校验，至少8个相邻安全探针0 fail-open，不能仅靠source字符串；②精确当前型号/传感器料号/支持OS生命周期/计费单位，至少5官方事实0错，同时保存可复算的完整stdout/输出原始字节与SHA。若R19未获得独立报告则DELAYED_BASELINE，禁止声称有效。
