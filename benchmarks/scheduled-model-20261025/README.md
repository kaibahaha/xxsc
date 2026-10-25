# ChatGPT 定时任务独立编程能力测评 / 2026-10-25

benchmark_id: SCHED-CODE-20261025
repository: kaibahaha/xxsc
branch: exp/scheduled-coding-benchmark-20261025
question_dir: benchmarks/scheduled-model-20261025/
result_dir: results/scheduled-model-20261025/
language: Python 3.11+ 标准库
status: READY
timezone: Asia/Shanghai

## 测试目的
验证 ChatGPT 网页版定时任务能否在没有交互帮助的条件下，从指定 Git 分支读取题目、独立实现、提交可执行源码、回读核验，并通过确定性测试。**不能由答题能力反向认定底层模型精确型号或推理档位。**

## 固定任务及顺序
1. P01.md — 半开时间窗合并（数据结构、边界与去重）；建议难度 2/5。
2. P02.md — 乱序订单事件重放（幂等、版本裁决、异常输入）；建议难度 3/5。
3. P03.md — 有容量约束的依赖作业分波调度（DAG、确定性贪心）；建议难度 4/5。
4. P04.md — 向量时钟冲突汇聚（偏序、因果覆盖、并发裁决）；建议难度 5/5。

每道题都要求写入一个**真正可执行**的 Python 文件，不接受只有文字、伪代码、结论或仅编写报告。所有测试均不允许网络访问，不依赖三方包。不要调用其他 Agent、Claude、Codex、WorkBuddy 或外部解题接口协作；此处测量当前被调度模型自身的能力。

## 读写协议（仅针对本测评，不影响现有 A/C/D 队列）
- 先读取本 README、对应 P0x.md、public_tests.py；严格按题目函数名、参数和返回值实现。
- 只写 result_dir 下两个文件：P0x.py（完整 Python 源码）和 P0x_REPORT.md（执行报告）。不得修改题目、公开测试、其它 Agent 队列或旧结果。
- 创建前检查路径是否存在；存在则只读核实并报告 ALREADY_SUBMITTED，禁止覆盖。
- 只使用 GitHub 连接器真实返回确认状态；写入后同分支同路径回读，并在报告里记录 commit SHA、回读状态。失败就标记 WRITE_BLOCKED，不得伪造。
- 报告必须包含：题号、开始/结束北京时间、实际读到的 Git 路径、实现摘要、逐项测试结果（只有真正执行过才写 PASS）、异常/边界分析、提交 commit SHA/回读、未解决问题。
- 如果该轮没有执行代码的工具，提交代码并标记 TEST_NOT_EXECUTED；不得把“人工检查通过”写成自动运行通过。
- 若联网读取失败：标记 READ_BLOCKED，不以常识编造题目。若代码已生成但写入受阻，把源码完整放在定时任务运行回复中，以免丢失。

## 公共测试
若具备 Python 运行环境，在仓库根目录执行：
```bash
python -m unittest discover -s benchmarks/scheduled-model-20261025 -p public_tests.py -v
```
公开测试只覆盖基础边界；最终评估另使用不放在 Git 仓库内的保留测试，防止直接针对测试用例硬编码。无执行条件时不得声称已通过。

## 评估维度
每题满分 25 分：读取与任务理解 4，代码与正确性（含保留测试）15，输入校验与复杂度 3，提交回读与真实报告 3。四题累计 100。单独记录三个非同义指标：
- SOLVE: 算法是否正确；
- RUN: 是否能实际执行并提供可复现证据；
- GIT: 是否能成功原生读写、取得真实 commit 和回读。
不要把 Git 接入故障算作模型算法错误，反之亦然。

## 防止交叉污染
本目录属于独立测评。与旧生产任务的工作区、路径、调度、截止时间严格隔离。本仓库为公开仓库，禁止在这里放私人标准答案、密钥、敏感信息。
