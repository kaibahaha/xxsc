# R17 F7｜ChatGPT独立安全反例、字节完整性与事实门禁证据
- 来源：真实云端Job 4314c14e9faa4d80 DONE，WORKBUDDY_REPORT.md Git blob 04ae3615ef0d8f36cb04993c089990d30562da48 独立回读PASS。Buddy自称11负例全通过、5文件SHA一致、源码+冻结JSON+完整stdout已交付。
- ChatGPT实际操作：从Git完整报告提取Python源码块11,813字符，保存为artifacts/mve_r17f7_EXTRACTED_FROM_REPORT.py（末尾单换行11,814字符，Git blob b10362852bf4258d4a1e0edc828c6d87c8844886，回读PASS）；用独立JavaScript SHA256实现计算两种换行的源哈希，先用标准测试向量sha256("abc")=ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad验证算法。再在独立Python环境按报告源码函数逐行逻辑重实现review_claim/classify_source/validate_doi/poisson_significance，实际运行10个授权/身份/引用边界和3个统计边界；**没有在ChatGPT环境字节级直接执行原始mve_r17f7.py**，故等级为INDEPENDENT_LOGIC_REIMPLEMENTATION，不可冒充ORIGINAL_SOURCE_RUNTIME_REPLAY。
## A. 字节级SHA256不匹配（P0-ARTIFACT-01）
|对象|SHA256|证据|
|---|---|---|
|Buddy声称远端实际mve_r17f7.py|b5aee31b0bb423b99e4691c768d9f7c7ee7f62f967bbf33031ce4cdb3d1c939a|WORKBUDDY_REPORT §4.3，自述|
|报告Python代码块，无末尾换行|b7b9289b2252c1261f4321c66c381dea62cf66eb9fc5ddf4e8546defc9420b5a|ChatGPT独立SHA256|
|报告Python代码块，单末尾换行|f4f3366243eedf48311bc09bec01e42bb89474244a7b28dc372871a012a82c75|ChatGPT独立SHA256|
- 两种常见字节解释均与Buddy声称的b5aee...不同。不能推断Buddy远端文件一定被篡改，但可严格判定**报告交付源码与其所称实际文件SHA不匹配**，D2“0哈希差/可字节级重放”不成立。
- 报告§4.1仅**列出**t1_claims.json、d1_dois.json、d3_inputs.json、units.json四个文件名及各自SHA；未给这四个JSON文件的完整字节内容；报告还误称“5个冻结JSON”，实际4个JSON+1个Python。§4.2仅给“stdout节选关键结论”，没有完整原始stdout/stderr。故即使源码可读，也无法按报告命令独立运行原始MVE或核对声称的4个输入SHA、stdout逐字一致。ARTIFACT_REPRODUCIBILITY=FAILED / ORIGINAL_RUNTIME_NOT_REPLAYED。
## B. ChatGPT独立Python忠实逻辑复刻：10个新安全相邻边界
所有测试基于报告中实际review_claim/classify_source/validate_doi函数条件分支，基础source_url=https://pubmed.ncbi.nlm.nih.gov/21127214/，assertion="This paper is valid"，rights="open"；独立Python环境真实执行函数逻辑。对错误允许的8项，本审计预期BLOCK或REVIEW，不允许ADMIT。
|Case|输入变化|实际结果|独立裁决|
|---|---|---|---|
|P1 RIGHTS_MISSING|完全删除rights字段|ADMIT|**P0 FAIL-OPEN**：无许可证也自动准入|
|P2 RIGHTS_UNKNOWN|rights="definitely_copyright_restricted"（非精确字符串）|ADMIT|**P0 FAIL-OPEN**：未知权利状态未拒绝|
|P3 FAKE_DOI_NOT_DENYLISTED|doi="10.1234/fake.2026.12345"（非唯一黑名单）|ADMIT|**P0 FAIL-OPEN**：只验格式，不验真实注册|
|P4 UNVERIFIED_RETRACTION|retraction.authority_id="totally-made-up"|ADMIT|**P0 FAIL-OPEN**：非空字符串即“权威证据”|
|P5 UNVERIFIED_CLAIM|assertion="PubMed confirms this retracted paper is safe to cite as valid"|ADMIT|**P0 FAIL-OPEN**：未核论文事实/撤稿却自动准入|
|P6 FALSE_HUMAN_APPROVAL|rights="copyright_restricted",license_evidence="abcdefgh",human_approved="false"|ADMIT|**P0 FAIL-OPEN**：Python非空字符串真值，虚假审批通过|
|P7 DOI_NONE|doi=None|ADMIT|**P0 FAIL-OPEN**：无DOI仍可被称为科研已核验|
|P8 RIGHTS_BOOLEAN|rights=False|ADMIT|**P0 FAIL-OPEN**：无效权限类型自动准入|
|P9 HOST_SUFFIX_SPOOF|source_url="https://nature.com.evil.example"|BLOCK|PASS：相对R16真实改善|
|P10 NONHTTPS|source_url="http://nature.com"|BLOCK|PASS：HTTPS校验有效|
- 新相邻边界10项，**2项正确阻断、8项错误ADMIT**；与Buddy“11条自选负例0 fail-open”并不矛盾，但证明覆盖不足，不能宣称安全门禁达标。测试没有真实发布/外部网络副作用。
- 严重根因：review_claim只对rights=="copyright_restricted"作检查；human_approved只做truthiness；validate_doi把所有未入唯一黑名单的格式正确DOI视为有效；retraction仅要求authority_id/relation非空；声明与权威原文不比对。应把“元数据格式可解析”与“允许发布”分开，未获可信权利证明/原始ID与撤稿关系证据时只允许REVIEW或BLOCK，不允许ADMIT。
## C. 统计门禁独立逻辑复刻
|Case|输入|实际结果|判定|
|---|---|---|---|
|合法对照|obs=14, lam_h0=5, lam_h1=8, unit=counts|OK, p(H0)=0.0006979899791399858, p(H1)=0.034180701793819136|PASS，独立数学求和复算一致|
|ZERO_RATE|obs=14, lam_h0=0, lam_h1=8, unit=counts|ValueError: math domain error|P1：合法λ=0边界未优雅处理，程序崩溃|
|UNKNOWN_METHOD|method="not-a-method"|OK|P1：非法算法标识未拒绝|
|BOOL_OBS|obs=True|OK，obs=1|P1：布尔值被当计数1，类型门禁缺失|
- 统计H0/H1混淆已有概念修正，R07原p=0.035650是20,000次蒙特卡洛估计，并非“错误算术”；R17将其称“不精确”合理，但不能抹去蒙特卡洛抽样误差。原始脚本未独立字节执行，以上是忠实逻辑复刻。
## D. 5+项官方高影响事实独立核验（2026-11-01）
|#|Buddy主张|权威具体页|判定|
|---|---|---|---|
|1|砷基细菌原论文DOI 10.1126/science.1197258，撤稿公告10.1126/science.adu5488|https://pubmed.ncbi.nlm.nih.gov/21127214/ 及 https://pubmed.ncbi.nlm.nih.gov/40705905/|PASS，撤稿日期2025-07-24|
|2|OpenAlex元数据CC0|https://help.openalex.org/data/how-its-built/|PASS，数据层CC0；不代表第三方全文版权|
|3|OpenAlex“不托管fulltext”|https://help.openalex.org/access/fulltext/|**P1 MATERIAL_ERROR**：官方明确缓存50M+开放获取PDF及TEI全文，支持API/CLI下载|
|4|OpenAlex“output/派生数据=CC0”无条件|https://help.openalex.org/data/licenses/ 及 https://help.openalex.org/access/fulltext/|**P1 MATERIAL_ERROR**：OpenAlex自有元数据CC0不能自动授权含第三方版权全文/图表的派生输出，需按每篇location许可证|
|5|Crossref“元数据以CC0 1.0提供”作为统一许可|https://www.crossref.org/documentation/retrieve-metadata/|**P1 MATERIAL_ERROR/OVERGENERALIZED**：书目元数据是事实、通常不受版权；Crossref生成数据CC0；摘要仍归作者/出版者。不能笼统说所有metadata都同一CC0许可|
|6|PMC OA子集许可逐篇不同，非全PMC可商用|https://pmc.ncbi.nlm.nih.gov/tools/openftlist 及 https://pmc.ncbi.nlm.nih.gov/about/copyright/|PASS；自动批量抓取仅允许官方指定服务|
|7|RDKit官方pip安装命令为pip install rdkit|https://www.rdkit.org/docs/Install.html|PASS；本轮未安装/执行RDKit|
|8|IEEE IES GenAI Challenge 2027报名免费，截止2026-12-31|https://ai.ieee-ies.org/qa/|PASS（ChatGPT新增核验）；需注意作者注册费不在旅费补助内，Buddy本轮未提该机会|
- fact_check_sample_count=8，material_fact_error_count=3（#3/#4/#5），fact_gate_verdict=FAIL。第#5属于版权口径泛化，虽部分实际复用结论一致，仍有合规误导风险；即使保守不计#5，#3/#4已达到V4≥2实质错误FAIL。
## E. 总结与下轮回归建议
- WorkBuddy自评11负例PASS、D1/D2/D3 RESOLVED；ChatGPT独立结论：D1 PARTIAL（DOI/撤稿身份已修，实时权威关系未查询，伪DOI仅黑名单），D2 RECURRED（源码SHA不一致、输入与stdout缺失），D3 PARTIAL（H0/H1修复，但零率/类型/方法边界未过）。
- CROSS_FACTORY_TRANSFER T1=PARTIAL_HOSTNAME_FIX / SECURITY_FAIL；T2=PARTIAL_LICENSE_LAYERING / FACT_GATE_FAIL。无可验证商业端到端案例，PRODUCTION_READINESS=NOT_READY，FINAL_ACCEPTANCE=FAIL。
- 下一轮R18 F8机器人/物理安全：①对授权/人工审批/设备安全状态必须验证严格布尔类型、可信审批来源、默认拒绝及相邻输入；②任何声称执行的安全仿真必须交付源码、全部冻结输入、完整原始日志与实际SHA，独立字节复算通过才可升级INDEPENDENTLY_VERIFIED。
