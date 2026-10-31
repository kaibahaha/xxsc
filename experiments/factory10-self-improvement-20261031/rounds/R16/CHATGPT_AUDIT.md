# R16 F6 研究报告工厂｜ChatGPT独立质量审计（2026-11-01 Asia/Shanghai）
## A. 三方结论分离
**WORKBUDDY_SELF_REPORT**：唯一Job 135fcff83e044e3b DONE，返回BEGIN_FULL_REPORT/END_FULL_REPORT共30439字符，称8次外部检索、0子代理、15/15自选测试通过、U1五事实0错、D1-D5基本修复；不自称ChatGPT验收。
**CHATGPT_INDEPENDENT_AUDIT**：真实MCP正文经Git报告commit ec813ddb7c690dec15393f9d739dd85a4f738b76独立回读；提取源码和冻结输入为两个Git工件，分别独立回读并通过独立SHA256复算。独立官方网页抽查至少7组高影响事实，其中两项许可/归属错误。独立Python环境根据源码逻辑逐函数重实现安全门禁，构造9项相邻攻击，全部被错误ADMIT（至少4项严重fail-open）；详见INDEPENDENT_SECURITY_PROBES.md。原始Python文件的normal/-O模式**未由ChatGPT字节级直接运行**，不可冒充全量独立重放。
**FINAL_ACCEPTANCE**：**FAIL（FACT_GATE_FAIL + P0_SECURITY_FAIL）**；研究材料PARTIAL，工件内容/哈希已验证，发布前门禁不可投入生产。Job DONE、报告长、15/15自选PASS不等于安全。

## B. 固定五维100分及同厂纵向
|维度|R06 F6基线|R16 F6|Δ|依据|
|---|---:|---:|---:|---|
|证据准确性25|17|17|0|5项核心官方事实可核，但OpenAlex与Crossref许可两项错误，Google项目开放状态不明|
|战略20|17|18|+1|研究证据准入/发布门禁对十大工厂通用，IEEE竞赛和免费学术API有价值|
|操作技巧20|12|15|+3|源码14375字符和JSONL3801字符实交，SHA独立复算；但域名/权利/语义安全边界失败|
|五案例20|11|12|+1|A部分执行、E自报执行并有源码，其余B/C/D NOT_TESTED，0商业端到端|
|风险真实性15|8|5|-3|自评边界诚实，但存在严重P0发布门禁fail-open与许可误报|
|**总分**|**65**|**67**|**+2**|不同任务难度/证据范围，分差不证明整体模型进步|
研究评分67/100不覆盖P0门禁；生产就绪=NOT_READY。

## C. 官方高影响事实独立抽查（截至2026-11-01）
|#|Buddy原主张|官方独立证据|裁决|
|---|---|---|---|
|1|Runway Dev API $0.01/credit，gen4.5=12cr/s，$7.20/min为推导|https://docs.dev.runwayml.com/guides/pricing/ ，$0.01/credit及gen4.5 12 credits/s，12×0.01×60=7.20|PASS；仅API基本费，税费另计|
|2|Suno Pro 2500 credits/月及20 downloads/月为独立额度|https://suno.com/home / https://suno.com/pricing ，两独立额度及商用权|PASS；不证明任何曲目必有版权保护|
|3|ElevenLabs创业赠金33M字符/credits总额、12个月，不是每月|https://elevenlabs.io/blog/elevenlabs-startup-grants-just-got-bigger-now-12-months-and-over-680-hours-of-conversational-ai-audio ，官方写total 33 million free credits / next 12 months|PASS；实际账户资格与权益未核|
|4|HeyGen翻译无唇形4、Speed6、Precision10 credits/min|https://help.heygen.com/en/articles/10029081-how-to-get-started-with-video-translation 及 https://help.heygen.com/en/articles/15125761-heygen-credit-based-pricing-plans-subscriptions-explained |PASS；不同功能费率不同|
|5|Nature nature12968 Published 2014-01-29、nature13598 Retraction Published 2014-07-02|https://www.nature.com/articles/nature12968 、https://www.nature.com/articles/nature13598 官方搜索可读版本|PASS；Crossref updated-by原始JSON未取得，字段NOT_VERIFIABLE|
|6|OpenAlex API元数据“data CC-BY”|https://help.openalex.org/access/pricing/ §Free data, paid services 及 https://help.openalex.org/api/ 明确**OpenAlex数据CC0**；单篇论文全文版权需分别判断|**P1 MATERIAL_ERROR**，CC-BY与CC0混淆，许可义务错误|
|7|Crossref免费元数据“reuse需署名”|https://www.crossref.org/documentation/retrieve-metadata/ §Licensing：书目元数据基本不受版权约束，Crossref生成数据CC0，摘要可能受作者/出版社版权约束|**P1 MATERIAL_ERROR**，泛化署名要求并混同摘要与元数据|
|8|Google Research Scholar Program 2026/27仍有Dec1 2026截止、最高$60k|https://research.google/programs-and-events/past-programs/ 将Research Scholar Program列为过去项目；当前官方开放入口与截止未核实|**NOT_VERIFIABLE**，不得列可行动机会|
- fact_check_sample_count=8；material_fact_error_count=2；fact_gate_verdict=**FAIL**（V4规则≥2实质错即FAIL）；not_verifiable_count=1。来源冲突不得靠营销页消解。

