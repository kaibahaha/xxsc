# R16 F6｜派单前双反馈链与预注册可证伪指标
- planned_at: 2026-11-01 01:25 Asia/Shanghai; predispatch only, do not submit before scheduled time.
- R15 F5真实Job 2b73e0b468c74b33 DONE 416s/14060字符，Git报告与独立审计回读，71/100，事实7抽4错，P0安全fail-open；来源R15/CHATGPT_AUDIT.md、R15/ADAPTATION.md、R15/STATUS.md。
- R06 F6真实Job e8d1a46374fc4607 DONE 668s/9622字符，Git独立审计65/100（17/17/12/11/8），同厂三项高优先级缺陷为429跨服务混因、API/Web价格语义混用、Nature原文日期错；另超12次检索、原始工件缺失。来源R06/CHATGPT_AUDIT.md与R06/WORKBUDDY_REPORT.md。
## CROSS_FACTORY_TRANSFER
|source_round|source_factory|target_round|target_factory|method_change|baseline_metric|target_metric|observed_metric|verdict|evidence_path|
|---|---|---|---|---|---|---|---|---|---|
|R15|F5|R16|F6|U1官方具体页/单位/版本/资格双核|R15 7事实4实错|≥5事实0实错|PENDING|PENDING_TEST|R15/CHATGPT_AUDIT.md §C;R16/FEEDBACK_TO_BUDDY.md §A|
|R15|F5|R16|F6|U2严格类型/有限值/范围+相邻红队+完整工件|R15 5自选负例过但3类相邻fail-open|≥8负例0 fail-open、1套独立可复现MVE|PENDING|PENDING_TEST|R15/INDEPENDENT_REPLAY_EVIDENCE.md;R16/FEEDBACK_TO_BUDDY.md §A|
## SAME_FACTORY_REMEDIATION
- R06 baseline=65/100(17/17/12/11/8); R16待报告，score_delta=NOT_EVALUABLE。
- D1 429服务级归因、D2 Runway API/Web与Suno配额语义、D3 Nature出版日期/撤稿证据为3项主整改；D4检索预算与D5原始工件移交为硬门禁。逐条修复要求、证据、验收见FEEDBACK_TO_BUDDY.md。
- R06五案例A-E逐项复盘已在FEEDBACK §C，禁止冒充全量执行。
## AFTER_RESULT
- WorkBuddy报告实际返回后，ChatGPT核验U1/U2是否逐字注入且实施，独立至少5项官方事实抽查、≥5负例及相邻边界，标RESOLVED/PARTIAL/RECURRED/NOT_VERIFIABLE并计算R06同厂五维Δ；不得将跨厂总分差视为因果。
- 下一轮R17 F7应优先继承真实证据支持的最多两项方法，未验收标NOT_VERIFIED。
## AFTER_RESULT｜R16完成后的独立观察（取代上方PENDING，保留预注册历史）
|source_round|source_factory|target_round|target_factory|method_change|baseline_metric|target_metric|observed_metric|verdict|evidence_path|
|---|---|---|---|---|---|---|---|---|---|
|R15|F5|R16|F6|U1官方具体页/单位/版本/资格双核|R15 7事实4实错|≥5事实0实错|R16独立8抽2项许可错误：OpenAlex元数据CC0被写CC-BY、Crossref元数据一般无署名限制被写必须署名；Google Scholar开放状态NOT_VERIFIABLE|FAILED_FACT_ACCURACY|R16/CHATGPT_AUDIT.md §C;R16/WORKBUDDY_REPORT.md §③/⑥|
|R15|F5|R16|F6|U2严格类型/有限值/范围+相邻红队+完整工件|R15既定5负例PASS但相邻3类fail-open|≥8负例0 fail-open、1套独立可复现MVE|R16源码14375字符/JSONL3801字符真实Git+SHA256独立匹配；Buddy自选14负例PASS自报；ChatGPT忠实逻辑复刻新增9恶意输入全部被错误ADMIT，域名/授权/声明严重P0|ARTIFACT_TRANSFER_EFFECTIVE / SECURITY_FAIL|R16/artifacts/*;R16/INDEPENDENT_SECURITY_PROBES.md;R16/CHATGPT_AUDIT.md §D|
## SAME_FACTORY_REMEDIATION 完成判定
- R06 F6 65/100 (17/17/12/11/8) → R16 F6 67/100 (17/18/15/12/5), Δ+2；研究目标/难度变化，不能将Δ当作因果。
- D1 PARTIAL：跨服务429归因纠正方向，原始头自述；D2 RESOLVED：Runway API/Web与Suno计量语义纠正；D3 PARTIAL：Nature原文日期纠正但Crossref原始关系未核；D4 RESOLVED_BY_SELF_REPORT：8次检索未发现超限；D5 PARTIAL：源码移交/SHA独立通过，但发布安全P0。resolved_count=2/5(含D4自述)，partial=3，新增P0≥2，fact_gate=FAIL。
## R17 F7必须实际注入的两项通用方法
**T1 [P0] 来源身份/发布权利可信锚与恶意URL**：R16源代码`any(domain in url ...)`导致`https://nature.com.evil.example`、`https://evil.example/?ref=nature.com`、`javascript:nature.com`被ADMIT；`authorized=True`+copyright_restricted也放行，空claim/虚假撤稿论文论断可发布。F7至少5项恶意域名/来源伪造/权限自报/撤稿语义负例，必须精确解析HTTPS scheme/hostname、独立权利与事实核验、0 fail-open，提供可独立重放工件，缺证据FAIL。假设：字符串包含与自报布尔替代了信任链；证伪：任一攻击被接受。
**T2 [P1] 学术数据许可分层**：R16把OpenAlex CC0元数据误报CC-BY，把Crossref元数据大体可自由复用误报必须署名；说明研究摘要/全文版权与元数据许可混淆。F7至少5项高影响科学数据/论文/API许可官方具体页核查，分元数据CC0、原论文全文/摘要许可、商用/再分发、用户账户资格、计费周期；0实质错误，冲突UNKNOWN。证伪：任何一项许可或计费单位错即FAIL。
- 两条反馈线均已真实注入R16 MCP 4705字符prompt；效果按独立证据评价，不接受Buddy自评15/15替代。R17须保留R16新的安全反例，而非只重复原有14例。
