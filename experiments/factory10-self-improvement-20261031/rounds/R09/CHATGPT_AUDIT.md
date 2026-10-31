# R09 F9｜ChatGPT独立审计｜2026-10-31
- 实验 FACTORY10-SELF-IMPROVEMENT-20261031，R09 F9 AIoT智能硬件首次正式BASELINE。唯一WorkBuddy Job **75e17092ec644e6c**；桥接器list_workbuddy_jobs确认 **DONE/231秒/17221字返回文本**；实际取得BEGIN_FULL_REPORT/END_FULL_REPORT之间完整正文16964字符。WORKBUDDY_REPORT.md Git commit **9e5255815b0bdfbcd916c27d6eeed571a8214e2c** / blob **ada19a28cda58e5b90ae1b13375a4d94b131015d**，Git逐字回读PASS。桥接成功不等于AIoT硬件/真实MQTT/商业生产成功。
- 旧实验F9 Job a178c0e82f10461d FAILED_NOT_SUBMITTED_TO_CODEBUDDY/0字，无旧WORKBUDDY_REPORT/CHATGPT_AUDIT。SAME_FACTORY_BASELINE_MISSING；旧内容错误解决率、复发率、同厂分数Δ均**NOT_COMPARABLE**。本轮65/100是R19正式基线；不得拿R08 F8 73/100跨厂差值当质量改进因果。

## 固定五维独立评分（总分100）
|维度|得分|独立核验依据|
|---|---:|---|
|证据25|16|MCP完整报告、S1 3426字节Python源码SHA独立一致，双模式故障可复放；但Case B无源码/六条完整输入，无法独立重放；8项官方版本/价格自评0错与官方现行事实冲突，来源列表多为域名而非逐项精确URL。|
|战略20|18|离线优先MQTT、OTA、边缘推理、NAS任务中心与低预算试点方向匹配；客户需求、报价、回报仍为假设。|
|操作技巧20|13|S1离线安全门禁与故障注入真实可执行；mosquitto_sub示例缺主题参数，ESP/HA等命令未经环境验证，部分安全/身份语义不够准确。|
|五案例20|11|A-E字段较完整，Case B有声称运行结果，但缺Case B源码和冻结JSONL，无法独立重放；Case C仅S1 OTA拒绝分支，不等于OTA完整A/B升级案例；A/D/E未实跑。|
|风险及真实性15|7|明确零真机、SHA≠签名、QoS≠应用层幂等；但独立红队发现缺少预配置设备ID、缺时间戳、空命令列表均错误地返回ACCEPTED，安全门禁仍有fail-open；RPi价格及软件版本错误。|
|**合计**|**65/100**|**CONDITIONAL_ACCEPT_RESEARCH / NOT_READY_FOR_PRODUCTION**；真实交付通过，研究内容有重要错误，必须整改。|

## 独立可复现代码审计（不是WorkBuddy自述）
- 从Git完整报告的唯一Python fenced block提取，按UTF-8/末尾LF原样保存到隔离审计环境，实际文件3426字节；SHA256 **fb578da666b7f489a189ac2ffabf46d1d6593d88b4f2081b494f2d6f83c20c79**，与Buddy所报完全一致（源码SHA 1/1）。
- 独立构造与报告语义一致的冻结JSON输入，分别用普通Python和 `python -O` 运行。合法2命令控制组两模式exit0、stdout `ACCEPTED: OK_ALL_COMMANDS_ACCEPTED\n`；重复cmd_id、伪造device_id、时间戳倒退、错误OTA HMAC、缓存6条超5上限，**五类故障×两模式=10/10非零退出**，stderr包含预期BLOCKED字符串。这证明R08 `assert` 优化模式绕过在已覆盖故障上确实消失。注意：报告未提供这些JSON文件的完整字节，故属于独立构造等价输入复放，不能称原始输入文件SHA已核对。
- **P0 NEW-SAFETY-01 设备身份缺失时放行**：输入 `{"commands":[{"cmd_id":"x","ts":1000}]}`，缺`expected_device_id`与命令`device_id`，代码比较`None == None`，普通和-O均exit0/ACCEPTED。必须在比较前显式验证预配置设备ID为非空、命令ID为非空，并用可信认证/授权而非只比较用户自报字符串。
- **P0 NEW-SAFETY-02 时间戳缺失时放行**：`expected_device_id="dev-AA01"`、命令含正确device_id但不含ts，普通与-O均exit0/ACCEPTED；空`commands=[]`也exit0/ACCEPTED。必须校验字段类型、范围、空负载、时钟漂移及重放窗口；缺失/空命令拒绝。两模式各测试，任何exit0即失败。
- **P1 NEW-SAFETY-03 未捕获异常与状态回滚**：第二条命令`ts=null`时`None < int`抛TypeError，exit1但不是结构化SafetyBlocked；缓存超过MAX_CACHE时先append再raise，报告声称回滚但没有可验证持久化快照或回滚工件。须将类型错误转为结构化拒绝，提供快照/恢复实际日志。
- HMAC使用内嵌固定SIM_KEY仅限toy演示；不可作为设备固件可信签名认证。S1脚本既不连接真实MQTT broker，也没有真实设备证书/权限校验。R08→R09安全方法判定 **PARTIAL_EFFECTIVE**：原assert绕过修复，但新增fail-open P0，不能宣称“不可绕过安全门禁整体通过”。

