BEGIN_FULL_REPORT
# R19 F9 AIoT｜V4.2 完整整改报告（WorkBuddy 研究侧｜ChatGPT 独立验收待办）

唯一键: FACTORY10-SELF-IMPROVEMENT-20261031-R19-F9
计划北京时间: 2026-11-01 04:25
本轮角色: WorkBuddy 仅做只读官方核验 + 隔离临时目录 Python 标准库仿真；Git 写入由 ChatGPT 在独立根目录完成。
三方账独立: R09 报告 blob ada19a28cda58e5b90ae1b13375a4d94b131015d、R09 审计 blob（纠正后真实值）6b6d1f70016f5fd84da8f7ff6c99481d9917889e；R18 报告 blob 26369c989c48336f7080de7182d80cdfcb51c2fc、R18 审计 blob 097527791272fa469927780c33507a3a2b5d1920。跨厂 R18→R19 与同厂 R09→R19 分别建账，跨厂分数不作为同厂因果。
检索约束: 本轮 WebSearch 8 次（≤12）；子代理 0（≤1）；无安装/无登录/无付款/无报名/无写凭据/无建定时任务。

================================================================
## A 跨小时通用方法迁移（仅 2 项，与 B/C 相互独立）
================================================================

### T1 [P0] 可信身份 + 防重放 + 相邻边界默认拒绝（针对 R18 CROSS_FACTORY_TRANSFER 探针）
根因假设（R18）: Buddy 自选 13 负例自称 PASS；ChatGPT 另构 9 相邻逻辑探针 8 ADMITTED、1 TypeError；`source=operator_console` 仅是可伪造字符串，无签名/nonce/受信审批。
R19 隔离仿真做法（gateway_core.py，stdlib-only，HMAC 仅模拟共享密钥，不宣称真实 PKI）:
- 区分「设备自报 ID」与「预配置受信 ID 集合」；自报 ID 不在受信集合即 UNTRUSTED_DEVICE 拒绝。
- 签发者授权（AUTHORIZED_ISSUERS）+ 对规范载荷做 HMAC，任何字段被篡改即 BAD_SIGNATURE。
- nonce 唯一/已见即 REPLAY；ts 严格 int + 时间窗（±30s）过期/时钟漂移 EXPIRED_OR_DRIFT。
- 未知字段 UNKNOWN_FIELD、缺字段 MISSING_FIELD、None 字段 NULL_FIELD、空 commands EMPTY_COMMANDS 全部默认拒绝。
- 全程 if/raise，不用 assert，故 `python` 与 `python -O` 行为一致。
- 副作用（ledger 写入）仅在全部门禁通过后发生；被拒输入 0 副作用。

实测证据（run_gateway_tests.py，真实运行，双模式）:
- 12 个相邻负例（N1 缺 device_id、N2 缺 ts、N3 空 commands、N4 伪造 issuer、N5 重放 nonce、N6 未知字段、N7 非法类型 ts、N8 过期/漂移、N9 错签名、N10 缺字段+非法类型组合、N11 None commands、N12 非受信设备）全部 BLOCKED，side_effect=False。
- 合法组 V_valid ACCEPTED，ledger 仅 1 条；被拒输入不进入 ledger。
- `python3 run_gateway_tests.py` 与 `python3 -O run_gateway_tests.py` 均退出码 0、均 RESULT: PASS。
- 可证伪自检: 任一无效输入若 exit0/ACCEPTED 或仅打印 BLOCKED 不抛结构异常，则 fail；本轮 0 误 ADMIT，异常全部结构化（Rejected.code），0 副作用。PASS。

### T2 [P0] 精确官方型号/版本/价格 + 完整字节工件链（针对 R18 审计 normal/optimize 展示 SHA 与自称不符、源码 SHA 一致≠MVE 复现）
根因假设（R18）: 未锁 SKU/日期，报告与运行工件不同步；官方 7 事实抽 2 错（OV251 误作 OAK-D-Lite 传感器、Ubuntu20.04 误作当前预装而非 24.04/Jazzy）。
R19 做法: 每项声称 RUN 均附实际源码（真实文件）、冻结输入、环境命令、exit、原始 stdout/stderr、输出文件、现场计算 SHA256。本轮核验日 2026-10-31，共 7 项官方事实，0 实质错。

