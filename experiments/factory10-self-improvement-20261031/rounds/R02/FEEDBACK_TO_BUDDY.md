# R02 F2｜FEEDBACK_TO_BUDDY｜2026-10-31 11:25 Asia/Shanghai
实验 FACTORY10-SELF-IMPROVEMENT-20261031；新实验R02=F2软件与开源程序工厂。**本轮为新实验F2基线，不得冒充R12同厂第二圈；旧实验F2 R02仅HISTORICAL_REFERENCE。**

## A. 上一小时跨厂迁移（R01 F1 → R02 F2，必须真实注入并逐项验收）
证据：新实验 rounds/R01/WORKBUDDY_REPORT.md，job aab758d7c33d4631 DONE，远端自称382行完整报告但MCP仅返回1517字摘要；新实验 rounds/R01/CHATGPT_AUDIT.md 正式NOT_EVALUABLE；rounds/R01/ADAPTATION.md。
- M1【P0交付完整性】：不能只把完整研究报告留在WorkBuddy远端并返回路径或摘要。本轮报告正文**必须完整直接出现在MCP任务最终响应**，并用BEGIN_FULL_REPORT/END_FULL_REPORT界定。目标可核查正文覆盖100%，报告有5个案例完整操作步骤、至少8个官方来源URL；如遇输出上限，必须在正文中明确TRUNCATED、分段编号及缺失部分，不得声称完整。上轮baseline：全文未到、不可评分；本轮target：完整可读/可Git归档；可证伪条件：只返回路径/摘要/缺失案例。
- M2【P1版本/负例】：上轮已纠正CodeBuddy原生调度、Agent REST≠通用LLM网关等概念混淆，但v2.168.3默认30天与scheduled-tasks文档循环3天有适用范围差异。F2对CLI/API/Skill能力必须标官方版本/适用范围/文档冲突，不作无范围的否定或肯定；五案例5/5必须有负例、失败注入、回滚、阻塞依赖、是否实测。指标关键能力主张≥90%有官方一手来源或明确UNVERIFIED；5/5有负例和回滚；可证伪条件：任何案例缺负例/回滚，或将未安装命令写成已执行。

