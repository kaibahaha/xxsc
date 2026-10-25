# P03 执行报告（R2 轮次）

EXPERIMENT_ID=SCHED-CODE-20261025-BLIND-T5-R2
PROBLEM_ID=P03
SCHEDULED_AT=2026-10-25T11:10:00+08:00
STARTED_AT=2026-10-25T11:18:20+08:00
COMPLETED_AT=2026-10-25T11:22:08+08:00
DURATION_SECONDS=280
SOURCE_GIT_PATH=/benchmarks/scheduled-model-20261025/P03.md
SOURCE_BLOB_SHA=919f6358d1dcd9e551f06a215feb909d90ef3a48
TEST_SOURCE_GIT_PATH=/benchmarks/scheduled-model-20261025/public_tests.py
TEST_SOURCE_BLOB_SHA=e666569fcf2ad8a6403908595a49069fb6dcac5b

## SOLUTION_SUMMARY
实现 `schedule(jobs, completed, capacity)`，纯 Python 3.11 标准库：

1. 校验：`jobs`/`completed` 必须 list；`capacity` 正真整数（bool 被拒）；每个 job 必须 dict 且含 `id/depends/cost/priority`；`id` 非空字符串且唯一；`depends` 必须是列表、元素为非空字符串、无重复；`cost` 为真整数且 `1 <= cost <= capacity`；`priority` 为真整数。
2. 引用校验：`depends` 只允许引用 jobs 中定义的 id（缺失引用 ValueError），自环 ValueError。
3. `completed` 元素为非空字符串、无重复、必须都在 jobs 内。
4. 全图环检测：用 Kahn 算法遍历**整个** jobs 图（不因节点被标记 completed 而跳过），有剩余节点即抛 ValueError，满足「环内作业已 completed 也要报错」。
5. 波次推进：候选 = 尚未完成且其依赖在**本波次开始前**已完成的 job（本波次选中者下一波次才算完成）；候选按 `(-priority, id)` 排序；依次遍历，能放进剩余 capacity 就选中并累加 load，放不下就跳过继续尝试后续候选；按实际选择顺序记录 `job_ids`。本波次一个都选不出而仍有剩余任务时抛 ValueError。
6. 返回 `{"waves":[{"job_ids","load"},...], "total_waves"}`；jobs 全部已完成或 `jobs=[]` 时返回 `{"waves":[],"total_waves":0}`；不修改输入。

复杂度：校验 O(V+E)；每波次对候选集排序 O(V log V)，总 O(W·V log V)（W 为波次数）；额外空间 O(V+E)。题目允许按每轮扫描/排序实现。

## CODE_GIT_PATH
/results/scheduled-model-20261025/P03.py（目标路径）

## CODE_COMMIT_SHA
4b23dae72ab111e7cb2e250e794fea444b5f9a95 —— 承载 P03 源码的 commit，已 push 到 `exp/scheduled-coding-blind-20261025`（推送成功）。

## CODE_BLOB_SHA
5b4fbb7a626585b342b73369ab2d07a6a82e5698 —— 已入库，远端回读一致。

## GIT_READBACK_STATUS
GIT_READBACK_PASS（push 后回读同分支同路径，blob SHA = 5b4fbb7a626585b342b73369ab2d07a6a82e5698）

## TEST_EXECUTION_STATUS
EXECUTED_LOCAL_PYTHON311（真实执行，非静态检查）

## TEST_CASES_PASS / FAIL
- 公开测试全量运行：Ran 16 tests, OK；其中 P03 四项 test_example / test_with_completed / test_empty / test_cycle_even_if_completed 全 PASS。
- P03 专项补充边界自测：13/13 PASS，0 FAIL。覆盖：样例波次结果、自环、重复依赖、cost>capacity、completed 引用未定义、全部已完成返回空波次、贪心跳过（cost 3/2/1 与容量 3 下先取 b+c 再取 a）、同优先级按 id 排序、本波次选中者不解锁同波次后继、环内节点已 completed 仍报错、重复 job id、缺失依赖引用、capacity=0 被拒。
- 隐藏验收由发起人事后独立运行，未访问未猜测。

## ERRORS / UNFINISHED_WORK
- 首次经连接器 OAuth 令牌写入返回 401；后用发起人提供的有效 PAT（scope=repo）写入成功，源码 commit `4b23dae72ab111e7cb2e250e794fea444b5f9a95` 已 push。
- 无算法层面未完成项。

## FINAL_STATUS
ALGORITHM_COMPLETE=YES；TEST_REALLY_EXECUTED=YES；GIT_REALLY_WRITTEN=YES；GIT_READBACK=PASS；LIBRARY=见下方字段

## LIBRARY_PATH
/test/SCHED_CODE_BLIND_20261025/P03_DELIVERY.md

## LIBRARY_FILE_ID
49J4cnGGB8qbnzPjmNkvK0

## LIBRARY_READBACK_STATUS
LIBRARY_READBACK_PASS（node-info 回读：title=P03_DELIVERY.md, kind=doc, parentId=ULpRMuAj5QYS83AQ6WuYCK, URL=https://www.workbuddy.cn/space/d/49J4cnGGB8qbnzPjmNkvK0）

## MODEL_ID
MODEL_NOT_EXPOSED

## SUPERSEDED_OLD_BLOB_SHA
0138c75e0ac34efb128864854a3ef4f02283af97（旧 RETRY 轮次 P03.py）
6dcc74bb7ae29feb9afca2fc9b42c97a05c6cb0d（旧 RETRY 轮次 P03_REPORT.md）
