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
## R08实际完成后的CROSS_FACTORY_TRANSFER（最终审计；上方PENDING是预注册历史）
|source_round|source_factory|target_round|target_factory|method_change|baseline_metric|target_metric|observed_metric|verdict|evidence_path|
|---|---|---|---|---|---|---|---|---|---|
|R07|F7|R08|F8|Q1源码SHA/stdout逐字一致|R07源码SHA0/1、stdout0/1|源码SHA1/1、stdout1/1|R08两套源码SHA2/2一致、主程序stdout1/1一致；独立Python3.13.5 exit0|**EFFECTIVE_FOR_DETERMINISTIC_REPRODUCTION**|rounds/R07/CHATGPT_AUDIT.md;rounds/R08/FEEDBACK_TO_BUDDY.md;rounds/R08/WORKBUDDY_REPORT.md §A Q1;rounds/R08/CHATGPT_AUDIT.md|
|R07|F7|R08|F8|Q2官方标识+真正安全负例|R07错误DOI1、单位负例仅打印|≥3官方标识无错、≥2负例真阻断|普通Python5/5真实非零；但-O急停assert绕过exit0、ROS2引用ROS1 Fuerte、TB4相机泛称、D435官方$314与报告$179不符|**PARTIAL_EFFECTIVE / SAFETY_AND_VERSION_FACT_ERRORS_RECUR**|rounds/R07/CHATGPT_AUDIT.md;rounds/R08/FEEDBACK_TO_BUDDY.md;rounds/R08/WORKBUDDY_REPORT.md §A Q2;rounds/R08/CHATGPT_AUDIT.md|
- 实际注入：FEEDBACK_TO_BUDDY.md 3945字符，Git blob f4ca36d529a7461e5cb95c559d211a6034ec42b6，MCP submit prompt 4354字符逐字包含反馈。Job b76c0601c10f4d60 DONE 489秒/14517字符；报告Git blob 853cbb7dc1c574d0653f8318969c3e64bdeb0d56逐字回读PASS；独立审计Git blob e38e48bb3a3f1f452c3ce84103d8bb19ee143592逐字回读PASS。
## SAME_FACTORY_REMEDIATION最终
- 旧F8历史Job fc588db4b904442c failed/0字，旧实验仅STATUS/FEEDBACK/ADAPTATION，无完整正文和独立评分；same_factory_baseline_round=old experiment R08 HISTORICAL_REFERENCE_ONLY，formal_old_content_defects=0，historical_evidence_delivery_gaps=5，same_factory_score_delta=NOT_COMPARABLE，old_error_recurrence=NOT_COMPARABLE。
- HIST-F8-01 RESOLVED_DELIVERY_ONLY；HIST-F8-02~05 PARTIAL；旧内容修复率NOT_COMPARABLE。本轮新正式F8基线 **73/100 (19/18/15/13/8)**，供R18纵向复测。五个业务案例均PLAN_ONLY/NOT_TESTED，Q1/Q2标准库实验成功≠真实ROS/硬件生产。
- 新错误：assert急停门禁在python -O被绕过、单位负例实为正确换算后越界、ROS2消息引ROS1 Fuerte、TB4 OAK-D-Pro写泛、RealSense D435官方$314而报告$179、商业预算未核实。
## 下一小时R09 F9两项强制方法迁移
**S1 [P0] 字节级可复放+不可绕过安全门禁**。Q1本轮成功SHA2/2、stdout1/1；但Q2 estop用assert，普通Python exit1、python -O exit0。原因假设：把测试断言误作运行时安全机制。R09须对至少1套零硬件AIoT协议/离线控制模拟交源码+输入+原始stdout/stderr+SHA，普通与-O模式都运行≥2真实故障，必须用显式if/raise，目标两模式阻断均2/2、字节一致1/1；可证伪=任何模式故障输入exit0或SHA/stdout不符。
**S2 [P0] 官方版本/型号/价格精确核验**。R08把ROS2 Range引到ROS1 Fuerte旧版、TurtleBot4标准相机OAK-D-Pro泛化、D435硬件价$179与官方$314不符。原因假设：官方链接虽存在却不匹配版本/型号，价格未锁定日期。R09须≥3项AIoT核心设备/协议/SDK官方精确版本URL+同日型号价格/许可，目标版本错配0、价格错配0；可证伪=任一旧版链接冒充新版、不同型号混价、无官方现价却标确定采购预算。
- 上一小时通用改进：计划Q1/Q2→Git完整注入→Q1实证有效、Q2部分有效且安全/事实仍有错→R09调整S1/S2；跨厂总分不作因果证据。
