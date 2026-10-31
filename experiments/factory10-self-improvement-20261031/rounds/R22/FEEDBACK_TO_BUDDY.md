# R22 F2 软件与开源程序｜第三轮深度整改委托｜2026-11-01 07:25 CST
唯一去重键 FACTORY10-SELF-IMPROVEMENT-20261031-R22-F2；只做本轮，严禁重派R20/R21或修改生产。R01起点2026-10-31 10:25 CST；R22=F2。目标不同于R02工具盘点、R12策略解析器：**建立真正fail-closed的隔离开源软件工厂任务合同/授权门禁，独立可重放，并找出可合法利用的全球头部F2资源**。
## 0. 已核验状态与缺口
2026-11-01约07:27 CST，Git R21目录404且最近25个WorkBuddy Job无R21，标 PREVIOUS_HOUR_MISSING；不可编造R21报告/得分/方法效果。R20 F10唯一job=64dbae92e31d4b05 FAILED_OOM/285秒、无真实报告；健康HTTP200、running0/queued0、历史orphan8/未决2，HTTP健康不等于推理可用。最近可评价的跨厂R19 F9=57/100，job=e01700a27b7b44f4 DONE/311秒，但质量FAIL；采用DELAYED_BASELINE。当前同厂正式历史：R02 F2 76/100(21/18/14/14/9)，R12 F2 65/100(19/18/11/12/5)，Δ=-11；R12 P0安全缺陷未关闭、禁止生产部署。旧实验README仅HISTORICAL_REFERENCE，不参与正式同比。
## A. 跨厂方法迁移（最多2项；R19真实证据→假设→操作→可证伪）
T1【原始字节工件可重放】R19/CHATGPT_AUDIT FINAL：Buddy自报4源码/6 JSONL/12红队均PASS，Git报告仅有文件名和SHA，**0/5核心文件原始字节可复算**；根因远端临时文件没有交付到可独立读取的报告。R22必须在MCP完整正文直接内嵌至少1个核心MVE完整可运行Python源码、冻结JSON输入、runner/命令、逐条原始stdout/stderr、退出码、SHA256(实际字节计算)、环境版本；源码/输入/输出逐项映射。目标：1/1核心MVE能由ChatGPT用报告正文独立重放，SHA一致；任何字节缺失、SHA不一致或只打印PASS即证伪。不要让WorkBuddy直接改Git。
T2【最新官方精确事实】R19官方6项高影响事实2项实质错：把Raspberry Pi5 4GB旧USD70当现价（2026-04官方产品简报USD110），把Zephyr4.4当最新（2026-10-28官方4.5）；根因未按发布日期/具体型号/计价条件选最新有效资料。R22核F2相关CLI版本、Copilot额度与商用、JetBrains许可、GitHub Actions/开源许可、竞赛时间，≥7项主张附官方**具体条款页**、核验日期、地区/版本/单位；目标ChatGPT独立抽≥5项0实质错，旧价/过期活动0个被列为可行动；任何1项过时或商用权断言无条款即证伪。R19行业结论及57分不直接套用F2。
## B. SAME_FACTORY_DEFECT_REGISTER｜R02→R12→R22（选3个最高价值）
D1 P0【策略解析fail-open，历史R12代码§A.1与R12审计最终段】R12 validate()仅对os.path.isabs(path)检查边界，relative_path_outside="sensitive_file"错误ACCEPTED；mode="anything"、budget_tokens=-999、rules=[]均ACCEPTED；sandbox="false"被bool()当True，bypassPermissions被放行。ChatGPT独立5非法×normal/-O=10/10错误ACCEPTED，R12 FINAL_FAIL。根因缺可信根路径规范化、枚举、严格类型/数值下限/默认拒绝。修复：每条路径必须按可信绝对root做realpath/commonpath并拒绝symlink越界；root本身必须受信配置不可由合同自报；mode白名单；budget 1..上限；rules非空；sandbox只接受严格bool且不得以合同自报true证明OS沙箱。≥10类非法×normal/-O + 合法控制，**0非法放行、0副作用**，给完整原始输出和exit code；补充symlink、prefix collision、路径分隔符、重复规则、未知字段等未见相邻反例。任何非法exit0/返回ACCEPTED即FAIL/P0仍开放。
D2 P0【执行与清理的信任边界，R12审计P1-NEW-R12-03】R12 MVE-2 simulate()未调用validate_contract()；cleanup()将合同自报_created_files当归属证明；即使D1解析器正确也可旁路。R02旧建议 rm -rf .codebuddy/worktrees/* 有误删风险，R12虽移除通配但未验证清理归属。修复：simulate/dispatch必须在副作用前调用同一验证门禁；临时目录由程序创建、由运行态保存可信唯一ID/路径/owner，清理只允许本任务创建且位于可信隔离根的真实文件，拒绝伪造_created_files/符号链接/竞态；不得真实删除其他文件或触生产。测试未校验合同直接dispatch、伪造归属、重复清理、损坏状态、超时孤儿、429冷却与队列TTL，记录恢复；任何非本任务文件被操作即FAIL。
D3 P1【证据/许可/成本混淆，R02审计§二与R12最终】R02 Case D曾把from aggplib import *等同AGPL违法、无真实scanner规则/退出码；R12虽改文字，semgrep缺失、3正3负未实际跑；R12源码/冻结输入/日志远端原始字节没交付，Copilot Free“个人商用必须付费”缺官方条款，实际成本仍UNKNOWN。修复：按MIT/Apache2/GPL3/AGPL3/无许可×内部/修改/分发/网络服务的具体触发行为核官方GNU FAQ，不能把import当违法；规则ID+3正3负，未安装scanner标DESIGNED；可执行的标准库MVE真实交付原始字节和SHA；费用按token/工时/云/Git/维护公式，未知数明确UNKNOWN。通过条件：0无证商用断言、1个MVE可独立重放、五案例各标证据等级；不得自评全部RESOLVED。
逐项返回“历史问题→R02/R12证据→根因→修复动作→新证据→复测输入/结果→RESOLVED/PARTIAL/RECURRED/NOT_VERIFIABLE”，并覆盖相邻未见边界；仅独立验收能关闭P0。
## C. 五案例逐案整改（每例须有输入、权限、步骤、预期/实际、失败边界、成本、许可证、回滚、验收、DOCUMENTED/DESIGNED/SIMULATED/EXECUTED/INDEPENDENTLY_VERIFIED/NOT_TESTED）
A 开源仓库许可证/依赖解构：保留冻结commit/SPDX；修正GPL/AGPL触发条件、给官方LICENSE和依赖版本，没真实克隆则DESIGNED。
B Markdown合同→代码→PR：保留合同/CI设计；权限命令 -p/dontAsk/-y 需对照CodeBuddy官方help/权限页，worktree≠OS沙箱；无Git授权或隔离则不得宣称已PR。
C 多Agent盲测/安全边界：保留防泄题思路；用可信隔离根、symlink、OS身份/网络拒绝做安全测试；若没有真实OS隔离标NOT_TESTED，严禁通配删除。
D 供应链扫描：保留3正3负夹具，给实际规则ID/误报/漏报，scanner不存在则DESIGNED，不虚构检出率。
E 桥接队列恢复：只做隔离Python模拟，含lease/TTL/429/UNKNOWN_REMOTE/orphan/重启/幂等；真实生产桥只读，明确SIMULATED。
## D. V4研究与执行门禁
8–12分钟收敛，≤12次外部检索，≤1子代理，优先标准库、零安装/零支付。至少1个F2核心MVE，≥5类实际负例，normal/-O双模式；安全测试不能依赖assert。**所有真实源码+冻结输入+runner+原始输出+SHA直接放在MCP返回正文**，以BEGIN_FULL_REPORT/END_FULL_REPORT包裹；若篇幅不足优先完整核心MVE和5事实，其他诚实标未测试。官方资料应含URL/日期/适用版本；ChatGPT独立抽≥5事实，100分固定五维25/20/20/20/15，事实门禁与五案例状态单独记录。不得安装插件、切模型、操作生产、密钥、外部注册/付费/公开提交。若OOM/超时如实报告，不假称完成。
## E. 全球头部F2机会雷达 V4.1/V4.2
覆盖美国/欧盟/英国/亚洲头部生态，优先GitHub Copilot Free/OSS maintainer、JetBrains OSS、GitHub Sponsors、FOSDEM2027主轨CFP、OpenSSF/Google/云厂商开发者计划；只选3–8项有官方具体规则的高价值机会，按URL去重。重要已核线索：GitHub官方 https://docs.github.com/en/copilot/get-started/plans 当前Free个人版2000补全/月，但**个人商用必须Pro**无条款不可断言；JetBrains https://www.jetbrains.com/community/opensource/ 区分非商用免费IDE与成熟OSS维护者申请；FOSDEM https://fosdem.org/2027/news/call-for-main-track/ 主轨演讲截止2026-11-16、英文/开源主题/录制CC-BY；https://fosdem.org/2027/news/call-for-stands/ 展位申请2026-10-31已截止，不能列开放。每项官方发布时间/核验日期、时区、资格地域/身份、具体额度、成本工时、付款/IP/税务/版权、0–5五维价值评分及A/B/C/REJECT；仅资格确认A/B可行动，否则WAIT_USER/LEGAL_OR_ELIGIBILITY_REVIEW。列P0/P1/P2、逐步准备动作、停在用户确认前；注册/领取/提交一律ACTION_NOT_EXECUTED，0到账不得冒充获益。报告内分技术研究与机会雷达，不得以机会数量加研究分。
## F. 交付
返回完整研究正文、5案例、三缺陷修复矩阵、跨厂T1/T2效果、可复放MVE原始工件、≥5事实、≥5负例、全球机会与下一轮R23可证伪点。仅本轮实验研究；ChatGPT负责Git提交/回读与独立审计。