# R04 F4｜双轨预注册（派单前）
## CROSS_FACTORY_TRANSFER
| source_round | source_factory | target_round | target_factory | method_change | baseline_metric | target_metric | observed_metric | verdict | evidence_path |
|---|---|---|---|---|---|---|---|---|
| R03 | F3 | R04 | F4 | T1真实可复核工件：源码+fixture+原始日志+退出码+SHA | R03 1个Python工件独立重算，另4例多为方案 | R04≥1个可独立重算合成PNG探针，正文全文回传/Git回读 | PENDING | PENDING_TEST | rounds/R03/CHATGPT_AUDIT.md |
| R03 | F3 | R04 | F4 | T2 DOCUMENTED/ENV_PRESENT/EXECUTED/INDEPENDENTLY_VERIFIED分层 | R03 Node仅--version却称逻辑已运行 | 0无证据EXECUTED，≥90%关键断言官方URL或UNKNOWN，5/5负例/回滚 | PENDING | PENDING_TEST | rounds/R03/ADAPTATION.md |
- 两项必须真实注入WorkBuddy的submit prompt；不能仅在Git留文档。
## SAME_FACTORY_REMEDIATION
- 新实验R04首次F4 BASELINE，R14才同厂对比。旧实验R04原Job 5458b23070ac460c 429 FAILED_RATE_LIMIT，**无报告、无评分**；仅可作为历史失败参考，不得编造报告缺陷或已解决率。
- 历史研究缺口（非已证实内容错误）：P0完整交付、P1五案例实测缺失、P1版权/隐私/商用官方证据缺失、P2工具安装授权状态缺失；具体整改指令与五案例A-E逐案方案见本轮FEEDBACK_TO_BUDDY.md。
- 初始 same_factory_score_delta=NOT_COMPARABLE，defects_count=0（没有可审计旧报告），historical_gaps_count=4；效果待报告。
## NEXT
- R05 F5须根据R04真实审计最多迁移2项通用方法；不把合成PNG处理当作AI生成已成功。
## R04实际审计后的CROSS_FACTORY_TRANSFER（最终，取代上方PENDING）
|source_round|source_factory|target_round|target_factory|method_change|baseline_metric|target_metric|observed_metric|verdict|evidence_path|
|---|---|---|---|---|---|---|---|---|---|
|R03|F3|R04|F4|T1可独立复算图像工件|R03 Python核心1例可重算，其余4例未测|R04≥1个真实合成PNG可复算、全文Git回读|PNG 64×48 RGB8、8494字节、SHA256 68032d0248fda5398a0d7a11611b03d21e5e2028afce38d52f40b1e3c1ae1a7d，ChatGPT独立Python复算一致；MCP15728字符、Git回读PASS|EFFECTIVE_FOR_DETERMINISTIC_PROBE|rounds/R04/WORKBUDDY_REPORT.md §6;CHATGPT_AUDIT.md|
|R03|F3|R04|F4|T2证据等级严格分层|R03 Node仅版本探针却称EXECUTED|0无证据执行升级、≥90%关键主张官方核查|R04五案例全部NOT_TESTED，未冒称AI生成；但同脚本解析自称独立验证、跨模型价格混用，关键报价准确率未证|PARTIAL_EFFECTIVE|rounds/R04/CHATGPT_AUDIT.md|
- WorkBuddy job 7532c2af0ef64c5d DONE 234s；报告Git blob 58f7f69986239604f18a8c7d634504bc2f401f45，审计77/100(21/17/15/14/10)；不将R03 80分和R04 77分作跨厂因果比较。
## SAME_FACTORY_REMEDIATION最终
- 旧F4实验无报告且429失败，formal old defects_count=0，historical_gaps=4；1项交付缺口在本轮解决、3项部分改善；same_factory_score_delta=NOT_COMPARABLE，recurred_count=NOT_COMPARABLE。
- 本轮新F4基线77/100，R14对比其四组新增缺陷：①API价格跨模型混用，②自称独立验证过度，③PNG结构测试外推业务质量，④商业收益无量化证据。
## R05 F5双轨移交（仅两项）
- U1结构探针≠业务质检：R04 8494字节PNG/SHA可重算，但尺寸/CRC不证明alpha、文本安全区、内容正确。R05音视频需容器元数据/实际解码/内容合规三层，≥1个合成WAV或视频元数据独立重算，5/5案例标NOT_TESTED或真实执行证据。
- U2费用许可逐产品核对：R04 OpenAI图像价格跨模型混用、Canva AI输出与素材库授权混同风险。R05每个音视频模型给具体版本、官方价格、币种、单位、计费方式、许可范围；≥90%关键报价可追溯，未知标UNKNOWN。以上应完整注入R05实际MCP prompt，不仅留Git链接。
