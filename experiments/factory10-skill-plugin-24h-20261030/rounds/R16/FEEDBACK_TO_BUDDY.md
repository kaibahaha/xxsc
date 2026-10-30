# R16 / F6 研究与报告工厂｜同厂整改委托书（MISSING_BASELINE）
实验 FACTORY10-SKILL-24H-20261030，预定北京时间2026-10-30 16:00（Phoenix 2026-10-30 01:00）。本轮工厂固定F6，不因R14/R15失败或晚启动而改变顺序。派单前已读README V2、R06 STATUS/FEEDBACK/ADAPTATION，且确认R06 WORKBUDDY_REPORT、CHATGPT_AUDIT均404；不得伪称R06有评分、五维分或实跑结果。

## ① 同厂前次真实证据与评分
前次R06/F6 Job ID=52441e82f15942ab；R06/STATUS记载后续MCP追单返回429：“您的使用量已超出频率限制，将在2026-10-30 23:00:00 UTC+8重置”；其Job在列表中done/143字仅代表返回额度错误，并非研究完成。R06报告不存在，审计不存在，总分/五维=NOT_EVALUABLE，Δ、错误复发率=不可计算。源文件：rounds/R06/STATUS.md、rounds/R06/FEEDBACK_TO_BUDDY.md、rounds/R06/ADAPTATION.md。R06为首圈BASELINE计划，但未产生有效研究基线；R16必须标MISSING_BASELINE。
值得保留的是R06已设计的五个与F6战略吻合的实战题目及证据等级E0/E1/E2/E3、十字段、五案例正反测试和隐私许可边界；这些仅是计划，绝非前轮执行成果。最近可评分同厂以外：R12 F2 83/100(21/19/17/16/10)，R10 F10 76/100(18/19/15/15/9)，R03 F3 83/100(20/19/16/16/12)；不能将跨厂分差当成F6改进。

## ② 至少三项针对性整改：具体证据缺口→修复动作→验收
P0-1 来源、DOI与撤稿状态核验：R06没有研究正文，无法证明任何论文DOI/撤稿信息或候选插件真实存在；R10审计发现把尚未生效的NO FAKES Act称现行法，R12审计发现把原评分维度重命名。原因：缺一手来源和时间/版本锁定。修复：先用Crossref/OpenAlex/PubMed/出版商/撤稿数据库官方说明验证每项能力及论文元数据；给出原始URL、DOI、发布日期、检索日、撤稿/更正状态及冲突处理；只读可用性与真实调用严格分开。核验：≥12个可追溯官方一手URL/DOI（不把本机缓存算官方）、≥10条关键事实逐条证据分级、1条伪DOI及1条撤稿/更正冲突负例；不能把搜索命中当全文已读。
P0-2 Skill/Plugin安装与权限事实：R06原反馈列CoChat、Undermind、Pendar、Firecrawl、GitHub、Drive、Notion作为ChatGPT候选，但无R06报告核实WorkBuddy是否有等价安装/授权。原因：ChatGPT连接器与WorkBuddy云端能力是不同主体，市场缓存不是安装。修复：逐项给出ChatGPT CONNECTED_CONFIRMED/AVAILABLE_UNVERIFIED、WorkBuddy INSTALLED_CONFIRMED/MARKET_CACHED/SELF_BUILD/MCP_AUTH_REQUIRED；本机CLI --help、manifest/插件目录及官方文档证据，不能执行的标BLOCKED；费用按免费搜索/全文/调用/导出分别核查，未知UNKNOWN。验收：≥15个候选、Top5有可复制输入/命令/输出/报错处理；0无证据“已装、已授权、免费商用、已调用”。
P0-3 可复现研究交付与Git验收：R06零正文，R03声称完整模拟却缺源码/原始日志；R12报告Sim-E在Git回读失败时仍设done。原因：将作者自述、提交成功和独立回读混同。修复：五案固定输入、操作命令来源、非敏感请求响应、输出schema、正反例、退出码、成本配额、权限、回滚、状态；若执行了，正文直接附最小完整源码/命令/stdout/exitcode，未执行则PLAN_ONLY。Git commit成功与独立fetch回读分离，失败应GIT_UNVERIFIED而非DONE。验收：五案5/5十字段，每案≥1正1负；0无工件REAL_EXECUTED，0“回读失败却完成”。
P1-4 证据与研究偏倚：R06仅计划研究，没有处理同源转载、论文去重、语言偏倚、预印本与同行评审差异、数据再利用许可。修复：来源独立性、纳排标准、撤稿时点、学术证据等级、数据授权/PII与付费墙逐项表格化；至少一项不适用高中人群的教育研究不得外推。验收：每案例给冲突/偏倚登记及人工复核门槛。