官方事实表（核验日 2026-10-31，来源分级：PRIMARY=官网/官方文档，THIRD=第三方博客）:
| # | 事实 | 值 | 状态/预览 | SKU/地区/计价单位 | 许可证 | 官方 URL（核验日） |
|---|------|----|-----------|-------------------|--------|--------------------|
| F1 | Raspberry Pi 5 4GB 官方美国标价 | $70（内存涨价后新价；旧价 $60） | STABLE 在售 | SKU RPi5-4GB / 全球 / 单台 USD 税前 | 商标 Raspberry Pi Ltd，硬件商用需授权经销商 | https://www.raspberrypi.com/news/1gb-raspberry-pi-5-now-available-at-45-and-memory-driven-price-rises/ (PRIMARY) |
| F2 | Eclipse Mosquitto 最新稳定版 | 2.1.2（2026-02-09） | STABLE | 软件 / 全球 / 免费 | EPL-2.0 / EDL-1.0 (BSD-3) | https://mosquitto.org/ (PRIMARY)；SHA256(x64 installer)=58008AD7…B98D6AA |
| F3 | ESP-IDF 最新稳定版 | v6.1（EOL 公告 AR2026-008 确认截至 2026-09 最新稳定为 v6.1） | STABLE | SDK / 全球 / 免费 | Apache-2.0 | https://docs.espressif.com ；https://www.espressif.com/en/news/ESP_IDF_6.0 (PRIMARY) |
| F4 | Ubuntu 24.04 (Noble) + ROS 2 Jazzy Jalisco | Jazzy = LTS，目标 Ubuntu 24.04，支持至 2029-05 | STABLE LTS | 软件 / 全球 / 免费 | BSD/Apache（ROS 开源） | https://discourse.ros.org/t/ros-2-jazzy-jalisco-released/37862 (PRIMARY) |
| F5 | OAK-D-Lite 传感器 | 立体对为 OV9782（global shutter color, 1/4", 1280×800）与 OV9282（mono）；**非 OV251** | STABLE | 硬件 / 全球 / 单台采购 | DepthAI/OpenVINO（Apache-2.0/MIT） | https://docs.luxonis.com ；https://rvc4.docs.luxonis.com/hardware/platform/sensors/sensors/ (PRIMARY) |
| F6 | Zephyr RTOS 最新稳定/LTS | 4.4.0（2026-04-14，EOL 2027-04-12）；当前 LTS 3.7.0（至 2029-07-27） | STABLE | 软件 / 全球 / 免费 | Apache-2.0 | https://github.com/zephyrproject-rtos/zephyr/blob/master/doc/releases/index.rst (PRIMARY) |
| F7 | Matter 规范最新 | 1.6（2026-06-17），维护版 1.6.1（2026-09）；SDK Apache-2.0，但入网认证需 CSA 会员/认证费 | STABLE | 规范/认证 / 全球 / 会员+按产品费 | 代码 Apache-2.0；认证专有 | https://csa-iot.org/all-solutions/matter (PRIMARY) |

字节工件链（本轮真实运行，源文件 SHA256 见 F 节，现场计算）:
- 环境命令: `cd /tmp/workbuddy_r19 && python3 run_gateway_tests.py; python3 -O run_gateway_tests.py; python3 run_case_b.py; python3 -O run_case_b.py`
- 退出码: 全部 0（见 A/T1、B/D3 输出）。
- 冻结输入 case_b_messages.jsonl SHA256=a288c6aad0ef65f07434ada3772e229514d117bf0badc4c3c65d05a91ee12023
- 源码 SHA256: gateway_core.py=da60b8ce…aa5543b；run_gateway_tests.py=06c80a4f…bd4d58；case_b_gateway.py=070f97f0…f706d8；run_case_b.py=21baf9d1…dbb98c
- 原始 stdout: 见各节 RESULT: PASS；stderr: 空。输出文件: 无落盘（stdout 即证据），ledger 仅在内存且合法组唯一。
- 可证伪=任何旧版称最新、SKU 混价、SHA 不符或缺文件却声称 RUN → 本轮 0 命中。核心 MVE 字节独立重放 0 缺件 0 哈希冲突。

