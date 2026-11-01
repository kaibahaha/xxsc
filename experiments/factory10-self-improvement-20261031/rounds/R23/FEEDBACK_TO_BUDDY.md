# R23 F3 游戏互动｜第三轮精准整改委托书（V4/V4.1/V4.2）
- 唯一去重键 FACTORY10-SELF-IMPROVEMENT-20261031-R23-F3；计划 2026-11-01 08:25 Asia/Shanghai。R23=F3，不得重派/补派R21或R22。研究目标区别于R03的Python玩具战斗和R13的Node安全状态机：**交付真正可复现、可试玩的单文件HTML交互微游戏原型（如文字策略/塔防）及可独立验证的逻辑安全门禁，并比较全球高价值Game Jam/发行资源**。无浏览器则只能证明Node逻辑，UI NOT_TESTED。
- 仅云端临时隔离 /tmp/factory10-self-improvement-20261031/R23/，只读官方资料与零安装合成实验；严禁更改生产、桥接器、模型、其他分支、授权、用户账号或凭据；不安装、不发布、不注册、不付费。研究8–12分钟、最多12次检索、最多1子代理。远端R22发生OOM，优先小体量完整核心工件，不要调用多代理/长上下文；OOM直接原样报告，不能伪装DONE。
## 0. 已核验历史与两条反馈线
R03 F3 job=491e5363958242bd，Git报告blob=208cc9a522974cdf50e7bb29a1671b2b3961ba8d，ChatGPT独立80/100(22/18/15/14/11)，可独立复算Python战斗SHA=5a1ef86d9cd682307e587922c79aa1cafe556d3b7de41c9a1f903e29b1b1f3d1，但Node只跑node --version却声称逻辑EXECUTED，三进程原始日志只有一份完整，未交单HTML。R13 F3 job=1192f68c0b0d449a DONE632s，Git报告blob=88127942ac4c528e326878bc3b1a222941b4e1c4，报告自述Node16/16、双模式28/28、单HTML和三进程日志；R13/CHATGPT_AUDIT.md后置独立审计发现报告只有一个2549字符core.js代码围栏，**没有完整game.html、core.test.js、Python测试、冻结夹具和原始日志字节**；R13正式100分仍NOT_EVALUABLE、五事实未完整独立审计，不能编造R03→R13的分差。
上一小时R22 F2 job=1b6feeaf3f514af1已通过MCP get_result真实确认FAILED_OOM（90s/232字），无WORKBUDDY_REPORT，故跨小时标PREVIOUS_HOUR_REPORT_MISSING；R21亦Git404且job未见。最近已完成且独立审计R19 F9 job=e01700a27b7b44f4，57/100、6项官方事实2错、0/5核心源码可独立复算，作为DELAYED_BASELINE；不得把F9行业结论或57分迁移到F3。
## A. 跨厂通用方法迁移（2项，必须在研究中落实）
T1【实际工件交付，不让OOM或远端路径吞掉成果】R19 F9自称4源码/6 JSONL/12红队均PASS，Git全文只见文件名/SHA，0/5核心工件可复算；R22 F2唯一Job又OOM，无Buddy正文。假设：复杂大输出+只存远端路径使证据不可交付。修复：优先完成一个最小自包含HTML/JS微游戏+Node可运行纯逻辑测试，将完整源码、冻结输入、真实命令、stdout/stderr、退出码、实际SHA256（从文件算）**原样内联BEGIN_FULL_REPORT/END_FULL_REPORT正文**；控制报告规模，其他4案例允许DESIGNED/NOT_TESTED。目标1/1核心MVE源码输入输出可被ChatGPT独立重放，五案例0次等级夸大；证伪：只给远端路径、SHA不符、日志省略、无正文、模型OOM。若核心HTML过长优先提供完整单HTML及最小Node测试，禁止宣称未交付文件已交付。
T2【现行官方条款、活动时区与可行动资格】R19 F9用Raspberry Pi5 4GB旧USD70替代2026-04官方USD110、Zephyr4.4当最新4.5，官方6抽2实错；R13 F3机会表把Game Off 2026标立即可参与，实际上官方 https://itch.io/jam/game-off-2026 显示**2026-11-01 21:37:27 UTC才开放提交**（本轮北京时间08:25时尚未开放）；GDevelop #10官方 https://itch.io/jam/gdevelop-big-game-jam-10 显示2026-11-06 19:00 UTC才开始，且**必须用GDevelop引擎、英文、浏览器可玩、≤4人、itch和gd.games双提交**；R13仅写“现金奖”漏条件。假设：只认官网不核日期、时区与资格，造成机会错分。修复：≥7条关键产品/许可/活动断言附当前官方具体规则页、访问日、时区、适用地区/引擎/版本；将未来开放、正在开放、截止和资格未知分开；目标ChatGPT后抽≥5项0实错、0未开放活动标立即报名；证伪：过时数字、资格缺漏、主页冒充规则、未开放标OPEN。
## B. SAME_FACTORY_DEFECT_REGISTER｜R03→R13→R23，三项最高价值整改
D1 P0【核心可玩HTML及原始工件未交】R03审计Case B：仅Python单文件，无HTML/JS；R13报告§A.T2自述game.html存在，但R13审计后置发现报告无<!DOCTYPE html>、无HTML完整字节，亦无core.test.js/fixtures/三进程日志。根因远端临时文件不等于交付。修复：真正单个HTML内联JS，具有按钮、可见状态、回合推进、胜负/错误反馈；附可独立运行Node纯逻辑测试和至少5断言，冻结事件输入、原始stdout/stderr/exit与实际SHA；UI若未实际浏览器运行标NOT_TESTED。通过：Git能保存全文，ChatGPT可提取源码复跑核心测试并核SHA；否则NOT_VERIFIABLE。
D2 P0【模拟鉴权/哈希链冒充真实安全】R13内联core.js把auth_token硬编码为公开字符串 AUTH-R13-F3-VALID，SECRET=公开常量factory10-r13-f3-anchor-v1；verifyChain与写入同源，无外部可信锚，攻击者能同时改日志和哈希；R03已明确普通SHA不等于防作弊。根因信任边界混淆。修复：明确威胁模型；本地toy仅用于演示校验失败，不声称安全授权；游戏状态验证采用白名单动作、合法状态迁移、不可负资源、重复event_id拒绝、无授权publish拒绝，至少5类边界含缺字段/非法类型/越界/重放/同源篡改/伪造令牌；真实服务端鉴权/可信签发明确NOT_IMPLEMENTED。通过：实际负例有输入、预期/实际、退出码、0副作用、恢复方式；任一fail-open则P0仍开放，绝不生产部署。
D3 P1【执行等级和商业机会资格反复夸大】R03 Case2 node --version被标逻辑EXECUTED；R13虽自报Node16/16但缺测试源码和原始日志，不能独立验证；R13 §D机会表将未开放的Game Off、GDevelop、PROCJAM均标A级立即可参加，且将部分费用/IP/地域未经细则确认就断言全球资格。修复：按DOCUMENTED/DESIGNED/SIMULATED/EXECUTED/INDEPENDENTLY_VERIFIED/NOT_TESTED逐案例定级；Node版本查询≠运行，Git报告≠工件，加入官方赛事规则+时间/年龄/引擎/AI披露/IP/税费核查。通过：至少5高影响事实独立可抽、0执行等级误报、0未开放误报、赛事资格不明标LEGAL_OR_ELIGIBILITY_REVIEW。
每项必须输出「历史原主张及R03/R13定位→根因→修复动作→新证据→冻结复测输入/结果→RESOLVED/PARTIAL/RECURRED/NOT_VERIFIABLE」，不得自评即关P0。对D1新增HTML完整性、D2新增同源伪造相邻边界、D3新增时区状态相邻边界。
## C. 旧五案例A-E逐项复盘与新五案例
A 确定性游戏世界：保留R03可复算seed战斗、R13 Node状态机概念；本轮优先完整HTML微游戏+可独立运行的逻辑内核，给源码、输入、结果、SHA、5类负例、回滚。B 文字塔防/浏览器互动：必须真正单HTML内联JS与UI交互，浏览器未跑则UI NOT_TESTED，不能以Node代替浏览器。C 游戏素材与生成AI：Godot MIT只涵盖引擎，不等于素材权利；官方许可/来源/AI披露矩阵+未授权素材阻断例，未运行标DESIGNED。D 自动试玩：Node单测/Playwright Web E2E/Godot原生分别定级，无浏览器或授权不得安装，写NOT_TESTED。E 渠道发布：只做安全发布门禁与回滚设计，核Steam Direct $100/app、itch实际收费与税、Game Jam平台/源码公开要求，不实际上传/付费/注册。五例分别写输入、权限/账号、步骤、预期/实际、失败与边界、费用、许可/IP、回滚、验收、证据状态，不用MVE代替其他案例。
## D. V4质量与红队门禁
≥5高影响事实可按官方具体条款独立抽样；每个数字有日期、币种/单位/地区/计算口径。1个核心MVE真实源码+冻结输入+命令+原始stdout/stderr+exit+实际SHA；≥5类实际负例，至少一项针对R13公开token/同源hash；测试必须非零失败退出码，不靠仅打印PASS或可关闭assert；可独立重放才可能INDEPENDENTLY_VERIFIED。区分WORKBUDDY_SELF_REPORT、CHATGPT_INDEPENDENT_AUDIT、FINAL_ACCEPTANCE；严禁自封独立验证/READY。100分五维25/20/20/20/15仅ChatGPT打分。
## E. V4.1/V4.2 全球头部F3机会雷达（与技术主线独立）
全球头部优先、覆盖北美/欧盟/日韩/新加坡/中国高信誉生态，不凑数。重点官方候选：
1 Game Off 2026 https://itch.io/jam/game-off-2026 2026-11-01 21:37:27 UTC至12-01 21:37 UTC，GitHub主办，公开Git仓库+itch提交，当前WAIT_OPEN。
2 GDevelop BIG Game Jam #10 https://itch.io/jam/gdevelop-big-game-jam-10 2026-11-06 19:00 UTC至11-15 20:00 UTC；必须GDevelop、英文、浏览器、双平台提交、≤4人，奖金规则以页内官方为准，当前WAIT_OPEN。
3 thatgamejam #02 https://itch.io/jam/thatgamejam02 2026-10-24 07:00 UTC至11-08 07:59 UTC，当前提交开放；需Windows/Mac可运行、英文默认、AI素材披露，奖品USD3000/2000等，官方要求作品版权归作者但授权主办展示；用户是否有成品及身份资格未确认，不得标可直接提交。
4 Epic MegaGrants https://www.unrealengine.com/megagrants 2026第二周期9月4日23:59 ET已截止，下一期未公告，仅观察，不列开放。
可扩展Godot/Unreal/GitHub创作者计划或其他真正官方高价值资源，最多3-8项；每项主办/规则URL、日期时区、资格（国籍/居住地/年龄/团队/引擎）、费用/奖金单位、支付/税务/IP/AI政策、0-5五维筛选、A/B/C/REJECT、P0/P1/P2、预计工时、操作清单、下一步及明确停止条件；资格不明UNVERIFIED，不得称已领取/报名。禁止任何登录、注册、支付、公开发布和法律提交。机会表只计官方可核，不把发现当获得。
## F. 交付要求
以BEGIN_FULL_REPORT/END_FULL_REPORT包围完整研究正文，优先把核心MVE完整源码/fixture/原始输出内联，避免R19缺件和R22 OOM；报告含插件/Skill/MCP存在性、安装/权限/成本、五案例、三缺陷、跨厂T1/T2、5事实、5类负例、全球机会、NEXT_AGENT_INSTRUCTIONS。不得自行写Git，ChatGPT负责独立审计及Git提交。若受内存限制，只返回实际完成与失败原文，禁止虚构。