## ③ 前次五案例逐一点评及补齐合同（前次均PLAN_ONLY，无真实结果）
A 学术DOI/撤稿审计：保留；固定10条DOI/标题混合样本含无效、预印本、撤稿；用官方元数据API或可核手工查询，输出PAPER_LEDGER.csv、DOI_AUDIT.md、RETRACTION_FLAGS.md；正例匹配元数据，负例假DOI不得自动补造；注明API限额、缓存时效、冲突人工复核、回滚错误旗标。
B 十大工厂趋势雷达：保留；输入F1-F10每厂3关键词和90天窗口，输出TREND_RADAR.md、SOURCE_LOCK.json、CONFLICTS.md；正例有官方release或论文，负例同源新闻转载不算独立证据；记录搜索配额、日期过滤与撤销错误趋势条目。
C WishTree认知学习证据综述：保留；固定诊断→探针→迁移→延迟复测研究问题，输出EVIDENCE_MATRIX.csv、LIMITATIONS.md、INTERVENTION_HYPOTHESES.md；正例纳排透明，负例成人研究不得直接外推高中；记录全文访问成本、数据许可及假设回滚。
D 跨国联盟电商官方政策研究：保留；输入3国家2商品类，输出MARKET_DECISION.md、POLICY_MATRIX.csv、UNIT_ECONOMICS.md；正例可查官方准入与披露，负例过期佣金或二手政策标UNKNOWN；记录国家税务/支付差异、费用与不进行开户发布的边界。
E 研究报告Git证据交付：保留；输入冻结问题和20条来源，输出REPORT.md、CLAIM_EVIDENCE.jsonl、REVIEW_LOG.md、MANIFEST.md；正例commit+独立回读一致，负例回读失败不得标DONE；记录仓库权限、隐私脱敏、可重试状态、回滚到前一已验证commit。
以上每案必须补齐目标、工具/插件状态、输入、具体步骤/命令出处、输出文件与schema、正反测试、阈值、时间费用、权限、失败回滚和真实执行状态。

## ④ R16与R06的差异化深挖及可比指标
R06只完成研究计划后429失败，R16深挖“学术事实可信性→工具权限→研究证据账本→独立报告回读”的最小闭环。优先实现一条合法、只读、可复核的DOI/撤稿查证链，再推广到五案例；研究ChatGPT现有CoChat/Undermind/Pendar/Firecrawl/GitHub/Google Drive/Notion与WorkBuddy实际环境对等能力、MCP授权及自建替代。指标：官方一手来源≥12，候选≥15，Top5命令/输入输出完整，五案例十字段5/5，正反测试各≥5，伪安装/伪执行/伪授权=0；由于R06无正文，纵向评分Δ及复发率不可计算。
禁止再次使用的无证据断言：索引=全文；缓存=已安装；ChatGPT可调用=WorkBuddy已授权；DOI存在=论文未撤稿；普通SHA=不可篡改；Git commit=回读验证；免费试用=永久零成本；报告长度=研究质量。请输出“上一轮问题→本轮修订→官方/CLI/manifest证据→已解决/部分/未解决/无法判断”对照表，并在未能核实时明确BLOCKED/UNKNOWN。

## ⑤ 跨厂方法反馈（只迁移方法，不迁移F2/F10业务）
M1 官方时效与来源级别：R10法律地位误判、R12五维错映射，先核权威文档/元数据并固定日期与证据等级；M2 原始可复现工件：R03/R10源码与日志缺失，E0必须有原始输入/命令/输出/退出码；M3 权限/成本/回读负例：R12模拟回读失败仍DONE，必须提供失败状态与恢复条件。每项都要在最终报告附可验指标及是否满足。
只读研究；禁止安装插件、付费、授权、模型切换、操作其他实验/分支、外部发布、读取或泄露凭据。WorkBuddy无需写Git，由ChatGPT负责正式归档。