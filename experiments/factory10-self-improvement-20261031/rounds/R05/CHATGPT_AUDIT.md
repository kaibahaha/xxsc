# R05 F5｜ChatGPT独立审计｜2026-10-31
- Experiment FACTORY10-SELF-IMPROVEMENT-20261031；F5本实验首次正式BASELINE，R15才作同厂纵向复测。
- WorkBuddy唯一Job **09ea81a5a538420a**，MCP真实DONE，返回13721字符含BEGIN_FULL_REPORT/END_FULL_REPORT；Git报告 commit **b0e357429f121b09e2529331542935690f9609d8**、blob **2758bf8630378dd70ce0ebbdc7e6532dbb467577**，逐字回读PASS。执行耗时以最终WorkBuddy任务列表为准，不臆造。
- 本轮评分 **73/100（证据18/25、战略17/20、操作技巧15/20、五案例14/20、风险真实性9/15）**；CONDITIONAL_ACCEPT_FOR_RESEARCH / NOT_READY_FOR_COMMERCIAL_PRODUCTION。仅证明研究与合成媒体探针可复现，未验证AI音视频商业生产。
## 一、五维独立评分
|维度|得分|依据|
|---|---:|---|
|证据/事实25|18|13候选矩阵、原始stdout自述与WAV完整源码可复算；但Runway每分钟成本算错、Opus年付/月付写错、Suno曲数/版权结论过度；多行引用聚合站却标DOCUMENTED(官方)。≥90%官方可核价格目标未证明。|
|战略20|17|聚焦零预算多语视频音频、五类商业工厂联动和权限/版权门禁；但市场规模UNKNOWN、真实渠道转化与人工工时缺实测，单位经济的价格错误影响排序。|
|操作技巧20|15|标准库WAV合成/哈希可独立重算；明确ffmpeg/ffprobe/sox/whisper缺失；其余商业API与编辑命令未执行，Case A scale=1080:1920可拉伸原素材，不能直接用于可靠9:16产线。|
|五案例20|14|A-E逐案有输入/命令/输出/负例/回滚/授权/成本/状态；五个商用案例均未端到端运行，E只有合成单音WAV探针。部分负例为纸面条件，无真实拒绝日志。|
|风险真实性15|9|区分L1/L2/L3与NOT_TESTED、无未经授权发布；但Suno royalty-free≠不会Content ID、AI商业权≠版权保护、若干工具商业许可与成本表述过强；五案例发布权限/平台政策缺逐项官方证据。|
|**总计**|**73/100**|研究有条件接受，真实商业执行未就绪。|
## 二、独立WAV字节级复算（与远端自述分开）
- 从报告§1.1取完整Python源码逻辑，ChatGPT在独立Python环境重新生成：SR=8000、DUR=1s、FREQ=440Hz、AMP=0.6、N=8000、PCM16 mono；Python wave默认RIFF/WAVE头44字节，PCM数据16000字节。
- 独立结果：**16044 bytes**，SHA256 **5fc01c0f096e4def771d173852278fe14fbd9240326d4461394af901e9be4a65**；wave重新打开得channels=1、sampwidth=2、framerate=8000、nframes=8000、readframes=16000 bytes，全部与报告一致。
- 判断：**INDEPENDENTLY_VERIFIED_FOR_DETERMINISTIC_WAV**。这不是独立登录远端服务器查看其文件或stdout，也不是音质、语音可懂度、视频渲染、平台版权的验证；报告所谓“独立解码”同属WorkBuddy自述，只有ChatGPT重算才是本轮独立复核。
## 三、2026-10-31官方来源抽查：关键事实与错误
1. **Opus Clip订阅周期错误（P0-PRICE-01）**：报告Top5称“Pro $14.5/年”，Case B称“Pro $14.5/年”；官方 https://www.opus.pro/pricing 显示**$14.50/月、按年支付$174**（月付$29/月），非$14.5/年。报告§2矩阵“$29($14.5年)”虽有歧义，Top5与案例明确定价错误。需按年度总现金支出、月等效价和用量分列。
2. **Runway单分钟成本算错（P0-PRICE-02）**：报告§4“Gen-4.5≈$15/分钟（12 cr/s×$0.01）”数学错误：12×0.01×60=**$7.20/分钟**（仅按开发者API基础生成价，不含附加输出格式/重试/税）；官方 https://docs.dev.runwayml.com/guides/pricing/ 给API credit $0.01、Gen-4.5 12 credits/s，https://help.runwayml.com/hc/en-us/articles/15124877443219-How-do-credits-work 给Web端12 credits/s。API与Web订阅credits不能直接混为同一现金成本；旧报告$15/min不可采信。
3. **Suno版权/产能过度推断（P1-RIGHTS-03）**：报告称“Pro$8、2500cr≈500曲→$0.016/曲，royalty-free可规避Content ID”。官方 https://suno.com/ja 当期Pro列2500 credits/月但**20 song downloads/月**，无法用2500 credits直接证明500首可下载商用作品；https://help.suno.com/en/articles/9601665 明确商业使用权**不保证作品受版权保护**，也不能保证无Content ID争议；https://help.suno.com/en/articles/2416769 区分付费生成与免费生成作品权利。
4. **ElevenLabs免费商用限制可核（正例）**：https://elevenlabs.io/sound-effects 与 https://elevenlabs.io/pricing 区分Free个人使用与付费商业权，10k credits/月与Starter$6等可核。但“每字符$0.0005–0.001”缺套餐与具体模型/credit算法支持，须标估算而非官方报价。
5. **HeyGen基本档位可核（正例）**：https://www.heygen.com/pricing 当前Free 3条/月水印、Creator$29/月、Pro$49/月；报告Free“1–3条/月”模糊，博客换算秒价不能与正式API报价混同。
6. **Descript基本档位可核（正例）**：https://www.descript.com/pricing 当前Hobbyist $16/月年付、Creator $24/月年付，月付Creator $35/月；须区分计费周期。
7. **ffprobe范围（方法核查）**：https://www.ffmpeg.org/ffprobe.html 说明ffprobe是媒体流与容器信息探针，不能仅据其元数据输出证明听感、视频内容正确、授权合规。本环境ffprobe自报未安装。
8. **YouTube政策缺口（P1-POLICY-04）**：https://support.google.com/youtube/answer/1311392 说明大量重复/批量生产内容可能不符合变现资格；报告仅泛提Content ID/reused-content，没有给平台对AI内容标识、联盟披露、自动发布的逐项可核政策和适用范围。真实上线前仍需政策矩阵。
## 四、CROSS_FACTORY_TRANSFER R04 F4→R05 F5
|method_change|R04真实基线|R05实测|verdict|
|---|---|---|---|
|U1 L1格式/元数据≠L2可听/解码≠L3内容/版权|R04 PNG 8494B哈希可重算，但商业视觉5案例未测|R05标准库WAV 16044B、SHA一致，独立wave读取8000帧；明确音质/商用5案例未测。仍未试听/语音识别/商业发布|**EFFECTIVE_FOR_DETERMINISTIC_MEDIA_PROBE；NOT_PROVEN_FOR_PRODUCTION**|
|U2 逐产品价格、许可、地区/计费单位核验|R04图像模型混价与授权混淆|R05矩阵更细，但Opus年付误写、Runway算术错误、Suno版权与产能外推、聚合价标官方|**PARTIAL_FORMAT / FAILED_FACT_ACCURACY**；≥90%官方核验目标未通过|
- R04 77/100与R05 73/100属于不同工厂，不得相减作因果改进。
## 五、SAME_FACTORY_REMEDIATION：历史旧实验没有内容基线
- old experiment F5 R05 job **6f4057fc78094c63** 最终429额度失败；无完整旧研究报告或独立评分。formal_same_factory_defects_count=**0**（无可审旧报告），historical_delivery_gaps=4；same_factory_baseline_round=old R05 HISTORICAL_REFERENCE_ONLY；same_factory_score_delta=**NOT_COMPARABLE**，recurred_count=NOT_COMPARABLE。
|历史真实缺口|WorkBuddy自述|ChatGPT独立复核|
|---|---|---|
|HIST-F5-01 429无研究全文|RESOLVED|**RESOLVED_DELIVERY_IN_NEW_RUN**：本轮新Job DONE，完整MCP文本与Git全文回读通过；不等于429根因被修复。|
|HIST-F5-02 五案例仅旧计划无执行|PARTIAL|**PARTIAL**：5/5案例有字段，仅合成WAV探针可独立复算，商业案例未运行。|
|HIST-F5-03 商用版权/声音/平台政策无研究报告|PARTIAL|**PARTIAL**：有权利边界但Suno权利推断和YouTube/TikTok/Meta逐项官方政策不全。|
|HIST-F5-04 工具/Skill/价格候选缺最终核验|PARTIAL|**PARTIAL**：13候选与Top5齐，但多个价格/许可误判，安装/授权仅自述，ChatGPT连接器与WorkBuddy能力未完整逐项核。|
- 旧报告缺陷解决率**NOT_COMPARABLE**（分母0）；历史交付缺口改善1/4、其余3项PARTIAL。新发现4组缺陷：P0-PRICE-01 Opus周期，P0-PRICE-02 Runway算术，P1-RIGHTS-03 Suno权利/下载量，P1-POLICY-04平台政策与授权；另外Case A画面比例拉伸风险。不能用“新Job成功”证明旧429不会再发生。
## 六、五案例逐案审计与R15必须整改的可测条件
- A 联盟视频：保留claims/region/rights.json设计；ffmpeg scale=1080:1920直接变形，需scale+pad/crop策略及源宽高/安全区测试；真实广告披露、平台发布权限、品牌授权与投放审批未测。
- B 长视频切片：保留SRT对齐/版权/重用内容门禁；Opus Pro价格应改$14.5/月年付$174；须冻结一段自有素材并执行字幕时间戳正负例。
- C 游戏预告：保留shot_evidence.csv与真实玩法约束；需实际源视频帧号映射和不存在玩法拒绝日志，未运行引擎不能自称试玩。
- D 科学微课：保留双语事实清单；须真实音画同步、科学事实反例与人工签核，不能只写“审核”。
- E 有声剧：保留同意台账与WAV探针；440Hz单音不能代表TTS语音/混音，需真实合法授权台词、响度、剪切、角色一致性及人工试听。
## 七、下一轮R06 F6跨厂最多两项方法迁移
**V1 数值/报价自检**：每个商业价格、单位经济、费用推导必须给可重算公式、计费周期、来源与币种；至少抽查5项官方计费与算术，任何错误判FAIL，UNKNOWN不虚构。R05实证Opus $14.5/年误写、Runway $15/min误算、Suno $0.016/曲忽略下载上限。
**V2 工件可复算与语义/权利门禁分层**：R05合成WAV 16044B/SHA独立复算，但无法证明音质/商业合规。F6研究报告工厂必须把DOI/元数据结构校验、原论文/撤稿状态与论点语义准确、版权/数据权限三层分开；至少1个真实可独立复核DOI/元数据或确定性引用格式探针，未读全文不得称“原论文已证实”。5案例标真实执行与未执行，禁止自述越级。
## 八、最终判断
**73/100：R05研究交付和WAV确定性探针通过，价格事实准确性、商业权利与真实生产验证仍不合格。** R15以本次73/100和本审计四组缺陷作为正式同厂整改基线；R06跨小时检验V1/V2。不得以跨厂总分比较声称模型质量进退。