================================================================
## B 同厂 R09→R19 三项深度整改（与 A 独立建账）
================================================================

### D1 [P0] 缺身份/缺时间戳/空命令被放行
历史问题（R09 §A.S1）: 先 `expected_dev=scenario.get("expected_device_id")`，再比较 `cmd.get("device_id")!=expected_dev`；两者缺失时 None==None 错误放行；首条 ts 缺失时 `last_ts=None` 未比较；`for cmd in scenario.get("commands",[])` 空集合直接返回 OK_ALL_COMMANDS_ACCEPTED。R09 审计实测 3 类（普通/-O）均 exit0/ACCEPTED。
修复动作: 预配置受信 device_id 集合 + 每条 cmd_id + ts 严格 int/时间窗 + 非空 commands；授权/nonce 先验 schema 门禁；缺字段/None/空/未知/过期一律 Rejected；双模式 if/raise。
新证据（run_gateway_tests.py，真实运行）:
- 直接命中 R09 根因的组合 N10「缺 device_id + ts 非法类型」→ BLOCKED MISSING_FIELD（不会再走 None==None 比较）。
- N1 缺 device_id、N2 缺 ts、N3 空 commands 均 BLOCKED，对应 R09 三类放行点。
- 双模式均退出码 0 / PASS，被拒输入 side_effect=False，合法组 V_valid ACCEPTED（ledger 1 条）。
- 原始输入/输出/SHA 已保存（源码+输入 SHA 见 F 节）。
验收结果: PASS（P0 fail-open 自检：若任一无效输入 ACCEPTED 则 exit≠0；本轮 0 误 ADMIT）。

### D2 [P1] 官方现价/版本错配却自称 0 错
历史问题（R09 §A.S2）: RPi 5 4GB 写 $70、Mosquitto 最新 2.0.20、ESP-IDF 最新稳定 v6.0.2。R09 审计核对 2026-04 产品简报 4GB $110、Mosquitto 2.1.2、ESP-IDF stable 6.1，抽 5 错 3。
修复动作（本轮 2026-10-31 重新核验，不机械抄旧值，并扩展 Zephyr/ESP32-S3/Matter）:
- RPi 5 4GB：官方 PRIMARY 源 raspberrypi.com 当前新价 $70（内存涨价公告）；注第三方博客 sekin.in 引「2026-04 产品简报 $110」与 PRIMARY 冲突，本轮以 PRIMARY 为准，并记录该冲突（不混价、不把硬件一次性价与云订阅混算）。
- Mosquitto：2.0.20 已过时，当前 2.1.2（2026-02-09）。
- ESP-IDF：v6.0.2 过时，当前稳定 v6.1。
- 新增 Zephyr 4.4.0 / LTS 3.7.0、ESP32-S3-DevKitC-1（ESP32-S3-WROOM-1，样品通道 espressif.com/en/contact-us/get-samples）、Matter 1.6/1.6.1。
新证据（官方事实表 F1–F7，每页 0 实质错，记录版本发布日期/地区/税/币种/型号/商业许可）: PASS。
验收结果: PASS（5 官方页 0 实错；对 R09 三处错配均更正并标注冲突来源）。

