# P01 执行报告（R2 轮次）

EXPERIMENT_ID=SCHED-CODE-20261025-BLIND-T5-R2
PROBLEM_ID=P01
SCHEDULED_AT=2026-10-25T11:10:00+08:00
STARTED_AT=2026-10-25T11:11:30+08:00
COMPLETED_AT=2026-10-25T11:18:13+08:00
DURATION_SECONDS=403
SOURCE_GIT_PATH=/benchmarks/scheduled-model-20261025/P01.md
SOURCE_BLOB_SHA=3737e14bacfa4f666034bf5c54cf7a44ea456b94
TEST_SOURCE_GIT_PATH=/benchmarks/scheduled-model-20261025/public_tests.py
TEST_SOURCE_BLOB_SHA=e666569fcf2ad8a6403908595a49069fb6dcac5b
PROTOCOL_GIT_PATH=/benchmarks/scheduled-model-20261025/BLIND_T5_PROTOCOL.md
PROTOCOL_BLOB_SHA=1d904c0fe3ae8fb5d4dd1dfc8107437e963f5fa1

## SOLUTION_SUMMARY
实现 `merge_windows(events, gap)`，纯 Python 3.11 标准库：

1. 容器与 gap 校验：`events` 必须 list；`gap` 必须真整数且 >= 0（bool 被拒）。
2. 逐条校验：事件必须 dict 且含 `event_id/tenant/start/end` 四字段；`event_id`、`tenant` 为非空字符串；`start`、`end` 为真整数（bool 被拒）且 `start < end`。
3. 全局幂等去重：以 `event_id` 为键保存 `(tenant,start,end)` 签名；完全相同的重复事件折叠为一条，同一 id 任一字段不同即抛 `ValueError`。
4. 按 tenant 分组，组内按 `(start,end,event_id)` 升序扫描合并：当 `next.start <= cur.end + gap` 时并入（相接也并入），`end` 取两者最大值，否则开新窗。
5. 输出 `{"tenant","start","end","count"}`，`count` 为该合并窗内不同 event_id 数；按 `(tenant,start,end)` 字典序升序（按 tenant 排序分组 + 组内 start 递增自然满足）。
6. 全程只读输入，不修改传入对象；空列表返回 `[]`。

复杂度：时间与排序同阶 O(n log n)；额外空间 O(n)（不计输出）。

## CODE_GIT_PATH
/results/scheduled-model-20261025/P01.py（目标路径）

## CODE_COMMIT_SHA
352982fa917148e7021284eb13bd2389a07089e4 —— 承载 P01 源码的最终 commit（`git log -1 -- results/scheduled-model-20261025/P01.py`），已 push 到 `exp/scheduled-coding-blind-20261025`。

## CODE_BLOB_SHA
56ad4d803ff90ddb1ceb4fb525011d3ca24520a3 —— 已入库，远端回读一致。

## GIT_READBACK_STATUS
GIT_READBACK_PASS（push 后经 GitHub API 回读同分支同路径，blob SHA = 56ad4d803ff90ddb1ceb4fb525011d3ca24520a3）

## TEST_EXECUTION_STATUS
EXECUTED_LOCAL_PYTHON311（真实执行，非静态检查）

## TEST_CASES_PASS / FAIL
- 公开测试 `python3.11 -m unittest discover -s benchmarks/scheduled-model-20261025 -p public_tests.py -v`：Ran 16 tests, OK（P01 四项 test_example / test_zero_gap_and_negative / test_empty / test_invalid 全 PASS）。
- P01 专项补充边界自测：11/11 PASS，0 FAIL。覆盖：负数时间窗、gap=0 相接合并、嵌套窗合并、多租户字典序、gap 为 float 与 bool 被拒、events 非 list 被拒、空 tenant 被拒、start==end 被拒、缺字段被拒、输入对象未被修改。
- 公开样例仅覆盖基础边界，隐藏验收由发起人事后独立运行，未访问、未猜测。

## ERRORS / UNFINISHED_WORK
- 首次尝试经 GitHub 连接器 OAuth 令牌写入返回 401 Bad credentials（重试 4 次一致），P01.py 未能入库。
- 后续由发起人提供有效 Personal Access Token（scope=repo，login=kaibahaha）后重新写入成功：源码 commit `bfa930bc22cd7aaba9092a3624742716963dd338` 已 push 到 `exp/scheduled-coding-blind-20261025`。
- 无算法层面未完成项。

## FINAL_STATUS
ALGORITHM_COMPLETE=YES；TEST_REALLY_EXECUTED=YES；GIT_REALLY_WRITTEN=YES；GIT_READBACK=PASS；LIBRARY=见下方字段

## LIBRARY_PATH
/test/SCHED_CODE_BLIND_20261025/P01_DELIVERY.md

## LIBRARY_FILE_ID
5zXOfQ2C3M6qfxXauCaL8x

## LIBRARY_READBACK_STATUS
LIBRARY_READBACK_PASS（node-info 回读：title=P01_DELIVERY.md, kind=doc, spaceId=WPndKuF4MLFD4JSLHtPoZ1, parentId=ULpRMuAj5QYS83AQ6WuYCK，URL=https://www.workbuddy.cn/space/d/5zXOfQ2C3M6qfxXauCaL8x）

## MODEL_ID
MODEL_NOT_EXPOSED（运行环境未暴露可验证的模型元数据）

## SUPERSEDED_OLD_BLOB_SHA
ed7eee312c9a4f0fb04d56b171141b5add209e22（旧 RETRY 轮次 P01.py）
8c150ec15d72f3ac08511dc9b99b3d3d53e34380（旧 RETRY 轮次 P01_REPORT.md）
