# R08 F8｜ChatGPT独立审计｜2026-10-31
- 实验 FACTORY10-SELF-IMPROVEMENT-20261031，F8机器人感知与动作，本实验首轮正式BASELINE；R18同厂复测。
- 唯一Job **b76c0601c10f4d60**；WorkBuddy MCP list_workbuddy_jobs确认为 **DONE / 489秒 / 14517字符**，get_workbuddy_result实际返回BEGIN_FULL_REPORT/END_FULL_REPORT完整正文；Git WORKBUDDY_REPORT.md commit **af138af32037bec1c145236137c8cd939906234e**，blob **853cbb7dc1c574d0653f8318969c3e64bdeb0d56**，逐字回读PASS。桥接成功≠机器人生产能力通过。
- 旧实验F8 Job fc588db4b904442c failed/0字，旧Git无WORKBUDDY_REPORT/CHATGPT_AUDIT，SAME_FACTORY_BASELINE_MISSING；R07 F7独立68/100只作Q1/Q2跨厂方法来源，不能跨厂比较总分因果。

## 固定五维独立评分（总分100）
|维度|得分|独立依据|
|---|---:|---|
|证据25|19|完整MCP原文、20候选、两份完整Python脚本，两个源码SHA及stdout SHA独立一致；但ROS2 Range误引ROS1 Fuerte文档、TurtleBot4相机型号泛化、RealSense硬件价格错误，10次检索仅Buddy自报无原始搜索轨迹。|
|战略20|18|低成本机器人感知→安全动作→仿真→试点路线清晰，适合小团队；客户需求与付费意愿仍为假设。|
|操作技巧20|15|ROS2/Nav2/MoveIt2/Gazebo/MediaPipe等Top5给出具体命令和前置条件；但ROS/Gazebo/硬件均未实装实测，版本与许可存在泛化。|
|五案例20|13|A-E均有输入/步骤/负例/回滚/状态，Q1/Q2零硬件代码真跑；但五个具体业务案例均PLAN_ONLY或NOT_TESTED，不能把安全闸门算作五个业务场景已跑通。|
|风险及真实性15|8|诚实声明零实体控制；但急停负例使用assert，python -O可直接绕过；“错误单位”实为正确换算后越界；错误硬件报价、版本证据和不限定路径的rm -rf cache不宜进入生产。|
|合计|**73/100**|**CONDITIONAL_ACCEPT_FOR_RESEARCH / NOT_READY_FOR_PRODUCTION**。本轮73为R18正式同厂基线，跨厂R07 68→R08 73不代表自我改进因果或同厂提升。|

