# R15 F5 视频音频｜ChatGPT独立审计（2026-11-01）
## A. 三方结论分离
**WORKBUDDY_SELF_REPORT**：唯一Job 2b73e0b468c74b33 DONE，完整BEGIN_FULL_REPORT/END_FULL_REPORT 14060字符；声称D1-D3已修、5条事实0错、WAV/SRT SHA一致、5类负例拒绝。
**CHATGPT_INDEPENDENT_AUDIT**：实际读取MCP正文并Git独立回读；独立Python重新生成WAV/SRT，大小及SHA256与远端报告逐字一致；直接重放5个既定负例均拒绝，但4个相邻边界发现3类fail-open（错误布尔授权、NaN、超长时间戳）。通过官方页核验7组关键事实，发现4组实质错误/误导。详见INDEPENDENT_REPLAY_EVIDENCE.md。
**FINAL_ACCEPTANCE**：**FAIL（P0安全门禁、事实门禁双失败）**；研究资产PARTIAL，确定性WAV/SRT探针可复现，**PRODUCTION_NOT_READY**。工具成功、MVE哈希一致不等于产品安全或商用就绪。
## B. 五维评分及同厂纵向
R05 F5=**73/100 (18/17/15/14/9)**。R15 F5=**71/100 (证据16/25、战略18/20、操作技巧16/20、五案例15/20、风险真实性6/15)**；同厂Δ **-2**，五维Δ=(-2,+1,+1,+1,-3)。R15聚焦字幕/版权/价格，任务难度变化使分数不构成严格因果结论。正向改进是源码移交与哈希独立复算；严重负向是安全布尔fail-open、事实错误复发。
## C. ≥5项高影响事实独立官方抽查（核验2026-11-01）
|#|WorkBuddy原主张|官方证据|裁决/严重度|
|---|---|---|---|
|1|OpusClip Pro $29/月，$14.50/月按年付$174|https://www.opus.pro/pricing 明确$174 billed annually|**PASS**；地区差需核|
|2|Runway Gen-4.5 API 12 credits/s × $0.01=$7.20/min，ProRes额外5cr/s，HDR额外20cr/s|https://docs.dev.runwayml.com/guides/pricing/ |**PASS**，只适用于API基础费，不含重试/税|
|3|Suno Pro 2500credits/月、商业权“上限$1M收入”，500曲下载数UNKNOWN|https://suno.com/ 当前Pro **2500 credits/月但20 song downloads/月**；https://help.suno.com/en/articles/9601665 未给“商用上限$1M”说法|**FAIL P1**：把Stability类$1M门槛错误移植到Suno；未披露关键20下载/月上限，严重影响每曲可下载成本|
|4|HeyGen Creator 600 credits=600分钟、$29/600≈$0.048/分钟|https://www.heygen.com/pricing 仅确认600 credits，官方FAQ说明不同模型/功能/时长消耗credits不同|**FAIL P0-UNIT-ECON**：没有1credit=1minute统一换算依据，错误低估视频单价|
|5|ElevenLabs Startup Grants “33M chars/月”|https://elevenlabs.io/startup-grants 明确**33,000,000 characters总额/12个月**，非每月33M|**FAIL P1-RESOURCE**：把总额度误当月额度，潜在12倍资源高估|
|6|“Segmind 1 Billion AI Film Award”，每人只能提交一部|主办方正式条款 https://www.1billionsummit.com/ai-award-2027/terms-and-conditions §1.1主办New Media Academy LLC，§5.2允许每人多部各自合规作品；Segmind https://www.segmind.com/1-billion-ai-film-award-2027 自述非主办方且营销页写1人1部|**FAIL P1-EVENT**：主体混淆且营销摘要与正式条款冲突，应以主办方条款为准|
|7|ElevenLabs Creator $22/月，121k credits，约121min|https://elevenlabs.io/pricing 列Creator$22、121k credits、约121分钟TTS|**PASS_WITH_SCOPE**：具体模型/产品信用消耗不同，不是所有音频功能121分钟|
fact_check_sample_count=7; material_fact_error_count=4; fact_gate_verdict=**FAIL**（≥2错误）；价格/额度/资格是商业关键事实，不能把WorkBuddy自报5/5当独立核验。
## D. MVE独立复算与P0红队
从报告§④源码逻辑在独立Python环境重算：SR8000、DUR8秒、双正弦PCM16单声道，WAV**128044 bytes** SHA256 **d5e639d3ee20c29cde0e710b7f9df9f77fb9f825fe9705009895385f2c6fac76**；SRT**159 bytes** SHA256 **8c477ec992ccb9f3829cb8d0dd44d766bdad9025e053717ca8a2d3854adde5d4**；与远端自述完全一致。直接重放5既定Cue验证负例均按预期拒绝（codes4,3,2,5,6）。**这证明确定性WAV/SRT内容可复算，不证明完整视频/TTS/平台发布或远端文件确实存在。** 全脚本子进程命令在当前Python环境尝试超时，故完整端到端子进程执行标NOT_INDEPENDENTLY_REPRODUCED；直接函数与文件生成已复核。
**新增P0 SAFETY-BOOL-01**：validate(Cue(0,0,8,"valid","false")) 返回 **(True,"accepted",0)**。字符串"false"在Python中truthy，授权类型未严格校验，违反fail-closed并复发R12跨厂布尔类型缺陷。**生产禁止使用**。
**新增P1 TIME-BOUND-02**：validate(Cue(0,0,8000,"valid",True)) 返回接受，但实际WAV只有8秒；没有检查cue.end<=media_duration，可能放行严重不同步。
**新增P1 TIME-NAN-03**：start=float('nan')或end=float('nan')均返回接受；浮点比较与NaN导致检查失效。应要求math.isfinite、数字类型、0<=start<end<=media_duration。
**安全整改要求**：授权必须type(authorized) is bool and authorized is True，且必须绑定不可伪造的授权证据/签名；时间戳有限数值且严格在真实媒体时长内；实际SRT解析器与Cue验证器连通测试；运行至少9类负例（5原有+4新增），在Python -O下安全拒绝同样生效。**不要将简单布尔值当真实版权许可凭证**。
red_team_test_count=9（5原有+4新增；NaN起/终分别计2），original_pass_count=5, additional_blocked_count=0, additional_fail_open_count=4；p0_open_count=1; p1_open_count≥3; production_readiness=NOT_READY。
## E. SAME_FACTORY_REMEDIATION R05→R15
|缺陷|原始问题|独立状态|依据|
|---|---|---|---|
|D1 Opus周期|$14.5/年|**RESOLVED**|官方年付$174，公式12×14.5=174|
|D2 Runway算术|12×0.01×60错误报$15|**RESOLVED**|官方12credits/s×$0.01=$7.20/min|
|D3 Suno版权/额度|500曲下载与商用保证过度推断|**PARTIAL/RECURRED_ADJACENT**|已承认500曲非保证、商用≠版权；但新造“商业权上限$1M”并遗漏20下载/月|
same_factory_defects_count=3; resolved_count=2; partial_count=1; recurred_count=1（同一许可/额度事实族）；resolution_rate=2/3=66.7%；critical_error_recurrence_rate=1/3=33.3%。新增安全P0与价格/机会事实错误不能以修好D1/D2抵消。
## F. CROSS_FACTORY_TRANSFER R14→R15
T1（逐型号/计费周期/公式核价）：已注入且WorkBuddy表格齐，但7抽4错；**FAILED_FACT_ACCURACY**。原因：只核算术未核积分换算、资格额度、主体和条款版本。下轮引入“产品/版本/单位/来源逐字对齐+不同来源冲突检查”。
T2（源码/输入/原始日志/SHA移交）：已注入，完整Python源码与冻结输入在报告，独立WAV/SRT哈希匹配；**EFFECTIVE_FOR_DETERMINISTIC_ARTIFACT_TRANSFER**，但边界安全FAIL，端到端商业能力NOT_PROVEN。
## G. 五案例与机会
A DESIGNED；B SIMULATED（仅Cue门已执行）；C DESIGNED；D DESIGNED；E EXECUTED_FOR_DETERMINISTIC_WAV_SRT, INDEPENDENTLY_VERIFIED_FOR_HASH_ONLY。**0/5商业视频/有声剧端到端**。官方AI Film Award奖项$1m/截止2026-11-20 Dubai已独立核实，但版权授权极广、制作费自担、身份资格未确认；见OPPORTUNITY_RADAR.md。ElevenLabs Grants 33M是12个月总量非月度。
case_status_counts={DESIGNED:3,SIMULATED:1,EXECUTED_DETERMINISTIC:1,INDEPENDENT_HASH_REPLAY:1}; core_mve_status=EXECUTED_SELF_REPORTED; core_mve_independent_replay=HASH_AND_CUE_FUNCTIONS_PASS_WITH_P0; artifact_reproducibility_verdict=PARTIAL; claims_overstated_count≥4; production_readiness=NOT_READY。
## H. R16 F6跨小时交接（最多2项）
U1 **事实单位与资格版本双核**：R15 7抽4错，尤其33M总额度写月度、600 credits写600分钟、Segmind宣传页当主办方正式条款。F6每项高影响数字/DOI/许可证/活动资格必须官方主办页/原文版本+单位/适用范围/日期核对，至少5抽0实质错，来源冲突先列冲突不猜测。
U2 **输入类型与相邻边界红队**：R15代码if not authorized接受字符串"false"，NaN与时间超媒体长度均接受。F6报告发布/证据权限门必须严格布尔/身份授权证据、math.isfinite、范围、跨环境-Python -O检查；至少5负例+针对上述3类相邻边界，0 fail-open；完整源码/日志可独立复算。以上需逐字注入R16实际WorkBuddy委托。