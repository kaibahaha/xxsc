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

## R19 actual MCP injection evidence
- Git FEEDBACK_TO_BUDDY.md 4620 chars/blob 0aceedcbd77a2cd2d582ce7f8d93b345b4d20933, readback exact; actual WorkBuddy submit prompt 4908 chars contains complete feedback verbatim; unique job **e01700a27b7b44f4**. Both cross-hour T1/T2 and same-factory D1/D2/D3 were actually injected; observed quality=PENDING, not yet effective.
- CROSS_FACTORY_TRANSFER verdict for T1/T2 updated from PRE_REGISTERED_NOT_YET_INJECTED to INJECTED_PENDING_TEST; same-factory remediation D1/D2/D3 remains NOT_VERIFIABLE until real report + independent audit.

## R19 FINAL｜双轨真实效果（替代预注册PENDING判断）
- 唯一job e01700a27b7b44f4 DONE/311s，真实报告16592字符，Git blob 2c37f144b6ed397be5c077e02eff9c639f033861 readback PASS；ChatGPT独立审计 blob 417cfce01243d5dd55117a8fa0e7b8158b753f82 readback PASS；实际MCP prompt 4908字符逐字包含Git FEEDBACK 4620字符。不能将研究文本交付与质量验收混同。
## CROSS_FACTORY_TRANSFER FINAL
|source_round|source_factory|target_round|target_factory|method_change|baseline_metric|target_metric|observed_metric|verdict|evidence_path|
|---|---|---|---|---|---|---|---|---|---|
|R18|F8|R19|F9|T1可信身份/签发者nonce/缺字段默认拒绝|R18独立9相邻探针8 ADMITTED、1 TypeError|≥8真实负例0误ADMIT并可独立重放|Buddy自述12例PASS，报告缺全部4源码/6JSONL/原始日志，独立执行0；同口径不可比|INJECTED_NOT_VERIFIED|R19/FEEDBACK_TO_BUDDY.md;R19/WORKBUDDY_REPORT.md §A;R19/CHATGPT_AUDIT.md|
|R18|F8|R19|F9|T2官方版本/现价+字节工件链|R18官方7抽2错、stdout SHA不符|R19≥5官方事实0错、完整MVE字节复放|R19官方6抽2错（RPi5 USD70过时、Zephyr4.4非最新）；0/5核心源码/输入文件可复算|FAILED_FACT_AND_ARTIFACT_GATE|R19/CHATGPT_AUDIT.md §高影响官方事实;R19/WORKBUDDY_REPORT.md §F|
## SAME_FACTORY_REMEDIATION FINAL
|defect|R09事实|R19独立结果|status|
|---|---|---|---|
|D1 P0|缺ID/ts/空commands放行|Buddy自述新schema/nonce及12负例，源码和日志缺，无法独立证实无fail-open|PARTIAL / P0_OPEN|
|D2 P1|RPi/Mosquitto/ESP-IDF旧版当现行|Mosquitto/ESP修正，但RPi旧价重复、Zephyr最新版本又错|RECURRED|
|D3 P1|Case B缺源码/6JSONL，Case C OTA分支冒充闭环|Case C诚实DESIGNED，但Case B仍只有SHA/文件名没有源码/输入，无法重放|RECURRED|
- R09 65(16/18/13/11/7)→R19 57(14/18/11/10/4)，Δ=-8；resolved=0/3, partial=1/3, recurred=2/3, recurrence=2/3；不同研究任务/证据难度不能推断模型因果。五案例独立复现0/5，事实门禁FAIL，production NOT_READY。
## 上一小时通用改进：计划→实际注入→实际效果→下轮调整
- T1计划签发者/nonce+相邻红队→Git和MCP全文实际注入→Buddy声称12负例PASS，但缺源码无法独立验证，**NOT_VERIFIED**→R20 U1必须完整原始工件在报告内可直接重放。
- T2计划最新官方事实+完整SHA→Git和MCP实际注入→6抽2错、0/5核心文件可复算，**FAILED**→R20 U2必须按发布时间/版本/适用SKU锁定官方最新有效页。
- R20 F10跨厂只迁移U1/U2研究方法，不移植F9行业结论或分数；R20同厂另读取R10做专项整改。机会发现≠领取，0到账。
