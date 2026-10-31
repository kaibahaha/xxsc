# R17 F7｜独立质量审计（待真实报告）
- WORKBUDDY_SELF_REPORT=PENDING，job_id=4314c14e9faa4d80，只有submit确认，无研究正文。
- CHATGPT_INDEPENDENT_AUDIT=NOT_EVALUABLE；FINAL_ACCEPTANCE=PENDING。
- same_factory_baseline_round=R07；R07 score=68/100（17/17/13/13/8）；R17五维=NOT_EVALUABLE；same_factory_score_delta=NOT_EVALUABLE。
- SAME_FACTORY_REMEDIATION: D1 DOI/撤稿、D2 SHA/stdout、D3负例/统计假设均已完整注入实际prompt，RESOLVED/PARTIAL/RECURRED/NOT_VERIFIABLE待正文与独立核查。
- CROSS_FACTORY_TRANSFER: T1域名/权利可信锚与红队、T2学术许可分层已注入，实施结果NOT_VERIFIED；不得用R16总分与R17总分做因果比较。
- fact_check_sample_count=0（报告未到）；material_fact_error_count=NOT_EVALUABLE；fact_gate_verdict=NOT_EVALUABLE；case_status_counts=NOT_EVALUABLE；core_mve_status=PENDING；core_mve_independent_replay=NOT_VERIFIED；artifact_reproducibility_verdict=NOT_VERIFIED；red_team_test_count=0；red_team_pass_count=0；red_team_blocked_count=0；p0_open_count=UNKNOWN；p1_open_count=UNKNOWN；p2_open_count=UNKNOWN；claims_overstated_count=NOT_EVALUABLE；production_readiness=NOT_ASSESSED。
- 不因派单成功、文档预归档或Buddy自评给分。取得真实报告后再补审并保留本记录。


