# R02 F2｜跨小时迁移与同厂历史整改预注册
## CROSS_FACTORY_TRANSFER
| source_round | source_factory | target_round | target_factory | method_change | baseline_metric | target_metric | observed_metric | verdict | evidence_path |
|---|---|---|---|---|---|---|---|---|
| R01 | F1 | R02 | F2 | M1完整研究正文回传MCP/Git，不只路径和摘要 | R01远端382行仅1517字摘要 | 100%正文可读、Git回读 | PENDING | PENDING_TEST | rounds/R01/CHATGPT_AUDIT.md |
| R01 | F1 | R02 | F2 | M2关键CLI/API官方版本与文档冲突核查；5/5案例负例+回滚 | R01案例全文不可读，无法验收 | 关键主张≥90%可核；5/5案例有负例回滚 | PENDING | PENDING_TEST | rounds/R01/ADAPTATION.md |

- 实际注入：上述M1/M2完整文本与六项F2历史缺陷、五案例整改已包含在submit_workbuddy_task prompt，Job 762c8f0887fc4188。
- 不能用R01 F1的NOT_EVALUABLE与旧F2的81分做跨专题分差。
## SAME_FACTORY_REMEDIATION
- 新实验R02为F2基线；同厂前次新实验R-10不存在。
- 历史参考：旧实验F2 R02，81/100 (22/18/16/15/10)，六项问题：工作区隔离≠安全隔离、headless权限过宽、GPL/AGPL一刀切、工具依赖缺失、供应链门禁无实测、商业优先级偏差。
- 要求WorkBuddy逐项回答并复盘五案例；所有解决状态PENDING，需ChatGPT独立核查。
- 后续R12 F2应以本轮新实验报告与审计作为正式同厂比较基线。