## 官方事实与版本抽查（2026-10-31）
1. **P0 NEW-PRICE-01 Raspberry Pi 5 4GB错误报价**：Buddy称官方挂牌**$70**，并把第三方$110视为零售差异；官方Raspberry Pi 2025-12公告4GB确曾从$60涨至$70，但2026-04公告再次上涨（2026-02亦曾涨价），官方2026-04版Raspberry Pi 5产品简报明确4GB **$110**。R09沿用过期2025价格却宣称截至2026-10最新，S2“0/8错”自评不成立。官方来源：https://www.raspberrypi.com/news/1gb-raspberry-pi-5-now-available-at-45-and-memory-driven-price-rises/ ; https://www.raspberrypi.com/news/a-new-3gb-raspberry-pi-4-for-83-75-and-more-memory-driven-price-increases/ ; https://pip-assets.raspberrypi.com/categories/892-raspberry-pi-5/documents/RP-008348-DS-4-raspberry-pi-5-product-brief.pdf
2. **P1 NEW-VERSION-02 Mosquitto版本过时**：Buddy把2.0.20列为当前版本；官方项目下载页提供**2.1.2**。旧版可存在，但不得声称最新/当前。官方：https://www.mosquitto.org/download/
3. **P1 NEW-VERSION-03 ESP-IDF版本过时**：Buddy把**v6.0.2**称最新稳定版；Espressif稳定版文档已标**v6.1**，且v6.0.2迁移文档明确提示不是最新稳定版。官方：https://docs.espressif.com/projects/esp-idf/en/stable/esp32/ ; https://docs.espressif.com/projects/esp-idf/en/v6.0.2/esp32/migration-guides/release-6.x/6.0/index.html
4. **通过的抽查**：Zephyr官方发布表确有4.5.0于2026-10-28发布；RealSense D435官方公开价格确为**$314**（R08旧错已纠正）。官方：https://docs.zephyrproject.org/latest/releases/index.html ; https://www.realsenseai.com/stereo-depth-cameras/
5. S2抽核5项（RPi5、Mosquitto、ESP-IDF、Zephyr、D435）中3项不准确、2项准确；仅代表本次样本，不可推算全部8项错误率。报告“版本/价格0/8错配”**RECURRED_FACT_ACCURACY_ERROR**。多个来源仅给根域名，不满足委托“每项精确可核URL”。

## 工具/案例可执行性审计
- `mosquitto_sub -q 2`示例未指定主题（缺`-t`或`-T`等匹配条件），不构成可执行的QoS2验证；`mosquitto_pub -h localhost ...`也要求本地broker实际存在，报告已承认未安装。不得将DOCUMENTED标EXECUTED。
- Case A WishTree：PLAN_ONLY；缺合成事件输入文件、混淆矩阵真实输出、误检测试。Case B MQTT：报告声称RUN并给trajectory/rejects及SHA `025d721c...`，但**没有case_b_gateway.py源码，也没有6条case_b_messages.jsonl完整字节**；无法独立复现或确认SHA属于何物。判**PARTIAL/NOT_INDEPENDENTLY_VERIFIED**。Case C OTA：S1故障分支确能拒绝HMAC错误，但没有完整OTA版本门禁、A/B状态机、断电回滚测试，不能认定整例端到端RUN。Case D边缘推理NOT_TESTED，Case E NAS PLAN_ONLY；五例完整业务闭环0/5独立确认。
- 成本：零额外云API费用可成立于本地标准库测试，但并不代表硬件、电力、存储、维护或商业试点总成本$0；采购预算应按当前官方型号/日期核对。