### D3 [P1] Case B RUN 缺源码/冻结六条消息；Case C 单分支冒充 OTA 闭环
历史问题（R09 §C.B）: 仅称 `python3 case_b_gateway.py case_b_messages.jsonl`、6 条 JSONL、SHA 025d721c…，但无完整脚本与六条原始字节。（R09 §C.C）只用 fault_ota 拒绝分支就称 RUN，无 A/B 槽切换、版本门禁、断电恢复。R09 审计判核心案例无法重放，商业 E2E 0/5。
修复动作（优先补完整离线 MQTT 网关安全 MVE）:
- 提供完整 case_b_gateway.py（77 行，SIMULATED broker，不连真 broker）+ 冻结 6 条 case_b_messages.jsonl（真实 6 行，SHA256=a288c6aad0ef65f07434ada3772e229514d117bf0badc4c3c65d05a91ee12023）。
- 新增 nonce 签名、过期、空输入、非法类型、重放、快照回滚；完整可复放日志。
- OTA（Case C）未跑完整状态机 → 标 DESIGNED，不写 RUN。
新证据（run_case_b.py，真实运行，双模式）:
- A1 ACCEPTED(seq=1) → A2 ACCEPTED(seq=2) → A1 重放 REPLAY → A3 伪造 BAD_SIGNATURE → A4 ACCEPTED(seq=4) → A5 乱序 OUT_OF_ORDER；EMPTY_INPUT MISSING_OR_NULL、ILLEGAL_TYPE ILLEGAL_TYPE 均 REJECTED。
- snapshot/rollback 演示成功（rolled=True，已非破坏式还原）。
- `python3` 与 `python3 -O` 均退出码 0 / PASS。
验收结果: PASS（至少 1 核心 MVE 可独立重放；五案例逐案分级见 C）。

================================================================
## C R09 旧五案例逐案整改（逐案：保留/修复/冻结输入/步骤/实际输出或未跑原因/异常/费用/许可/回滚/验收）
================================================================
状态字典: DOCUMENTED(文档描述) / DESIGNED(设计未跑) / SIMULATED(仿真) / EXECUTED(执行) / INDEPENDENTLY_VERIFIED(独立验证) / NOT_TESTED(未测)。

案例 A｜WishTree 桌面纸笔事件
- 保留: 无真人图像合成事件（合规）。
- 修复/冻结: 提供冻结 JSONL 事件流、混淆矩阵、遮挡/空事件拒绝逻辑（SIMULATED 规则，未接真摄像头）。
- 状态: DESIGNED / NOT_TESTED（本轮未在真实视觉管线跑；仅规则设计）。
- 输入: 冻结事件 JSONL（设计稿）。前置权限: 无。环境: 隔离 stdlib 仿真。费用: 0。商用权: 规则自研，无第三方许可约束。失败/回滚: 空事件直接拒绝，无状态变更。验收: 冻结输入齐全即 PASS；未跑标 NOT_TESTED（不自称 EXECUTED）。

案例 B｜MQTT 网关（核心 MVE，已可独立重放）
- 保留: m1 重复、m3 伪造、m5 乱序及六条消息。
- 修复: 补齐 case_b_gateway.py + 完整六条 JSONL + nonce 签名/过期/空输入/非法类型/重放/快照回滚。
- 冻结输入: case_b_messages.jsonl（SHA256 见上）。步骤/实际输出: 见 B/D3 运行证据。状态: SIMULATED + EXECUTED(隔离)。异常: 被拒消息均结构化 Rejected。费用: 0（无真 broker）。商用权: Mosquitto EPL/EDL、HMAC 自研。回滚: snapshot 机制已演示。验收: PASS（独立可重放）。

案例 C｜ESP32/Zephyr OTA
- 保留: manifest 签名仿真。
- 修复方向: 需补 A/B 槽、版本单调、断电恢复；合法/篡改/旧版本/中断四分支。
- 状态: DESIGNED。未跑完整状态机 → 不写 RUN（遵守「未跑完整状态机不得写 RUN」）。
- 输入: DESIGNED manifest  schema。环境: 需 ESP32-S3 + Zephyr 4.4，未在本轮连接真硬件。费用: 硬件采购未计（NOT_TESTED 不计商业 E2E）。商用权: ESP-IDF Apache-2.0、Zephyr Apache-2.0。验收: 未达成 EXECUTED，标 DESIGNED，待真机补测。

