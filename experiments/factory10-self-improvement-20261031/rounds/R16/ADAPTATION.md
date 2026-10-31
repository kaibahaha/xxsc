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