## Q1独立代码/字节/输出复放（真实独立Python3.13.5）
- 从Git报告的两个 ```python fenced blocks逐字提取，按报告“UTF-8 + 最后一个LF”保存为隔离临时文件，不调用外部网络/机器人。
- robot_zero_hw_safety_sim.py 源码SHA256 **6aeb8a8875d451ee0f1c0fba7fd1d57bfa5ab1e79320758cc9104febb43f8baa**，与Buddy自报完全一致；独立Python3.13.5 exit **0**，stdout原文 `{"executed_linear": 0.8, "status": "OK", "ts": 1000, "vmax": 1.0}\n`；stdout SHA256 **0adbdd2d96766e4624ee54428105c5513b7e7d42c7b0f2eab39b1573c0a3a072**，与Buddy自报完全一致，stderr空（在独立普通container Python3.13.5执行）。
- safety_negatives.py 源码SHA256 **3c5cbc32ac3866a9440af7450c377441caf4178ca19b5d30ba7f03924361a380**，与Buddy自报一致。
- 结论：Q1 **EFFECTIVE_FOR_BYTE_REPRODUCIBILITY**，源码SHA一致2/2、正常stdout一致1/1，R07“源码/输出版本漂移”本轮未复发。该结论仅证明文本工件与确定性脚本可复现，不代表ROS/Gazebo/真机仿真能力已验证。

## Q2五负例独立重放与安全红队测试
|场景|Buddy声称|独立普通Python结果|加严核查|
|---|---|---|---|
|speed超速|exit1 ValueError|exit1，错误文本一致|仅常量v/vmax，未接真实指令入口|
|estop急停|exit1 AssertionError|exit1，错误文本一致|**P0: python3 -O safety_negatives.py estop → exit0，安全门禁被完全绕过**；assert不可作为生产急停拒绝逻辑|
|ts时间倒退|exit1 ValueError|exit1，错误文本一致|仅静态输入，尚未与真实传感器时钟对接|
|unit错误单位|exit1 ValueError|exit1，错误文本一致|270度已正确转换成4.7124弧度，触发的是角度范围超限，**不是未转换单位的检测**；负例命名/覆盖失实|
|net断网|exit3 stderr|exit3，错误文本一致|online=False静态布尔，不是实际网络失联故障注入|
- 普通解释器五个负例**5/5确实返回非零**，纠正R07“只print阻断”的问题；但优化模式下急停**1/5可绕过**，安全门禁健壮性未达标。不能把“异常代码已执行”推广为安全认证。
- Q2 **PARTIAL_EFFECTIVE / FAIL_SAFE_GATE_NOT_ROBUST**。R09必须使用显式if/raise并分别在正常与python -O模式运行，目标5/5两模式均阻断；对输入解析、NaN/Inf、零/负vmax、时间戳、单位标识等边界做真正参数化测试。

## 官方来源与商业事实独立核查
1. **P1-ROS-VERSION-LINK**：Buddy把ROS 2 `sensor_msgs/msg/Range`指向 `https://docs.ros.org/fuerte/api/sensor_msgs/html/msg/Range.html`；Fuerte是旧ROS1发行版，不能作为ROS2发行版的精确官方标识证据。ROS2官方源码 `https://github.com/ros2/common_interfaces/blob/rolling/sensor_msgs/msg/Range.msg` 确认`field_of_view`为rad，`range/min_range/max_range`为m；**单位事实正确、版本证据错配**。
2. **P1-TB4-CAMERA**：`https://turtlebot.github.io/turtlebot4-user-manual/overview/features.html`支持Create3底座、Raspberry Pi4B 4GB、RPLIDAR A1M8、0.31m/s安全速度、0.46m/s非安全模式、1.90rad/s、9kg；但标准TurtleBot4为**OAK-D-Pro**、Lite为**OAK-D-Lite**，Buddy的“OAK-D/OAK-D-Lite”泛称不准确。
3. **P1-REALSENSE-PRICE**：`https://www.realsenseai.com/products/stereo-depth-camera-d435/`支持D435 <2% @2m、0.3–3m、1280x720/90fps及USB-C 3.1等技术规格；但`https://www.realsenseai.com/stereo-depth-cameras/`官方公开价格D435为**$314**，不是Buddy报告案例D及预算中写的**$179**。旧价/二手价若无证据不能当当前新品价格；TurtleBot4套件预算也未给同日可核官方报价。
4. **P1-REAL-EXECUTION**：Gazebo官方`https://gazebosim.org/docs/harmonic/ros2_integration/`确认ros_gz_bridge桥接功能；Nav2官方`https://docs.nav2.org/rolling/community/maintainer_docs/distribution_release/`存在tb4_simulation_launch.py。**官方命令存在不等于WorkBuddy实际安装或运行**，本轮未启动ROS/Gazebo。
5. **P2-MARKET-ROI**：教育套件$1500–2500、SO-100双臂$230–244及“可达性高”等未经逐项当前报价、运费、税、许可/客户需求核实；只能视为粗略机会假设，不可直接商业采购。
6. **P2-CODE-SAFETY**：`rm -rf cache`未限制路径/权限，不适合直接用于业务自动化；Q1脚本仅验证linear速度比例，未验证angular、ts、真实设备输出，键名`executed_linear`只表示toy报告字段而非真机执行。

## CROSS_FACTORY_TRANSFER：R07 F7→R08 F8（方法与效果，不用跨厂分数作因果）
|method|R07具体证据|本轮实际注入|R08独立观察|verdict|
|---|---|---|---|---|
|Q1源码/哈希/stdout字节一致|R07源码SHA不符1/1、stdout不符1行|Git FEEDBACK 3945字符完整内嵌MCP 4354字符prompt|R08源码SHA 2/2一致，正常stdout 1/1一致，exit0；无ROS/真机运行|**EFFECTIVE_FOR_DETERMINISTIC_REPRODUCTION**|
|Q2官方ID+真实负例阻断|R07原论文DOI错误、单位错只打印|同上|普通Python5/5真实阻断；但-O急停绕过、ROS2引用ROS1旧文档、TB4相机泛化、D435价格错|**PARTIAL_EFFECTIVE / SAFETY_AND_VERSION_FACT_ERRORS_RECUR**|
- 跨厂同类指标：R07代码SHA0/1、stdout0/1 → R08源码SHA2/2、stdout1/1（内容与难度不同，说明局部方法有效，不证明总体研究质量因果）；R07真负例仅部分 → R08普通解释器5/5，但优化模式4/5；官方标识/价格仍有错误。

