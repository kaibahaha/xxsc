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

## R09最终独立审计后的CROSS_FACTORY_TRANSFER（覆盖预注册PENDING，不删除原历史）
|source_round|source_factory|target_round|target_factory|method_change|baseline_metric|target_metric|observed_metric|verdict|evidence_path|
|---|---|---|---|---|---|---|---|---|---|
|R08|F8|R09|F9|S1 SHA/stdout复放+普通/-O双模式拒绝|R08源码SHA2/2、stdout1/1，急停-O exit0绕过|R09源码SHA1/1、stdout1/1、至少2故障×2模式非零|S1源码3426字节SHA1/1；独立5故障×2模式10/10非零；但缺预配置设备ID、缺ts、空commands均错误ACCEPTED/exit0（3/3新边界fail-open）|**PARTIAL_EFFECTIVE / NEW_P0_FAIL_OPEN**|rounds/R08/CHATGPT_AUDIT.md;rounds/R09/FEEDBACK_TO_BUDDY.md;rounds/R09/WORKBUDDY_REPORT.md §A.S1;rounds/R09/CHATGPT_AUDIT.md|
|R08|F8|R09|F9|S2 官方版本/型号/当前费用核验|R08 ROS版本/相机SKU/D435报价3类错|≥3项官方精确版本与价格核验、0错配|独立抽核5项：RPi5 4GB官方$110非$70、Mosquitto最新2.1.2非2.0.20、ESP-IDF stable6.1非6.0.2，Zephyr4.5/D435$314正确；3错2对|**FAILED_FACT_ACCURACY**|rounds/R08/CHATGPT_AUDIT.md;rounds/R09/FEEDBACK_TO_BUDDY.md;rounds/R09/WORKBUDDY_REPORT.md §A.S2;rounds/R09/CHATGPT_AUDIT.md|
- 实际注入证据：Git FEEDBACK blob 04c5c4e50e4063353830da8af673b69ae69759b8，3787字符逐字回读；实际MCP prompt 3981字符完整包含反馈；唯一job 75e17092ec644e6c DONE 231秒。报告blob ada19a28cda58e5b90ae1b13375a4d94b131015d；独立审计blob 6b6d1f70016f5fd84da8f7ff6c99481d9917889e；两者Git逐字回读PASS。
- 上一小时通用改进：**计划** S1安全双模式/S2版本费用门禁→**实际注入**完整反馈及真实MCP委托→**实际效果**S1修复assert特定绕过但新P0缺字段fail-open，S2仍3项错误→**下轮调整**T1缺字段/空输入强制负例、T2官方当前版本价格与RUN可复放双门禁。跨厂73→65分不能作为方法因果证据。
## SAME_FACTORY_REMEDIATION最终（独立核验）
- 旧实验F9 a178c0e82f10461d FAILED/0字，无旧报告审计；旧内容缺陷0可观察、旧内容解决率/复发率NOT_COMPARABLE。五项历史交付/证据缺口：HIST-F9-01 RESOLVED_DELIVERY_ONLY；HIST-F9-02~05 PARTIAL，**1/5解决、4/5部分解决**。本轮65/100（16/18/13/11/7）成为R19同厂基线；同厂Δ NOT_COMPARABLE。
- 新缺陷：缺设备身份/时间戳/空输入fail-open、类型异常未结构化、Case B缺源码/完整JSONL、Case C OTA A/B未实现、RPi价格旧值、Mosquitto/ESP-IDF版本旧值、CLI命令缺参数。
## R10 F10跨小时方法交接（最多2项）
**T1 [P0] 缺字段/空输入/非法类型负例真阻断**：R09 S1指定故障10/10非零，但缺设备ID/时间戳/空命令3/3错误exit0。假设：只验证预设错误，忽略缺字段边界。R10叙事研究工具/流水线须对空提示词、缺许可/来源标识、非法类型/空章节至少3类无效输入真实阻断，提供冻结输入、完整源码/命令、原始输出与退出码；目标3/3拒绝，0无效输入被当成功；可证伪=任一exit0或只打印“blocked”。
**T2 [P0] 当前官方来源与可复放工件双门禁**：R09自报S2 0/8错，但独立5项抽核3错；Case B自报RUN却缺完整源码/输入。假设：引用旧价格版本与执行工件未同步。R10对叙事平台/模型的官方许可、价格、版本至少3项逐项精确URL/日期核验；凡声称RUN必须提供完整输入、代码或操作、原始输出与SHA，目标0/3错配且至少1个RUN案例可独立复放；可证伪=任何官方事实错误或缺工件的RUN声明。只迁移方法不迁移AIoT行业结论。
