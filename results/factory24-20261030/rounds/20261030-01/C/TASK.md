# C｜并发限流与熔断策略模拟平台

- Experiment: FACTORY24-20261030
- Round: 20261030-01 (Asia/Shanghai)
- Task ID: FACTORY24-20261030-20261030-01-C
- WorkBuddy job_id: `fb21843915d24025`
- State at dispatch: QUEUED (not completed)

## Functional specification

多租户固定/滑动窗口与令牌桶、可注入时钟、租户配额、公平性、幂等TTL、CLOSED/OPEN/HALF_OPEN熔断器、确定性失败注入、指数退避与种子PRNG抖动、权重后端选择、重试预算、JSONL可重放审计、CLI。测试边界、并发扣减、HALF_OPEN探针、时钟回退、幂等重复计费、重放一致性等。

## Acceptance and delivery

Python 3.11+标准库；独立工作目录 /home/workbuddy_agent/factory24_20261030/20261030-01/C/；至少6业务模块、40条真实unittest；可注入时钟、确定性故障注入、CLI；真实运行 python3 -m unittest discover -s tests -v 并记录退出码；完整src/、tests/、README.md、REPORT.md、TEST_RESULTS.txt、MANIFEST.md(SHA256)。不得读取密钥/生产配置，不得安装依赖。Git仓库 kaibahaha/xxsc，分支 exp/factory24-20261030，根路径 results/factory24-20261030/rounds/20261030-01/C/；要求推送实际代码及测试并回读核实；无Git授权则如实报告GIT_BLOCKED。目标35分钟内，不能假报通过。

## Verification note

This is the ChatGPT-issued task brief, **not source-code delivery**. Actual source/tests are pending WorkBuddy execution and independent verification.
