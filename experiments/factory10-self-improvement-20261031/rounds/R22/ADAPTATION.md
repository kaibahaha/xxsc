# R22 F2｜双轨自我改进预登记
## CROSS_FACTORY_TRANSFER
R21 Git与job均未找到，PREVIOUS_HOUR_MISSING；R20 F10 OOM无报告；采用R19 F9已完成且审计FAIL的DELAYED_BASELINE，不能拿R19总分57与F2总分做因果比较。
|source_round|source_factory|target_round|target_factory|method_change|baseline_metric|target_metric|observed_metric|verdict|evidence_path|
|---|---|---|---|---|---|---|---|---|---|
|R19|F9 AIoT|R22|F2软件|T1完整源码/冻结输入/runner/stdout stderr/实际SHA直接在报告交付|R19 0/5核心文件可独立复算|R22至少1/1 MVE原始字节齐全、可独立重放|PENDING|ACTUALLY_INJECTED_NOT_VERIFIED|R19/CHATGPT_AUDIT.md;R22/FEEDBACK_TO_BUDDY.md|
|R19|F9 AIoT|R22|F2软件|T2最新官方精确版本/价格/商用许可/日期核验|R19 6抽2实错|R22≥5独立事实0实错|PENDING|ACTUALLY_INJECTED_NOT_VERIFIED|R19/CHATGPT_AUDIT.md;R22/FEEDBACK_TO_BUDDY.md|
- T1根因假设：远端临时工件未随报告交付。证伪：任一核心源码/输入/原始日志缺失或SHA不符。T2根因假设：仅核官网/旧公告而非当前具体条款。证伪：任何过期价格、版本、资格、许可证错误。
## SAME_FACTORY_REMEDIATION
|defect|R02→R12独立证据|R22注入动作|status|
|---|---|---|---|
|D1 P0|R12相对路径、未知mode、负预算、sandbox字符串、空rules五非法×2=10错误ACCEPTED|可信root/realpath/symlink、严格类型/枚举/预算、双模式≥10类负例|PENDING|
|D2 P0|R12 simulate()未校验、cleanup()信任自报_created_files；R02通配rm -rf危险|dispatch前统一门禁、可信归属、隔离清理、TTL/429/orphan负例|PENDING|
|D3 P1|R02 import=AGPL违规误断，R12商用许可无依据/源码字节未交付/扫描未执行|官方许可证行为矩阵、3正3负、完整MVE、成本公式|PENDING|
- R02 baseline=76, R12=65, R22 score=NOT_EVALUABLE；resolved_count/recurred_count/same_factory_score_delta均PENDING。五案例A–E逐项整改要求已逐字写入4590字符反馈且实际包含于4910字符submit prompt。
## 上一小时通用改进：计划→实际注入→实际效果→下轮调整
- 计划：R21缺证据，不捏造；由R19延迟迁移T1/T2，兼顾R20 OOM基础设施风险。
- 实际注入：Git反馈回读exact，MCP submit prompt包含全文，job=1b6feeaf3f514af1 running。
- 实际效果：PENDING / NOT_VERIFIED；等待正文、5事实抽查、MVE重放与五案例审计。
- 下轮R23 F3先追R22；只迁移经实测的通用方法，不把F2安全结论机械套用游戏领域。

## R22 FINAL｜两条反馈链的真实效果
- R21紧邻上一小时Git 404且最近MCP任务未见R21，R20 OOM；R19为最近可审计跨厂延迟基线。T1/T2实际全文注入Git回读的4590字符反馈和4910字符MCP prompt，唯一job=1b6feeaf3f514af1，但模型OOM失败，**T1/T2对Buddy研究的效果=INJECTED_NOT_VERIFIED**，不得声称改善。独立ChatGPT原型四份工件落Git并回读，是另一路自主执行证据，不可用来冒充Buddy落实T1。
- D1 P0 R12解析器五类fail-open：ChatGPT独立新原型14输入×2模式=28/28通过（其中26非法拒绝），**PARTIAL_PROTOTYPE_ONLY**；真实Buddy/OS边界未验证，P0仍开放。D2 P0可信清理归属未实现=NOT_VERIFIABLE；D3 P1许可证/真实scanner/成本未验证=NOT_VERIFIABLE；严格resolved=0/3，正式recurred_count=NOT_EVALUABLE（无Buddy新报告）。
- R22正式五维/同厂Δ=NOT_EVALUABLE，不能拿R12 65或独立原型28/28代替研究评分。机会筛选3个官方具体页核查、资格确认0、领取0，独立于质量评分。
- 下一轮R23 F3先只读核桥接daemon是否仍OOM；若健康HTTP200但任务推理失败，按唯一Job记录失败而不无限重复。跨厂可迁移方法仍是完整工件+官方现行条款，**本轮未通过Buddy效果验证**；游戏工厂另需独立读取R03/R13真实缺陷，不能用F2原型直接代替。
## CROSS_FACTORY_TRANSFER FINAL
|source_round|source_factory|target_round|target_factory|method_change|baseline_metric|target_metric|observed_metric|verdict|evidence_path|
|---|---|---|---|---|---|---|---|---|
|R19|F9|R22|F2|T1原始源码/输入/runner/日志/SHA可重放|R19 0/5核心工件可复算|Buddy MVE 1/1可重放|Buddy无报告，ChatGPT独立原型另行28/28通过|INJECTED_NOT_VERIFIED|R22/FEEDBACK_TO_BUDDY.md;R22/WORKBUDDY_FAILURE_RAW.md;R22/INDEPENDENT_SECURITY_PROBES.md|
|R19|F9|R22|F2|T2现行官方版本/价格/许可精确核验|R19 6抽2错|Buddy ≥5项0实错|Buddy 0项可抽；ChatGPT背景官方核验不计Buddy抽样|INJECTED_NOT_VERIFIED|R22/FEEDBACK_TO_BUDDY.md;R22/CHATGPT_AUDIT.md|