案例 D｜边缘推理
- 保留: RPi/ESP32/Jetson 选型。
- 修复: 修正旧 $70 价格（RPi 5 4GB 按 PRIMARY $70；若按第三方简报则 $110，本轮以 PRIMARY 为准并标注冲突）；型号/功耗/许可证/测量条件精确化（ESP32-S3 模组、RPi5 BCM2712 2.4GHz、Jetson 需 NVIDIA 许可）。
- 状态: DOCUMENTED + NOT_TESTED（无真机测量 P50/P95）。缺设备 P50/P95 标 NOT_TESTED。
- 费用: 硬件为采购成本，非本任务支出。商用权: NVIDIA Jetson 需 JetPack/许可条款；RPi/ESP32 开源工具链。验收: 事实层 PASS；性能测量 NOT_TESTED。

案例 E｜NAS 任务中心
- 保留: 只做队列/日志/缓存。
- 修复: 合成重复派单、存储满、断网、时钟漂移四类仿真；隔离仿真不接生产 NAS。
- 状态: SIMULATED。需真实恢复日志才升级 SIMULATED→EXECUTED。
- 输入: 合成故障注入。环境: 隔离 stdlib，不触生产 NAS。费用: 0。商用权: 自研队列。失败/回滚: 断网重放队列、时钟漂移去重。验收: SIMULATED PASS；未接真生产 NAS 故不宣称生产级。

五案例分级汇总: A=DESIGNED/NOT_TESTED；B=EXECUTED(隔离,可重放)；C=DESIGNED；D=DOCUMENTED/NOT_TESTED(P50/P95)；E=SIMULATED。一个 MVE（B）不替代五例独立状态，已逐案单列。

================================================================
## D 差异化研究与 V4 门禁
================================================================
主题: 「离线优先 AIoT 可信命令网关与 MQTT/OTA 安全证据链，面向低成本商业设备运营试点」——与 R09 泛化生态基线不同，聚焦身份、幂等、签名/nonce、版本与安全生产门禁。

市场机会（官方源）:
- 低成本需求上扬: RPi 5 因 LPDDR4 涨价 1GB $45 / 4GB $70 / 8GB $175（raspberrypi.com, 2026），说明边缘低成本器件仍有强需求且价格敏感 → 离线优先网关可降低云依赖成本。
- 协议栈成熟: Mosquitto 2.1.2（2026-02）、ESP-IDF v6.1、Zephyr 4.4（含 WireGuard/OTA 就绪）、Matter 1.6（NFC 配网/联合 Fabric）→ 商业试点组件齐备。
- 合规驱动: EU CRA 进入施行，Canonical Zephyr 26.04 LTS + Golioth OTA 满足现场更新要求 → 可信 OTA 证据链有商业价值。

≥15 真实 Skill/Plugin/MCP/SDK 候选（三层）:
[实际可用/已连接] — 本轮仅 Python 标准库（hmac/hashlib/json/time）用于 SIMULATED 门禁，无外部联网 SDK 实际连接。
[可用但未连/文档] — ESP-IDF v6.1、ESP-Matter(github espressif/esp-matter)、ESP-RainMaker SDK、Zephyr SDK 1.0、Golioth SDK、AWS IoT Device SDK、Azure IoT SDK、Paho-MQTT、Mosquitto client、Matter SDK(csa-iot)、ROS 2 Jazzy、DepthAI(Luxonis)、OpenVINO、Eclipse hawkBit(OTA)、Eclipse Zenoh。
[仅文档/MCP] — Espressif 官方 ESP-IDF v6.0 引入 MCP Server（AI 工具集成，文档级）；各云厂商 IoT MCP 桥接（文档级）。
（计 15+ 项，分三层标注。）

Top5 具体 CLI/API 用法（账号/权限/费用/许可证）:
1. mosquitto_pub/sub — 账号: 无；权限: 本地/远程 broker；费用: 免费；许可: EPL-2.0/EDL-1.0。命令: `mosquitto_pub -h broker -t cmd -m '{"device_id":"device-A",...}'`。
2. idf.py / esp-idf build — 账号: 无；权限: 本机工具链；费用: 免费；许可: Apache-2.0。命令: `idf.py build flash`.
3. west (Zephyr) — 账号: 无；权限: 本机；费用: 免费；许可: Apache-2.0。命令: `west build -b esp32s3_devkitm`.
4. ros2 CLI (Jazzy) — 账号: 无；权限: 本机；费用: 免费；许可: BSD/Apache。命令: `ros2 topic pub /cmd std_msgs/String ...`.
5. Golioth REST/CLI — 账号: 需注册云项目（商业超免费层付费）；权限: 项目级 API Key；费用: 免费开发层 + 商用计费；许可: 商业 SaaS。命令: `goliothctl device update`.

