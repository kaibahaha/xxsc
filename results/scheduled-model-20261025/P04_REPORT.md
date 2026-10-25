# P04 执行报告（R2 轮次）

EXPERIMENT_ID=SCHED-CODE-20261025-BLIND-T5-R2
PROBLEM_ID=P04
SCHEDULED_AT=2026-10-25T11:10:00+08:00
STARTED_AT=2026-10-25T11:18:20+08:00
COMPLETED_AT=2026-10-25T11:22:48+08:00
DURATION_SECONDS=340
SOURCE_GIT_PATH=/benchmarks/scheduled-model-20261025/P04.md
SOURCE_BLOB_SHA=f93c0c0c428a1b07f772f74f9acd65e340072678
TEST_SOURCE_GIT_PATH=/benchmarks/scheduled-model-20261025/public_tests.py
TEST_SOURCE_BLOB_SHA=e666569fcf2ad8a6403908595a49069fb6dcac5b

## SOLUTION_SUMMARY
实现 `reconcile_versions(events)`，纯 Python 3.11 标准库：

1. 校验：事件必须 dict 且含 `event_id/key/clock/value/timestamp`；`event_id`、`key` 非空字符串；`clock` 为 dict，键为非空字符串、值为非负真整数（bool 被拒，可为空 dict）；`value` 为字符串或 None（None 为墓碑）；`timestamp` 为非负真整数。
2. 全局幂等去重：以 `event_id` 为键保存 `(key, clock 规范化项, value, timestamp)` 签名；完全相同折叠，同 id 任一字段不同抛 `ValueError`。
3. 按 key 分组。同一 key 内两两比较：取两 clock 的节点并集，缺失节点计数视为 0；若 x 在每个节点上 `>=` y 且至少一个节点严格 `>`，则 x 严格因果支配 y。`timestamp` 不参与支配判定。clock 完全相等时互不支配。
4. 被任意其他事件严格支配者进入 `superseded_ids`；其余构成极大版本集合 maxima。maxima 多于一个即为冲突，`conflict_ids` 为全部 maxima 的 event_id 升序；唯一 maxima 时 `conflict_ids` 为 `[]`（不放入 winner 自身）。
5. winner 在 maxima 内按 `(timestamp, event_id)` 降序取最大者（timestamp 相同按 event_id 字典序降序）。
6. 输出按 key 升序；空列表返回 `[]`；去重后不同 id 的相同 clock 版本并存为冲突，不合并；不修改输入。

复杂度：每 key O(m²·k) 两两比较（m 为该 key 版本数，k 为节点数，题目允许），加 O(n log n) 排序；空间 O(n + clock 条目总数)。

## CODE_GIT_PATH
/results/scheduled-model-20261025/P04.py（目标路径）

## CODE_COMMIT_SHA
GIT_WRITE_BLOCKED：GitHub 连接器 OAuth 令牌对 `https://api.github.com/user` 与 `git push` 均返回 `401 Bad credentials`（连续 4 次重试一致）。未创建 commit。

## CODE_BLOB_SHA
bd8f17363ae6546c18682568a1462a63e53d545a —— `git hash-object` 算出的内容对象 SHA，因未能 push **尚未入库**，不作为入库凭据。

## GIT_READBACK_STATUS
GIT_READBACK_BLOCKED（无写入，故无回读；远端同路径仍为旧 RETRY 版本 blob 7508b95af1d1cabf7eba33ba98d9551875e44075）

## TEST_EXECUTION_STATUS
EXECUTED_LOCAL_PYTHON311（真实执行，非静态检查）

## TEST_CASES_PASS / FAIL
- 公开测试全量运行：Ran 16 tests, OK；其中 P04 四项 test_example / test_equal_clock_is_conflict / test_empty / test_invalid_duplicate 全 PASS。
- P04 专项补充边界自测：12/12 PASS，0 FAIL。覆盖：空 clock、严格偏序链（superseded 为 a,b）、timestamp 相同按 event_id 降序取 winner、同 id 完全相同去重、隐含 0 计数（`{"A":1}` 与 `{"A":1,"B":0}` 判为并发冲突）、多 key 按 key 升序、负 clock 计数被拒、value 非字符串非 None 被拒、空节点名被拒、同 id 不同 value 被拒、clock 非 dict 被拒、timestamp 为 bool 被拒。
- 隐藏验收由发起人事后独立运行，未访问未猜测。

## ERRORS / UNFINISHED_WORK
- GitHub 写入通道 401，P04.py 与本报告未能进入目标分支（唯一阻断项）。
- 无算法层面未完成项。

## FINAL_STATUS
ALGORITHM_COMPLETE=YES；TEST_REALLY_EXECUTED=YES；GIT_REALLY_WRITTEN=NO（GIT_WRITE_BLOCKED 401）；GIT_READBACK=NO；LIBRARY=见下方字段

## LIBRARY_PATH
/test/SCHED_CODE_BLIND_20261025/P04_DELIVERY.md

## LIBRARY_FILE_ID
GIQnPgNhcecrzqrAEUiujL

## LIBRARY_READBACK_STATUS
LIBRARY_READBACK_PASS（node-info 回读：title=P04_DELIVERY.md, kind=doc, parentId=ULpRMuAj5QYS83AQ6WuYCK, URL=https://www.workbuddy.cn/space/d/GIQnPgNhcecrzqrAEUiujL）

## MODEL_ID
MODEL_NOT_EXPOSED

## SUPERSEDED_OLD_BLOB_SHA
7508b95af1d1cabf7eba33ba98d9551875e44075（旧 RETRY 轮次 P04.py）
489c0283a77ed69fe33e918dbb163315c4f09d97（旧 RETRY 轮次 P04_REPORT.md）
