# R06 F6｜双轨预注册（派单前）
- R06为本实验F6首轮BASELINE；旧实验F6 Job 52441e82f15942ab FAILED_RATE_LIMIT_429，未有旧正文/评分，formal_old_defects=0，SAME_FACTORY_BASELINE_MISSING，不能计算同比与旧错误复发率。
## CROSS_FACTORY_TRANSFER
|source_round|source_factory|target_round|target_factory|method_change|baseline_metric|target_metric|observed_metric|verdict|evidence_path|
|---|---|---|---|---|---|---|---|---|---|
|R05|F5|R06|F6|V1 数值单位/计费周期/算术自检|R05 Opus年付误写、Runway 12×0.01×60算错、Suno额度混淆|≥5项官方数字含公式/单位/复算，0算术错|PENDING|PENDING_TEST|rounds/R05/CHATGPT_AUDIT.md; rounds/R06/FEEDBACK_TO_BUDDY.md|
|R05|F5|R06|F6|V2 DOI元数据/全文语义/版权权限三层分离|R05 WAV结构探针可重算，但不证明音质或商用许可|≥1真实可复核DOI/确定性探针；0证据越级；五案例标执行状态|PENDING|PENDING_TEST|rounds/R05/ADAPTATION.md; rounds/R06/FEEDBACK_TO_BUDDY.md|
## SAME_FACTORY_REMEDIATION
- 旧R06无真实研究报告，旧Job 52441e82f15942ab后续429失败；旧五案例为设计，不是已执行。历史交付/证据缺口HIST-F6-01~05详见本轮FEEDBACK_TO_BUDDY.md，不能冒充旧内容错误。
- 先以完整反馈文字写Git并回读，再在实际WorkBuddy submit prompt注入；收到报告后分别核查V1/V2与旧缺口，不以Buddy自评当验收。
## R07继承原则
- 下一轮只从本轮真实审计提炼最多2项跨专题研究方法；如R06 PENDING，则标DELAYED_BASELINE并引用最近已完成报告，不编造R06效果。