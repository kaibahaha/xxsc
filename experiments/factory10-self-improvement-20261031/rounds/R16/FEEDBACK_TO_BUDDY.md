# R16 F6 研究报告工厂｜派单前冻结整改委托书（V3.2/V4/V4.1/V4.2）
计划北京时间 2026-11-01 01:25；R16=F6第二轮整改；R06同厂基线65/100（证据17、战略17、操作12、五案例11、风险8）。唯一任务去重键 FACTORY10-SELF-IMPROVEMENT-20261031-R16-F6。计划时刻之前仅PREPARED，不提前派单。8–12分钟收敛，外部检索总计≤12次（包含子代理检索），子代理≤1；只读隔离环境，禁止安装插件、登录、付费、修改Git/生产、切模型、注册/提交作品/发布、输出密钥。报告正文必须经MCP完整返回 BEGIN_FULL_REPORT / END_FULL_REPORT，不得仅报远端/tmp路径；ChatGPT独立Git归档与审计。

## A. 上一小时R15 F5→R16 F6跨专题通用方法迁移（两项，必须完整注入实际submit prompt）
U1【官方具体页+单位+资格/版本核对；事实零错门禁】R15/CHATGPT_AUDIT.md §C独立抽查7项有4项实质错误/误导：把HeyGen积分直接等同视频分钟；把ElevenLabs Grants总赠金误当每月；Suno Pro商用权/收入上限与下载量错误；AI电影奖宣传页与主办方正式规则冲突。R15=71/100、FACT_GATE_FAIL。根因假设：算术自检替代官方计费语义和条款版本核验。F6必须选择至少5项高影响研究工具/API价格、学术数据权限、发表日期、撤稿/更正、会议/投稿截止、免费额度与实际资格，逐条给官方具体URL、访问日期、原文定位、产品/模型/单位、地区、订阅/API/计费周期、时区、计算式与复算值、官方冲突；无法确认标UNKNOWN，不计正确样本。目标≥5项独立可查且0实质错误；若任何一项被独立证伪，U1失败。禁止把营销摘要、搜索摘要或主页当条款。
U2【严格输入类型与相邻边界安全红队+完整工件移交】R15/INDEPENDENT_REPLAY_EVIDENCE.md与R15/CHATGPT_AUDIT.md：原脚本5类既定负例通过、WAV/SRT SHA独立匹配，但validate(authorized='false')被Python truthiness错误放行，NaN时间戳、超媒体长度亦fail-open，P0。根因假设：只覆盖自选正负例，缺类型/有限值/范围约束。F6核心MVE改为研究报告证据准入与发布前门禁，严格 type(x) is bool、math.isfinite、边界/授权证明与可追溯source，禁止使用assert作安全拒绝；至少5类负例+3项相邻边界（字符串false、NaN/Inf、越界日期/页码/权利声明），正常与python -O都fail-closed，0未授权发布/0写盘副作用。完整可复制源码、冻结输入、真实stdout/stderr/exit、原始输出及SHA256直接随报告返回，不能只给远端路径。目标≥1独立可重放核心MVE且≥8负例0 fail-open；任一错误接受即安全门禁FAIL。仅验证格式不能声称研究结论真实或商业许可有效。

