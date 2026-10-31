# R03 F3 游戏互动工厂｜ChatGPT独立审计｜2026-10-31
- experiment: FACTORY10-SELF-IMPROVEMENT-20261031；本实验R03为F3首次基线，R13才可作同厂纵向比较。
- original WorkBuddy Job: `491e5363958242bd`；MCP返回完整BEGIN_FULL_REPORT/END_FULL_REPORT，原文16357字符；Git WORKBUDDY_REPORT.md blob `208cc9a522974cdf50e7bb29a1671b2b3961ba8d`，全文独立回读一致。Git提交 `4bc5fa513f80a4cf0bbb7faed2cfd779534f7da1`。
- 旧实验F3 R03 Job `5b8ee940847e42f2`，83/100（20/19/16/16/12），仅HISTORICAL_REFERENCE；不同研究重点和评分证据不能计算83→本轮的因果提升。
- **本轮正式评分：80/100（证据22/25，战略18/20，技巧15/20，五案例14/20，风险真实性11/15）。CONDITIONAL_ACCEPT_FOR_RESEARCH；游戏逻辑验证局部通过，未达到可玩游戏/发布就绪。**

## 一、固定五维独立评分
| 维度 | 满分 | 得分 | 核心理由 |
|---|---:|---:|---|
| 证据与事实 |25|22|完整回传内联Python源码与冻结fixture、命令/输出/哈希；ChatGPT独立按报告算法与输入重算SHA256=5a1ef86d9cd682307e587922c79aa1cafe556d3b7de41c9a1f903e29b1b1f3d1，EVENT_COUNT=16、RESULT=win，与报告一致。Godot/Steam/itch官方来源抽核通过；但3个原始进程日志仅第1次完整，2/3为省略版，源码文件SHA未独立核验，部分官方价格/平台政策未经证实。|
| 工厂战略契合 |20|18|确定性游戏世界裁决+LLM叙事、零安装逻辑实验与分阶段发行路线符合F3；但市场验证、玩家留存、产品发行、商业授权尚无数据，IceCube科学模拟被更换为战斗toy模型，不能说原科学模型已校准。|
| 操作技巧 |20|15|源码/fixture/哈希复现步骤具体，区分Godot、Node、Playwright与发行层；但Node JS逻辑代码并未生成，Case2仅node --version便称“逻辑EXECUTED”，属证据等级升级错误；Skill/Plugin具体授权/版本及运行证据仍缺。|
| 五案例 |20|14|5/5列输入、正负例、回滚、权限/成本/状态；Case1确有可复算工件，Case3有许可查证路线；Case2没有HTML/JS和真实Node测试，Case4无浏览器试玩，Case5未发布/回滚演练，案例3/4/5的负例大多是计划性阻断而非真实注入。|
| 风险、成本、真实性 |15|11|正确指出普通SHA无外部可信锚无法抗恶意重算、无外部发布和授权，工具缺失显式披露；但自评6缺陷5项RESOLVED过于乐观，Case2把未执行逻辑写EXECUTED，itch默认10%实际有官方资料却标UNKNOWN，Steam/微信费用、Inworld套餐尚缺独立证据。|
| **合计** | **100** | **80** | **研究及确定性内核可用作原型输入，不代表游戏已运行于浏览器、引擎已安装或可发布。** |