## D. MVE/红队与复现
- 实际源码Git：artifacts/evidence_gate_r16.py，SHA256 **313071e5ac6aeabff24fbba7e052ca70659b880a3949099e67d11d6195444e19**；冻结输入：artifacts/frozen_cases_r16.jsonl，SHA256 **fcc03db36a1a3d2cc47d0985c80b19a00f47b63fe99ca2a368390dc1de587ddf**。两SHA由ChatGPT独立JavaScript实现复算且通过标准向量，Git写后回读一致。源码文件/输入真实交付通过，执行证据仍部分自述。
- Buddy原14负例+1正例正常/-O均通过属于**SELF_REPORTED**，原脚本normal/-O未直接独立执行。ChatGPT按原源码决策逻辑在独立Python环境复刻，新增9个相邻边界输入（另1合法对照），9/9错误ADMIT；典型：`https://nature.com.evil.example`、`https://evil.example/?ref=nature.com`、`javascript:nature.com`均因`domain in url`错误通过；`rights='copyright_restricted'`+自报authorized=True被允许发布；空claim、空version、虚假撤稿论文主张亦通过。
- **P0-F6-SEC-01** 源URL子串校验而非HTTPS/hostname解析，恶意来源可伪造。**P0-F6-SEC-02** 授权自报布尔+版权受限标签被允许发布，无权利证明/审批可信锚。**P0-F6-FACT-03** 研究声明任意文本、日期与原始论文不比对，不能证明语义事实，若用于自动发布会传播虚假主张。
- 新增独立红队：red_team_test_count=9（不含1合法对照），red_team_pass_count=0，red_team_fail_open_count=9，red_team_blocked_count=0；这是忠实逻辑复刻的测试，不冒充原脚本字节级运行。原14项仍SELF_REPORTED。p0_open_count≥2，p1_open_count≥4；artifact_reproducibility_verdict=SOURCE_AND_INPUT_SHA256_VERIFIED / ORIGINAL_RUNTIME_NOT_REPLAYED；core_mve_status=EXECUTED_SELF_REPORTED / SECURITY_FAIL；core_mve_independent_replay=PARTIAL_LOGIC_REIMPLEMENTATION_ONLY。
- 核心MVE不允许READY或发布生产；需使用URL解析和可信源证据，拆分“入库”与“发布”，校验授权签名/许可范围与原文事实；对这些新增攻击形成强制回归。

