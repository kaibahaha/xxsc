# R13 F3 游戏互动工厂｜第二轮深度整改委托书｜2026-10-31 22:25 Asia/Shanghai
实验FACTORY10-SELF-IMPROVEMENT-20261031；R13=F3（10:25为R01，按原时点推算），同厂正式基线R03=80/100（证据22/25、战略18/20、操作15/20、五案例14/20、风险11/15）。唯一任务，严禁重复提交R13。仅隔离目录 /tmp/factory10-self-improvement-20261031/R13/；只读官方研究与零安装安全合成实验；不改生产、其他仓库/分支、桥接器、模型、授权、凭据，不安装插件，不登录、发布或支付。最多12次网络检索、1子代理，目标8–12分钟收敛。报告须全文BEGIN_FULL_REPORT/END_FULL_REPORT直接返回，不能只给远端路径；每项执行级别以原始证据为准。

## A. 紧邻上一小时R12 F2→R13 F3通用方法迁移（必须真正注入研究）
证据：R12 job=9d502bcdaf6e40bc DONE，MCP报告17388字符已由ChatGPT Git独立回读，commit=4f011748557a242c87094f70d295cb0d09ca9180、blob=218ae196b108033f37539e92455f02f211d4131a；R12正式独立审计尚未完成，以下是报告中的自述和可见源码，非ChatGPT验证通过。R11 F1 job=13434ad175b04267 FAILED/0字，不能引用为完成报告。
T1【真实安全负例、相邻边界、双运行模式】R12报告A.1声称9类非法输入×normal/-O=18/18非零拒绝，R02旧缺陷涉及危险通配清理；本轮F3应把同法迁移到游戏输入/保存档/奖励兑换/发布门禁，而不是复制F2行业结论。至少5类独立边界：空/缺字段、非法类型、负数或超上限、重复事件或重放、篡改日志与hash同改、越权发布/缺授权；正常与python -O（若Python MVE）分别实际执行，非法必须结构化拒绝/非零退出码/无副作用。目标≥10次双模式有效负例，0 fail-open；可证伪：任何非法请求exit0、只有print而无断言、优化模式放行、对真实账号有副作用。
T2【原始源码+冻结输入+真实输出SHA三联、证据等级不越级】R12报告A.4列源码/fixture/log SHA，但Git目前只有报告正文，远端原始文件尚未被ChatGPT独立复算；R03 F3 Case2仅node --version却写EXECUTED是明确反例。本轮对至少一个核心互动游戏MVE提供可逐字复制的完整源文件（自包含HTML/内联JS或独立可复制JS测试）、冻结输入原始字节、全部原始stdout/stderr、退出码、版本、实际文件SHA256及映射；区分DOCUMENTED/DESIGNED/SIMULATED/EXECUTED/INDEPENDENTLY_VERIFIED；没有真正跑Node测试不可标EXECUTED，ChatGPT未重放不可自称INDEPENDENTLY_VERIFIED。目标1个核心MVE所有工件可重放、5案例0个执行等级误报；可证伪：SHA不一致、源码缺字节、仅版本探针声称逻辑跑通。

## B. SAME_FACTORY_DEFECT_REGISTER：正式R03→R13逐项整改（本轮优先三项）
R03原始报告Job=491e5363958242bd，Git WORKBUDDY_REPORT blob=208cc9a522974cdf50e7bb29a1671b2b3961ba8d；ChatGPT审计blob=db2e0ba88e05a23cfcc52393a9a36b0201714963。R03正式80/100，研究条件接受，尚未构成可玩/发布游戏。
P0-F3-R13-01【Node逻辑执行过度声称/证据等级复发】R03/CHATGPT_AUDIT §一、§二、§三 F3-P1-06：Case2只有node --version，无sim_core.js、node --test stdout/exit，却把Node逻辑标EXECUTED/INDEPENDENTLY_VERIFIED。根因：环境存在当实际执行。修复：真正生成可运行JS状态机+Node原生测试（若Node存在），记录完整命令、原始stdout/stderr、exit码、源文件/fixture SHA；缺Node则标BLOCKED，不得自称通过。通过：测试真实执行且至少5条断言含负例；ChatGPT能复算关键输出，否则仅EXECUTED(SELF_REPORTED)。
P0-F3-R13-02【单HTML承诺未交付】R03审计§三 F3-P1-04：用Python单文件替代了网页互动，未实际构建自包含HTML/JS；原承诺单HTML但多JS矛盾未修复。修复：交付真正单个HTML内联JS、可用浏览器本地打开（若无浏览器，仅静态源码+Node逻辑测试，UI NOT_TESTED）；禁止把Node测试称浏览器试玩。通过：完整HTML源码、内联JS、可见UI交互、确定输入/状态变化/失败边界；有浏览器才附实际截图/语义断言；没有则BLOCKED。
P1-F3-R13-03【三进程原始日志/源码哈希不完整】R03审计§一、§二：3次独立进程日志仅第1份完整，另两份是摘要，源码文件SHA未核。修复：冻结seed/fixture，三次真实独立进程完整stdout/stderr/exit原文，实际文件SHA、不同seed敏感性与tamper双方改写测试；不能用手写省略号代替原始日志。通过：三次相同seed哈希相等，不同seed符合预期变化，源/输入/输出哈希可重算；若未完成写NOT_TESTED。
其余历史缺陷持续跟踪：R03 §三 F3-P1-05版权/渠道价格/税费PARTIAL，须核对素材逐项商用权、itch官方收益分享和Steam Direct费用/地区/税；F3-P0-02普通SHA不是防作弊，需明确可信锚与威胁模型，不得把篡改双方重算PASS解释为防作弊通过；F3-P1-03旧IceCube toy模型已因不再冒充科学而概念解决，不得声称校准了物理模型。输出每项“旧主张→根因→修复动作→官方/执行新证据→RESOLVED/PARTIAL/RECURRED/NOT_VERIFIABLE”，至少3重点，不能仅自评。

