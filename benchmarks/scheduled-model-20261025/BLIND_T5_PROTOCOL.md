# SCHED-CODE-20261025-BLIND-T5｜5分钟一次性盲测执行协议

## 指定任务与隔离
- 该实验通过**另一个全新 ChatGPT 对话**创建的**一次性定时任务**执行，非本协议作者代答。
- 调度：在新对话完成定时任务创建的实际时刻起 **5 分钟后仅触发一次**，Asia/Shanghai。不要使用本仓库历史 README 中的旧时槽。该协议不允许创造第二条任务，也不允许自动重试循环。
- 唯一权威仓库：`kaibahaha/xxsc`；Git 分支：`exp/scheduled-coding-blind-20261025`。绝不写 `main` 或 `exp/scheduled-coding-benchmark-20261025`。
- 读取题目（Git 路径）：
  `/benchmarks/scheduled-model-20261025/P01.md`
  `/benchmarks/scheduled-model-20261025/P02.md`
  `/benchmarks/scheduled-model-20261025/P03.md`
  `/benchmarks/scheduled-model-20261025/P04.md`
  公共测试：`/benchmarks/scheduled-model-20261025/public_tests.py`
- Git 交付目录（仓库根目录内路径）：`/results/scheduled-model-20261025/`
- ChatGPT Library 交付目录（云端库绝对路径，不是本地文件系统）：`/test/SCHED_CODE_BLIND_20261025/`
- 一次性独立实验 ID：`SCHED-CODE-20261025-BLIND-T5`。

## 无污染要求
当且仅当定时器在无人值守运行时，才读取四道题的完整内容；创建任务的聊天阶段不得读取题干、提前求解或手工创建答案。不可向先前设计题目的会话询问答案，不得调用 Codex、WorkBuddy 或任何其他大模型解题；Git 仓库中的其它历史任务与结果不可用作解答。尽量使用当前定时 ChatGPT 自身可用的代码执行工具；若无工具须如实报告。

## 本次运行的四题协议
执行时严格依次 P01/P02/P03/P04，独立完成各题的函数实现。每题优先完成**Git 代码提交、Git 回读、Git 独立报告**，再进行下一题。不能等待所有题都解决才提交，以免运行超时导致全部丢失。一题失败不妨碍下一题。原题和 public_tests.py 必须只读。

对每题 i：
1. 用 GitHub 授权连接器从**独立实验分支**读取对应 P0i.md 和测试，记录该题原始 blob SHA；若读取失败记录 READ_BLOCKED，不凭空生成答案。
2. 解题并编写 Python 3.11 标准库完整代码，提供规定的导出函数、输入校验、边界条件；输出的不是伪代码。
3. 有实际 Python 运行工具时运行对应 unittest；只有真实运行可报告 PASS。无法运行时 TEST_NOT_EXECUTED。允许使用非远程第三方模型的本地标准库运行，但不可通过外部解题服务变相委托。
4. 提交 Git `results/scheduled-model-20261025/P0i.py`，再提交 `results/scheduled-model-20261025/P0i_REPORT.md`。创建前检查同名是否已存在，已有文件绝不覆盖。记录每一次 create_file 的真实 commit SHA；写入后在同一 Git 分支独立 fetch_file 回读，记录 blob SHA。
5. 每道题在 Git 提交与回读后，立即把**源码全文、该题报告内容及真实 Git commit SHA / Blob SHA / 回读状态**组合成一个 UTF-8 Markdown 本地文件，通过 files__manage_library upload 到 `/test/SCHED_CODE_BLIND_20261025/P0i_DELIVERY.md`，再以 files__list（可行时 files__read）独立回读，保留真实 Library ID。不要等四题全完成才第一次尝试 Library 写入；单题 Library 失败应记录，不阻塞其它题。四道题的每份镜像分别是 P01_DELIVERY.md、P02_DELIVERY.md、P03_DELIVERY.md、P04_DELIVERY.md。文件已存在不覆盖、不换名规避，记录 ALREADY_EXISTS。
6. 每题报告必须包含：EXPERIMENT_ID、PROBLEM_ID、SCHEDULED_AT、STARTED_AT、COMPLETED_AT（均标北京时间+08:00并区分计划/实际）、SOURCE_PATH、SOURCE_BLOB_SHA、CODE_GIT_PATH、CODE_COMMIT_SHA、CODE_BLOB_SHA、CODE_READBACK、TEST_STATUS（带真实日志或 TEST_NOT_EXECUTED）、算法与复杂度、已知风险、MODEL_ID（若无可访问真实元数据写 MODEL_NOT_EXPOSED）、STATUS，禁止编造或把 Git 写入成功与代码测试通过混同。

## Library 总报告（必交）
执行接近结束时，新建一个 ChatGPT Library Markdown 文件：
`/test/SCHED_CODE_BLIND_20261025/SCHED_CODE_20261025_BLIND_T5_REPORT.md`。
使用当前工具实际生成 UTF-8 Markdown 文件，然后 files__manage_library upload，之后用 files__list 和尽可能 files__read 真正回读，记录 Library 的真实 ID、保存路径和状态，禁止只回复聊天文字就称入库。

该报告须独立记录已上传各题 Library 文件的真实 ID / 路径 / 回读状态；此总报告不代替逐题 Library 镜像。该报告包括：
- EXPERIMENT_ID、一次性触发计划时刻和实际开始/结束（Asia/Shanghai +08:00）、实际完成题数；
- 四题的逐题 SOLVE、TEST、GIT_WRITE、GIT_READBACK、完成时间、源 blob SHA、每次 commit SHA、最终完整文件路径；
- 每题生成的**源码全文**（代码围栏），即使 Git 不可写也要保留可审计原始交付；
- 逐题错误、不可访问权限、工具受阻和回退情况；禁止虚称提交成功。
如执行预算不足，也须尽力保留已完成题目的真实证据，不得伪造剩余题的完成。

## 结果核验与严禁行为
- Git 交付以 `create_file` 的真实回执与同路径 `fetch_file` 回读为准；Library 交付以 `files__manage_library` 实际上传+list/read 回读为准。源代码文件存在不等于它运行通过。
- 隐藏验收测试不在仓库中，由本次测试发起者事后独立运行；答题者不访问或猜测。
- 不得写旧分支、main、旧 A/B/C/D、WorkBuddy、旧生产结果、旧 Library 测试目录；不得覆盖、删除或修改任一现有文件。
- 不要向用户索要 PAT，也不能绕过连接器安全检查。
- 任一写入失败须报告 WRITE_BLOCKED 和原始错误，并在最终定时任务回复中粘贴未能落盘的源码及报告。
- 最终返回一张清晰的四题状态表及 Git/Library 的真实落盘凭证。未完成或无法核验部分用 UNKNOWN / FAILED / NOT_EXECUTED，不得估计为成功。

## 仓库文件网页绝对链接规则
分支根地址：https://github.com/kaibahaha/xxsc/tree/exp/scheduled-coding-blind-20261025
源码链接示例：https://github.com/kaibahaha/xxsc/blob/exp/scheduled-coding-blind-20261025/results/scheduled-model-20261025/P01.py
注意链接只有在该文件实际写入并回读后才作为完成凭据，不能因为本协议里有示例链接就称文件存在。
