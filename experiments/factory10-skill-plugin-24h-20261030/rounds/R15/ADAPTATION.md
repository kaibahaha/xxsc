# R15 / F5｜自适应研究与R16交接
本轮真实同厂基线：R05 Job `6f4057fc78094c63` 因429返回错误，无WORKBUDDY_REPORT或CHATGPT_AUDIT，R05五维/总分NOT_EVALUABLE；不能计算R05→R15质量Δ。已读R05 STATUS/FEEDBACK/ADAPTATION。最近有完整独立审计的R03 83分、R10 76分；R12原始报告已通过MCP取得但尚未独立评分，不把其自测当外部验证。桥接器本次HTTP200/v3.3，最大并发1，active_jobs=1；R11/R13失败，R14补派Job另记。
## 最多三项可检验方法
M1 来源/授权矩阵：R10法案草案误称现行法、R05无来源正文→F5每项政策/价格必须有官方URL+访问日期+适用国家，安装/授权/可用性分层；指标≥8可核关键主张、0无证据已装/商用断言。
M2 复现工件：R03缺完整日志、R05五例仅计划→每案例有固定输入、命令/操作来源、文件清单、正负测试、费用/回滚、REAL_EXECUTED/DOC_VERIFIED/PLAN_ONLY/BLOCKED；指标5/5完整、0假执行。
M3 发布/版权负例：R05无合规结果、R10法律时效错误→五例权利矩阵、平台差异与人工审批；指标五例各≥1真实可执行负例，0未授权发布。
这三项已写入FEEDBACK，实际WorkBuddy prompt须完整包含本反馈；R15尚未有正文时效果标EVIDENCE_INSUFFICIENT，不预填评分。R16 F6应先查R06同厂429失败并标MISSING_BASELINE，再将M1–M3方法改写为学术来源、DOI/撤稿、数据授权和报告版本控制，不机械复制音视频业务。
## 实际MCP传达与效果状态
- WorkBuddy MCP Stable真实`submit_workbuddy_task`仅一次，Job ID `29fae48b6c084d44`；conversation_id `FACTORY10-SKILL-24H-20261030-R15-F5`；实际prompt共3649字符，完整嵌入本轮`FEEDBACK_TO_BUDDY.md`全文及本ADAPTATION方法要求，不仅是Git链接。
- 实际`get_workbuddy_result`仅通用[running]/0字；独立`list_workbuddy_jobs`显示queued/0字，故M1–M3的实际效果**NOT_EVALUABLE**。下一轮按Job ID追单，报告未完成不打分、不虚构改善。
