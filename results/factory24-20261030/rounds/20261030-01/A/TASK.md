# A｜持久化租约调度器与崩溃恢复

- Experiment: FACTORY24-20261030
- Round: 20261030-01 (Asia/Shanghai)
- Task ID: FACTORY24-20261030-20261030-01-A
- WorkBuddy job_id: `9712edf966b54027`
- State at dispatch: QUEUED (not completed)

## Functional specification

状态机READY/LEASED/ACKED/FAILED/DEAD；可注入时钟、延迟优先级队列；lease fencing token、续租、超时回收；幂等键原子去重；CRC/JSONL事件日志、尾部截断恢复、checkpoint、重放；确定性退避、最大重试、DLQ；线程安全claim与CLI。测试并发claim、过期token、重启重领、断电窗口、幂等冲突、checkpoint不一致等。

## Acceptance and delivery

Python 3.11+标准库；独立工作目录 /home/workbuddy_agent/factory24_20261030/20261030-01/A/；至少6业务模块、40条真实unittest；可注入时钟、确定性故障注入、CLI；真实运行 python3 -m unittest discover -s tests -v 并记录退出码；完整src/、tests/、README.md、REPORT.md、TEST_RESULTS.txt、MANIFEST.md(SHA256)。不得读取密钥/生产配置，不得安装依赖。Git仓库 kaibahaha/xxsc，分支 exp/factory24-20261030，根路径 results/factory24-20261030/rounds/20261030-01/A/；要求推送实际代码及测试并回读核实；无Git授权则如实报告GIT_BLOCKED。目标35分钟内，不能假报通过。

## Verification note

This is the ChatGPT-issued task brief, **not source-code delivery**. Actual source/tests are pending WorkBuddy execution and independent verification.
