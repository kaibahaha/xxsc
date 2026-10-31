# R08 F8｜双轨自我改进预注册（2026-10-31）
- planned_at: 2026-10-31 17:25 Asia/Shanghai；本次新实验F8正式BASELINE；旧F8 fc588db4b904442c失败0字，仅HISTORICAL_REFERENCE，无可比正文/评分：SAME_FACTORY_BASELINE_MISSING。
- R07 F7 c20368ab43794a78 DONE，完整Git回读，独立68/100(17/17/13/13/8)；仅迁移研究方法，不能跨厂比较总分因果。
## CROSS_FACTORY_TRANSFER
|source_round|source_factory|target_round|target_factory|method_change|baseline_metric|target_metric|observed_metric|verdict|evidence_path|
|---|---|---|---|---|---|---|---|---|---|
|R07|F7|R08|F8|Q1 源码/哈希/stdout字节一致性|R07源码SHA不符1/1、stdout不符1行|至少1套独立复放，SHA一致1/1、stdout逐字一致1/1|PENDING|PENDING_TEST|rounds/R07/CHATGPT_AUDIT.md;rounds/R08/FEEDBACK_TO_BUDDY.md|
|R07|F7|R08|F8|Q2 官方ID与真实负例阻断|R07错误DOI1条、单位负例仅打印|≥3官方型号/接口/单位核验0错、≥2真阻断|PENDING|PENDING_TEST|rounds/R07/CHATGPT_AUDIT.md;rounds/R08/FEEDBACK_TO_BUDDY.md|
- Q1原因假设：执行工件与报告版本漂移；可证伪=任何SHA/stdout不一致。Q2原因假设：标识未经原文核对、文本打印冒充程序阻断；可证伪=错误官方标识或负例无异常。
## SAME_FACTORY_REMEDIATION
- 旧F8只有STATUS/FEEDBACK/ADAPTATION，Job最终FAILED_NOT_SUBMITTED_TO_CODEBUDDY、0字，无WORKBUDDY_REPORT/CHATGPT_AUDIT。历史缺口HIST-F8-01~05（交付/来源/安全/五例/生态），不是旧内容事实错误。正式旧内容缺陷数0、旧评分/复发率NOT_COMPARABLE。
- 本轮研究必须将Q1/Q2与HIST-F8-01~05完整注入实际MCP prompt；待报告真实返回后独立验收、填实测CROSS_FACTORY_TRANSFER，R18同厂复测。
## 下一轮预留
- R09 F9 AIoT硬件仅继承最多2项经审计的通用方法；若本轮PENDING只追真实job，不重复派单。