## R17 FINAL｜三方结论分离（2026-11-01）
**WORKBUDDY_SELF_REPORT**：唯一Job 4314c14e9faa4d80 DONE 291s、云端返回26062字符（包含前导进度），完整BEGIN_FULL_REPORT/END_FULL_REPORT 25909字符；Buddy称11负例0 fail-open、5文件SHA一致、D1/D2/D3均RESOLVED、5官方许可事实无错。外部检索0次，未实时核官方页。MCP全文Git commit 2e095bcb32abb88fe4aa9ee0cdb3df692da761fc / blob 04ae3615ef0d8f36cb04993c089990d30562da48，独立逐字回读PASS。
**CHATGPT_INDEPENDENT_AUDIT**：实际读取Git全文、从报告提取源码11813字符并Git归档；独立JS SHA256（先经abc标准向量验证）计算两种换行均与Buddy声称源码哈希不符；报告缺4份冻结JSON原始内容和完整stdout/stderr，不能原始MVE字节级重放。独立Python忠实重实现报告函数逻辑并真实运行10个新增权限/身份/DOI相邻边界，**8/10错误ADMIT，2/10正确阻断**；3个统计异常边界发现λ=0抛ValueError、非法method和bool obs错误接受。官方网页独立核验8项高影响事实，3项实质许可/内容托管错误。全部输入输出与来源见INDEPENDENT_SECURITY_PROBES.md（commit 24fd403bdb71c87ce5a1815b34ebb7118df53a9b / blob 548fa811d2dcca85c7247f048287f3e5401a5cbf，独立回读PASS）。原始Python脚本未由ChatGPT字节级直接执行，只有逻辑忠实复刻，不能冒充独立原文件重放。
**FINAL_ACCEPTANCE=FAIL**（FACT_GATE_FAIL + P0_SECURITY_FAIL + ARTIFACT_INTEGRITY_FAIL），研究资料可保留供整改，PRODUCTION_READINESS=NOT_READY。
### 固定五维100分与同厂R07比较
|维度|R07基线|R17独立评分|Δ|原因|
|---|---:|---:|---:|---|
|证据准确性25|17|16|-1|DOI/撤稿ID纠正，但OpenAlex全文托管、派生输出许可、Crossref元数据许可泛化3实错，0次远端检索|
|战略价值20|17|18|+1|科研可信证据门禁、学术数据与合规服务具跨厂价值；无真实付费客户/ROI|
|操作技巧20|13|12|-1|有11813字符真实源码块与Python标准库门禁，然而4 JSON输入未交、stdout仅摘要、源码SHA不符，无法原文件重放|
|五案例20|13|12|-1|A DOCUMENTED，B/E自报运行，D模拟自报运行，C未测；独立数学与逻辑抽查不等于完整MVE重放，商业E2E 0|
|风险与真实性15|8|4|-4|8/10新增边界fail-open，授权字符串false可被接受，伪DOI/伪撤稿可自动ADMIT；自评“安全全通过/字节一致”证据不支持|
|**总分**|**68**|**62**|**-6**|任务难度、证据覆盖不同，分数下降不等于模型整体能力下降；P0安全门禁直接FAIL|
### 官方事实门禁
8项抽查/3项实质错误/FACT_GATE_FAIL：①砷基细菌原论文10.1126/science.1197258与撤稿公告10.1126/science.adu5488，PubMed PASS；②OpenAlex元数据CC0 PASS；③OpenAlex“不托管全文”错误，官方 https://help.openalex.org/access/fulltext/ 明确缓存50M+全文PDF；④OpenAlex“所有output/派生数据=CC0”无条件错误，第三方全文和图表按单篇许可；⑤Crossref“全部metadata统一CC0”过度泛化，官方 https://www.crossref.org/documentation/retrieve-metadata/ 区分不受版权的书目事实、CC0生成数据、受版权保护摘要；⑥PMC OA逐篇许可PASS https://pmc.ncbi.nlm.nih.gov/tools/openftlist ；⑦RDKit当前pip install rdkit PASS https://www.rdkit.org/docs/Install.html ；⑧IEEE IES 2027免费报名/截止2026-12-31 PASS https://ai.ieee-ies.org/qa/ （ChatGPT补核，Buddy本轮未提）。若对#5采用更宽容口径，#3/#4仍满足≥2项实质错FAIL。
### SAME_FACTORY_REMEDIATION｜R07→R17
|缺陷|旧证据|新实施|独立裁决|
|---|---|---|---|
|D1 P0 DOI/撤稿|R07错误DOI10.1126/science.332.1163|R17改为正确原文/撤稿DOI；PubMed独立核对|**PARTIAL**：ID已纠正，伪DOI只靠一个denylist、伪造retraction authority仍可ADMIT，真实API关系未核|
|D2 P0 源码SHA/stdout|R07源码SHA不匹配、stdout虚增文本|R17自报hashlib与sha256sum一致、源码随报告返回|**RECURRED**：Buddy声称b5aee31b…，ChatGPT提取代码SHA有换行f4f33662…、无换行b7b9289b…；4冻结JSON/完整stdout缺失|
|D3 P0 真负例/H0|R07单位/seed仅print，H0/H1不清|R17显式H0=λ5、H1=λ8，独立数学复算正确；有结构化拒绝|**PARTIAL**：λ=0崩溃、method任意字符串OK、obs=True当1，安全边界未过；原始脚本未独立运行|
- same_factory_baseline_round=R07; same_factory_defects_count=3（主整改）; resolved_count=0; partial_count=2; recurred_count=1; same_factory_score_delta=-6; key_error_recurrence_rate=1/3（严格旧缺陷复发口径）；new_security_fail_open=8/10; new_p0≥2。额外P1：旧rdkit-pypi文档命令已纠正；OpenAlex匿名10万/天旧无据不再宣称；K-Dense版本未知诚实标注。
### CROSS_FACTORY_TRANSFER｜R16 F6→R17 F7
T1来源/权利可信锚：**实际注入**4804字符FEEDBACK全文（5017字符MCP prompt），hostname HTTPS/精确域名能阻断2项老式伪造，但8项新增相邻安全输入仍被错误ADMIT；**PARTIAL_IMPLEMENTED / FAILED_SECURITY**。T2许可分层：**实际注入**，部分区分metadata/abstract/fulltext，但独立8抽3项实错；**PARTIAL_IMPLEMENTED / FAILED_FACT_ACCURACY**。不能把R16 67分与R17 62分作跨厂因果比较。
### 五案例与MVE证据分级
A DOI/撤稿=DOCUMENTED（官方身份核验由ChatGPT独立完成，Buddy未联网API）；B统计=EXECUTED_SELF_REPORTED / INDEPENDENT_MATH_CHECK_ONLY；C RDKit=NOT_TESTED；D单位=SIMULATED_SELF_REPORTED / INDEPENDENT_LOGIC_ONLY；E证据门禁=EXECUTED_SELF_REPORTED / INDEPENDENT_SECURITY_REIMPLEMENTATION_FAIL。INDEPENDENTLY_VERIFIED完整原始商业案例0/5，真实科研数据/硬件校准0，商业E2E 0。
- fact_check_sample_count=8; material_fact_error_count=3; fact_gate_verdict=FAIL; case_status_counts={DOCUMENTED:1,EXECUTED_SELF_REPORTED:2,SIMULATED_SELF_REPORTED:1,NOT_TESTED:1,INDEPENDENTLY_VERIFIED:0}; core_mve_status=EXECUTED_SELF_REPORTED_BUT_SECURITY_FAIL; core_mve_independent_replay=LOGIC_REIMPLEMENTATION_ONLY; artifact_reproducibility_verdict=FAILED_SOURCE_SHA_AND_MISSING_FROZEN_INPUTS; red_team_test_count=10; red_team_pass_count=2; red_team_fail_open_count=8; red_team_blocked_count=0; p0_open_count>=2; p1_open_count>=4; p2_open_count=UNKNOWN; claims_overstated_count>=3; production_readiness=NOT_READY。
### 全球机会与下轮整改
ChatGPT独立核验IEEE IES GenAI Challenge 2027（2026-12-31截止、免费报名，但会议作者注册费不由旅费补助承担）及OpenAlex免费API $1/day（验证邮箱、无支付方式、未领取），去重纳入OPPORTUNITY_LEDGER。Buddy列10项云厂商/竞赛候选但外部检索0、无当前开放/资格/规则证据，全部UNVERIFIED/OBSERVE，不计已可行动。registration_attempted=0; registration_completed=0; resource_claimed=0。
R18 F8机器人必须继承最多2项：①可信授权/审批/安全停机必须严格类型和来源验证，未知默认拒绝，新增相邻负例不得仅自选通过；②原始源码+全部冻结输入+完整stdout/stderr+实际SHA独立字节复算，缺一不得声称INDEPENDENTLY_VERIFIED。