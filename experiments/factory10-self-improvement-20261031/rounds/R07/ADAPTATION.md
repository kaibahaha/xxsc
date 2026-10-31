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
## R07实际完成后的CROSS_FACTORY_TRANSFER（最终判定；上方PENDING为预注册历史）
|source_round|source_factory|target_round|target_factory|method_change|baseline_metric|target_metric|observed_metric|verdict|evidence_path|
|---|---|---|---|---|---|---|---|---|---|
|R06|F6|R07|F7|W1 服务级错误归因|R06 Crossref API429误认WorkBuddy模型429同源|跨服务混因0、至少1错误分类正反例，真实响应需headers|Buddy给服务级正反例，概念上不混因；未触发真实429/403，header=UNKNOWN|**PARTIAL_IMPLEMENTED / REAL_ERROR_HANDLING_NOT_VERIFIED**|rounds/R06/CHATGPT_AUDIT.md; rounds/R07/FEEDBACK_TO_BUDDY.md; rounds/R07/WORKBUDDY_REPORT.md §A W1; rounds/R07/CHATGPT_AUDIT.md|
|R06|F6|R07|F7|W2 数值语义与原始工件双验|R06 8工件只给SHA、API/Web订阅混价|≥5数值语义正确、≥1完整源码+冻结输入+stdout独立复放|Case B代码和输入交付、独立数值复放PASS，但源码SHA与报告不符、stdout一行不符，砷基细菌DOI错误，单位负例只打印未阻断|**PARTIAL_EFFECTIVE / FAILED_ARTIFACT_INTEGRITY_AND_FACT_ACCURACY**|rounds/R06/WORKBUDDY_REPORT.md; rounds/R07/WORKBUDDY_REPORT.md §3 Case B; rounds/R07/CHATGPT_AUDIT.md|
- 实际注入：FEEDBACK_TO_BUDDY.md 4210字符，Git blob 2790f631d6e6b89fc2924fbab8c4c748b4bbe0a3，WorkBuddy submit prompt 4695字符逐字包含反馈。Job c20368ab43794a78 DONE 372s/19114字符；Git报告blob 4763ad29eeb654d3ed247c25dca095ce94072e08回读PASS，独立审计blob dedbe365cf57cc77380a4fb504340282266d2ec3回读PASS。
## SAME_FACTORY_REMEDIATION最终
- 旧F7仅摘要，无Git旧全文/独立评分；same_factory_baseline_round=old experiment R07 HISTORICAL_REFERENCE_ONLY，formal_old_content_defects=0，historical_evidence_delivery_gaps=5，old_score_delta=NOT_COMPARABLE，old_error_recurrence=NOT_COMPARABLE。
- HIST-F7-01 RESOLVED_DELIVERY_ONLY，HIST-F7-02~05 PARTIAL（Buddy自评全RESOLVED不接受）。本轮新正式F7基线 **68/100 (17/17/13/13/8)**，供R17同厂比较。
- 本轮最重要反例：原论文DOI错误（正确10.1126/science.1197258）、Git源码SHA不等于自报SHA、stdout含未由源码打印的文本、单位错未真正阻断、泊松p值零假设未明确、OpenAlex配额/RDKit命令/Skill数量缺版本核对。
## 下一小时R08 F8两项强制方法迁移
**Q1 [P0] 工件字节级完整性**。R07报告Case B源码无末尾换行SHA c3fdc971a2f492c5d88439f1f84cd68e856210b9fa76df79430efcff2bfe708b，加末尾换行SHA 6ece596a93d4df7c717d9ef5748e6e6d819835a9886742b8cfe59a044ebf43ab，均不等于Buddy自报64fab3a0122aba1239f7fcae9d3a991a26b53d3afd00ae84b8c07cd892298dbb；stdout也多了“(0<=p<=1)”。成因假设：远端运行文件与报告嵌入代码版本漂移/输出人工改写。R08 F8必须把实际执行的完整仿真源码、冻结输入、原始stdout/exit码按字节锁定，ChatGPT独立提取重放；目标SHA一致1/1、stdout逐字一致1/1，任一不符判FAILED_ARTIFACT_INTEGRITY。
**Q2 [P0] 权威标识核验与真实负例门禁**。R07砷基细菌原论文DOI误写为10.1126/science.332.1163，正确10.1126/science.1197258；单位错误仅print blocked并未validate。成因假设：将页码当DOI、将文字演示当实际阻断。R08 F8至少3个关键硬件型号/传感器单位/API接口必须由官方精确URL核验，至少2个安全负例由真正assert/结构化错误/非零退出触发；目标官方标识错误0、负例实际阻断≥2。可证伪：任何错误型号/虚构API或仅print blocked即失败。只限安全仿真，不操作实体机器人。
- 上一小时通用改进：计划→实际注入→实际效果→下轮调整：R06 W1/W2已注入R07，效果部分；R08再测Q1/Q2。跨厂总分不作因果比较。
