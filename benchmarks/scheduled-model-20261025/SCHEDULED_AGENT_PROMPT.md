# 单条定时任务执行指令（四次触发，各领一题）

这是对“当前 ChatGPT 定时任务实际推理与工具能力”的无人协作测试，不是给 WorkBuddy/Codex 派单。严格遵守如下不变参数：
- GitHub repo: kaibahaha/xxsc
- Git branch: exp/scheduled-coding-benchmark-20261025
- 题目入口: benchmarks/scheduled-model-20261025/README.md
- 题目文件: benchmarks/scheduled-model-20261025/P01.md / P02.md / P03.md / P04.md
- 测试脚本: benchmarks/scheduled-model-20261025/public_tests.py
- 交付目录: results/scheduled-model-20261025/
- 时区: Asia/Shanghai
- 执行时槽: 2026-10-25 10:20 => P01；11:20 => P02；12:20 => P03；13:20 => P04。
- 不得调用其他 Agent 或外部大模型协助；不得阅读该测评目录外的项目代码来抄答案。

每次自动唤醒时：
1. 从调度轮次对应的北京时间时槽确定**唯一题号**（不要扫描旧的 A/C/D 派单）。对于任务运行延迟，仍按原定时槽映射。若无法确定轮次，先查四个结果文件，按 P01、P02、P03、P04 找第一个尚无 P0x.py 的题；如四题都有结果，报告 COMPLETED 后停止。本机制仅用于本测试。
2. **实际使用 GitHub 连接器**读取 README、对应 P0x.md 和 public_tests.py；不能成功读取则报告 READ_BLOCKED，不得凭空回答。
3. 不调用 Codex、WorkBuddy、其他 Agent 或模型。不复制其它任务的解答。独立推理、实现 Python 3.11 标准库函数，并验证基础样例。优先保证数据结构、边界处理、时空复杂度；如果具备真实代码执行工具，运行当前题目对应公共测试并留日志；若不具备，明确 TEST_NOT_EXECUTED。
4. 使用 GitHub 文件写入工具创建 `results/scheduled-model-20261025/P0x.py`，内容必须为完整可直接运行的 Python 源码。提交前先查已有文件，禁止覆盖。写入若失败，回复中完整给出源码并记录 WRITE_BLOCKED；不要伪造 commit。
5. 写入 `results/scheduled-model-20261025/P0x_REPORT.md`，记录：题目名称、运行时槽、实际执行时间、读取结果、简要算法说明、公开测试真实执行情况、GitHub commit SHA、回读是否成功、异常；不要声称有内部模型标识，若不可获取写 MODEL_NOT_EXPOSED。
6. 对已创建的每个文件，必须同分支同路径重新 fetch/read 并确认内容；如报告自身还未创建不要伪称已回读。若无法提交报告或回读，回复中报告具体失败。
7. 最终回复格式：`SLOT | PROBLEM | READ | SOLVE | TEST | GIT_WRITE | GIT_READBACK | SHA | MODEL_LABEL_AVAILABLE`，附官方 GitHub 文件路径及未解决问题。不要把“模型解出题”与“写入连接器成功”混为一谈。

若时间超过最后一个时槽，不得重置提交结果；不重试已完成题目、不修改历史、不触碰仓库的其他路径。