## E. 同厂专项整改SAME_FACTORY_REMEDIATION（R06→R16）
|缺陷|R06原始错误/缺口|R16实施证据|独立裁决|
|---|---|---|---|
|D1 P0 429跨服务归因|把Crossref429与模型额度429当同源|报告按服务区分头与限流语义，未提供独立原始响应头|PARTIAL（方向正确，原始头未独立核验）|
|D2 P0 API/Web混价及额度比值误释|Runway网页订阅价冒充API价；Suno比值当真实扣费|官方Runway/Suno页与公式独立核对|RESOLVED|
|D3 P1 Nature日期与撤稿字段|原论文错写01-28；Crossref关系无原始API|出版者页01-29/撤稿07-02核实；Crossref原始关系仍缺|PARTIAL|
|D4 P0 检索预算|R06自述13次直接+子代理超限|R16自述8次/0子代理，未发现相反证据|RESOLVED_BY_SELF_REPORT（日志不独立核）|
|D5 P1 原始工件缺失|仅8文件SHA、源码/输入未交付|源码/JSONL实交+Git+独立SHA；但MVE安全失败|PARTIAL|
- same_factory_baseline_round=R06；same_factory_defects_count=5；resolved_count=2（D2、D4，其中D4仅自述预算）；partial_count=3；recurred_count=0（旧问题直接重复未确认）；same_factory_score_delta=+2；critical_new_p0≥2；同厂关键三缺陷D1/D2/D3中严格RESOLVED=1/3。任务难度与采样不同，不能据分数声称系统自我改进已通过。
- 五案例：A PARTIAL_EXECUTED / DOCUMENTED；B NOT_TESTED；C NOT_TESTED；D NOT_TESTED；E EXECUTED_SELF_REPORTED（门禁源/输入哈希独立核，发布安全FAIL）。INDEPENDENTLY_VERIFIED商业案例0/5，商业E2E 0/5。

## F. 跨小时方法迁移CROSS_FACTORY_TRANSFER（R15 F5→R16 F6）
U1 事实单位/官方规则双核：**已实际注入**4311字符FEEDBACK至4705字符MCP prompt；Buddy声称5 VERIFIED+1 UNKNOWN，ChatGPT扩抽8项发现2实质许可错误，**FAILED_FACT_ACCURACY**。下一轮要求版权/数据许可/摘要/全文逐层核查。
U2 严格类型/相邻红队+工件移交：**已实际注入**；源码/冻结输入/SHA可核，纠正R15的字符串false和NaN；但新独立9项攻击全部fail-open，**PARTIAL_IMPLEMENTED / FAILED_SECURITY**。下一轮必须测试域名伪造、授权真实性、受限版权发布、空声明与撤稿语义。
跨厂总分R15=71、R16=67不用于推断迁移因果；只比较事实错误率、工件可复算性、安全fail-open数。

## G. 机会与业务价值
- ChatGPT独立核验IEEE IES Generative AI Challenge 2027（https://ai.ieee-ies.org/）已开放2026-10-20至2026-12-31报名，规则年满18岁、1–5人、原创工业/IoT生成式AI，IP归团队但录用论文授予发表权，2027年1–5月投入研发，至少6项旅费资助（前三每队USD2000、后三每队USD1000）。资格待用户确认，ACTION_NOT_EXECUTED，A/P1。
- OpenAlex官方每日USD1免费API额度需免费key/账号，未领取；Crossref Public/Polite无需注册但有429限流；Google Scholar项目当前状态NOT_VERIFIABLE，不能按Buddy列表作为可申请资金。全部实际注册0、资源到账0。
- 机会雷达/行动清单及OPPORTUNITY_LEDGER独立Git回读；真实商业生产/客户验证未执行。

## H. 质量仪表盘与下一轮
fact_check_sample_count=8; material_fact_error_count=2; fact_gate_verdict=FAIL; case_status_counts={PARTIAL_EXECUTED:1,NOT_TESTED:3,EXECUTED_SELF_REPORTED:1,INDEPENDENTLY_VERIFIED:0}; core_mve_status=SELF_REPORTED_EXECUTED_BUT_SECURITY_FAIL; core_mve_independent_replay=PARTIAL_LOGIC_REIMPLEMENTATION; artifact_reproducibility_verdict=SOURCE_INPUT_SHA256_VERIFIED; red_team_test_count=9; red_team_pass_count=0; red_team_blocked_count=0; p0_open_count=2+; p1_open_count=4+; claims_overstated_count=至少2（“15/15安全达标”与“OpenAlex/Crossref许可”）； production_readiness=NOT_READY。
R17 F7下一轮最多两项通用整改：T1【URL/身份/权利可信锚】以hostname精确校验+授权证明/许可范围+撤稿/原文主张三层门禁，至少5个恶意来源/权限负例0放行；T2【许可与元数据/全文区分】OpenAlex CC0元数据≠单篇全文许可，Crossref元数据多CC0而摘要可能受版权，至少5条官方来源0错误并给版本/日期。两项须完整注入R17真实prompt，若无法独立重放标NOT_VERIFIED。