## 二、独立重算与官方交叉核验
1. **确定性算法独立复核：PASS（逻辑层）**。从WORKBUDDY_REPORT.md的Python状态机与SEED_FIXTURES.json按同一Python random.Random(20261031)、规范JSON序列化及SHA256重算，得到精确哈希 `5a1ef86d9cd682307e587922c79aa1cafe556d3b7de41c9a1f903e29b1b1f3d1`、事件16条、win、玩家HP15、敌方HP-5。证明报告的核心状态机输出可独立重现；不证明WorkBuddy声称的3次远端进程日志全部真实，因为其2/3日志仅摘要。
2. **篡改威胁模型：PASS（概念与算法）**。若攻击者可同时改event_log.json和event_log.sha，普通SHA校验可被绕过；报告的tamper模式返回PASS(false)，但这是“验证器被绕过”的失败示范，不是防篡改保护成功。未实现签名/外部可信锚，不得称防作弊安全已上线。
3. **Godot官方CLI：确认文档存在，不等于本机引擎运行**。官方 https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html 支持--headless、--export-release，但需真实编辑器与导出模板。官方 https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_web.html 还说明Godot4 C#项目目前不能导出Web、Web导出要求WebGL2、单线程Web导出更适合itch等渠道；F3若后续采用Godot必须按具体语言/渲染器/版本验证。
4. **itch.io官方费用：可更精确**。官方 https://itch.io/docs/creators/payments 明确Open Revenue Sharing卖家可设0–100%，例子默认10%，支付手续费常见约$0.30+2.9%，且退款、地区税、Payout模式另计。报告“默认~10% UNKNOWN”过度保守；同时其“免费发布/0费”不可理解为零交易费或零税费。
5. **Steam Direct：官方$100/app确认**。https://partner.steamgames.com/doc/gettingstarted/appfee 支持$100应用费与符合条件后可回收；报告提到的“Steam 30%抽成”未在此官方页证明，不能当本轮已验证。
6. **环境能力：仅远端自述**。报告python3/node/godot/playwright安装探针属于WorkBuddy本机自述，ChatGPT没有独立SSH读取其环境；能独立重算Python算法，不等于独立验证远端安装/授权。特别是A.M1 #3将“Node无浏览器逻辑可执行”标EXECUTED+INDEPENDENTLY_VERIFIED，实际无sim_core.js或node --test日志；应降为ENV_PRESENT(SELF_REPORTED)/DESIGN_ONLY。

## 三、SAME_FACTORY_REMEDIATION：旧实验F3六项历史缺陷逐条判定
| ID | 旧缺陷 | Buddy自评 | ChatGPT独立判定 | 证据与下轮门槛 |
|---|---|---|---|---|
| F3-P0-01 | 旧确定性模拟无完整源码、fixture、日志 | RESOLVED | **RESOLVED（可重算核心算法）** | 本轮Python源码/fixture内联，ChatGPT独立重算哈希完全一致；但三进程原始stdout仅第一份完整，R13需提交三份原始stdout/退出码与文件SHA。|
| F3-P0-02 | 普通SHA误当防篡改 | RESOLVED | **RESOLVED（概念与负例）** | 双侧篡改正确标UNDETECTABLE；可信签名/外部锚仍未实现，不能称安全防作弊已通过。|
| F3-P1-03 | 玩具泊松模拟误作真实IceCube科学 | RESOLVED | **RESOLVED（移除不当科学主张）** | 本轮明确TOY_MODEL战斗模拟，不再声称物理真实性；这不是对原IceCube科学模型的校准成功。|
| F3-P1-04 | 单HTML承诺与多JS产物矛盾 | RESOLVED | **PARTIAL** | 本轮用单Python文件替换了游戏内核，但没有交付单HTML/JS网页游戏，旧HTML目标并未完成。R13需实际单HTML和独立逻辑测试。|
| F3-P1-05 | 素材版权、发行费、AI credits不清 | PARTIAL | **PARTIAL** | Godot/Steam/itch有官方来源，部分精确价/授权未核；报告未给实际素材许可证据和地区税费。|
| F3-P1-06 | 引擎、浏览器、沙箱和schema证据边界 | RESOLVED | **PARTIAL/RECURRED（执行等级错误）** | Godot/Playwright边界文本改进，但Case2无JS/Node测试却标逻辑EXECUTED，属于历史“设计当执行”的同类问题复发。|
- historical_defects_count=6；**resolved_count=3（仅概念或可重算层）**；partial_count=3；recurred_count=1（F3-P1-06证据等级同类复发）；strict resolved_rate=50%，不代表原游戏产品已完成。
- new_defects=3组：Node执行过度声称、3进程原始日志不完整、商业费用/许可证据与执行混淆。旧83/100→新80/100为不同实验及审计重点，**same_factory_score_delta=NOT_COMPARABLE**。