## CROSS_FACTORY_TRANSFER（R08 F8→R09 F9，跨厂不比较总分因果）
|method|前轮证据|本轮实际注入|独立实施证据|质量结果|verdict|
|---|---|---|---|---|---|
|S1 可复放工件+双模式安全拒绝|R08源码SHA2/2、stdout1/1；estop在-O exit0|Git FEEDBACK 3787字完整嵌入MCP prompt3981字，job 75e17092ec644e6c|源码SHA1/1一致；独立10/10预期故障两模式阻断|修复assert特定漏洞，但缺设备ID/时间戳/空命令3类fail-open|**PARTIAL_EFFECTIVE / NEW_P0_FAIL_OPEN**|
|S2 精确版本/型号/价格|R08 ROS版本、TB4型号、D435报价错误|同上|D435 $314、Zephyr4.5.0核对正确；RPi5 4GB $70、Mosquitto2.0.20、ESP-IDF6.0.2当现行错误|抽核5项3错，S2自报0/8错不成立|**FAILED_FACT_ACCURACY**|
- R08→R09同类可比指标：源码SHA均独立一致；两模式已覆盖故障的assert绕过消失，但新增缺字段fail-open；官方版本/价格仍出现错误。不同工厂难度和事实集合不同，不能以73→65的总分变化证明因果。

## SAME_FACTORY_REMEDIATION（旧F9报告缺失，正式旧内容缺陷0）
|历史证据缺口|Buddy自评|ChatGPT独立判定|依据与下一次通过条件|
|---|---|---|---|
|HIST-F9-01 旧无完整报告|RESOLVED|**RESOLVED_DELIVERY_ONLY**|本轮MCP全文16964字，Git回读PASS；旧失败根因未证明修复|
|HIST-F9-02 官方/环境/实跑证据|RESOLVED|**PARTIAL**|源码可复放，但官方版本/价格3项错，Top5命令有不可执行项|
|HIST-F9-03 MQTT/OTA/身份安全|RESOLVED|**PARTIAL**|已覆盖10/10指定故障，但缺设备身份/时间戳等输入可被放行，真设备认证未测|
|HIST-F9-04 五案例闭环|PARTIAL|**PARTIAL**|Case B缺完整代码/输入，Case C只有单分支，A/D/E未运行|
|HIST-F9-05 生态/成本商业性|RESOLVED|**PARTIAL**|22候选、市场路径存在，但RPi5价格过期，客户/成本未验证|
- 历史交付/证据缺口 **1/5解决、4/5部分解决**。旧内容错误复发率、旧内容解决率、同厂评分Δ：**NOT_COMPARABLE**；本轮新发现缺陷至少6类（fail-open设备身份、缺时间戳/空命令、非结构化异常、RPi价格、Mosquitto/ESP-IDF版本、Case B工件缺失）。

## 下一轮R10 F10小说叙事工厂：最多2项通用方法改进
**T1 [P0] 负例边界“缺字段/空输入”强制测试**：本轮S1在正常和-O下对预设故障10/10阻断，却对缺预配置ID、缺ts、空commands 3/3错误放行。原因假设：只测试预设负例，忽略缺字段/空集合/非法类型。R10迁移为文本/叙事工具的输入验证：至少3类空输入、缺字段、非法引用/授权标识真正拒绝；输出源码/输入/命令/异常及独立可复放证据，目标3/3真实拒绝、0错误成功；可证伪=任何无效输入exit0或被当合法产物。
**T2 [P0] 官方来源版本与可重放产物双门禁**：R09 S2宣称0/8错，独立抽查5项3错；Case B自报RUN但没有源码/冻结输入。原因假设：旧价格/版本快照与报告产物未同步。R10对叙事模型/平台的当前条款、商用许可、价格和接口版本至少3项逐项官方精确URL/日期核对，所有RUN案例必须提供完整原文输入、程序或可重放步骤、原始输出及SHA；目标官方错配0/3、RUN可复放1/1。可证伪=官方资料错配、缺工件却自报RUN。
- 只改研究方法与委托提示词，不改调度、工厂顺序、评分权重、Git路径、生产系统、模型或插件授权。

## 最终结论
**65/100**：真实MCP交付、Git报告回读和S1代码独立复算通过；指定故障两模式拒绝确实修复了R08的assert漏洞。但R09仍存在P0缺字段fail-open、3项官方版本/价格错误、Case B缺可复放源码输入、Case C实跑覆盖过度推断。研究有条件接受，**NOT_READY_FOR_PRODUCTION**。
