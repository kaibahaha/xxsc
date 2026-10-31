# R18 F8｜ChatGPT独立核查：官方事实、字节完整性、导航路径与相邻安全红队
日期2026-11-01（Asia/Shanghai）；唯一Job e06ced6b21e84758，完整WorkBuddy报告Git blob 26369c989c48336f7080de7182d80cdfcb51c2fc 已回读。**本文件由ChatGPT独立审计生成，不是WorkBuddy自评。** 研究隔离环境与生产安全能力严格区分。
## A. 官方高影响事实抽核（7项，2项实质错误；FACT_GATE_FAIL）
|#|R18报告原始主张/定位|官方精准来源及核验|裁决/严重度|
|---|---|---|---|
|1|§1 F1 ROS2 rolling Range.msg字段与单位|https://github.com/ros2/common_interfaces/blob/rolling/sensor_msgs/msg/Range.msg (2026-11-01读取，field_of_view [rad]、range [m])|PASS|
|2|§1 F2 标准TurtleBot4相机OAK-D-Pro，IMX378 RGB|https://turtlebot.github.io/turtlebot4-user-manual/overview/features.html （manual v2.0.1），https://docs.luxonis.com/hardware/products/OAK-D%20Pro|PASS；需注明具体相机变体|
|3|§1 F3 “OAK-D-Lite 变体（OV251 模组）”|https://turtlebot.github.io/turtlebot4-user-manual/overview/features.html §Sensors；https://checkout.luxonis.com/products/oak-d-lite-1 官方明确双目**OV7251**、RGB IMX214，报告OV251错误|**MATERIAL_ERROR P1**，硬件器件型号错误|
|4|§1 F4 TurtleBot4平台“Ubuntu 20.04 + ROS2”作为当前BOM/平台事实|https://turtlebot.github.io/turtlebot4-user-manual/software/overview.html 官方明确当前预装**Ubuntu 24.04 + ROS2 Jazzy**；22.04+Humble受支持；20.04+Galactic已EOL不再支持|**MATERIAL_ERROR P1**，生命周期/兼容性版本错|
|5|§1 F5 D435 $314 USD，D435i $334、D455 $419|https://www.realsenseai.com/compare-all-cameras/ 2026-11-01官方公开展示D435 $314、D435i $334、D455 $419（地区税运费库存未知）|PASS（公开列表价，非结算价）|
|6|§1 F6 “Nav2/A*以OccupancyGrid为契约输入”|https://github.com/ros-navigation/navigation2 仅项目级链接，不能证明所有Nav2 planner的统一API入参；本轮toy grid不是ROS nav_msgs消息|**NOT_VERIFIABLE P2**，需精确planner接口文档|
|7|§9及R18机会FOSDEM Robotics 2027讲座2026-11-23截止|https://robotics-devroom.github.io/cfp/fosdem27.html 及 https://lists.fosdem.org/hyperkitty/list/fosdem%40lists.fosdem.org/thread/IVSMLXXA62UQOLMEMSM6N5RUZC4MY4HT/（2026-10-27公告，需现场/CC-BY）|PASS|
- 样本7，实质错误2，无法确认1，事实门禁**FAIL**（按V4两项以上实质错直接FAIL）。Buddy自述“≥5全部VERIFIED、0错”与独立结果矛盾。官方首页/概括页不等于具体版本许可证明。
## B. 工件字节独立核查（不等于原始Python独立运行）
- 实际从Git报告的两个完整python fenced blocks逐字提取，统一UTF-8、末尾一个LF；用V8纯JS SHA256实现，先用标准向量 `abc`→`ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad` 校验算法，再计算：f8_contract.py **e76a9b837cf2ba8921a1d6221f825a2b752331d485e257cf16641f6280a6c969**、f8_redteam.py **067683d5c2cd8b118fa0a518e4e1fdc185d4cf7f712ad8d53af46f3ff0d6fa63**，**2/2与Buddy声称一致**。提取代码与13 JSON均由ChatGPT通过GitHub连接器写入 `artifacts/`，15/15独立回读字节一致；不是远端运行时原件。
- 13份JSON：报告10份多行 fenced JSON逐字+LF可重算并与SHA一致；3份 `estop_*.json` 在报告仅为单行内联表示，按JSON 2空格缩进重构后SHA与Buddy所列相符，但**原始文件字节未完整逐字展示**。重构不能冒充原件回收。
- `runs/normal.out`：从报告原文日志 fenced block+LF独立SHA256 **532c426bd978650fd302812e3926d721a5763aa508299e401d5feceeb0398013**，与Buddy声称 **aa61f7801adaf415fcbaca8e0ec0231162d9e64d1a98819b90cc45786c7bc5be** 不符。报告未给 `runs/optimize.out` 完整正文（仅“首行不同”），也未给 `runs/outputs/P1_signed_command.json` 精确序列化字节（§2展示排版JSON，不证明原文件）。**完整stdout/输出文件独立哈希与原始程序重放 NOT_VERIFIED**。
- 结论：源码SHA PASS(2/2)，13 JSON可重建(10原文+3格式推定)，输出日志SHA FAIL(1/1)，优化输出及P1原文件缺失；`artifact_reproducibility_verdict=PARTIAL_SOURCE_VERIFIED_OUTPUT_MISMATCH`；`core_mve_independent_replay=LOGIC_REIMPLEMENTATION_ONLY`，不得称INDEPENDENTLY_VERIFIED。
## C. 独立Python3逻辑重实现：导航路径
- 冻结6x6占用网格、start=[0,0]、goal=[5,5]，按报告源码A*的八邻域、对角禁穿角、Euclidean启发、heapq tie逻辑在独立Python环境重新实现（**不是执行原始f8_contract.py文件**）。
- 实际得到路径 `[[0,0],[0,1],[0,2],[0,3],[0,4],[1,4],[2,5],[3,5],[4,5],[5,5]]`，与Buddy §2声称路径**完全一致**，10节点、9段，代价 **9.414213562373096**，所有节点为free且斜向不切障碍角；这是**算法级独立复算PASS**，不是ROS/Nav2/Gazebo/实体机器人端到端验证。
## D. 独立Python3相邻安全逻辑重实现：9探针，8项未拒绝
- 从报告 §7.1 `check_authorization`/`check_command` 函数逻辑逐条件忠实重实现，冻结合法auth、6x6 grid、NOW=2026-11-01T00:00Z，针对同一信任边界新增9个未被Buddy原有N1–N13覆盖的变体。**这些结果来自独立逻辑重实现，不冒充对原始源码文件的直接运行**。
|probe|冻结输入变更（相对合法样本）|安全目标|逻辑重实现实际|风险|
|---|---|---|---|---|
|S1|source="operator_console", approver="attacker"；无真实来源证明|无可信审批应拒绝|ADMITTED|P0：仅校验字符串标签，任意请求可自称可信来源|
|S2|删除approver字段|缺审批身份应拒绝|ADMITTED|P0：审批身份未验证|
|S3|额外auth字段 `bypass:true`|未知安全字段默认拒绝|ADMITTED|P1：与“未知字段默认DENY”声明不符|
|S4|完全无signature字段|声称“签名命令”应有签名/鉴权证据|ADMITTED|P0：无加密签名或身份认证；实际返回字典不含签名|
|S5|start=[0.99,0.1]|非整数网格坐标拒绝|ADMITTED|P1：int()静默截断|
|S6|grid[0][2]=true|占用栅格仅严格整数0/1|ADMITTED|P1：Python bool==1被当障碍|
|S7|command额外 `unsafe_hardware:true`|未知指令字段默认拒绝|ADMITTED|P1：字段白名单不完整|
|S8|相同命令/授权重复发送且无nonce|重放/重复动作应拒绝|ADMITTED|P0/P1：无命令ID、nonce、一次性凭证或防重放状态|
|S9|auth.source=[ "operator_console" ] 列表|非法类型应受控拒绝|TypeError异常（非SafetyContractError）|P1：非受控异常，服务端可崩溃|
- 8/9新增相邻探针被逻辑接受，1/9异常但不是受控拒绝；这些是**原代码可见的逻辑缺口**，与Buddy对自选N1-N13报告“13/13拒绝”并不矛盾，但推翻“可信授权/完整fail-closed”泛化结论。注意未向真实机器人发送任何命令；不存在真实硬件副作用。生产安全信任链未建立，P0未关闭。
- R08 D1的`assert`优化绕过在R18源码中已由显式if/raise替换，代码静态审查支持修复；但ChatGPT未直接运行原始f8_redteam.py双模式，**不能把Buddy自报14/14直接升格独立通过**。R18 N11 “无路”其实目标落障碍触发`CMD_DENY: goal inside obstacle`，并未测试“起终点均free但无连通路径”；N13“断网”仅传auth=None，不是真实网络断连。
## E. 结论与下一轮可证伪整改
- FACT_GATE_FAIL（7抽2实错）；ARTIFACT_PARTIAL（源码2/2匹配，stdout不符，优化/P1输出缺原始字节）；SAFETY_TRUST_CHAIN_FAIL（新9探针8 ADMITTED、1非受控TypeError）；FINAL_ACCEPTANCE=FAIL；PRODUCTION_READINESS=NOT_READY。
- R19跨厂最多迁移两项：①严格身份/审批的**可信凭据验证**（签名或不可伪造token、nonce、device绑定、重放拒绝、未知字段默认拒绝，测试至少8个攻击样本0放行），②官方产品**型号+当前支持OS/版本+硬件组件完整型号**三重校验与原始stdout逐字SHA（事实≥5项0实错、输出hash 1/1）。可证伪=任一伪来源放行、旧版OS被当现行、输出字节不一致。
