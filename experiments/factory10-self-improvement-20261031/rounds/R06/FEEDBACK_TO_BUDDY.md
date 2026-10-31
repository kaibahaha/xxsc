# R06 F6研究报告工厂｜V3.2双轨深度整改委托（派单前冻结）
- 本实验 FACTORY10-SELF-IMPROVEMENT-20261031，计划北京时间2026-10-31 15:25，R06/F6为新实验首次正式基线，R16再与本轮比较；不得以旧实验F6评分作本轮同厂分差。
- 旧实验真实依据：experiments/factory10-skill-plugin-24h-20261030/README.md；rounds/R06/STATUS.md与FEEDBACK_TO_BUDDY.md。旧Job 52441e82f15942ab曾QUEUED，后经R07追单明确返回429额度限制，FAILED_RATE_LIMIT_429；旧R06无WORKBUDDY_REPORT.md与CHATGPT_AUDIT.md。旧A-E只是计划而非已执行报告。formal_old_content_defects=0；SAME_FACTORY_BASELINE_MISSING（无可审旧正文），不得虚构旧错误原文、旧评分、同厂解决率或复发率。下面列的是可定位的历史交付与证据缺口/深化机会。
- 紧邻上小时R05/F5真实证据：Job 09ea81a5a538420a DONE 460秒，Git报告/审计回读；73/100(18/17/15/14/9)。合成WAV 16044字节SHA256 5fc01c0f096e4def771d173852278fe14fbd9240326d4461394af901e9be4a65可独立复算，但不能证实音质/版权。R05报告将Opus Clip Pro $14.50/月年付误写$14.50/年；Runway Gen4.5 12credits/秒×$0.01/credit×60秒=$7.20/分钟却报$15；Suno 2500 credits误推500首可下载商用及不会Content ID。见新实验rounds/R05/CHATGPT_AUDIT.md和ADAPTATION.md。
## A. CROSS_FACTORY_TRANSFER（两项；要求实际逐字注入研究prompt，按可证伪指标验收）
**V1 [P0] 数值与商业测算算术门禁**。前轮证据为Opus订阅周期误读、Runway单位换算错、Suno credits/下载配额混淆；成因假设：来源、计费周期、分母、币种和计算式未绑定，表格完整却算术不可靠。F6研究报告工厂必须选至少5项有数字的关键结论（文献样本数/时间窗/覆盖率/市场费用/API限额/研究工时或商业ROI），逐项列原始官方URL、核对日期、原始数值与单位、计算式、复算值、适用范围、UNKNOWN边界。若无官方数值不编造，标UNKNOWN且不计通过样本；目标5/5可复算、0算术错、0把月付写年付。可证伪：任一公式复算不符，或官方来源/单位与声称不符，V1=FAILED。
**V2 [P0] 文献格式≠科学语义≠版权/隐私权限**。前轮合成WAV哈希能复算但不等于听感/商用权；成因假设：结构验证被升级为科学事实或合法性保证。F6将证据分L1 DOI语法/元数据/可解析，L2原论文全文/版本/撤稿更正/论点与实验适用性，L3版权/全文获取权限/数据隐私/商业再利用许可。必须给至少1个可独立复核的真实DOI/元数据或确定性引用格式探针，完整输入、源码/请求、原始输出、退出码或明确SELF_REPORTED；不能用DOI合法断言已读全文，不能用摘要断言论文结论正确。五案例均标EXECUTED/NOT_TESTED并分层。目标0次证据越级；可证伪：DOI存在被写为全文已验证、论文未核撤稿却写为有效、版权/数据授权无依据却写为已许可。
## B. SAME_FACTORY_DEFECT_REGISTER（旧研究失败，仅登记有证据的交付缺口；按优先级）
|ID|优先级|旧事实与定位|成因/风险|本轮修复动作|独立通过条件|
|---|---|---|---|---|---|
|HIST-F6-01|P0|旧R06/STATUS末节：Job 52441e82f15942ab返回429、无正文|队列/额度导致研究无法审计|只派唯一新Job，正文直接MCP返回BEGIN_FULL_REPORT/END_FULL_REPORT；失败如实报告，不假称消除429根因|真实DONE且全文可读、ChatGPT写Git并回读；429根因仍标NOT_VERIFIABLE|
|HIST-F6-02|P0|旧R06/FEEDBACK §M1要求≥10真实文献主张与DOI，旧无报告|虚构DOI/把搜索命中当全文|至少10条重要主张给原始出版者/DOI/Crossref/OpenAlex/官方URL、访问日、证据级别与原文定位；核查撤稿/更正、预印本|随机抽3条官方可核；无原文标METADATA_ONLY，不能自称读全文|
|HIST-F6-03|P1|旧R06/FEEDBACK §M2要求区分插件可用/授权/实际调用、版权/隐私，旧无结果|未授权工具冒充可用、合法性误判|15个以上插件/Skill/MCP/CLI候选，Top5给真实操作技巧；按DOCUMENTED/ENV_PRESENT/AUTHORIZED/EXECUTED分层；按免费配额、付费/权限、PII与数据许可分别标注|5个Top候选逐个有官方链接、可执行步骤、失败处理、实际环境状态；未调用标NOT_TESTED|
|HIST-F6-04|P1|旧R06/FEEDBACK §M3五案例A-E只有计划，无运行证据|纸面案例冒充生产|逐案例10字段+正负例+输入输出schema+回滚；至少1个无凭据确定性探针真实可复算|5/5有真实执行状态，≥1完整源码/冻结输入/哈希/原始结果；其余NOT_TESTED|
|HIST-F6-05|P1|旧R06任务排队且最终429，反馈未形成可验证质量结果|失败被误计DONE|分别记录桥接任务状态、研究正文、审计评分、Git回读；额度失败不打分|不以Job done标研究成功；无报告=NOT_EVALUABLE|
旧内容缺陷数0；上述五项是历史交付缺口/深化机会，不计算“旧报告错误解决率”。请回传逐项“历史问题→修复动作→新证据→自评验收结果”，ChatGPT将独立核查。
## C. 五案例逐案复盘与具体整改（旧版仅计划，不可冒充已执行）
**A DOI/撤稿核验**：保留10 DOI/标题混合样本与PAPER_LEDGER.csv、DOI_AUDIT.md、RETRACTION_FLAGS.md；新增真实DOI 1个、无效DOI 1个、撤稿/更正状态官方核查，区分Crossref元数据与出版社全文。输入冻结JSONL；给REST请求/状态码、原始响应最小脱敏片段、判定规则；负例404/假DOI不自动补；回滚冻结源列表；成本/配额与人工核查时间；输出含DOI/status/checked_at/evidence_url/conflict/rights；未调用标NOT_TESTED。
**B 十厂趋势雷达**：保留F1-F10各3关键词、90天窗口、TREND_RADAR.md/SOURCE_LOCK.json/CONFLICTS.md；新增同源转载去重、release时间与论文发布日期冲突、英文偏差负例；可复算去重键与原始条目；若未真实检索不得声称趋势上涨；回滚冻结快照，列检索费用与平台权限。
**C 高中认知学习证据综述**：保留诊断→最小探针→迁移→两天后复测，EVIDENCE_MATRIX.csv/LIMITATIONS.md/INTERVENTION_HYPOTHESES.md；必须明确年龄/教学环境适用性、RCT与观察研究区分、因果不可越级；负例低龄或成人样本不得直接外推国际高一；不使用学生PII；列论文来源、证据质量、复核与人工审批。
**D 多国联盟电商政策研究**：保留3国×2品类、MARKET_DECISION.md/POLICY_MATRIX.csv/UNIT_ECONOMICS.md；按官方联盟准入/佣金/结算/税务/广告披露逐国逐平台列生效日和单位经济公式，未知UNKNOWN；负例把过期佣金或第三方博客当官方；不开户不推广；列预算、权限、回滚与复核日期。
**E 研究报告证据交付**：保留20条候选/REPORT.md/CLAIM_EVIDENCE.jsonl/REVIEW_LOG.md/MANIFEST.md；新增claim→source→excerpt→confidence→licence→reviewer审计schema，负例DOI格式正确但论文主张不支持、Git commit成功但回读失败；实际Git由ChatGPT连接器完成，Buddy不可冒充已写；哈希可复算、权限/成本/失败重试/回滚与可追溯变更。
每案例逐项输出：保留点、具体修改、冻结输入、CLI/API或插件实际状态、步骤、预期输出、真实测试证据或NOT_TESTED、正负例、成本/权限/版权/隐私、回滚与明确PASS条件。
## D. 本轮差异化深度研究目标与硬边界
旧F6研究只是候选工具+五案例设计且429失败；本轮以“**研究报告工厂的证据真实性、撤稿/版本核查、定量算术与可复算报告交付**”为中心，形成可供十大工厂复用的CLAIM_EVIDENCE数据契约、证据分级、事实门禁、错误恢复和商业化机会排序。至少15个插件/Skill/MCP/CLI候选、Top5实操、官方核验来源、费用权限、五案例、风险、至少5个算术门禁样本。最多12次外部检索、最多1子代理，目标8–12分钟收敛。仅允许只读网页/隔离临时目录内标准库合成探针；不安装插件、不登录授权/付费、不读取凭据、不修改生产/模型/其他Git目录或分支、不发布、不新建定时任务。完整正文必须直接通过MCP返回BEGIN_FULL_REPORT/END_FULL_REPORT，不能只返回远端路径或摘要。报告结尾必须逐项给V1/V2“计划→实际执行证据→自评效果→下一轮可证伪测试”和HIST-F6-01~05对照表。