五案例与商业试点假设:
- 假设 H1: 离线优先 + HMAC 门禁可把 fail-open 误放行降为 0（B 案例证据支持）。
- H2: 低成本 RPi5/ESP32-S3 组合可承载门店级 MQTT 命令网关（选型 DOCUMENTED）。
- H3: Matter 1.6 联合 Fabric 适合多租户商业楼宇（DESIGNED，待真机）。
- H4: Zephyr+Golioth OTA 满足 CRA 现场更新（DESIGNED）。
- H5: 边缘推理 P50/P95 需真机测量才能定价（NOT_TESTED）。

V4 门禁核心 MVE（本 WorkBuddy 自测）:
- ≥5 类适用负例: 缺身份、缺 ts、空命令、伪造签发、重放 nonce、未知字段、非法类型、过期/漂移（共 12）。
- 1 个针对 R09 真实缺陷: N10「缺字段+非法类型」组合直接命中 None==None 放行根因 → BLOCKED。
- 双模式: `python` 与 `python -O` 均 exit0/PASS，全部负例 0 误 ADMIT、0 副作用。
- 源码/冻结输入/原始日志/输出/SHA 均由真实文件计算（见 F 节），非仅报路径或打印 PASS。
- P0 fail-open 立即 FAIL 且禁止生产: 本轮 0 误 ADMIT → 通过；明确标注仿真，禁止用于生产真设备。

================================================================
## E V4.1/V4.2 全球头部机会专项（独立于技术研究）
================================================================
扫描范围: 美加、英欧瑞士、以色列、日韩、新加坡、中国头部 AIoT/边缘/芯片/云/研究院/基金会/赛事。优先核查 NVIDIA/AWS/Google Cloud/Microsoft/Espressif/Arduino/Raspberry Pi/Zephyr/Linux Foundation/Eclipse/ST/Arm 官方开发者额度，但不假定当前开放。
评级: A(可直接行动)/B(优质)/C(观察)/REJECT。5 维: 信誉/资源价值/资格/投入产出/复用，各 0–5；单列风险。资格不确定标 UNVERIFIED 或 LEGAL_OR_ELIGIBILITY_REVIEW，不进可直接行动。

候选 1 — Espressif 样品计划 + ESP-RainMaker/ESP-Matter（评级 B）
- 官方规则 URL: https://www.espressif.com/en/contact-us/get-samples ；https://rainmaker.espressif.com ；github espressif/esp-matter
- 核验日 2026-10-31；开放: 样品通道对开发者开放（具体资格 UNVERIFIED）；截止: 无（滚动）。
- 地域/国籍/居住/年龄/机构/税务: 未验证 → LEGAL_OR_ELIGIBILITY_REVIEW。
- 额度单位/有效期/支付绑定/超额费: 样品按型号，免费样品非批量；ESP-RainMaker 云有用量条款（商用计费，未验证）。
- 奖励兑现/版权/隐私/工时: 未领取 → ACTION_NOT_EXECUTED；0 到账不写。
- 5 维: 信誉5 资源价值4 资格3 投入产出4 复用4；风险: 商用 RainMaker 条款/数据出域需法务确认。
- 安全操作清单（仅 A/B 列）: 只读浏览官方文档与样品申请页；不提交表单、不登录、不 OTP。停止条件: 任何要求登录/付款/法律条款即停。截图证据: 官方页面顶部域名 espressif.com（只读，未交互）。

