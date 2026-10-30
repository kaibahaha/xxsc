# R16 / F6｜跨厂方法自适应、效果验证与R17交接
本轮按README V2，固定北京时间2026-10-30 16:00 R16/F6。R06 Job 52441e82f15942ab 因429无正文，R06报告和审计404，MISSING_BASELINE，旧评分/Δ/复发率NOT_EVALUABLE。R14 Job e14a5a97707c4bbe 与R15 Job 29fae48b6c084d44 已通过MCP确认failed/not submitted/0字，非排队待完成；不重复派单。
近期有完整审计：R12/F2 83(21/19/17/16/10)、R10/F10 76(18/19/15/15/9)、R03/F3 83(20/19/16/16/12)。R12仍有Sim-E回读失败标done、headless权限歧义；R10法案地位误判且RUN源码不可取；R03模拟代码和原始日志不足。不同工厂分数不能证明改进因果。
## 三项且仅三项方法调整
M1 先证据后结论：观察R10法案时效错误、R12五维历史错映射→要求F6官方URL/DOI/时间戳、E0/E1/E2/E3、独立原始来源；指标≥12官方来源、≥10关键断言、0伪DOI/伪现行法律。下一轮R17验证实际来源有效率。
M2 原始工件与负例：观察R03/R10实跑自述缺完整源码、R12作者模拟未独立复跑→要求5案例固定输入、原始命令/响应/退出码、正反测试与BLOCKED标记；指标5/5十字段、0无工件REAL_EXECUTED。R17对比可复现比例。
M3 可信边界/权限/回读：观察R12回读失败仍done、跨Agent授权混淆→要求安装/授权/费用分层、Git提交与回读分离、假DOI/撤稿/权限拒绝负例；指标0伪授权、0未回读DONE、至少5个失败样本。
以上M1-M3已包含于R16 FEEDBACK_TO_BUDDY.md；仅在真实MCP submit成功后才标实际注入。R16未有完整报告前，效果=EVIDENCE_INSUFFICIENT，不虚构质量提升。
## R17交接
R17/F7 AI for Science：先追R16既有Job，若DONE先归档原文并独立审计；F7同厂R07只有约1309字摘要和私有路径，未得完整正文，须追取或标MISSING_BASELINE；只迁移证据分级、可复现工件、失败状态方法，不机械复制F6的商业研究案例。禁止安装、授权、付费、切模型、修改其他任务。
## 实际传递与状态回填
- R16 FEEDBACK先Git创建commit f192e50232a3225e8d1e02d4c2d096fc9d4363e4并独立回读PASS；ADAPTATION先创建commit 63970cb6465468115f34993313965a5606e6b746并独立回读PASS。
- WorkBuddy MCP Stable submit_workbuddy_task真实仅调用一次，conversation_id=FACTORY10-SKILL-24H-20261030-R16-F6；实际prompt 5367字符，全文包含3628字符反馈包及本文件1052字符方法计划，返回Job ID **7445121c541e4f63**。后续list_jobs具体QUEUED/0字；get_result通用running占位0字，不能将其当成已实际执行。M1–M3实际研究效果仍NOT_EVALUABLE。

## 最新质量闭环状态：远端OOM，研究不可评估
- 同一R16唯一Job 7445121c541e4f63 的get_result返回“Model request paused: the daemon is still out of memory after reclaiming unused memory”，list_jobs=done/232字错误文本；这不是完成报告。M1/M2/M3效果全部EVIDENCE_INSUFFICIENT，质量评分NOT_EVALUABLE，R06→R16 Δ不可计算。
- 下一轮仅继承研究方法，先核验MCP实际可执行性；若内存故障持续则记BLOCKED，不允许用模型切换、服务重启或额外任务伪造恢复。本轮不重复提交。
