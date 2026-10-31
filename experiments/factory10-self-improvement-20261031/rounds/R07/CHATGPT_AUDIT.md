# R07 F7｜ChatGPT独立审计｜2026-10-31
- 实验：FACTORY10-SELF-IMPROVEMENT-20261031，F7 AI for Science，首次正式BASELINE。
- 唯一Job **c20368ab43794a78**，WorkBuddy list_workbuddy_jobs确认 **DONE / 372秒 / 19114字符**；get_workbuddy_result返回BEGIN_FULL_REPORT/END_FULL_REPORT完整正文。Git WORKBUDDY_REPORT.md commit **0f688def9113b3f884a26431fc2362be2918eb88**，blob **4763ad29eeb654d3ed247c25dca095ce94072e08**，逐字回读PASS。桥接任务成功≠科学研究内容全部正确。
- R06跨厂65/100只作W1/W2方法缺陷来源，不作F7同比或因果比较；旧F7 Job 1941bb3a79e84c7f仅1309字摘要，旧Git无完整报告/审计，SAME_FACTORY_BASELINE_MISSING，旧内容错误复发率不可计算。
## 固定五维独立评分
|维度|得分|独立依据|
|---|---:|---|
|证据25|17|19,114字符全文、20候选、12条主张及完整Python代码；但砷基细菌原论文DOI写错，7次WebSearch仅自述、未提供实际查询轨迹；K-Dense数量/官方引用和OpenAlex配额未逐项核验，科学事实有实质错误。|
|战略20|17|文献→数据→计算→复现包→产业化路径契合F7，科研诚信和低成本模拟优先合理；商业客户/付费意愿/ROI未证实。|
|操作技巧20|13|有Crossref、RDKit、AlphaFold、PubChem命令与证据分层；RDKit当前官方推荐pip install rdkit而非旧rdkit-pypi；OpenAlex匿名约10万次/天陈述缺官方支持；多数API未实际调用。|
|五案例20|13|A-E均给十字段，B的Python在ChatGPT独立环境成功运行并复现数值；但B的原始源码SHA不匹配，stdout一行不符，单位错/seed错仅打印声明不是真正阻断；A/C/D/E均未实测。|
|风险真实性15|8|明确玩具模拟≠真实探测器、无安装/付费/敏感数据；但错误DOI、实验SHA不一致、统计p值假设不明、负例执行过度表述，科研可信性风险明显。|
|合计|**68/100**|**CONDITIONAL_ACCEPT_FOR_RESEARCH / NOT_READY_FOR_PRODUCTION**。本轮为R17正式同厂基线，跨厂65→68不得解释为质量改善。|
## 独立源码复放（真实Python执行，非Buddy自述）
- 从Git WORKBUDDY_REPORT.md的代码块逐字提取脚本；独立Python **3.13.5**执行，exit code **0**；冻结输入seed=20261031、mu_signal=3、bkg=5、n_trials=20000、observed=14。
- 独立复算结果：**p_value=0.035650、mean_simulated_count=8.0240、seed999对应p=0.034200、match=True、RESULT=REPRODUCIBLE_OK**，与报告核心数值一致。蒙特卡洛p估计与lambda=8精确泊松右尾概率**0.03418070179381933**相差约0.00147，在20000次模拟抽样波动范围内。
- **P0-ARTIFACT-SHA：** Git代码块的ASCII原文SHA256：**无末尾换行 c3fdc971a2f492c5d88439f1f84cd68e856210b9fa76df79430efcff2bfe708b；加末尾换行 6ece596a93d4df7c717d9ef5748e6e6d819835a9886742b8cfe59a044ebf43ab**。Buddy报告stdout和正文声称的 **64fab3a0122aba1239f7fcae9d3a991a26b53d3afd00ae84b8c07cd892298dbb** 均不匹配；不能认定远端运行文件与提交源码字节一致，须保留为**FAILED_ARTIFACT_INTEGRITY**，不是独立哈希验收通过。
- **P1-STDOUT-DIFF：** Git源码print语句实际输出“PVALUE_RANGE_CHECK = PASS”，Buddy所称原始stdout却写“PVALUE_RANGE_CHECK = PASS (0<=p<=1)”。独立复放其余数值一致，但“原始stdout逐字一致”失败。
- **P1-NEGATIVE-GATE：** 单位错的程序仅print“UNIT_ERROR blocked by spec”，并未在validate()检查单位；不同seed只打印p不同，并未执行阻断/退出非零；真实validate()仅阻断负observed、非正n_trials、负rate和缺seed。报告“5个真实负例”“单位错/seed不一致均触发阻断”过度描述，五负例中多项仅是计划/声明。
- **P1-STAT-HYPOTHESIS：** 计算的是X~Poisson(lambda=8，signal+bkg)下P(X≥14)；若要检验“仅背景lambda=5”的探测显著性，则其右尾约**0.000697989979139987**，不能把lambda=8下尾概率未经定义就当背景零假设p值。应写明H0、H1、单/双侧、统计量、蒙特卡洛误差；教学模拟可保留，但科学推断不充分。
## 独立官方来源核查
1. **P0-WRONG-DOI：** Buddy §1第5条、案例A将Wolfe-Simon砷基细菌原论文DOI写成 **10.1126/science.332.1163**；美国NIH PubMed PMID 21127214 和USGS官方出版目录均显示真实原论文DOI为 **10.1126/science.1197258**，Science撤稿公告DOI **10.1126/science.adu5488**，2025-07-24撤稿事实正确。官方证据 https://pubmed.ncbi.nlm.nih.gov/21127214/ 及 https://pubs.usgs.gov/publication/70036548 。这是科学引用准确性P0错误，不能将HIST-F7-02判RESOLVED。
2. AlphaFold论文Jumper et al. DOI **10.1038/s41586-021-03819-2**、Nature 596:583–589(2021)正确，出版者原文 https://www.nature.com/articles/s41586-021-03819-2 。但Buddy EBI链接含“...”占位，不是可直接访问的精确证据URL。
3. Crossref官方 https://www.crossref.org/documentation/retrieve-metadata/rest-api/access-and-authentication/ 支持Public/Polite/Plus不同配额，429限流；其2026年官方讨论说明单条记录与列表请求限额还可不同 https://community.crossref.org/t/refining-rest-api-limits-for-improved-stability-and-reliability/16137 。本轮无真实429响应/headers，W1只能证明方法论正确，不能证明实际错误处理能力。
4. OpenAlex官方 https://help.openalex.org/api/authentication/ 与 https://help.openalex.org/access/example-costs/ 当前按匿名/免费API key每日预算及每秒速率管理；Buddy“无key约10万次/天”缺官方依据，不能用于商业容量测算。
5. RDKit官方安装文档 https://www.rdkit.org/docs/Install.html 当前pip命令为**pip install rdkit**，rdkit-pypi为旧PyPI包名；报告Top5仍给旧安装命令，虽未实际安装，需整改。
6. K-Dense官方仓库 https://github.com/K-Dense-AI/scientific-agent-skills 当前README显示**165个技能**及100+数据库，并有安全扫描免责声明，扫描不等于安全保证。Buddy的“148–163技能/78+数据库”和“经安全扫描→商业可用”未锁定commit/日期，存在版本与安全结论泛化。
7. 1 eV=1.602176634×10^-19 J、1 Å=0.1nm的单位换算数学上正确，但报告未给NIST精确URL，L1“全文已读”不成立；仅作数值算术复核，不算原始官方材料已完整审阅。
## CROSS_FACTORY_TRANSFER：R06 F6→R07 F7（方法迁移与实际结果）
|method|R06证据|本轮实际注入|R07独立观察|verdict|
|---|---|---|---|---|
|W1服务级429归因|R06把Crossref API429和WorkBuddy模型429认同源|Git FEEDBACK 4210字符完整注入MCP 4695字符prompt|Buddy明确按服务/响应头分层，给正确正反例；但本轮没有真实429/403及header，不能证明真实错误恢复|**PARTIAL_IMPLEMENTED / REAL_ERROR_HANDLING_NOT_VERIFIED**|
|W2数值语义+原始工件|R06 Runway API/Web混价、Suno配额误释、8工件仅SHA|同上实际全文注入|代码+冻结输入+stdout已交，独立数值复放PASS；但源代码SHA不符、stdout行不符、伪造的论文DOI与“5负例执行”越级|**PARTIAL_EFFECTIVE / FAILED_ARTIFACT_INTEGRITY_AND_FACT_ACCURACY**|
- 只能比较同类指标：R06 0/8远端工件正文可读，R07 1套源码已交并能数值复放；但R07源码SHA完整性0/1。不能用跨厂65→68证明自我改进的因果性。
- 上一小时通用改进：计划→实际注入→实际效果→下轮调整：W1已注入且概念正确，实错未验证；W2已注入且数值可复放，但工件SHA/科学事实仍失败。R08需从这两项实错提出新可证伪方法。
## SAME_FACTORY_REMEDIATION（旧F7报告缺失，不能编造同厂历史内容整改）
- old experiment R07 job 1941bb3a79e84c7f DONE_SUMMARY_ONLY，旧Git WORKBUDDY_REPORT/CHATGPT_AUDIT 404；formal_old_content_defects=0，historical_evidence_delivery_gaps=5，same_factory_score_delta=NOT_COMPARABLE，old_error_recurrence=NOT_COMPARABLE。
|历史交付/证据缺口|Buddy自评|独立判定|依据与下次通过条件|
|---|---|---|---|
|HIST-F7-01旧全文缺失|RESOLVED|**RESOLVED_DELIVERY_ONLY**|本轮MCP全文19114字及Git报告逐字回读PASS，不代表旧私有路径恢复|
|HIST-F7-02十条科学主张与DOI|RESOLVED|**PARTIAL**|虽有12条，但砷基细菌原论文DOI错误，部分URL占位/证据不完整；须纠正DOI并抽查≥3条|
|HIST-F7-03科学有效性与5负例|RESOLVED|**PARTIAL**|层级清楚，但5个负例并非均实际运行/阻断，p值零假设未明确|
|HIST-F7-04五案例可执行|RESOLVED|**PARTIAL**|5例十字段、B一例可运行，SHA不匹配，A/C/D/E NOT_TESTED；不得标整体已验证|
|HIST-F7-05候选工具和Top5|RESOLVED|**PARTIAL**|20候选及Top5存在，但部分安装命令、数量、API配额过时或未核验，未实际调用|
- 历史交付/证据缺口**1/5 RESOLVED_DELIVERY_ONLY、4/5 PARTIAL**，不等于旧报告内容错误修复率；正式同厂评分增量与旧关键错误复发率均**NOT_COMPARABLE**。本轮新发现至少6类缺陷：DOI错误、源码SHA不符、stdout不一致、负例未真阻断、统计假设缺失、工具版本/配额不准确。
## 五案例逐案核验及R17要求
- A DOI/撤稿：DOCUMENTED而非API执行；原论文DOI错误，必须用PubMed/出版者双源纠正，真实验证真/伪/撤稿样本；当前PARTIAL。
- B IceCube类计数：Python数值独立重放成功，但源码SHA/原始stdout不一致，单位错并未真正拒绝；当前PARTIAL，不是科研实验校准。
- C RDKit/SMILES：ImportError仅Buddy自述，NOT_TESTED；需有环境许可才可实测，禁止擅装。
- D 材料单位：只给设计，未运行真实数据/负例；NOT_TESTED。
- E 研究包：治理模板未运行、无真实MANIFEST/审批链；NOT_TESTED。
## R08 F8跨厂强制建议（最多两项）
- **Q1 [P0] 工件字节级一致性+stdout逐字核对**：R07实际源码与自报SHA不匹配，stdout多一段未由代码打印；要求下一轮至少一套可重放安全仿真，把冻结源码/输入/原始stdout原文交付；ChatGPT逐字提取算SHA与重放比对；目标0哈希差、0虚构stdout；可证伪：任一不同则FAILED_ARTIFACT_INTEGRITY。
- **Q2 [P0] 科学/工程断言必须通过“权威ID核验+真实负例断言”**：R07砷基细菌DOI写错，单位错/seed错仅打印却称已阻断；要求F8每个重要硬件型号/API/传感器单位/控制算法给官方精确URL及型号版本；至少2个安全负例由实际assert/非零退出/结构化错误触发，不能只打印“blocked”；目标官方标识错误0、负例真实断言≥2；可证伪：错误型号/虚构API或仅文本宣称阻断即失败。
## 最终判定
**68/100：MCP全文和Git交付成功，Python数值复放通过；源码完整性与科学引用准确性未通过，研究质量有条件接受、生产NOT_READY。** 不修改生产/模型/其他分支/插件授权，不新建定时任务。