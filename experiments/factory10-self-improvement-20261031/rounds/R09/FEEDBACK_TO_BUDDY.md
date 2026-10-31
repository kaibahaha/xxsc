# R09 F9｜AIoT智能硬件工厂｜BASELINE与双轨整改委托（北京时间2026-10-31 18:25）
实验 FACTORY10-SELF-IMPROVEMENT-20261031；本轮为F9首次正式基线，R19才进行同厂纵向对比。禁止把旧实验R09或R08 F8分数当本实验F9基线。仅允许本轮唯一一次submit_workbuddy_task，不得创建其他定时任务。

## 事实基线（已通过GitHub连接器读取）
紧邻R08 F8：Job b76c0601c10f4d60 DONE，489秒，14517字符，Git完整报告/审计/状态/改进均可读，独立73/100（证据19、战略18、技巧15、案例13、风险8）。R08正常Python下5个安全负例退出非零，但急停用assert，python3 -O safety_negatives.py estop实际exit0，属于P0绕过；两份源码SHA独立一致2/2、stdout一致1/1。R08将ROS2 Range引至ROS1 Fuerte文档，将TurtleBot4标准版OAK-D-Pro泛称OAK-D/OAK-D-Lite，将D435当前官方$314错写$179。跨厂只迁移可核查的方法，不能用73分跨厂因果比较。
旧实验（HISTORICAL_REFERENCE）README在 experiments/factory10-skill-plugin-24h-20261030/README.md；旧R09 Job a178c0e82f10461d最终FAILED_NOT_SUBMITTED_TO_CODEBUDDY/0字，只有旧STATUS、FEEDBACK、ADAPTATION，无完整WORKBUDDY_REPORT/CHATGPT_AUDIT。旧F9内容缺陷无法判断；只能修复有证据的历史交付/验证缺口，不能捏造旧报告错误。新R09首轮正式MISSING_BASELINE，同厂评分差与旧错误复发率NOT_COMPARABLE。

## A. CROSS_FACTORY_TRANSFER（强制实际执行，逐项报告“前轮证据→本轮执行→新工件→实测指标→判定”）
**S1 [P0] 字节级可复放+双模式不可绕过安全门禁。** R08源码SHA2/2、stdout1/1虽成功，但estop使用assert导致普通模式exit1、python -O模式exit0。原因假设：把调试断言误用为运行时安全保护。整改：至少1套零硬件AIoT离线协议/控制模拟，Python标准库、冻结输入、完整原始源码独立fenced block、UTF-8与末尾LF、版本、运行命令、原始stdout/stderr、exit code、64位SHA256。至少2种真实故障（如MQTT重复命令、设备身份错误、OTA签名不符、时间戳倒退、离线缓存超限）必须使用显式if/raise/非零退出，分别用python3与python3 -O实际运行，给4次原始结果；不得使用assert承担安全门禁。目标源码SHA与独立复放1/1、stdout1/1，2故障×2模式=4/4阻断；可证伪=任何故障在任一模式exit0、代码与哈希不一致、仅打印blocked、用SHA冒充数字签名。严禁连接真设备或真实broker。
**S2 [P0] 官方版本/型号/当前成本逐项对应。** R08存在ROS2引用ROS1旧文档、TB4标准相机型号泛化、D435报价$179与官方$314冲突。原因假设：官方网页存在但产品版本、SKU、日期和计费语义未锁定。整改：至少3个AIoT核心设备/协议/SDK（例如ESP32-S3+ESP-IDF、MQTT v5 OASIS、Zephyr版本、Matter CSA、Raspberry Pi、Eclipse Mosquitto）逐项写出官方精确URL、文档/硬件版本、适用范围、截至本轮查证日期、价格/费用单位/许可；无当前官方价格标UNKNOWN，不可虚构。独立检查版本错配0/3、价格/许可错配0/3；可证伪=用旧版本冒充新版、不同SKU混价、未核实价格写精确采购预算。不要把官方文档可用误写为环境已安装/权限已获批。

