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
## R06实际完成后的CROSS_FACTORY_TRANSFER（最终判定；上方PENDING为预注册历史）
|source_round|source_factory|target_round|target_factory|method_change|baseline_metric|target_metric|observed_metric|verdict|evidence_path|
|---|---|---|---|---|---|---|---|---|---|
|R05|F5|R06|F6|V1 数值/计费周期/算术门禁|R05 Opus周期错、Runway $15/min误算、Suno额度混淆|≥5项官方数值公式可复算且语义正确，0错误|Buddy5项算术自述、Opus纠正；Runway把网页订阅均摊价当API价并否定官方API $0.01/credit，Suno额度比值误当扣费|**PARTIAL_IMPLEMENTED / FAILED_FACT_ACCURACY**|rounds/R05/CHATGPT_AUDIT.md; rounds/R06/WORKBUDDY_REPORT.md §§2,11; rounds/R06/CHATGPT_AUDIT.md §§官方核验,迁移|
|R05|F5|R06|F6|V2 DOI结构/语义/版权分层|R05合成WAV16044B可复算但不能证明音质/权利|≥1真实DOI/无效DOI/撤稿，0证据越级，5案例状态标注|Nature原文撤稿及2014-07-02撤稿公告ChatGPT独立官网核实；Buddy OpenAlex HTTP200/404未附原始响应，Crossref updated-by未独立核实；论文原文发表日错一天|**PARTIAL_EFFECTIVE / FIELD_NOT_VERIFIED**|rounds/R06/WORKBUDDY_REPORT.md §§3-4,7; rounds/R06/CHATGPT_AUDIT.md|
- 实际注入：FEEDBACK_TO_BUDDY.md 4210字符、Git blob 064a435fd7462e3c975c9917c88d6cacaddd3295；WorkBuddy实际submit prompt 4686字符包含V1/V2完整内容与旧F6五项证据缺口。Job e8d1a46374fc4607 DONE 668s，MCP完整9622字符；Git报告blob 71e40f821e30c9ec732d8bf6c604e05710382514回读PASS，审计blob 498076ed41b44fe0bbaaa119128b0661c10a324d回读PASS。
## SAME_FACTORY_REMEDIATION 最终
- 旧实验F6 Job 52441e82f15942ab因WorkBuddy额度429失败，无正文/评分；same_factory_baseline_round=old R06 HISTORICAL_REFERENCE_ONLY，formal_old_content_defects=0，score_delta=NOT_COMPARABLE，old_error_recurrence=NOT_COMPARABLE。
- HIST-F6-01本轮交付缺口RESOLVED_DELIVERY_ONLY，HIST-F6-02~05四项PARTIAL。注意本轮Crossref GET 429不是旧WorkBuddy/模型额度429的同一故障，Buddy的“同源”主张属新P0事实错误。
- R16须核查：≥10条可追溯文献主张、至少1个完整API原始响应与冻结源码、18候选逐行完整清单、五案例至少1真实可独立复放、≤12检索、API与订阅价分开、429按服务归因。
## R07 F7下一小时强制继承（恰好两项）
**W1 [P0] 错误来源隔离。** R06报告将Crossref 9/10 HTTP429误称与旧WorkBuddy模型429同源；原因假设为仅按状态码归类忽略服务边界。F7需给服务名、endpoint、响应头/时间/配额层与重试规则，至少1个错误分类正反例，缺原始响应只能UNKNOWN；指标0次跨服务混因，0次把不同429认定同一根因。可证伪：把模型配额429与论文API429或插件授权403合并原因即失败。
**W2 [P0] 数值语义+可独立重放工件。** R06五项公式可算但Runway API与网页订阅混价、Suno配额比值误当扣费；远端列8个SHA却未回传文件。F7要求≥5项重要数值绑定官方URL/版本/单位/计费场景/公式/适用边界，至少1套完整源码+冻结输入+原始输出直接嵌入MCP正文；自述日志只标SELF_REPORTED。目标5/5算术及语义正确、≥1套独立复放、0将工件SHA自述冒充ChatGPT独立验收。可证伪：任何公式场景错配或缺可重放原文却称独立验证即失败。
- R06独立评分65/100 (17/17/12/11/8)仅为新F6基线，不可与R05 F5 73分跨厂作因果判断。