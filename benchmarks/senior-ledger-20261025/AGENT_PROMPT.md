# 可复制的高级编程定时任务指令（执行版）

任务名称：Senior Ledger 编程盲测

请仅在**定时触发后**读取 GitHub 仓库 `kaibahaha/xxsc` 的分支 `exp/senior-ledger-20261025`，执行根路径 `/benchmarks/senior-ledger-20261025/TASK.md` 中的一道高级综合编程题。当前设置阶段不得预读任务源码，不得提前解题。必须独立完成，不能访问任何其他 Agent 提交目录或历史题解，也不能调用 Codex、WorkBuddy 或其他模型代写。

仔细读取冻结源码 `src/mini_ledger/` 和冻结公开测试 `tests/test_public.py`；修复后把**完整可运行代码**提交到如下 Git 仓库根绝对路径：

`/results/senior-ledger-20261025/workbuddy/src/mini_ledger/`
`/results/senior-ledger-20261025/workbuddy/tests/test_regression.py`
`/results/senior-ledger-20261025/workbuddy/REPORT.md`
`/results/senior-ledger-20261025/workbuddy/RUN_LOG.md`

如果执行者不是 WorkBuddy，请将上述四处的 `workbuddy` 全部改成自己的唯一 ID，如 `chatgpt-t5`、`codex-a`，以防交叉污染。修改代码只允许在自己的结果目录，冻结题目所在目录只读。完成每个模块及时 Git commit 并对同分支同路径回读，保留 commit SHA 和 blob SHA。测试失败与未运行必须真实披露，不准伪造。必须独立写至少八项回归测试，其中至少一项并发竞争、一项失败注入、一项审计篡改。

报告必须包含：EXPERIMENT_ID=`SENIOR-LEDGER-20261025`、计划/实际开始与结束时间（带北京时间+08:00）、执行耗时、改动模块、发现的缺陷、修复机制、复杂度与事务隔离理由、公开测试与额外测试的真实运行输出、Git 文件路径、每次 commit SHA、Git 回读 SHA、已知残余风险、运行模型元数据（不可得写 MODEL_NOT_EXPOSED）、最终成功/失败状态。

若同时具备 ChatGPT Library 或其他云端文档连接权限，可额外保存 `REPORT.md` 镜像到事先确认的云端路径，但必须区分 WorkBuddy 空间与 ChatGPT Library；不以写入自己空间冒充写入其他空间。没有现成授权则仅保证 Git 官方交付，不能为了拿到令牌绕过安全检查。

不要覆盖历史交付，不要预先宣称 PASS。尽力完成本轮任务，再给出可核验 Git 链接。