## B. SAME_FACTORY_DEFECT_REGISTER（旧F9无真实报告：下列为历史交付/证据缺口，不是虚构的旧内容缺陷）
|ID|级别|可核历史事实与风险|本轮修复动作|独立通过条件|
|---|---|---|---|---|
|HIST-F9-01|P0|旧Job a178c0e82f10461d最终failed/0字、无完整正文|直接通过MCP返回BEGIN_FULL_REPORT至END_FULL_REPORT全文，非仅远端路径|ChatGPT取得真实报告并Git逐字回读，失败保持NOT_EVALUABLE|
|HIST-F9-02|P0|旧反馈M1要求事实/安装/授权/实跑四层证据，但无报告可验证|≥10一手官方来源，≥15真实候选，Top5官方URL/版本/命令/权限/费用；明确DOCUMENTED/ENV_PRESENT/EXECUTED/INDEPENDENTLY_VERIFIED|独立抽查≥3条官方事实，0无工件实跑断言|
|HIST-F9-03|P0|旧反馈M2要求MQTT QoS/幂等、OTA签名、TLS设备身份/安全边界，但无执行证据|实现S1双模式故障注入；解释QoS不是业务端恰好一次、SHA不是签名、TLS不是设备授权；零真机|≥2真负例×双模式、明确仿真≠安全认证，关键术语与官方规范一致|
|HIST-F9-04|P1|旧五案例A-E仅委托设计，未返回执行工件|逐例冻结输入→步骤/命令→输出工件→正反例→异常/回滚→权限→成本→执行状态，至少一个零硬件案例实际运行|五例字段5/5，至少1例端到端可复放，其余标NOT_TESTED|
|HIST-F9-05|P1|旧没有可审计的成本/商业落地报告|比较本地/边缘/云端费用、数据隐私、客户与付费假设，给可用Skill/Plugin/MCP和部署限制|≥15候选、Top5深度操作、成本来源清楚，不把市场机会当已验证营收|
旧内容缺陷数0（因旧报告缺失）；上述5项历史缺口按RESOLVED/PARTIAL/RECURRED/NOT_VERIFIABLE分别返回“历史缺口→修复动作→新证据→验收结果”，不能宣称旧故障根因已修复。

## C. 五个AIoT商业案例逐项复盘（旧实验只有计划，不是旧成功）
A **WishTree桌面纸笔边缘感知**：保留合成桌面纸笔事件→JSON；补遮挡/误检/权限/隐私与缓存删除；冻结合成事件输入，输出事件JSON及混淆矩阵；禁止真人/未成年人图像，未跑标PLAN_ONLY。
B **MQTT消息网关**：保留温湿度与设备状态，采用本地离线合成消息而非真实broker；明确MQTT QoS 0/1/2与应用层幂等差别；输入含重复/乱序/断网/设备身份错误，输出去重轨迹和拒绝日志，回滚临时缓存；优先选为端到端可复放案例。
C **ESP32/Zephyr OTA安全演练**：仅模拟签名验证/版本门禁/A-B槽与断电恢复；输入合法/篡改manifest，输出拒绝/回滚状态；不要把sha256摘要等同于数字签名，不刷真实固件。
D **边缘AI推理选型**：比较已有CPU/GPU与ESP32/RPi/Jetson等候选硬件，官方型号/SKU/价格/功耗区分，缺设备标NOT_TESTED；输入冻结模型/样本，输出P50/P95延迟、内存、功耗测量条件，禁止编造实测。
E **NAS离线任务中心**：只负责队列/日志/缓存，重推理交其他执行池；合成任务流测重复派单、存储满、断网重传、时钟漂移；输出幂等审计记录，回滚到只读快照，不接生产NAS。
每例必须明确保留点/缺陷、固定输入、官方工具与环境/授权、完整步骤、输出、正反测试、成本、回滚、RUN/PLAN_ONLY/NOT_TESTED、验收标准；至少1例端到端真执行，不能拿一个安全toy实验冒充五例完成。

## D. 差异化研究与安全约束
主题“低成本离线优先AIoT硬件工厂：MQTT网关、边缘推理、OTA可信更新、任务中心及无真机可复现验证”。要求市场机会与商业试点优先级、Skill/Plugin/MCP/SDK至少15个真实候选、Top5具体CLI/API使用技巧、官方来源≥10、费用/权限/许可证、5个可执行案例和风险；检索最多12次、子代理最多1个，8–12分钟内收敛，透明披露实际次数。允许只读官方网页与隔离临时目录Python标准库测试；禁止安装插件、切模型、改生产、改Git其他路径、操作真硬件/外部设备、付费授权、写凭据或创建定时任务。仅返回完整报告正文（BEGIN_FULL_REPORT/END_FULL_REPORT）；ChatGPT负责Git提交与独立审计。
结尾单列“上一小时通用改进：计划→实际注入→实际效果→下轮调整”，并逐项自查S1/S2和HIST-F9-01~05；诚实区分研究质量与工具调用成功。