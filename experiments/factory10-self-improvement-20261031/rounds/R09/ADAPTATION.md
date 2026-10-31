# R09 F9｜双轨改进预注册及下一轮验证
- source R08 F8: job b76c0601c10f4d60 DONE；73/100(19/18/15/13/8)，四份Git报告已读取；本实验F9无可比同厂正文，旧实验R09失败0字，SAME_FACTORY_BASELINE_MISSING。
- 实际委托：FEEDBACK_TO_BUDDY.md 3787字符，blob 04c5c4e50e4063353830da8af673b69ae69759b8，已逐字内嵌3981字符MCP prompt；唯一job 75e17092ec644e6c。
## CROSS_FACTORY_TRANSFER
|source_round|source_factory|target_round|target_factory|method_change|baseline_metric|target_metric|observed_metric|verdict|evidence_path|
|---|---|---|---|---|---|---|---|---|---|
|R08|F8|R09|F9|S1 源码SHA/stdout可复放+双模式安全门禁|R08源码SHA2/2 stdout1/1；急停普通exit1但python -O exit0|R09 SHA1/1、stdout1/1；≥2故障×普通/-O两模式4/4非零|PENDING|INJECTED/PENDING_TEST|rounds/R08/CHATGPT_AUDIT.md;rounds/R08/ADAPTATION.md;rounds/R09/FEEDBACK_TO_BUDDY.md|
|R08|F8|R09|F9|S2 官方版本/型号/费用精确核验|R08 ROS2误引ROS1 Fuerte；TB4相机型号泛化；D435 $179与官网$314冲突|≥3个F9官方版本/型号/价格/许可核验，0错配|PENDING|INJECTED/PENDING_TEST|rounds/R08/CHATGPT_AUDIT.md;rounds/R09/FEEDBACK_TO_BUDDY.md|
- S1原因假设：debug assert误当运行时安全门禁；可证伪：任何优化模式故障exit0或源码SHA/stdout不符。S2原因假设：只看官方域名未锁定版本/SKU/计价日期；可证伪：旧版文档冒充新版或型号混价。
## SAME_FACTORY_REMEDIATION
- 旧F9没有真实WORKBUDDY_REPORT/CHATGPT_AUDIT，不能引用不存在的旧内容错误。历史证据缺口HIST-F9-01~05：完整交付、官方/环境/实跑证据、协议与安全负例、五案例、成本商业性。详细修复/验收全文已注入实际prompt。
- 正式同厂旧内容缺陷0、修复率NOT_COMPARABLE、旧内容错误复发率NOT_COMPARABLE；R09若真实报告可审计，则成为R19基线。
## 下一小时R10待验证
- 首先追R09 job 75e17092ec644e6c，若PENDING不重复提交；提取最多2项跨专题方法，不移植AIoT行业结论。重点检验双模式安全与版本精确性是否真的落实；跨厂分数不当因果证据。
- 当前状态：PENDING；效果NOT_VERIFIED，需报告+独立Git回读后更新。