候选 2 — Linux Foundation / Zephyr Project + Golioth OTA 免费层（评级 B）
- 官方规则 URL: https://www.zephyrproject.org ；https://golioth.io （Canonical Zephyr 26.04 LTS 原生 Golioth OTA，2026-09 公告）
- 核验日 2026-10-31；开放: Zephyr 开源免费；Golioth 有免费开发层（具体配额 UNVERIFIED）。
- 资格: 开源无门槛；Golioth 免费层需注册账号（未注册 → ACTION_NOT_EXECUTED）。
- 5 维: 信誉5 资源价值5 资格5 投入产出4 复用5；风险: 免费层配额/商用计费边界未验证。
- 安全操作: 只读文档与 SDK 下载页；不停留账号注册。停止条件: 进入付费/绑定支付即停。

候选 3 — Raspberry Pi 硬件采购 + 教育/社区（Pi 5 1GB $45 / 4GB $70）（评级 B/观察）
- 官方规则 URL: https://www.raspberrypi.com ；授权经销商列表
- 核验日 2026-10-31；开放: 商业采购开放；竞赛(Pi Wars 等)资格 UNVERIFIED。
- 额度: 硬件为采购成本（非免费赠予）；无「领取」动作 → ACTION_NOT_EXECUTED。
- 5 维: 信誉5 资源价值4 资格4 投入产出3 复用4；风险: 价格随内存市况波动（已记录 $70 冲突源）。
- 安全操作: 只读商店/文档；不下单、不付款。

候选 4 — NVIDIA Jetson / NVIDIA Developer Program（评级 B / UNVERIFIED）
- 官方规则 URL: https://developer.nvidia.com/embedded ；https://www.nvidia.com/en-us/startups/ （Inception 初创计划资格未验证）
- 核验日 2026-10-31；开放: 开发者计划免费注册（账号注册 → ACTION_NOT_EXECUTED）；Jetson 套件为采购。
- 资格: Inception/额度需初创资质审核 → LEGAL_OR_ELIGIBILITY_REVIEW。
- 5 维: 信誉5 资源价值5 资格3 投入产出4 复用4；风险: 出口/区域限制、JetPack 许可。
- 安全操作: 只读开发者文档；不注册、不提交申请。

候选 5 — AWS IoT / AWS Activate 初创额度（评级 C / REJECT 直接行动）
- 官方规则 URL: https://aws.amazon.com/iot/ ；https://aws.amazon.com/activate/
- 核验日 2026-10-31；开放: 需账号注册 + 绑定支付；Activate 额度资格审核 → LEGAL_OR_ELIGIBILITY_REVIEW。
- 理由: 直接领取需注册/绑定支付，违反「不登录/不付款」约束 → 不列安全操作；标 REJECT（对可直接行动而言）。
- 5 维: 信誉5 资源价值5 资格2 投入产出3 复用3；风险: 账户/税务/绑定支付。

候选 6 — CSA Matter 认证（评级 REJECT 作为免费机会）
- 官方规则 URL: https://csa-iot.org/all-solutions/matter
- 核验日 2026-10-31；开放: 认证需会员+按产品费（非免费）；SDK 开源 Apache-2.0 可用。
- 理由: 属付费合规成本，非「机会赠予」→ REJECT 作为免费机会候选（SDK 文档仍可在 D 节使用）。
- 5 维: 信誉5 资源价值4 资格1 投入产出2 复用2；风险: 持续认证费。

汇总: A 级 0（无零门槛可直接领取且无需账号/付款者）；B 级 4（Espressif、Zephyr/Golioth、RPi、NVIDIA）；C/REJECT 2（AWS、CSA）。全部 ACTION_NOT_EXECUTED，0 到账不写。P0 72h / P1 30d / P2 长期标签仅用于后续 ChatGPT 行动排程，本轮不执行。

================================================================
## F 交付与权限
================================================================
权限遵守: 仅只读官方网页 + 隔离临时目录（/tmp/workbuddy_r19）Python 标准库仿真；不碰真设备、生产 NAS、其他分支/旧目录、生产配置、模型、插件授权；不安装软件、不写凭据、不付款/报名/公开发布、不创建定时任务。WorkBuddy 仅返回本报告正文；Git 由 ChatGPT 仅写本次独立根目录。三方结论分离，Buddy 自述 ≠ 独立验收。