## SAME_FACTORY_REMEDIATION（旧F8报告缺失；仅审计历史交付/证据缺口）
- old experiment R08 Job fc588db4b904442c FAILED_NOT_SUBMITTED_TO_CODEBUDDY，0字，旧Git无WORKBUDDY_REPORT/CHATGPT_AUDIT；formal_old_content_defects=0，historical_evidence_delivery_gaps=5；old_score_delta=NOT_COMPARABLE、old_error_recurrence=NOT_COMPARABLE，不能用本轮评分计算旧报告修复率。
|缺口|Buddy自评|ChatGPT独立判定|核验与下轮通过条件|
|---|---|---|---|
|HIST-F8-01旧无完整报告|RESOLVED|**RESOLVED_DELIVERY_ONLY**|本轮MCP全文14517字、Git逐字回读PASS；旧报告并未恢复|
|HIST-F8-02官方证据/源码|RESOLVED|**PARTIAL**|两脚本SHA正确，但ROS1/ROS2证据错配、部分价格/版本未经核对；须精确官方版本和真实环境状态|
|HIST-F8-03仿真/安全|RESOLVED|**PARTIAL**|普通Python5负例真跑，-O急停绕过；真实ROS/真机未测；须显式if/raise双模式PASS|
|HIST-F8-04五案例|PARTIAL|**PARTIAL**|5例字段较全但A-E均未作为完整案例独立实跑；至少一个案例端到端可重放|
|HIST-F8-05生态/市场|RESOLVED|**PARTIAL**|20候选、Top5存在，但硬件D435价格和采购预算错误；须锁定产品型号/日期/官方报价|
- 历史交付缺口**1/5 RESOLVED_DELIVERY_ONLY、4/5 PARTIAL**；同厂历史内容错误解决率与复发率不可计算。本轮新缺陷至少6类：assert安全绕过、单位负例误分类、ROS1/ROS2引用版本错配、TB4相机型号泛化、D435现价错误、五案例无端到端执行。

## 五案例逐案核验与R18要求
- A桌面纸笔：PLAN_ONLY；缺真正可复现的合成事件处理器、JSONL、误检/遮挡运行日志。通过=固定输入→JSONL+异常+清理实际执行。
- B机械臂：NOT_TESTED；仅ROS/Gazebo/MoveIt设计，未运行规划/碰撞检查；通过=冻结模型及真正仿真工件，不把toy当物理认证。
- C导航：NOT_TESTED；A*仅建议，缺地图/路径工件；通过=固定地图→路径+障碍/失联断言。
- D手势遥操作：PLAN_ONLY；未执行合成手势到白名单命令；D435硬件价格需纠正；通过=合成序列→白名单日志，误触发拒绝。
- E多传感器：NOT_TESTED；仅Q2时间戳常量负例，不等于同步误差评测；通过=冻结时间序列→max_offset/dropped_frames/drift真实报告。
- R18至少完成一个**完整业务案例**的输入→算法→输出→异常→回滚，且有独立复放证据；不必安装/控制实体机器人。

## R09 F9跨小时迁移建议（最多2项）
**S1 [P0] 可重放工件与不可绕过安全门禁**：R08两源码SHA2/2、stdout1/1成功；但急停assert在`python3 -O`下exit0。R09 F9必须给源码+输入+stdout/stderr+SHA，独立复放一致；安全拒绝使用显式if/raise，不用assert作运行时安全闸门；普通与-O模式均测试≥2故障，目标阻断2/2×2模式、0绕过。可证伪=任一模式exit0或字节不一致。
**S2 [P0] 版本精确官方证据与当前成本**：R08 ROS2 Range误引ROS1 Fuerte、TurtleBot4 OAK-D-Pro型号写泛、D435 $179与官方$314不符。R09 AIoT需对≥3核心设备/协议/SDK按具体版本官方URL和同日价格/许可核验，目标版本错配0、价格错配0；可证伪=任一旧版链接冒充新版、不同型号混价或来源不明的预算。只限研究prompt/方法，不改生产/调度/插件授权。

## 最终判定
**73/100：MCP真实报告与Git交付成功，零硬件Python仿真源码/输出独立复现PASS，普通模式五个安全负例真实触发；但优化模式急停绕过、版本/型号/价格事实错误、五个业务案例未端到端执行。研究有条件接受，生产NOT_READY。**