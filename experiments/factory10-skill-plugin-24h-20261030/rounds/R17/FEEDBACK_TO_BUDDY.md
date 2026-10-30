# R17 F7 AI for Science｜同厂反馈包（派单前）
实验 FACTORY10-SKILL-24H-20261030；计划北京时间2026-10-30 17:00；同厂R07，Job 1941bb3a79e84c7f。已读取同厂 rounds/R07/STATUS.md、FEEDBACK_TO_BUDDY.md、ADAPTATION.md；Git上R07/WORKBUDDY_REPORT.md和CHATGPT_AUDIT.md均404。真实get_workbuddy_result只返回约1309字摘要，称完整正文及12工件在WorkBuddy私有路径 /home/workbuddy_agent/f7_r07_baseline/F7_R07_REPORT.md；当前未取得完整原文。前次总分/五维=NOT_EVALUABLE；同厂Δ和错误复发率不可计算；MISSING_BASELINE_FULL_TEXT，禁止虚构历史评分。
## 保留的优点及证据级别
R07摘要声称用Python3.13.5标准库实现泊松教学玩具、seed=20261030/5000次重放；有10条文献样本含假DOI/撤稿负例，C分子/D材料因缺科学库诚实标PLAN_ONLY/BLOCKED，E科研治理包有MANIFEST与REPLAY_GUIDE；明确玩具模型不代表IceCube真实校准，ChatGPT侧应用权限不可由WorkBuddy验证。上述均属WorkBuddy自述，未经独立取得源码或日志。近期有效跨厂审计R12/F2 83分(21/19/17/16/10)、R10/F10 76分(18/19/15/15/9)，仅可迁移研究方法，不可推断F7质量。
## 四项整改：每条必须在本轮报告中列“R07问题→R17证据→是否解决”
P0-1【完整报告缺失】R07原话“完整的 Markdown 正文在 /home/workbuddy_agent/f7_r07_baseline/F7_R07_REPORT.md，附12个真实工件文件”，但Git仅有摘要状态、无原始报告。R17必须把完整Markdown报告直接作为MCP最终回复，不能只给私有路径或问是否需要贴出。至少两个RUN案例的最小源码、固定输入、原始stdout/stderr、退出码、校验方法应在正文可复制；验收0仅路径交付。
P0-2【运行证据不可复现】R07摘要称“无pip/numpy/scipy”等和“python3 sim.py exit0、5000次重放一致”，缺原始环境日志及脚本。先执行可脱敏的 python3 --version、python3 -m pip --version、模块importlib检查并提供真实退出码/输出；不能运行标NOT_TESTED。附完整标准库模拟源码、输入、固定seed与预期输出；至少5个负例（负lambda、单位错、参数、伪DOI、数据泄漏）；验收0无原始工件却称E0。禁止安装。
P0-3【科学来源核查链不完整】R07摘要称10条含假DOI/撤稿、Crossref HTTP200记录仍可能撤稿，却没有完整ID/响应/查询日期。R17提供≥12条一手论文/DOI/数据集/出版社或官方元数据来源、检索日期、字段、撤稿/更正信号、证据等级；负例假DOI、撤稿、更正、同名作者、虚假摘要。HTTP200不能当科学结论有效；网络失败标UNKNOWN。验收≥12可查来源、0伪DOI。
P1-4【跨账号授权误判】R07称WorkBuddy无法验证ChatGPT侧CoChat/Undermind/Pendar/Firecrawl/GitHub/Drive，不能由此断言ChatGPT未连接。R17分别列ChatGPT本会话连接器可调用（需ChatGPT独立验证）、WorkBuddy原生已装、市场缓存未装、需MCP授权、自建、未知状态；提供官方manifest/CLI help/API schema，严禁把市场存在当已装、把ChatGPT授权当WorkBuddy授权。验收≥15候选、Top5真实操作技巧、0权限臆断。
## R07五案例逐案审查及R17执行补强
A 文献真实性地图：R07摘要称有CLAIMS.csv/EVIDENCE.md/RETRACTION_CHECK.md，但正文/原始API响应不可见。保留；输入固定10 DOI含假DOI与撤稿，给Crossref/出版社核验命令、响应码、逐条输出和撤稿证据；负例429/伪DOI/更正，费用/限额注明来源或UNKNOWN，回滚到冻结数据版本；验收10条可追溯。
B IceCube/泊松玩具：R07称seed20261030、5000次重放一致；保留但必须给完整标准库脚本、参数JSON、命令、stdout/exitcode、输出CSV，负例负参数/单位/seed变化、统计检验；给时间与算力成本、脚本哈希回滚；明确非IceCube实测校准。
C 分子性质：R07为PLAN_ONLY/BLOCKED，禁止改称RUN。可给零安装SMILES字符串格式教学基线但不可冒称RDKit科学有效；固定公开许可样本、输入输出、命令/依赖、无效SMILES/泄漏负例、费用与版本回滚；需要RDKit则写安装前置，不执行。
D 材料数据：R07为PLAN_ONLY/BLOCKED；给标准库CSV单位/缺失/重复/来源质量门禁，公开许可输入、操作、输出、单位错/分布外负例、算力/人工费用与数据版本回滚；不得称真实模型已训练。
E 科研治理包：R07称有RESEARCH_PROTOCOL/MANIFEST/REPLAY_GUIDE/AUDIT_TRAIL，但未交可读正文；提供样例、哈希命令、人工批准与授权边界；未授权个人数据/伪引用/工件缺失/Git回读失败必须BLOCKED；普通SHA不能证明防恶意篡改；记录人力成本与回滚。
五案每案必须有目标、工具与授权状态、固定输入、具体操作/命令、输出文件、正反测试、验收阈值、依赖费用、失败回滚、RUN/PLAN_ONLY/BLOCKED；逐案评判R07问题是否解决。所有E0实测要原始证据，未实测不得声称成功。
## 本轮差异化目标及可比指标
R07偏工具地图与玩具模拟；R17专攻科学证据可信链、可重现最小研究包、零安装/限流/OOM时诚实降级。M1一手来源≥12且0虚构，M2至少2个RUN工件完整、5/5案例十字段，M3零无回读DONE和零跨账号授权误判。因R07无完整原文与审计，不得计算同厂评分差、错误复发率。报告必须逐条响应整改表并区分已解决/部分/未解决/不可判断。