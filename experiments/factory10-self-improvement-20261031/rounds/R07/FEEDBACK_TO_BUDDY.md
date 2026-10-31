# R07 F7｜AI for Science｜双轨研究整改委托（BASELINE + HISTORICAL_REFERENCE）
- 实验 FACTORY10-SELF-IMPROVEMENT-20261031；计划 2026-10-31 16:25 北京时间；本次新实验F7首轮正式BASELINE，R17才与R07同厂比较。
- 已独立读取旧实验README、旧F7/R07 STATUS和FEEDBACK：旧Job 1941bb3a79e84c7f 最终仅回传1309字摘要，完整报告位于WorkBuddy私有路径，Git无旧WORKBUDDY_REPORT/CHATGPT_AUDIT；旧研究内容与分数不可核查，SAME_FACTORY_BASELINE_MISSING；不得伪造旧报告错误或旧评分。旧实验是HISTORICAL_REFERENCE，不是本次正式基线。
- 已读取紧邻上一小时R06 F6的STATUS、WORKBUDDY_REPORT、CHATGPT_AUDIT、ADAPTATION，R06 Job e8d1a46374fc4607 DONE，独立65/100（17/17/12/11/8），Git回读PASS；不得把跨厂65分作为F7基线或因果证据。

## A. CROSS_HOUR_TRANSFER：R06→R07，两项必须逐字执行、可证伪
**W1 [P0] 服务级错误归因门禁**。R06 WORKBUDDY_REPORT §1/§6把Crossref API的429与旧WorkBuddy模型额度429认作同源，R06 CHATGPT_AUDIT P0-429-ORIGIN判定没有服务、响应头、请求ID等证据，跨服务同码不等于同根因。原因假设：按HTTP码聚类、忽视API/模型/插件/代理层。R07对每项实际429/403或故障分别记录service、endpoint、UTC或北京时间、HTTP码、可公开的响应头/限额提示、重试条件、证据等级；无法取得原始响应标UNKNOWN，禁止伪造headers。至少构造一个错误归因正反例（例如模型配额429与学术API429不能混同），目标跨服务混因0次、同状态码推同根因0次。可证伪条件：任何缺原始依据的“同源故障”断言即W1失败。
**W2 [P0] 数值语义与原始可重放工件双门禁**。R06 REPORT §2把Runway网页订阅积分均摊成本约$13.84/min当开发者API价，否定官方API $0.01/credit×12credits/s×60=$7.20/min；又将Suno 2500credits/20downloads比值当单次扣费。R06列8个远端工件SHA却未把完整源码/输入/输出交给ChatGPT。原因假设：算术正确却缺业务口径/单位与独立可重放原文。F7须对至少5项重要科学/费用/数据数值给原始权威URL、版本/发布日期、单位、分母、适用场景、计算式、算术及语义双验；无权威数值标UNKNOWN。至少一个真正运行的低风险确定性科学计算/数据验证实验，把**完整可执行Python标准库源码、冻结输入（seed、样本、参数）、原始stdout、exit code、环境版本、SHA计算方法**直接嵌入MCP正文；未提供原文只能SELF_REPORTED，禁止把自报SHA说成独立复算。目标5/5算术+语义正确、≥1套ChatGPT可独立复放、0证据越级。可证伪条件：科学单位/适用范围错配、缺原始文件却声称独立验证即失败。
**上一小时通用改进：计划→实际注入→实际效果→下轮调整**必须在报告单列W1/W2逐项执行证据与失败点，不能仅自评PASS。

