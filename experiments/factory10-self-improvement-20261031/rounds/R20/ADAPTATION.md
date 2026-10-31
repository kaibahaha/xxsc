# R20 F10｜双轨方法迁移预登记
- 本轮已真实向WorkBuddy唯一job 64dbae92e31d4b05 提交5759字符prompt，逐字包含Git回读的FEEDBACK_TO_BUDDY.md 5508字符。此为注入证据，不是效果证据。
## CROSS_FACTORY_TRANSFER
|source_round|source_factory|target_round|target_factory|method_change|baseline_metric|target_metric|observed_metric|verdict|evidence_path|
|---|---|---|---|---|---|---|---|---|---|
|R19|F9 AIoT|R20|F10 小说叙事|U1 RUN必须交完整源码/冻结输入/runner/原始stdout stderr/SHA并可独立重放|R19独立0/5核心工件可复算|R20核心MVE≥1/1字节齐全且独立重放成功|PENDING|INJECTED_NOT_VERIFIED|R19/CHATGPT_AUDIT.md;R20/FEEDBACK_TO_BUDDY.md|
|R19|F9 AIoT|R20|F10 小说叙事|U2最新官方有效条款与时间/地区/版本/计费单位核对|R19 6抽2实错（RPi5旧价、Zephyr旧版）|R20≥5官方高影响事实0实错，过期候选0|PENDING|INJECTED_NOT_VERIFIED|R19/CHATGPT_AUDIT.md;R20/FEEDBACK_TO_BUDDY.md|
- U1根因假设：远端/tmp工件与Git报告脱节；证伪：源码/输入/runner/输出任一缺失或SHA不符。U2根因假设：只核官网域名而忽略发布时间和具体SKU/服务存续；证伪：任何失效产品被列现行或过时价目覆盖新官方页。R19行业内容和总分不用于F10质量因果。
## SAME_FACTORY_REMEDIATION
|defect|R10真实独立证据|R20指令与验收|observed|status|
|---|---|---|---|---|
|D1 P0|source=true和自报授权source字符串可exit0 VALID，真实版权未经第三方核验|受信授权记录/作品哈希/范围/到期/撤销/伪造签发负例；0错误放行、0副作用|PENDING|NOT_VERIFIABLE|
|D2 P1|R10源码SHA两种结尾均≠Buddy自述；8 JSON与runner缺字节|核心MVE完整源/输入/runner/原始输出与SHA；独立重放≥1|PENDING|NOT_VERIFIABLE|
|D3 P1|R10 30独立测试14符合预期、16失败，空章节/重复ID/年龄矛盾等exit0|R10八类相邻探针全覆盖，≥10类×normal/-O，0 fail-open/0未捕获异常|PENDING|NOT_VERIFIABLE|
- same_factory_baseline_round=R10, baseline_score=62(16/18/12/8/8), same_factory_defects_count=3, resolved_count=PENDING, recurred_count=PENDING, same_factory_score_delta=NOT_EVALUABLE。
## 上一小时通用改进：计划→实际注入→实际效果→下轮调整
- U1/U2均完整写入Git反馈且逐字进入实际MCP；本轮报告未到，效果NOT_VERIFIED；下一轮R21 F1继续核验跨厂事实/工件指标并读取F1 R01/R11同厂历史，不能套用F10行业内容。
- 仅调整研究方法/委托提示词，不改变计划、评分、分支、路径、权限。


## R20 FINAL｜真实OOM故障与两条反馈链收口（2026-11-01）
- WorkBuddy唯一job 64dbae92e31d4b05 实际FAILED/285s，get_workbuddy_result原始错误“CodeBuddy daemon ... out of memory after reclaiming unused memory”；不是429/超时/队列拥塞。bridge postflight HTTP200 reachable=true、running=0 queued=0、unresolved_orphans=2（历史），不能从HTTP健康推断daemon推理可用。未重派、未重启、未切模型。
- U1/U2跨厂：Git反馈5508字符写后回读，MCP实际5759字符prompt包含完整反馈；由于OOM无正文，observed_metric=NOT_EVALUABLE、verdict=INJECTED_NOT_VERIFIED。不能把F9的2/6事实错与F10没有报告作改善比较。
- D1/D2/D3同厂：均已逐字委派；报告未生成，状态全部NOT_VERIFIABLE，resolved_count/recurred_count/score_delta均NOT_EVALUABLE。R10 62分继续作为正式基线，历史P0未关闭。
- 独立机会预筛：Reedsy 2026明确禁止AI生成书稿、IFComp2026人类可见内容限制、Unity允许AI但需披露；仅官方公开规则研究，0真实注册/资源到账；Git OPPORTUNITY_RADAR/ACTION_CHECKLIST/OPPORTUNITY_LEDGER已回读。机会筛选不能代替MVE质量分。
- 下一轮R21必须先做只读桥接健康+最小安全可用性判断，关注OOM可能持续；不得重派R20，不得未经授权重启CodeBuddy/改模型/改生产。继续固定F1第三轮R01/R11演化审计，若推理不可用记录实际故障并保全Git，不把失败当质量改善。
## CROSS_FACTORY_TRANSFER FINAL
|source_round|source_factory|target_round|target_factory|method_change|baseline_metric|target_metric|observed_metric|verdict|evidence_path|
|---|---|---|---|---|---|---|---|---|---|
|R19|F9|R20|F10|U1完整原始字节工件与SHA链|R19 0/5核心文件可复算|R20 ≥1/1可独立重放|无Buddy报告，未运行|INJECTED_NOT_VERIFIED|R20/FEEDBACK_TO_BUDDY.md;R20/WORKBUDDY_FAILURE_RAW.md;R20/CHATGPT_AUDIT.md|
|R19|F9|R20|F10|U2当前官方具体条款、日期/地区/版本|R19 6抽2实错|R20 ≥5抽0错|无Buddy事实可抽；ChatGPT独立背景核查7项不计Buddy抽样|INJECTED_NOT_VERIFIED|R20/FEEDBACK_TO_BUDDY.md;R20/CHATGPT_AUDIT.md|