## 四、跨小时R02→R03通用方法迁移（与同厂整改分账）
| 改进 | R02问题基线 | R03实测 | 结果 |
|---|---|---|---|
| M1证据四级+官方核验 | R02部分API权限/沙箱能力仅有文档无本机验证 | R03 10条断言多数带URL/UNKNOWN，环境探针有自述，且ChatGPT独立重算Python哈希；但Node被误标EXECUTED，部分价格/官方版本未经核 | **PARTIAL_EFFECTIVE**：证据可审计性提高，执行状态标注仍失准 |
| M2五案例负例+完整工件 | R02五例有负例/回滚字段但缺真实测试/原始日志 | R03内联Python源码/fixture与可复算SHA，双侧篡改负例清楚；其余四例多为方案、Case2假称逻辑已运行 | **PARTIAL_EFFECTIVE**：一个真实可复算案例；5/5真实负例目标未达到 |
- 不用R02 76分与R03 80分作跨厂因果提升判断。交付完整性再次通过（16,357字符MCP原文Git回读）。

## 五、五案例逐案R13整改门槛
- Case1状态机：保留Python核心，追加三份完整独立进程原始日志、源码文件SHA、可信锚的负例；验证不同seed/fixture能改变哈希且结果符合游戏规则。
- Case2 HTML+JS：必须提交实际可打开的自包含HTML、Node核心脚本与node --test原始输出/exit code；未执行前禁止写EXECUTED/VERIFIED。
- Case3素材：提交真实来源/许可/使用场景矩阵和至少一个缺许可证阻断的确定性规则测试；不能将Godot引擎MIT许可证等同于AI生成素材商业授权。
- Case4试玩：Playwright仅在授权安装后测试Web页面，语义断言、异常与回滚；未安装时维持BLOCKED，不得声称视觉或交互PASS。
- Case5发布：核实渠道官方地区费率、税费、审核/账号条件；只做本地发布门禁模拟，不实际发布；签名/回滚演练需真实工件证据。

## 六、R04 F4图像视觉工厂跨专题移交（最多两项）
- **T1完整可独立复核的工件证据链**：报告中若称生成/转换/检测“实际完成”，必须提供真实可取得的产物或确定性最小输入、源代码/配置、输出、原始日志、哈希、版本与授权；只有schema/演示文字不能标EXECUTED。目标≥1个可独立复核的只读/合成图像元数据或图像处理探针，报告全文Git可回读；未执行标NOT_TESTED。
- **T2防止“环境存在→业务执行”误升级**：每个核心工具/模型/插件标DOCUMENTED/ENV_PRESENT/EXECUTED/INDEPENDENTLY_VERIFIED，≥90%关键断言有官方URL或UNKNOWN，五案例明确实测/未测及真实负例。特别注意F3 Case2仅node --version却称逻辑测试PASS，R04必须避免；AI素材商业授权与来源不能由模型自述替代。
- 下一轮以实际F4历史报告为同专题参考，严格区分研究文档、图像生成成功、图像质量验收与商用版权。不得把游戏逻辑方法原样当图像领域结论。

## 七、结论
**80/100，研究可有条件接受。** 证据最强的是完整源码/fixture与ChatGPT独立重算一致；主要不足是Node执行误报、缺真正可玩网页与自动试玩、五案例实测覆盖有限。保留双轨审计，R04继续验证T1/T2，R13针对F3历史六项及新缺陷深度复测。无生产修改/安装/授权/发布证据，以上安全声明仅在可见调用范围内核验。