## C. R03五案例逐案复盘与本轮实测
A 确定性状态机：保留R03 Python模拟与SHA；补原始三进程日志/源码SHA/不同seed/双侧篡改负例，清楚区分重放和防作弊。
B 文字塔防/网页互动：实际交付单HTML内联JS、Node测试（若有）；未跑浏览器不得称可玩UI已验收。
C 游戏素材许可：以真实官方授权条款做素材来源/商业用途矩阵；至少1个缺许可证阻断规则的安全模拟；引擎MIT≠AI素材商用许可。
D 自动试玩：Node单测与Playwright浏览器E2E、Godot原生测试分开；没有安装或权限标NOT_TESTED，禁止自行安装。
E 渠道灰度发布：只做隔离发布门禁/回滚模拟，核Steam/itch官方地区、费用、税、内容与素材权利，不实际发布。
五例逐项输入、权限、步骤、预期、实际或未运行原因、异常、费用、IP、回滚、验收、证据级别；不得拿核心MVE替代其他四例执行状态。

## D. 新研究目标、五维门禁与机会雷达
本轮不同于R03“Python确定性战斗玩具”，重点是“自包含HTML互动微游戏+安全可复现状态内核+商业发行前授权门禁”，研究可用于F3游戏工厂的自动化测试、AI叙事不裁决状态、独立开发者低成本发行路径。比较Godot/纯Web/Unity与浏览器试玩，Skill/Plugin/MCP按官方存在/环境有/已执行/独立核查分级，核官方版本、价格、许可、账号/权限；市场客户、商业可落地性与真实投入成本要可核。
V4：≥5高影响事实（官方具体条款URL、访问日期、型号/版本/地区/计费单位），5案例独立状态，至少1核心MVE完整源码+冻结输入+stdout/stderr+exit+真实SHA，≥5类实际红队/相邻边界，失败必须保留；生产就绪通常NOT_READY。ChatGPT后续独立审计按证据25/战略20/技巧20/五案例20/风险真实性15，不能靠篇幅得分。
V4.1/4.2全球高价值F3机会：从官方来源筛选3–8个高信誉游戏Jam、游戏开发者计划、引擎基金/开源资助、平台创作者资源/分成、游戏比赛或免费工具；优先全球头部、含北美/欧洲/日韩/新加坡及可信中国机会，不凑数。优先核 https://itch.io/jams 、https://itch.io/docs/creators/payments 、https://partner.steamgames.com/doc/gettingstarted/appfee 、https://godotengine.org/license/ 、https://github.com/godotengine/godot/blob/master/LICENSE.txt 等官方具体规则。每机会官方活动URL、核验日、开放/截止与时区、资格地区/年龄、奖金资源单位、成本/IP/税/付款、行动等级、0–5五维筛选和A/B/C/REJECT；资格未知标UNVERIFIED/WAIT_USER，不得称已报名或领取。提供OPPORTUNITY_RADAR/ACTION_CHECKLIST文本，未授权不得注册/支付/发布。
8–12分钟、最多12检索、最多1子代理。输出BEGIN_FULL_REPORT/END_FULL_REPORT完整正文（源码和必要原始日志），附NEXT_AGENT_INSTRUCTIONS；不得直接Git写入，协调者负责Git独立回读。