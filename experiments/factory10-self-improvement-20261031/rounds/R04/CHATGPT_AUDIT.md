# R04 F4 图像视觉｜ChatGPT独立审计｜2026-10-31
- experiment FACTORY10-SELF-IMPROVEMENT-20261031；本实验F4首次基线，R14才进行同厂纵向评分。
- WorkBuddy job **7532c2af0ef64c5d** DONE 234s，MCP返回15728字符，BEGIN_FULL_REPORT/END_FULL_REPORT完整，实际报告 Git blob **58f7f69986239604f18a8c7d634504bc2f401f45**，commit **e5ef293f24e38781c1a9670fd21ac4d17a26b73e**，回读逐字一致。
- 独立复核：ChatGPT在独立Python执行环境按报告第6节的冻结输入W64/H48、RGB渐变、zlib压缩等级9、PNG chunks与CRC算法重新实现并计算：file_bytes=8494，SHA256=**68032d0248fda5398a0d7a11611b03d21e5e2028afce38d52f40b1e3c1ae1a7d**，与WorkBuddy报告完全一致。此项证实算法/字节级**可独立复算**；不等于独立访问WorkBuddy远端文件、观察原始进程stdout或执行AI图像生成。
- **独立评分 77/100（证据21/25、战略17/20、操作技巧15/20、五案例14/20、风险真实性10/15）**。CONDITIONAL_ACCEPT_FOR_RESEARCH；真实商业视觉流水线NOT_READY。
## 一、五维评分
|维度|满分|得分|证据|
|---|---:|---:|---|
|证据与事实|25|21|完整原文和11候选矩阵，PNG源码可独立重算；但gpt-image模型/计费混用、若干工具商业许可/功能断言未核、官方链接数量不等于主张正确性。|
|战略契合|20|17|围绕低成本可追溯视觉资产，覆盖游戏/联盟广告/科学/叙事/视频；但ROI、收益排序、国内合规摩擦、运营成本未提供可比样本或实测。|
|技巧与执行|20|15|标准库PNG合成及CRC/尺寸探针可复算，清楚披露Pillow/ImageMagick/libvips未安装；五案例的pipeline.build、compose、render_figure等CLI均是占位伪命令，未构建实际管线。|
|五案例|20|14|A–E十字段、权限/费用/负例/回滚都有；五个案例均NOT_TESTED，合成PNG RGB探针不验证A的alpha、不验证B广告声明水印、不验证C色盲与科学准确性、不验证E文字安全区。|
|风险与真实性|15|10|明确AI生成/发布未做，旧F4因429失败不冒充研究缺陷；但AI输出权利、第三方素材许可和各地广告责任需分层，报告“独立解析”发生在同一脚本，不能称真正独立执行验证。|
|**总计**|**100**|**77**|研究基线可用，产品级执行尚缺。|
## 二、官方资料独立抽查（仅核可证事实）
1. OpenAI API官方价格 https://developers.openai.com/api/docs/pricing ：当前页面 gpt-image-2列出文本输入$2.50/百万、图像输入$4/百万、图像输出$15/百万（页面有Standard/Batch不同展示）；报告把“GPT Image 2/1.5/1”混成统一文本$5/图入$10/图出$40，并用$0.005–$0.21单图区间，**缺模型版本与计费档位对应，不能作为当前报价**。需逐模型、Standard/Batch、尺寸/质量重核。报告“组织验证必需”亦不应无条件套用于所有模型/账户。
2. Canva官方 https://www.canva.com/pricing/ ：美国页面Pro $144/年、Business $250/人年可核；但价格受地区、税和计费周期影响。Canva AI条款 https://www.canva.com/policies/ai-product-terms-2026-06-26/ 与素材许可 https://www.canva.com/policies/content-license-agreement/ 区分AI输出与Licensed Content；不能把“使用Canva AI”推断为全部素材可转售/客户再许可。
3. ComfyUI官方 https://github.com/Comfy-Org/ComfyUI ：确有开源节点图、API、GPU/云端安装，GPL-3.0；不能由仓库存在推断本环境已安装、模型权重可商用或生成成本为零。
4. ImageMagick官方 https://imagemagick.org/identify/ ：identify可检查尺寸、格式、色彩和文件完整性；**不能凭尺寸/CRC证明文字没裁切、广告声明存在、科学内容正确、角色风格一致**。
## 三、T1/T2跨小时迁移：R03→R04
|method_change|R03基线|R04实际观察|结论|证据|
|---|---|---|---|---|
|T1完整可独立复算工件|R03仅1个Python核心可复算，其他案例缺原始日志|R04完整标准库PNG源码、冻结W64/H48、原始stdout自述、Git全文，ChatGPT另起Python重算8494字节与SHA完全一致|**EFFECTIVE_FOR_DETERMINISTIC_PROBE**，但不等于AI生成/五案例实测|R04/WORKBUDDY_REPORT.md §6；本审计独立重算|
|T2证据等级与反例|R03 Node仅--version却称逻辑EXECUTED|R04清楚标AI工具未安装/未授权、五案例NOT_TESTED；但同脚本解析自称INDEPENDENTLY_VERIFIED过度，OpenAI价格多模型混用|**PARTIAL_EFFECTIVE**，执行状态更谨慎，事实准确性仍需提升|R04/WORKBUDDY_REPORT.md §§1,3,5,6|
- R03 80分与R04 77分属于不同工厂，**不得作跨厂因果分差**。
## 四、SAME_FACTORY_REMEDIATION（严格证据口径）
旧实验F4 Job 5458b23070ac460c FAILED_RATE_LIMIT_429、无完整研究正文、无评分，故**SAME_FACTORY_BASELINE_MISSING / same_factory_score_delta=NOT_COMPARABLE**；旧报告可审计内容缺陷数=0（无报告），旧研究计划有4个可证实缺口，不能虚构历史错误。
|历史缺口（非旧报告内容错误）|实际响应|独立判定|
|---|---|---|
|HIST-P0-01 旧429无正文|本轮DONE、全文MCP回传并Git回读|**RESOLVED_DELIVERY_IN_NEW_RUN**；不是证明旧429根因已修复或额度不会再触发|
|HIST-P1-02 五案例无实际结果|A–E十字段齐备，全部NOT_TESTED，PNG合成探针仅结构验证|**PARTIAL**|
|HIST-P1-03 商用权利/隐私/广告政策无官方核查|提出权利矩阵与拒绝案例，Canva和OpenAI政策细节不完整|**PARTIAL**|
|HIST-P2-04 工具矩阵缺失|11候选有官方入口与状态，价格版本混用|**PARTIAL**|
- historical_report_defects_count=0; historical_gaps_count=4; delivery_gaps_resolved=1; gaps_partial=3; recurred_count=NOT_COMPARABLE（无旧内容）；new_defects=4组：价格跨模型混用、同脚本自称独立验证、PNG QA能力外推、商业收益缺数据。
## 五、五案例逐案R14整改要求
- A游戏资产：合成RGB探针不能测透明alpha或角色一致；需真实RGBA源图/独立alpha检查与3视图一致性人工/模型评价，附可复核素材授权。
- B跨境广告：尺寸/CRC不能证明SKU真实性或声明水印；需OCR/规则/人工复核与品牌授权书编号、平台政策、发布前阻断日志。
- C科学插图：PNG结构不证明物理正确或色盲可读；需有版本的事实清单、颜色对比计算、人工科学审校签字。
- D小说封面：比例通过不代表字体商用授权或肖像权；需实际字体许可证、RIGHTS_MATRIX与人工放行记录。
- E视频缩略图：尺寸正确不代表文字安全区或可读性；需实际bbox裁切测试、不同设备预览和A/B指标，未发布则不能称CTR改善。
## 六、R05 F5跨厂移交（最多2项）
- **U1“结构探针≠业务质检”分层**：R04合成PNG 8494字节/SHA独立复算通过，但RGB尺寸/CRC不能证明alpha、字幕安全区、商用权利。R05视频音频必须分别给“容器/元数据校验”“解码/播放或波形测试”“内容/版权人工审核”三层，若只跑ffprobe或wav header不得称视频质量/声音可听/授权通过；目标≥1个可独立重算的合成WAV/视频元数据探针，5案例各标测试层与NOT_TESTED。
- **U2“计费/授权逐产品逐版本核对”**：R04 OpenAI图像API将多模型费率混用，Canva AI输出与素材许可需区分；R05视频音频工具必须按具体模型/计费维度/地区/许可版本给官方链接，禁止用一家公司统一单价；目标≥90%关键报价可对应官方模型+日期/币种/单位，不可证标UNKNOWN，零无证据“已商用”。
## 七、最终结论
**77/100**：云端研究、全文Git交付、独立PNG字节级重算均通过；实际AI图像生成、商业视觉素材、五案例端到端、平台发布与商业授权未执行。下一轮F5应检验U1/U2；同厂R14才可与本次77分和4组新缺陷进行纵向整改对比。