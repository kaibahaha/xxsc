# R19 F9｜双轨预注册（派单前）
- PREPARED；source R18 F8 DONE e06ced6b21e84758 71/100；same_factory R09 F9 DONE 75e17092ec644e6c 65/100；R19正式评分PENDING。Git FEEDBACK 4620字符已逐字回读，实际MCP注入待派单后核验。
## CROSS_FACTORY_TRANSFER
|source_round|source_factory|target_round|target_factory|method_change|baseline_metric|target_metric|observed_metric|verdict|evidence_path|
|---|---|---|---|---|---|---|---|---|---|
|R18|F8|R19|F9|T1可信身份/签发者、nonce防重放、未知/缺字段默认拒绝、双模式相邻红队|R18独立9相邻探针8 ADMITTED、1 TypeError；source字符串可伪造|R19≥8相邻负例0错误ADMIT、0副作用|PENDING|PRE_REGISTERED_NOT_YET_INJECTED|R18/CHATGPT_AUDIT.md;R18/INDEPENDENT_SECURITY_PROBES.md;R19/FEEDBACK_TO_BUDDY.md|
|R18|F8|R19|F9|T2官方精确版本SKU/价格+原始stdout/stderr SHA链|R18官方7抽2错；normal stdout SHA不符，optimize/P1原始字节缺|R19≥5官方事实0实错、MVE完整工件0缺失/0哈希冲突|PENDING|PRE_REGISTERED_NOT_YET_INJECTED|R18/CHATGPT_AUDIT.md;R18/ADAPTATION.md;R19/FEEDBACK_TO_BUDDY.md|
- T1假设：字符串白名单替代受信签发与防重放；可证伪=任何无效输入exit0。T2假设：SKU/版本和运行快照未锁定；可证伪=任何当前版本错误或工件SHA不符。
## SAME_FACTORY_REMEDIATION
|defect|R09独立事实|R19修复与通过条件|observed|status|
|---|---|---|---|---|
|D1 P0|缺expected_device_id/ts/空commands均exit0 ACCEPTED|严格身份/时间戳/非空schema，≥8负例双模式0放行|PENDING|NOT_VERIFIABLE|
|D2 P1|RPi5 4GB $70、Mosquitto2.0.20、ESP-IDF6.0.2误当当前，5抽3错|本轮官方精确URL/日期/型号/计价核验≥5项0实错|PENDING|NOT_VERIFIABLE|
|D3 P1|Case B缺完整源码与6JSONL，Case C仅OTA拒绝分支却称RUN|完整MQTT网关MVE可复放，OTA未完整则诚实标DESIGNED|PENDING|NOT_VERIFIABLE|
- 同厂R09基线65(16/18/13/11/7)，same_factory_defects_count=3，resolved_count=PENDING，recurred_count=PENDING，same_factory_score_delta=NOT_EVALUABLE；五案例A-E逐案要求见FEEDBACK §C。
## 上一小时通用改进：计划→实际注入→实际效果→下轮调整
- 计划T1/T2详见FEEDBACK；Git写入已验证，尚未实际submit；实际效果NOT_VERIFIED；下轮R20先追R19唯一job并独立核验，若未返回保持PENDING，不把方法预注册当实施。
