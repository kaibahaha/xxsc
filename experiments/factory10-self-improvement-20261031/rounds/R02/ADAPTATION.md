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

## R02实际审计后的 CROSS_FACTORY_TRANSFER（完成判定）
| source_round | source_factory | target_round | target_factory | method_change | baseline_metric | target_metric | observed_metric | verdict | evidence_path |
|---|---|---|---|---|---|---|---|---|
| R01 | F1 | R02 | F2 | M1全文回传+Git回读 | 远端382行、MCP仅1517字摘要 | 全文100%可读且Git回读 | R02 MCP15843字符；Git16123字符逐字回读，blob f77061fc03d218c782960342e78adde3a0c9fd28 | **EFFECTIVE_DELIVERY** | rounds/R02/WORKBUDDY_REPORT.md；CHATGPT_AUDIT.md |
| R01 | F1 | R02 | F2 | M2官方版本+五案例负例回滚 | R01案例全文不可见 | 5/5字段完整，关键主张≥90%准确可追溯 | 5/5含负例回滚；但headless模式/许可义务/扫描样本有未解决错误，≥90%准确性不可独立证明 | **PARTIAL_EFFECTIVE / ACCURACY_NOT_PROVEN** | rounds/R02/CHATGPT_AUDIT.md |

- WorkBuddy实际任务Job 762c8f0887fc4188 DONE，463秒，最终MCP响应完整回传；Git报告commit 55ee23289ea9d6905846548801277e5bfa2475ae，审计commit ea6c8ba83df83a1f1ad9dd6e3887aae1686e5216。
- ChatGPT独立评分76/100（证据21、战略18、技巧14、五案例14、风险9）。此为新实验F2基线；旧实验F2的81/100只作历史参考，不宣称同厂同比下降5分。
## SAME_FACTORY_REMEDIATION 独立结果
- historical_source: old experiment R02 F2, 81/100, six defects.
- WorkBuddy自评六项全RESOLVED；ChatGPT复核**2 RESOLVED（概念/披露层）+4 PARTIAL，0直接复述旧错误，4组新增细节缺陷**。详情见CHATGPT_AUDIT.md。
- 下一次同厂R12须验证权限命令真实拒绝、许可证场景矩阵、门禁样本规则/退出码、沙箱实际可用性与危险回滚替代方案。
## R03 F3跨厂方法移交
- M1证据强度分层：官方存在/本机安装/实际执行/独立验收；≥90%关键主张有可核URL与适用版本，不能把“已生成游戏素材/脚本”当“引擎运行/发布”。
- M2五案例反例质量：5/5输入输出/负例/回滚/权限/成本/运行状态；至少一个真实可复现的只读命令或确定性随机种子测试，未运行标NOT_TESTED。
- R03须从本文件和CHATGPT_AUDIT.md读取实际问题并注入WorkBuddy，不能只复制Git链接。