## B. SAME_FACTORY_DEFECT_REGISTER：旧F7无可用正文，以下仅为真实交付缺口与深化机会，不是虚构的旧报告内容缺陷
|ID|级别|旧证据/缺口|原因/风险|本轮修复要求|通过条件|
|---|---|---|---|---|---|
|HIST-F7-01|P0|旧R07 STATUS末段：Job 1941bb3a79e84c7f DONE但只回传1309字摘要，完整报告只在远端私有路径|摘要不能独立审计、Git缺正文|完整报告必须直接在MCP返回 BEGIN_FULL_REPORT/END_FULL_REPORT，正文不要只给文件路径/摘要|ChatGPT确实取到全文、Git独立回读；失败标PENDING/NOT_EVALUABLE|
|HIST-F7-02|P0|旧R07 FEEDBACK M1要求至少10条科学主张的原始DOI/版本/来源及运行证据，旧无可回读正文|文献存在不等于主张成立、撤稿可能漏查|至少10条可核查科学/数据/工具主张；每条权威URL、访问日、证据层级、适用范围、可证伪点；至少1真DOI、1伪DOI、1撤稿/更正样本；未读全文不得声称全文验证|独立抽3条来源正确，0 DOI→科学有效越级|
|HIST-F7-03|P0|旧R07 FEEDBACK M2要求科学有效性分层与真实负例，旧仅摘要无法审计|玩具模拟误当真实科学结论、数据泄漏|区分TOY_SIM、REPRODUCED_COMPUTATION、STAT_VALIDATED、REAL_WORLD_CALIBRATED、PEER_REVIEWED；至少5个科学负例（单位错、伪DOI、数据泄漏、错误SMILES、分布外等），每个写阻断条件|真实执行项有完整工件，未执行标NOT_TESTED；0玩具→真实结论|
|HIST-F7-04|P1|旧R07 FEEDBACK M3要求五案例十字段与状态，旧无可核查完整案例|纸面案例冒充实操|A-E五案例每个目标/冻结输入/工具及授权/步骤/预期输出/真实状态/正负例/成本与时长/失败回滚/明确PASS；至少1例真正运行可复放|5/5十字段；至少1例源码、输入、stdout直接交付；其余NOT_TESTED|
|HIST-F7-05|P1|旧实验插件/Skill候选无法通过完整报告核验实际安装/调用|“市场存在”误判“已安装已授权”|≥15个候选（含科学文献、计算、分子、材料、数据/科研协作），Top5逐项官方URL、真实命令/操作、免费/付费/权限/许可证、环境状态DOCUMENTED/ENV_PRESENT/AUTHORIZED/EXECUTED/NOT_TESTED|不能仅凭ChatGPT侧已连接就断言WorkBuddy侧已装；抽查Top5至少3项官方证据|
旧同厂正式内容缺陷=0（报告缺失），旧评分/错误复发率不可比较；上述5项均按“历史交付与证据缺口”审计。返回逐条“历史缺口→修复动作→新证据→自评结果”对照表，ChatGPT独立判RESOLVED/PARTIAL/RECURRED/NOT_VERIFIABLE。

## C. 五案例A-E逐案修订（旧版只是计划，非真实成功）
**A 科学文献真实性与争议地图**：保留10篇DOI/CLAIMS.csv/EVIDENCE.md/RETRACTION_CHECK.md；冻结至少真实、伪造、撤稿3种样本；逐条官方原文/元数据及L1-L3证据；负例伪DOI不得自动替换，撤稿不可作为正面支持；失败保留原输入快照；成本只读免费优先；通过=来源/日期/版本/撤稿证据可独立抽验。
**B 冰立方/IceCube类计数教学模拟**：保留固定seed、泊松信号/本底、SIM_SPEC.json/代码/RUN_LOG/METRICS；改为无外部依赖Python标准库实现一个真实可运行最小统计实验；负例单位错、seed不一致、负计数或不合理p值必须触发校验；明确教学玩具≠真实IceCube探测器校准；通过=源码+冻结输入+原始stdout可独立重放，不需要访问IceCube真实数据。
**C 小分子性质实验**：保留公开许可小分子/SMILES/DATA_CARD/MODEL_CARD；若RDKit未安装则NOT_TESTED，不安装；设计骨架切分/随机切分泄漏对照、无效SMILES拒绝、许可证与计算资源；通过=真实工具状态明确，未经运行不宣称模型指标。
**D 材料/物理数据工作流**：保留公开材料样本/单位/缺失/重复/PROVENANCE/VALIDATION_LOG；负例eV与J、Å与nm混用、分布外数据；冻结单位转换与来源版本；若无许可数据只给可运行的标准库合成验证，不冒充真实材料预测；通过=单位正确与异常阻断可重放。
**E AI科研助理治理/可复现研究包**：保留RESEARCH_PROTOCOL、MANIFEST、REPLAY_GUIDE、AUDIT_TRAIL；增加预注册假设、原始数据/版本哈希、环境、统计多重比较与人工审批；负例伪引用、个人敏感数据、未授权实验或未审查发表必须阻断；通过=证据链与审批边界可审计，不能冒充已获伦理许可。
五案例须明确保留内容、补充动作、输入、输出、异常、成本、回滚、执行状态与验收条件；不触碰真实患者/学生数据、不进行湿实验或危险实体操作。

## D. 本轮差异化研究目标、商业价值与边界
F7专题为“**低成本AI for Science证据与计算复现流水线**”：覆盖科学文献发现→数据许可证→计算/模拟→统计检验→复现包→产业化机会。与旧F7仅罗列工具/计划不同，重点交付可复核的最小科学实验、失败模式与科学有效性边界。分析至少15个真实插件/Skill/MCP/CLI候选、Top5实际使用技巧（含命令、费用、权限、失败处理）、市场机会与商业可行性；至少10条重要权威来源主张；5个案例按上述A-E。最多12次外部检索（包括子代理调用的外部检索总数，计数透明），最多1子代理，8-12分钟内收敛。只读官方资料与隔离临时目录标准库测试；禁止安装插件、授权登录、付费、读取凭据、切换模型、改生产/其他分支/旧实验、创建定时任务。完整报告正文经MCP直接回传，必须有BEGIN_FULL_REPORT和END_FULL_REPORT标记。最后输出W1/W2及HIST-F7-01~05的逐项执行证据/自评与下一轮可证伪测试。