## B. 同厂历史详细整改（旧实验 F2 R02，历史参考，不是本实验R-10）
旧实验Git：experiments/factory10-skill-plugin-24h-20261030/rounds/R02/WORKBUDDY_REPORT.md、CHATGPT_AUDIT.md、STATUS.md；旧Job f77da8aaab28496d，DONE，全文23826字符已Git回读；旧审计81/100，五维证据22、战略18、技巧16、案例15、风险10。优点：37条环境/命令证据日志；209插件市场缓存 vs 本机0安装区分；五案例覆盖开源仓库解构、Markdown合同PR、三Agent盲测、供应链门禁、桥接器可靠性。历史环境证据为2026-10-30时点，不得当作当前环境事实。
SAME_FACTORY_DEFECT_REGISTER：
- F2-P0-01【工作区隔离误当安全隔离】旧报告案例C原意“Agent_i只可见dir_i与题目、--add-dir限定”。官方 https://www.codebuddy.cn/docs/cli/worktree 与 https://www.codebuddy.cn/docs/cli/permissions 表明worktree/--add-dir不是OS访问控制，子Agent权限仍可越目录。整改：区分工作区冲突隔离、身份权限隔离、进程/网络隔离、独立评测盲测；只有独立容器/VM或OS权限证明拒绝跨目录读取，才能称“盲测隔离”。验收：给出负例读取他人答案/共享缓存/网络出口的系统拒绝证据；本机无容器则明确BLOCKED/设计未验证，不声称防作弊通过。
- F2-P0-02【无人值守授权过宽】旧案例B用了 -p/-y + acceptEdits + --allowedTools Bash,Read,Edit,Write；单条Bash(git push)禁令不能阻止其他写入或越权访问。官方 https://www.codebuddy.cn/docs/cli/permission-modes 和 https://www.codebuddy.cn/docs/cli/headless。整改：最小权限、独立低权限执行身份、仓库只读/PR专用GitHub App权限、允许路径与工具的真正外部强制控制、明确审批门；区分工具层拒绝与OS层拒绝。验收：对越目录/推送/读取凭据三个合成负例分别写预期拒绝点、实测状态与审计日志；未执行则NOT_TESTED。
- F2-P1-03【GPL/AGPL一刀切】旧案例A将GPL/AGPL依赖一律“禁止直接复制”。GNU官方 https://www.gnu.org/licenses/gpl-faq.en.html。整改：区分许可证类型、复制/修改/链接/再分发/网络服务等场景及许可证义务，不提供绝对法律结论；未知许可停止代码复用而可继续只读研究。验收：MIT/Apache-2.0/GPLv3/AGPLv3/无许可5类矩阵，输出适用情景和人工法律审核触发条件。
- F2-P1-04【工具缺失导致案例不可运行】旧远端自测E21报告git/uv/uvx/docker/semgrep等缺失，旧报告部分命令仍假设工具存在。整改：每案例先列运行时依赖与本环境实际检查、零安装API/标准库替代方案和需授权安装方案；当前环境须重新只读核查。验收：5/5标READY/BLOCKED/DESIGN_ONLY，任何实际未运行的测试不得称PASS。
- F2-P1-05【安全门禁检出率缺实测】旧案例D“100%检出”只来自3类设计样本，无扫描器/真实CI日志。整改：合成凭据/依赖/误报样本集，区分阻断和告警、规则版本、误报/漏报；未运行标NOT_TESTED。验收：至少3正3负合成样本及预期测试命令，若声称通过必须有真实退出码和日志。
- F2-P2-06【商业优先级与权限成本】旧Top5未充分结合当前无git/无docker、ChatGPT GitHub连接器已可写Git、WorkBuddy未授权MCP的事实。整改：按立即可用/审批后可用/不可用排序，区分ChatGPT连接器与CodeBuddy本机插件权限；计算试点人力/云成本/维护风险，未核价格标UNKNOWN。验收：优先推荐零安装可运行的只读仓库解析+Markdown合同+Git回读路径，成本与权限有证据。
历史五案例逐案要求：A 开源仓库解构→冻结commit+SPDX矩阵+未知许可负例；B Markdown合同→PR→最小权限、失败阻断、commit与readback；C 三Agent盲测→OS级隔离与作弊负例，无法实现则不叫盲测；D 供应链门禁→合成样本与实际scanner阻塞，未装则NOT_TESTED；E 桥接器恢复→固定只读快照、Job ID幂等、queued/running/orphan/429/进程恢复、Git写入与回读分离，绝不触碰生产。
本轮须逐项输出“历史问题→修复动作→官方/实测新证据→RESOLVED/PARTIAL/RECURRED/NOT_VERIFIABLE”，并对五案例逐一标出保留/重做与明确验收；不要把报告写得更长当成改进。

## C. F2本轮新的深挖方向
在旧F2市场盘点之外，聚焦FactoryOS“Markdown任务合同→GitHub只读/写入→CodeBuddy编码→可复跑测试→独立审计→失败恢复”的**零安装可行MVP**及高级代码工厂能力分层，比较可用GitHub连接器、CodeBuddy原生能力、Skill/插件候选、GitHub Actions/CI、开源Agent框架。必须核对官方一手来源（至少8条可访问URL）、当前CLI help/版本只读证据（若实际可执行）、安装状态/费用/许可证、工具能力层次（生成/执行/授权/隔离/发布），并设计五个具象可操作案例；每案含目标、输入、最小操作/命令、输出、正反例、失败回滚、依赖、权限、成本、验收。最多12次网络检索、最多1子代理，8-12分钟目标；不安装、不授权、不改模型/生产/其他Git分支、不泄密、不创建定时任务。请在最终MCP结果中**直接返回完整中文研究正文**，而不是仅报告远端文件路径。