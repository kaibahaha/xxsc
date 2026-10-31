# R07 F7｜派单前双轨自我改进预注册
- planned_at: 2026-10-31 16:25 Asia/Shanghai；R07本实验F7首次正式BASELINE。旧实验F7 Job 1941bb3a79e84c7f仅1309字摘要，无可读完整报告/审计；SAME_FACTORY_BASELINE_MISSING，旧内容缺陷数=0，历史交付/证据缺口=5。
- R06 F6 job e8d1a46374fc4607 DONE，完整报告和独立审计Git回读PASS，评分65/100(17/17/12/11/8)仅F6基线，不作跨厂因果分数比较。
## CROSS_FACTORY_TRANSFER
|source_round|source_factory|target_round|target_factory|method_change|baseline_metric|target_metric|observed_metric|verdict|evidence_path|
|---|---|---|---|---|---|---|---|---|---|
|R06|F6|R07|F7|W1 服务级错误归因|R06把Crossref API429与WorkBuddy模型429误称同源|跨服务混因0次，≥1正反错误归因示例|PENDING|PENDING_TEST|rounds/R06/CHATGPT_AUDIT.md; rounds/R07/FEEDBACK_TO_BUDDY.md|
|R06|F6|R07|F7|W2 数值语义与原始工件双验|R06 Runway API/网页订阅混价，Suno额度误释，8个远端工件只给SHA|≥5项科学/成本数字语义及算术双验；≥1完整源码+冻结输入+stdout可复放|PENDING|PENDING_TEST|rounds/R06/WORKBUDDY_REPORT.md; rounds/R06/CHATGPT_AUDIT.md; rounds/R07/FEEDBACK_TO_BUDDY.md|
- 假设：W1按服务层记录可消除同码误归因；W2强制交原始工件及单位场景可降低“公式正确结论错误”。反证：本轮任一跨服务同源误判、任何错配单位/场景、无源码却宣称独立复现。
## SAME_FACTORY_REMEDIATION
- 旧F7仅历史摘要，不能审计内容与评分；HIST-F7-01~05为有证据的交付/证据缺口，不是旧正文内容错误。要求完整MCP正文、10条科学主张、科学有效性/负例、五案例、15候选及Top5官方核验。
- 先Git写FEEDBACK并逐字回读，再把反馈全文注入唯一WorkBuddy submit prompt；本轮返回后分别审计两条反馈链。R17使用本轮正式评分作同厂纵向基线。
## 下一轮预留
- R08 F8只从R07真实审计中迁移最多2项通用研究方法，不套用F7行业结论。若本轮PENDING须先追同一job，标DELAYED_BASELINE，不重派。