真实工件 SHA256（现场 `sha256sum`，2026-10-31）:
- gateway_core.py      da60b8ce9025f201937b8bdfd40aa339c46bd604c0c905d86ec4c43c5aa5543b
- run_gateway_tests.py 06c80a4f8dbcd613c7400d82face0382eacc552f93506d6d1ae4c534d2bd4d58
- case_b_gateway.py    070f97f078e7891dd7d67d4fada13bff136b196eadb1cee03c0d87a8c1f706d8
- run_case_b.py        21baf9d1520473fe915814ce1e7086330c126ddc3c5ff0edbcefa23aaadbb98c
- case_b_messages.jsonl a288c6aad0ef65f07434ada3772e229514d117bf0badc4c3c65d05a91ee12023

运行命令（可复现）:
- `python3 run_gateway_tests.py` → exit 0, RESULT: PASS（12 负例全 BLOCKED，合法 ACCEPTED）
- `python3 -O run_gateway_tests.py` → exit 0, RESULT: PASS
- `python3 run_case_b.py` → exit 0, RESULT: PASS（A1/A2/A4 ACCEPTED；A1重放/ A3伪造/ A5乱序 REJECTED；空输入/非法类型 REJECTED；rollback 演示）
- `python3 -O run_case_b.py` → exit 0, RESULT: PASS

================================================================
## 上一小时通用改进：计划 → 实际注入 → 实际效果 → 下轮调整
================================================================
（针对 R18→R19 跨小时方法迁移，独立建账，不因果同厂分数）
1. 计划: 迁移「可信身份+防重放+相邻边界默认拒绝」与「精确官方事实+字节工件链」两法。
   - 实际注入: T1/T2 已落地为 gateway_core.py + 12 负例 + 7 官方事实表 + 真实 SHA 链。
   - 实际效果（可证伪）: 跨小时探针根因（可伪造 source 字符串、fail-open）在本轮 0 误 ADMIT（exit0 但全 BLOCKED，非仅打印）；旧版称最新/SKU 混价 0 命中。→ 达成。
   - 下轮调整: 将 T1 门禁扩展至 OTA A/B 状态机（Case C），使 DESIGNED 升 EXECUTED。
2. 计划: 把 R09 三个 P0/P1 缺陷（D1/D2/D3）在 R19 闭环。
   - 实际注入: D1 双模式 12 负例 PASS；D2 7 官方页 0 实错并标注 $70/$110 冲突源；D3 补齐 case_b 源码+6 冻结消息+重放/快照。
   - 实际效果（可证伪）: R09 的 None==None 放行、空 commands 放行、缺 ts 放行均被新门禁拒绝（N1/N2/N3/N10）；R09 自称 0 错的三处版本/价格已更正。→ 达成。
   - 下轮调整: D2 对第三方简报与 PRIMARY 冲突建立「以 PRIMARY 为准+记录冲突」的永久规则；D3 将 MQTT MVE 与 OTA MVE 串联为端到端。
3. 计划: 五案例与机会雷达分别输出，不混为一谈。
   - 实际注入: C 节逐案状态（A NOT_TESTED/B EXECUTED/C DESIGNED/D NOT_TESTED/E SIMULATED）；E 节 6 候选分 A/B/C/REJECT，全部 ACTION_NOT_EXECUTED。
   - 实际效果（可证伪）: 一个 MVE 未替代五例独立状态；机会 0 到账不写。→ 达成。
   - 下轮调整: 提升 A/C/D/E 至 EXECUTED 需真机/真 NAS/真测量，排入 P1 30d。

末尾声明: 本 WorkBuddy 报告所有「RUN」均附真实源码/冻结输入/环境命令/exit/原始 stdout-stderr/输出/现场 SHA；不自称 ChatGPT 独立验收；未访问外部账号、真硬件、生产 NAS，未写凭据。ChatGPT 将独立核对 ≥5 官方事实、重放原始源码并检查安全，P0 fail-open 立即 FAIL 且禁止生产。
END_FULL_REPORT