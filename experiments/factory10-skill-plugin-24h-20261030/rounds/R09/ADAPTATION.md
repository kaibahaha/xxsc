# R09 F9 AIoT智能硬件｜动态RSI方法调整与交接
- 类型：首圈 BASELINE，F9无同厂历史，R19才能同厂复盘。已读README V2、ITERATION_LEDGER、R07/R08 STATUS、R08 ADAPTATION及R01–R03评分记录；R01 70/100、R02 81/100、R03 83/100均为不同工厂，不作因果Δ。
- 最近可评价的完整审计仍是R03/F3 83/100（20/19/16/16/12）。R04–R06真实429失败；R07仅1309字摘要和私有路径，无Git完整正文；R08最新MCP get_result返回 **[task failed] 任务尚未提交到CodeBuddy，status=None**，队列显示failed/0字；R08不是完成研究。方法有效性尚无新证据。
- R09已实际Git创建并回读 FEEDBACK_TO_BUDDY.md（blob 86bf1f4a820e4435a8f6ff5411cf1fa4ffbcf127），且将**全文**内嵌真实submit_workbuddy_task的prompt，conversation_id FACTORY10-SKILL-24H-20261030-R09-F9，Job a178c0e82f10461d。
## 仅三项可检验跨厂方法
| 方法 | 观察到什么→原因假设 | 实际注入R09 prompt的改变 | 验证指标 | 结果 |
|---|---|---|---|---|
| M1 证据与工件双轨 | R03自述“完整代码”缺源文件、R07仅私有路径→工具可发现与可重放混淆 | 官方来源≥10、Top5命令help/manifest、RUN必须含最小代码/固定输入/stdout/exit code；完整报告必须直接返回MCP文本 | ≥10一手来源、无工件RUN断言=0、Git完整原文可读 | R09仍排队，PENDING |
| M2 物理/网络安全分层 | R02 worktree隔离误判、R03 SHA防篡改误判→演示成功被误作安全认证 | 明确仿真/真机、TLS设备身份、MQTT QoS/幂等、OTA签名与A/B回滚、≥5负例，禁止真机 | ≥5故障/攻击负例、0仿真=认证或SHA=签名断言 | PENDING |
| M3 五案例完整验收 | R01缺负例、R02未运行、R03输出结构不一致→缺输入输出闭环 | 五个AIoT案例逐项固定输入、CLI/API、工件、正反测试、阈值、成本/权限、回滚、RUN/PLAN/BLOCKED | 5/5案例字段完整、至少一个不依赖真机的可复现工件 | PENDING |
## 下一轮R10交接
先追R09唯一Job a178c0e82f10461d，不重复submit。若返回完整报告则做100分固定五维独立审计、五案例点评和反馈响应表；若仅摘要/私有路径则NOT_EVALUABLE。R08任务已经失败且无正文，不要继续标QUEUED；不擅自补派R08。R10/F10小说叙事只迁移方法：证据与实际产物、版权/授权边界、五案例可测验收，不能机械复制AIoT内容。所有调整效果需要后续1–3份完整报告才可判断。