## B. 同厂R06 F6→R16 F6专项深度整改（同厂优先，逐条原文/定位→根因→修复→官方证据→复测→通过条件）
D1【P0 跨服务429根因混淆】R06/WORKBUDDY_REPORT.md §1/§4/§6把Crossref GET 429称与旧WorkBuddy模型额度429“同源”；R06/CHATGPT_AUDIT.md §2 P0-429-ORIGIN指出仅HTTP状态相同，不证明服务、配额或出口同根因。整改：记录服务名、endpoint、时间、HTTP码、Retry-After/RateLimit等响应头（不可得则UNKNOWN）、请求ID与重试结果；对Crossref、OpenAlex、模型网关分开分类；禁止无证据跨服务归因。验收：至少1正例1负例可复核分类，0“同码=同根因”；不额外触发付费或故意限流。
D2【P0 API与Web订阅价格混用、比值误当扣费】R06/WORKBUDDY_REPORT.md §2称Runway $0.01/credit非官方并以网页Standard套餐$12÷625×12.02×60=$13.8462/min冒充API价；官方 https://docs.dev.runwayml.com/guides/pricing/ 显示API $0.01/credit、Gen-4.5 12 credits/s，基础API $7.20/min。R06还以Suno 2500credits/20downloads=125推断每次下载成本/额度，除法正确但不等于真实扣费。整改：按API/Web订阅/折扣/税费/适用地区/模型分别核价，给原始单位、官方页、公式、语义适用性，未知标UNKNOWN。验收：至少5条高影响事实零错，Runway API/Web绝不混用、Suno上限比值不称单次消耗；新增学术API配额/投稿费同样严格核对。
D3【P1 Nature原论文日期错、撤稿字段证据不足】R06/WORKBUDDY_REPORT.md §4写Nature DOI 10.1038/nature12968 2014-01-28，R06独立审计核出版者 https://www.nature.com/articles/nature12968 的Published 2014-01-29；撤稿公告 https://www.nature.com/articles/nature13598 为2014-07-02。报告自述Crossref updated-by但缺原始API正文，不能认定已独立核验。整改：逐条以出版者原始页面、Crossref/OpenAlex元数据、撤稿公告/更正记录核日期和关系；出版日期、上线日期、卷期日期分离；无元数据正文时标NOT_VERIFIABLE_FIELD。验收：≥3个真实/撤稿/无效DOI原始响应可定位，撤稿事实不依赖标题关键词，0日期错。
D4【P0 超检索预算】R06/WORKBUDDY_REPORT.md §0/§1自报13次直接检索+子代理另检索，超过12次限制。整改：每次外部检索与子代理调用计入统一计数，先预算官方核验，达到12立即停止并标缺口；验收≤12总检索、≤1子代理、无隐性扩容。
D5【P1 工件缺失与五案例纸面化】R06/CHATGPT_AUDIT.md §2：报告列ARITH_CHECK.py、CLAIM_EVIDENCE.jsonl、PAPER_LEDGER.csv等8文件SHA，但未移交真实源码/输入/原始响应；五案例A/E自述EXECUTED，B/C/D未执行。整改：至少1完整证据准入MVE提供源码、输入、stdout/stderr、退出码、SHA、负例，ChatGPT可独立重放；15+插件/Skill/MCP/CLI候选中Top5明确DOCUMENTED/ENV_PRESENT/AUTHORIZED/EXECUTED和费用、数据许可、API限额；不得把已列出哈希当文件已交付。验收：1套独立可复现工件，五案例0证据越级。重点选择D1/D2/D3三项为本轮专项深改，D4/D5作为硬性门禁不得遗漏。

## C. R06五案例逐项复盘，R16不得只列计划
A DOI与撤稿核验：保留有效/无效/撤稿三样本，扩展到≥5条高影响主张；冻结DOI/出版者URL/访问日/原始响应，区分元数据、原文论点与版权，测试无效DOI/撤稿字段缺失/更正冲突；无全文不称论文论点通过。
B 十厂趋势雷达：R06 NOT_TESTED；保留90天窗口与同源去重设计，本轮至少运行一个小型冻结样本去重/时间窗口MVE（若资源允许），给时间窗边界、重复转载负例、来源质量，真实90天全量未检索仍NOT_TESTED。
C 高中认知学习综述：R06 NOT_TESTED；保留RCT/观察/适用年龄分级，构造至少1条论文样本的证据等级演示，禁止使用学生PII；未读全文不得推断因果。
D 多国联盟电商政策：R06 NOT_TESTED；保留3国×2品类框架，选择一条官方联盟准入或佣金规则作为可核验示例，给国家/地区/资格/税费/广告披露/版本；不注册不推广，剩余未执行如实标记。
E 研究报告证据交付：R06自述EXECUTED但仅远端哈希；R16优先实际运行claim→source→version→rights→reviewer门禁MVE，提供可复制Python源码+冻结JSONL+原始输出+SHA256，负例授权字符串false、NaN置信度、未来/无效日期、未授权来源、重复冲突、损坏JSON、路径越界等，明确正常与-O模式；不得将格式有效=论文正确=可商用。
每例逐项写目标、保留/修改、冻结输入、前置权限、操作步骤/命令、预期与实际输出、执行状态、边界负例、成本与授权、回滚、独立验收条件；至少一个核心MVE，五商业案例端到端执行数不得虚构。

## D. 差异化研究目标、全球机会与质量门禁
R06主题是“DOI撤稿/算术探针”；R16改为“可供十大工厂复用的研究证据发布前安全门禁与报告生产质量体系”：验证声明真实性、来源版本、许可/撤稿、异常恢复、跨工厂报告交付；给官方可核验市场需求、≥15工具候选、Top5真实使用技巧/权限/费用、五案例、成本与数据风险。全球头部优先搜集3–8项高信誉研究算力、科研API免费额度、论文/会议征集、研究竞赛、基金/创业项目与客户试点；官方规则、截止时区、资格、实际价值、IP/数据/支付风险、P0/P1/P2与A/B/C/REJECT，不符合资格或未知不得列可立即领取，全部ACTION_NOT_EXECUTED，不登录注册/付费/投稿。若无高质量机会则明确无。
输出BEGIN_FULL_REPORT/END_FULL_REPORT，包含：①D1-D5“旧证据→根因→整改→官方证据→复测→自评”表；②U1/U2实际证据与目标值；③至少5条可独立核验官方事实；④完整可复算源码/输入/日志/哈希/≥8负例；⑤五案例状态；⑥全球机会官方规则与行动卡；⑦剩余风险与未知；⑧下轮跨厂最多2项方法建议。最终五维评分仅由ChatGPT独立作出；Buddy自评不得冒充独立验收。