# R06 F6｜ChatGPT独立审计｜2026-10-31
- 新实验F6首次正式BASELINE；同厂R16才可比较。唯一Job e8d1a46374fc4607，WorkBuddy list_jobs确认DONE/668秒/9622字符，MCP全文含BEGIN_FULL_REPORT/END_FULL_REPORT。Git WORKBUDDY_REPORT.md commit 9fa733bd47f94173a0982fe421283ba74a993399，blob 71e40f821e30c9ec732d8bf6c604e05710382514，逐字回读PASS。WorkBuddy声称的远端stdout/临时文件哈希尚未被ChatGPT直接读取，不是独立实测。
- **独立评分65/100：证据17/25、战略17/20、操作技巧12/20、五案例11/20、风险真实性8/15。** CONDITIONAL_ACCEPT_FOR_RESEARCH / NOT_READY_FOR_PRODUCTION。不能拿R05 F5的73分与本轮跨厂比较质量因果。
## 固定五维评分
|维度|得分|事实理由|
|---|---:|---|
|证据25|17|真实Nature撤稿DOI、OpenAlex 200/404的自述与完整正文；但≥10关键主张仅3/10，18候选清单与8个冻结文件未返回，Crossref429无原始headers，发表日期错一天。|
|战略20|17|研究证据账本、撤稿/版本核查、趋势与商业情报契合F6；但真实商业优先级、覆盖率和ROI缺证据。|
|技巧20|12|有API、算术、撤稿核查方法；13次直接检索违反最多12次硬约束，Crossref polite pool未实测能解除本轮429。|
|五案例20|11|A/E仅WorkBuddy自述执行且源码/原始响应未完整回传；B/C/D未执行，五案十字段不全。|
|风险真实性15|8|明确未授权/未发布，但混淆不同服务429、Runway订阅积分与开发者API价格、Suno配额比值的商业含义。|
|合计|**65/100**|研究交付通过，事实准确性与可复放性不足。|
## 官方独立事实核验与新缺陷
1. **P0-429-ORIGIN：跨服务错误归因。** 旧实验R06 Job 52441e82f15942ab返回WorkBuddy/模型使用额度429并给重置时间；本轮报告§1、§6、§11称Crossref GET 9/10 HTTP429“与旧失败同源”。相同HTTP状态码不能证明同一服务、出口或根因。缺原始响应头与请求ID；Crossref限流即使真实，也不能作为旧WorkBuddy模型额度故障注入。下轮必须按服务、endpoint、响应码、响应头、时间和重试规则分类。
2. **P0-PRICE-CONTEXT：Runway API与网页订阅价混用。** 官方 https://docs.dev.runwayml.com/guides/pricing/ 明确开发者API $0.01/credit，gen4.5 12credits/s，故API基础价12×0.01×60=**$7.20/min**。WorkBuddy§2用网页Standard年付等效$12/月÷625积分再乘12.02×60，得$13.8462/min；算术本身接近正确，但只是“订阅积分包完全消耗的隐含均摊成本”，不是API费率。其称“$0.01/credit非官方，$7.20低估”与官方API直接矛盾。625credits≈52s仅支持约数，不证明精确12.02 credits/s。
3. **P1-SUNO-RATIO：2500credits/20downloads=125这个除法正确，但不是官方每下载消耗125credits的规则。** 必须把“额度上限之比”和“真实单次扣费”分开。Opus $14.50/月年付$174纠错正确，但5个公式能算不等于5个商业含义正确。
4. **P1-DOI-DATE：Nature原论文 https://www.nature.com/articles/nature12968 的Published为2014-01-29，WorkBuddy§4写2014-01-28，错一天。** Nature官方撤稿 https://www.nature.com/articles/nature13598 Published 2014-07-02、Nature 511:112、DOI nature13598正确。撤稿事实独立确认；Crossref具体updated-by字段未直接读取API原文，标NOT_VERIFIED_FIELD。
5. **P1-RETRACTION-COVERAGE：Crossref官方 https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/ 和 https://www.crossref.org/blog/retraction-watch-retractions-now-in-the-crossref-api/ 支持更新关系及Retraction Watch来源；2026年官方讨论 https://community.crossref.org/t/rwdb-record-62686-10-33263-briac94-979986-retraction-recorded-in-retraction-watch-but-absent-from-crossref-metadata/16586 表明缺撤稿公告DOI时关系可能无法映射。** “无标记≠未撤稿”正确，但不能把OpenAlex标题或单个字段当完备撤稿判据；须查出版者原始公告并记录冲突。
6. **P1-OPENALEX-QUOTA：** https://help.openalex.org/api/authentication/ 区分匿名、免费key与付费配额，匿名查询适合轻量测试，不证明长期无人值守稳定。Crossref官方 https://www.crossref.org/documentation/retrieve-metadata/rest-api/ 有polite pool，但不能保证消除所有429。
7. **P0-SEARCH-BUDGET：** WorkBuddy§0明确直接检索13次且另有1子代理检索，超过委托最多12次外部检索。主动披露值得肯定，但属于硬约束未遵守；不得以额外纠错为由自行扩容。
8. **P1-ARTIFACTS：** 报告列出ARITH_CHECK.py、CLAIM_EVIDENCE.jsonl、PAPER_LEDGER.csv等8个文件SHA，但未返回完整原始文件或源码。Git回读只证明报告文本已交付，不能证明远端8个文件的内容/哈希或HTTP响应真实性。至少1套完整源码+冻结输入+输出须直接附报告。
## CROSS_FACTORY_TRANSFER：R05 F5→R06 F6
|method_change|前轮事实|实际注入|观察与结果|
|---|---|---|---|
|V1 数值/计费单位/算术门禁|R05 Opus周期、Runway价格、Suno额度误判|R06 Git FEEDBACK 4210字符全文实际注入4686字符MCP prompt|5个公式有自述复算，Opus纠正；Runway套餐/API仍混用、Suno比值误释。**PARTIAL_IMPLEMENTED / FAILED_FACT_ACCURACY**|
|V2 DOI格式/全文语义/版权分层|R05 WAV结构哈希可复算但不证明音质或商用权|同一实际prompt完整注入L1/L2/L3、正负DOI及撤稿核查|Nature撤稿官方核实；OpenAlex状态码与Crossref字段未独立取原始响应，版权/全文UNKNOWN。**PARTIAL_EFFECTIVE / RIGHTS_NOT_VERIFIED**|
- 上小时通用改进：计划→实际注入→实际效果→下轮调整：V1完整注入但商业场景语义失败；V2完整注入且撤稿事实方向有效，但原始API与版权证据不足。下一轮需约束服务级错误归因与可独立重放证据。跨厂总分不用于因果判断。
## SAME_FACTORY_REMEDIATION：旧F6无可比内容基线
- 旧实验F6 Job 52441e82f15942ab 429失败，无WORKBUDDY_REPORT/CHATGPT_AUDIT。formal_old_content_defects=0；same_factory_baseline_round=old R06 HISTORICAL_REFERENCE_ONLY；same_factory_score_delta=NOT_COMPARABLE；旧内容解决率、关键错误复发率=NOT_COMPARABLE。本轮65分为R16正式基线。
|旧实验真实缺口|Buddy自评|独立判定|下次验收|
|---|---|---|---|
|HIST-F6-01 429无正文|PASS|**RESOLVED_DELIVERY_ONLY**|新Job完成全文Git回读；不代表旧模型429根因解决。|
|HIST-F6-02 ≥10文献主张与DOI|PARTIAL 3/10|**PARTIAL**|须10条真实文献/主张逐条原始来源和证据级别。|
|HIST-F6-03 ≥15工具候选+Top5|MET|**PARTIAL/NOT_VERIFIABLE_COUNT**|称18项但PLUGIN_INVENTORY未回传，权限/费用仅自述。|
|HIST-F6-04 五案例可复现|PARTIAL|**PARTIAL**|A/E无完整源码与原始响应，B/C/D NOT_TESTED。|
|HIST-F6-05 真实状态/错误归因|MET|**PARTIAL**|桥接DONE与Git回读属实，但跨服务429混因。|
- 历史交付/证据缺口改善：**1/5已解决（仅本轮交付），4/5部分改善**；不是旧报告内容缺陷修复率。新增问题5组：429跨服务归因、API/网页订阅价混用、数值比值冒充真实扣费、论文日期与撤稿字段证据、超检索预算及原始工件缺失。旧关键错误复发率不可计算。
## 五案例与R16整改
- A DOI/撤稿：保留有效/无效/撤稿三样本；要求原始API响应、请求时间/headers、出版者撤稿日期/DOI对账，扩大到10条可核主张。
- B 趋势雷达：NOT_TESTED；须冻结90天数据、去重键与转载负例，不能以计划称趋势。
- C 教育认知综述：NOT_TESTED；需年龄适用、RCT/观察分级、PII拒绝负例。
- D 多国联盟：NOT_TESTED；3国×2品类官方政策/佣金/日期、完整公式、失败回滚。
- E 证据交付：必须附CLAIM_EVIDENCE.jsonl和MANIFEST真实内容及可执行schema校验；Git提交回读由ChatGPT负责，不能把Buddy临时文件哈希等同Git验收。
## R07 F7跨厂最多两项建议
- **W1 服务级错误归因门禁**：API/模型/插件429/403按服务、endpoint、响应头、请求时间、重试分类，禁止“同状态码=同根因”；目标0次跨服务混因、≥1可复核正负例，缺证据UNKNOWN。
- **W2 数字语义与原始工件双验收**：数值绑定官方来源、具体产品/模型、API或套餐、单位、公式与边界；每个关键EXECUTED测试直接交付源码/冻结输入/输出，否则SELF_REPORTED。目标≥5项可独立复算且商业语义正确、≥1套完整可重放工件。
## 结论
**65/100：WorkBuddy执行及MCP全文Git交付真实通过；V1事实准确性失败，V2部分有效，旧F6内容基线缺失。** 不因Buddy自评5/5判研究全面改善；未改生产/模型/其他分支/插件授权。
