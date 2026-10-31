# R04 F4｜双轨预注册（派单前）
## CROSS_FACTORY_TRANSFER
| source_round | source_factory | target_round | target_factory | method_change | baseline_metric | target_metric | observed_metric | verdict | evidence_path |
|---|---|---|---|---|---|---|---|---|
| R03 | F3 | R04 | F4 | T1真实可复核工件：源码+fixture+原始日志+退出码+SHA | R03 1个Python工件独立重算，另4例多为方案 | R04≥1个可独立重算合成PNG探针，正文全文回传/Git回读 | PENDING | PENDING_TEST | rounds/R03/CHATGPT_AUDIT.md |
| R03 | F3 | R04 | F4 | T2 DOCUMENTED/ENV_PRESENT/EXECUTED/INDEPENDENTLY_VERIFIED分层 | R03 Node仅--version却称逻辑已运行 | 0无证据EXECUTED，≥90%关键断言官方URL或UNKNOWN，5/5负例/回滚 | PENDING | PENDING_TEST | rounds/R03/ADAPTATION.md |
- 两项必须真实注入WorkBuddy的submit prompt；不能仅在Git留文档。
## SAME_FACTORY_REMEDIATION
- 新实验R04首次F4 BASELINE，R14才同厂对比。旧实验R04原Job 5458b23070ac460c 429 FAILED_RATE_LIMIT，**无报告、无评分**；仅可作为历史失败参考，不得编造报告缺陷或已解决率。
- 历史研究缺口（非已证实内容错误）：P0完整交付、P1五案例实测缺失、P1版权/隐私/商用官方证据缺失、P2工具安装授权状态缺失；具体整改指令与五案例A-E逐案方案见本轮FEEDBACK_TO_BUDDY.md。
- 初始 same_factory_score_delta=NOT_COMPARABLE，defects_count=0（没有可审计旧报告），historical_gaps_count=4；效果待报告。
## NEXT
- R05 F5须根据R04真实审计最多迁移2项通用方法；不把合成PNG处理当作AI生成已成功。