# B｜可增量解析的策略DSL与安全执行引擎

- Experiment: FACTORY24-20261030
- Round: 20261030-01 (Asia/Shanghai)
- Task ID: FACTORY24-20261030-20261030-01-B
- WorkBuddy job_id: `a154efd28abc4eb5`
- State at dispatch: QUEUED (not completed)

## Functional specification

Lexer/Pratt parser/AST/类型检查/常量折叠/三值逻辑/资源预算安全解释器/版本缓存/CLI。DSL：rule <name> priority <int> when <expr> then allow|deny|review；deny优先，同优先级稳定。测试畸形输入、优先级、转义、未知字段、短路、资源预算、注入字符串、缓存失效、行列号等。

## Acceptance and delivery

Python 3.11+标准库；独立工作目录 /home/workbuddy_agent/factory24_20261030/20261030-01/B/；至少6业务模块、40条真实unittest；可注入时钟、确定性故障注入、CLI；真实运行 python3 -m unittest discover -s tests -v 并记录退出码；完整src/、tests/、README.md、REPORT.md、TEST_RESULTS.txt、MANIFEST.md(SHA256)。不得读取密钥/生产配置，不得安装依赖。Git仓库 kaibahaha/xxsc，分支 exp/factory24-20261030，根路径 results/factory24-20261030/rounds/20261030-01/B/；要求推送实际代码及测试并回读核实；无Git授权则如实报告GIT_BLOCKED。目标35分钟内，不能假报通过。

## Verification note

This is the ChatGPT-issued task brief, **not source-code delivery**. Actual source/tests are pending WorkBuddy execution and independent verification.
