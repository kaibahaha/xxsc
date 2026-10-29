# 20261030-0432-R04-A｜确定性多租户TTL缓存与并发去重引擎

- 唯一任务名：`FACTORY24-20261030-20261030-0432-R04-A`
- 已接受 Job ID：`5669468a86524c07`，提交工具：`submit_workbuddy_task`。
- 题目类型：独立新题，非旧A/B/C恢复任务。
- WorkBuddy工作目录：`/home/workbuddy_agent/factory24_20261030/restart_20261030_0132/20261030-0432-R04/A/`。
- Git唯一交付位置：`kaibahaha/xxsc`，分支 `exp/factory24-20261030`，目录 `results/factory24-20261030/rounds/20261030-0432-R04/A/`。

## 功能与验收标准

使用Python3.11+标准库，至少6个业务模块：clock（可注入时钟与FakeClock）、policy（租户隔离容量与TTL）、cache（LRU/过期/线程安全）、singleflight（同key并发加载去重及异常广播）、stats（线程安全统计）、faults（确定性故障注入）。需要TTL=0/边界到期/时钟跳跃/租户隔离/并发加载/异常恢复/删除竞争等测试，至少40项独立unittest，要求实际执行`python3 -m unittest discover -s tests -v`并记录真实退出码。实现期间不能修改其他任务、服务或生产文件。

提交真实`src/`、`tests/`、`README.md`、`REPORT.md`、`TEST_RESULTS.txt`、`MANIFEST.md`（SHA256清单不自哈希），优先20分钟完成最小版本，30分钟内完成测试与Git提交，避免3600秒硬杀线。必须Git push并回读至少一个源码、一个测试、报告和清单，报告真实commit SHA；如不可达明确标GIT_BLOCKED。不得上传凭据或敏感数据。当前仅已提交作业，源码与测试仍PENDING。
