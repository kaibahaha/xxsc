# R17 / F7 AI for Science科学研究工厂｜STATUS PENDING / QUEUED
- 实验 FACTORY10-SKILL-24H-20261030；固定计划北京时间2026-10-30 17:00（Phoenix 2026-10-30 02:00），第二圈F7，不改变24轮与工厂顺序。
- **交付契约**：已首先实际Git读取本分支README.md（blob 7c8e2a7ed21b22193d70db3cd0b14765dd9a86e6）。本轮派单前R17 STATUS/FEEDBACK/ADAPTATION/WORKBUDDY_REPORT/CHATGPT_AUDIT均404，且任务列表未见R17既有Job；无重复派单。
- **同厂纵向复盘**：已实际读取R07 STATUS、FEEDBACK、ADAPTATION；R07 WORKBUDDY_REPORT和CHATGPT_AUDIT均Git 404。唯一R07 Job 1941bb3a79e84c7f 经get_workbuddy_result回收约1309字摘要，声称完整报告及12工件仅存WorkBuddy私有路径 /home/workbuddy_agent/f7_r07_baseline/F7_R07_REPORT.md，尚未取得完整正文。标MISSING_BASELINE_FULL_TEXT；R07总分/五维及R07→R17 Δ、关键错误复发率均NOT_EVALUABLE，不虚构历史评分。五案例A文献地图/B泊松玩具/C分子PLAN_ONLY/D材料PLAN_ONLY/E科研治理已依据摘要逐案反馈。
- **历史追单**：R16 Job 7445121c541e4f63 经真实get_result返回远端daemon内存不足错误（232字），不是研究正文，状态FAILED_REMOTE_OOM；R14/R15历史均FAILED_NOT_SUBMITTED，未重派。近期完整审计R12/F2=83(21/19/17/16/10)、R10/F10=76(18/19/15/15/9)，仅继承通用方法。
- **反馈包已真实写入并回读**：R17 FEEDBACK_TO_BUDDY.md 2749字符，commit 1aecab09a24a0d76b08a4e345ac33db848912ce2，blob 56456a9bed921ae5b9e3725bfae3b5adbb663cc2，回读逐字PASS；包含四项P0/P1整改、R07五案例逐案反馈、MISSING_BASELINE限制和同厂比较指标。
- **方法包已真实写入并回读**：R17 ADAPTATION.md 719字符，commit 521427ff8f615789aaf544f5d3c8556eebb0ed89，blob 7fda7865423676a2c7082faa4797c7930bf5cd4a，回读逐字PASS；M1一手来源与时间戳、M2完整原文与可重放工件、M3权限/状态/回读分层。均已**完整嵌入**实际WorkBuddy MCP prompt，不只是Git链接。
- **唯一实际派单**：真实submit_workbuddy_task仅一次，conversation_id FACTORY10-SKILL-24H-20261030-R17-F7，prompt 4454字符（包含反馈2749字符及方法719字符），返回Job ID **7f44d8908f3f440b**。随后get_workbuddy_result(wait_seconds=0)显示通用[running]、0字，但list_workbuddy_jobs明确为**QUEUED/0字**，以列表区分队列与实际执行。未再次提交。
- **健康检查**：真实bridge_health HTTP200，版本 **3.4-candidate**，codebuddy_reachable=true，max_slot_seconds=2100，max_queue_wait_s=3600，max_queue_size=100，观测active_jobs=2/running_jobs=1/queued_jobs=1，unresolved_orphan_count=0、orphan_ledger_persist_ok=true。桥接健康不证明模型不再OOM；未切模型、未重启服务或更改生产。
- **研究结果**：PENDING/QUEUED，0字；WorkBuddy完整正文尚无，R17 WORKBUDDY_REPORT.md与CHATGPT_AUDIT.md不创建伪文件；评分NOT_EVALUABLE，整改与方法效果EVIDENCE_INSUFFICIENT。后续只按同一Job ID追单，取得完整报告才按25/20/20/20/15独立评分并与R07比较（若R07仍缺全文则标不可比）。
- **下一轮R18/F8**：先追R17唯一Job、补交原文/审计，若远端OOM/失败如实记终态；机器人方向只迁移证据、复现、权限方法，突出真机/仿真隔离、传感器校准、急停。禁止改动其他实验、插件安装/授权、模型切换、另建定时任务。
- **Git状态**：本STATUS和总账需分别提交与独立回读，commit回执与回读不可混淆。

## Git STATUS 独立回读确认
- 首次STATUS提交 b428b544003d4cf28b8efe7b13c135aa2622bfb2，随后fetch_file逐字一致、blob 6b5e11d68aef2a63a689d93432ec64065e932f57：PASS。后续若更新终态必须重新取当前blob SHA；本段更新本身仍以工具回执和下一次回读为准。

## R17后续真实结果核验（2026-10-30 北京时间约17:55）
- 本次首先重新读取README交付契约、R17 STATUS/FEEDBACK/ADAPTATION、同厂R07 STATUS并检查R17报告与审计仍Git 404；唯一已登记R17 Job为 `7f44d8908f3f440b`，**没有重复submit**。
- 实际调用WorkBuddy MCP `get_workbuddy_result(job_id=7f44d8908f3f440b,wait_seconds=0)`，原始结果为：`Error: Model request paused: the daemon is still out of memory after reclaiming unused memory, so this turn cannot be processed safely. The conversation history was preserved unchanged. Restart the app to free memory, then continue.`。独立`list_workbuddy_jobs`显示R17 `done 3s 232字`，但232字是错误信息而非研究报告，**业务终态 FAILED_REMOTE_OOM / NOT_EVALUABLE**，不是DONE_RESEARCH。0字有效正文。
- 同厂R07 Job `1941bb3a79e84c7f`再次实际get_result仍只返回约1309字摘要和WorkBuddy私有路径；完整原文/审计Git不存在。维持MISSING_BASELINE_FULL_TEXT；R07→R17评分差、五维差值、复发率均无法计算。
- 健康检查HTTP200、v3.4-candidate、codebuddy_reachable=true、running_jobs=1、queued_jobs=7、pending_queue_depth=7、unresolved_orphan_count=0、orphan_ledger_persist_ok=true。健康可达不代表模型可处理：R17实测OOM。
- R17已真实发送的反馈包和三项方法调整保留，因无有效研究正文，整改响应、五案例和方法有效性全部EVIDENCE_INSUFFICIENT；不得生成虚假的WORKBUDDY_REPORT.md或CHATGPT_AUDIT.md。后续R18应先检查真实Job与模型健康，若队列/模型持续故障仍记录状态，不切模型、不重启、不重复R17派单。
- 本轮只更新本实验分支R17 STATUS、ADAPTATION和迭代总账，均需各自写后独立Git回读；未改任何其他任务、分支、服务或权限。
