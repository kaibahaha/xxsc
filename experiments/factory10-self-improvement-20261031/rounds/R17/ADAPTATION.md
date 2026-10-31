# R17 F7｜双反馈链：派单前注册与后续独立验收
- R16 F6（上一小时）67/100；R07 F7（同厂）68/100；跨厂总分不可作因果比较。已真实读取两轮WORKBUDDY_REPORT/CHATGPT_AUDIT/ADAPTATION/STATUS以及R07 FEEDBACK，缺陷证据与修复要求完整写入本轮FEEDBACK并在5017字符MCP prompt中全文注入；job_id=4314c14e9faa4d80。
## CROSS_FACTORY_TRANSFER
|source_round|source_factory|target_round|target_factory|method_change|baseline_metric|target_metric|observed_metric|verdict|evidence_path|
|---|---|---|---|---|---|---|---|---|---|
|R16|F6|R17|F7|T1 HTTPS/hostname精确解析+许可与事实可信锚+相邻红队|R16 9/9恶意输入错误ADMIT，2+ P0|≥8负例，其中≥5相邻，0 fail-open，源码/输入/stdout/SHA独立可重放|PENDING|INJECTED_NOT_YET_TESTED|R16/CHATGPT_AUDIT.md §D; R17/FEEDBACK_TO_BUDDY.md §A|
|R16|F6|R17|F7|T2 元数据/摘要/全文许可分层+具体官方来源核验|R16 8事实2实质许可错误|≥5官方事实0实质错误，0元数据许可外推全文|PENDING|INJECTED_NOT_YET_TESTED|R16/CHATGPT_AUDIT.md §C; R17/FEEDBACK_TO_BUDDY.md §A|
- T1假设：字符串包含与自报布尔替代信任链；可证伪：任何伪域名/无授权/伪撤稿主张被放行。T2假设：品牌级许可外推导致错误；可证伪：任一平台元数据许可被错用为全文许可。
## SAME_FACTORY_REMEDIATION
|defect|R07真实缺陷|R17整改目标|实际状态|
|---|---|---|---|
|D1 P0 DOI|砷基细菌原论文DOI错写10.1126/science.332.1163；正确10.1126/science.1197258；撤稿公告10.1126/science.adu5488|≥3真/伪/撤稿样本官方身份与关系核对，0错误DOI|PENDING|
|D2 P0 工件|Buddy自报SHA64fab3a0...与提取代码两种换行SHA均不符，stdout多一行非源码输出|≥1套字节一致工件、0源码/输出差|PENDING|
|D3 P0 科学负例|单位/seed只打印“blocked”却未拒绝；p值lambda=8与背景H0 lambda=5混淆|≥5真实负例fail-closed，明确H0/H1/单位/误差|PENDING|
- R07五案例：A DOCUMENTED但DOI错；B TOY_SIM数值复放通过但工件SHA失败；C/D/E NOT_TESTED。R17五案例逐案修订已注入FEEDBACK §C；禁止将设计/模拟冒充真实科研/商用。
- 本轮WorkBuddy结果未返回，same_factory_score_delta、resolved/recurred、事实错误率与跨厂迁移效果均NOT_EVALUABLE；后续填实际观察与独立证据，不预判有效。
## 上一小时通用改进：计划→实际注入→实际效果→下轮调整
- T1/T2均已全文注入，Job 4314c14e9faa4d80已提交；实际效果PENDING/NOT_VERIFIED；若返回源码则独立重放恶意URL/许可/撤稿负例，若返回官方事实则逐项抽查许可对象；下轮R18 F8应只继承独立有效的方法。


## R17 FINAL｜双反馈链独立结果（覆盖PENDING，保留预注册历史）
|source_round|source_factory|target_round|target_factory|method_change|baseline_metric|target_metric|observed_metric|verdict|evidence_path|
|---|---|---|---|---|---|---|---|---|---|
|R16|F6|R17|F7|T1可信HTTPS hostname/权利/事实锚与相邻红队|R16 9/9独立恶意输入错误ADMIT|≥8负例0 fail-open|R17 ChatGPT独立Python逻辑复刻10个相邻边界：2正确拒绝，8错误ADMIT；授权字符串false、伪DOI、伪撤稿、rights缺失仍放行|PARTIAL_HOSTNAME_FIX / FAILED_SECURITY|R17/INDEPENDENT_SECURITY_PROBES.md §B|
|R16|F6|R17|F7|T2 metadata/abstract/fulltext许可与官方证据|R16 8抽2实质错误|≥5官方事实0实质错误|R17 8抽3实质错误：OpenAlex不托管全文、所有派生输出CC0、Crossref元数据统一CC0泛化|PARTIAL_IMPLEMENTED / FAILED_FACT_ACCURACY|R17/INDEPENDENT_SECURITY_PROBES.md §D|
- 两项均真实注入本轮4804字符Git FEEDBACK全文及5017字符MCP prompt；Buddy报告确实实施hostname检查和部分许可分层，但目标未达。跨厂R16 67与R17 62总分不作因果比较。
## SAME_FACTORY_REMEDIATION FINAL
- R07 68/100(17/17/13/13/8)→R17 62/100(16/18/12/12/4)，Δ=-6（难度/抽查覆盖不同）；D1 DOI/撤稿 PARTIAL（正确DOI已核但伪造权威关系可放行）；D2 源码SHA/stdout RECURRED（Buddy声称b5aee31b… vs ChatGPT独立单末尾换行f4f33662…，四JSON输入和完整日志未交）；D3统计负例 PARTIAL（H0/H1纠正，但λ=0抛错、未知method/bool obs接受）。resolved=0/3, partial=2, recurred=1, old_defect_recurrence=1/3。
- 五案例A DOCUMENTED、B EXECUTED_SELF_REPORTED+数学复核、C NOT_TESTED、D SIMULATED_SELF_REPORTED、E EXECUTED_SELF_REPORTED但安全失败。没有完整原始MVE独立重放或真实商业端到端。
## 上一小时通用改进：计划→实际注入→实际效果→下轮调整
- T1计划0 fail-open，实际全文注入，独立观察8/10 fail-open，**无效于完整安全目标**，下轮将检查权限/审批严格类型、可信来源与默认拒绝，不能只测旧恶意域名。
- T2计划5项官方事实0错，实际全文注入，独立观察8抽3错，**事实门禁失败**，下轮对官方产品型号/价格/数据授权必须逐项核原始规则与适用对象。
- R18 F8仅迁移2项具体方法：M1【P0严格可信授权/人工审批/安全状态类型和证据链】验证bool严格类型、无授权默认拒绝、至少5项相邻攻击0放行；M2【P0字节级完整工件】交源码、所有冻结输入、完整原始stdout/stderr/退出码/SHA；ChatGPT必须独立重放或明确NOT_VERIFIED。可证伪条件：任一未经授权指令被放行，或任一工件缺失/哈希不一致。
- Buddy外部检索0、候选机会未当期核验，故机会自报不作为可行动；ChatGPT只独立确认IEEE 2027和OpenAlex，均未申请领取。
