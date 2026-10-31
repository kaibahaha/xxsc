# R20 F10｜真实MCP失败原文（非WORKBUDDY_REPORT）
- unique_job_id: 64dbae92e31d4b05
- submit_workbuddy_task: 已提交；唯一job_id=64dbae92e31d4b05
- get_workbuddy_result 最后返回（原样，未经修订）：

```text
[task failed] 远端内存不足（CodeBuddy daemon 主动暂停本轮推理）；不是超时也不是队列堵塞，需重启 codebuddy 或缩小任务
job_id=64dbae92e31d4b05 status=completed

已收到部分内容：
Error: Model request paused: the daemon is still out of memory after reclaiming unused memory, so this turn cannot be processed safely. The conversation history was preserved unchanged. Restart the app to free memory, then continue.
```

- interpretation: TOOL_JOB_FAILED_OOM；没有BEGIN_FULL_REPORT/END_FULL_REPORT正文；不得建立虚构WORKBUDDY_REPORT.md、不得评分、不得宣称已完成研究。按唯一轮次去重规则，不重派R20；下一轮只做只读健康/队列/孤儿检查，若CodeBuddy仍OOM则报告并限制派单，不得擅自重启/切换模型/更改生产配置。
