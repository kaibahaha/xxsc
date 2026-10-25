# P02 执行报告（R2 轮次）

EXPERIMENT_ID=SCHED-CODE-20261025-BLIND-T5-R2
PROBLEM_ID=P02
SCHEDULED_AT=2026-10-25T11:10:00+08:00
STARTED_AT=2026-10-25T11:18:20+08:00
COMPLETED_AT=2026-10-25T11:20:46+08:00
DURATION_SECONDS=190
SOURCE_GIT_PATH=/benchmarks/scheduled-model-20261025/P02.md
SOURCE_BLOB_SHA=9c8d1cf9ac3714d576834453b16285c4c85399a6
TEST_SOURCE_GIT_PATH=/benchmarks/scheduled-model-20261025/public_tests.py
TEST_SOURCE_BLOB_SHA=e666569fcf2ad8a6403908595a49069fb6dcac5b

## SOLUTION_SUMMARY
实现 `replay(events)`，纯 Python 3.11 标准库：

1. 容器校验后逐条校验：必须 dict 且含 `event_id/order_id/revision/kind`；`event_id`、`order_id` 非空字符串；`revision` 真整数且 >= 0（bool 被拒）；`kind` 只接受 `"SET"` / `"DELETE"`。
2. `kind="SET"` 必须携带 `amount` 且为非负真整数（允许 0）；`kind="DELETE"` 一旦出现 `amount` 字段即报错（即便值为 None）。
3. 全局幂等去重：以 `event_id` 为键保存 `(order_id, revision, kind, amount)` 签名；完全相同折叠，同 id 任一字段不同抛 `ValueError`。
4. 版本冲突检查：同一 `(order_id, revision)` 只允许一个 `event_id`；出现两个不同 id 即抛 `ValueError`（不论 kind/amount 是否相同）。
5. 按 order 分组，组内按 `(revision, event_id)` 升序重放：`SET` 写入金额并激活（同时清除 tombstone），`DELETE` 移除并写入 tombstone；高 revision 覆盖低版本，故删除后更高 revision 的 SET 可令订单复活。
6. 返回 `{"active","deleted","total_amount"}`；active/deleted 按 `order_id` 升序；`total_amount` 用 Python 大整数求和，无溢出截断；不修改输入。

复杂度：时间 O(n log n)（排序主导），额外空间 O(n)。

## CODE_GIT_PATH
/results/scheduled-model-20261025/P02.py（目标路径）

## CODE_COMMIT_SHA
b67966b6dc2c3bbed0a6107bf86e783ed23bd283 —— 承载 P02 源码的 commit，已 push 到 `exp/scheduled-coding-blind-20261025`（推送成功）。

## CODE_BLOB_SHA
41f4f182a9552365e672f4d3e690cbdff513069e —— 已入库，远端回读一致。

## GIT_READBACK_STATUS
GIT_READBACK_PASS（push 后回读同分支同路径，blob SHA = 41f4f182a9552365e672f4d3e690cbdff513069e）

## TEST_EXECUTION_STATUS
EXECUTED_LOCAL_PYTHON311（真实执行，非静态检查）

## TEST_CASES_PASS / FAIL
- 公开测试全量运行：Ran 16 tests, OK；其中 P02 四项 test_example / test_resurrection / test_empty / test_invalid_revision 全 PASS。
- P02 专项补充边界自测：11/11 PASS，0 FAIL。覆盖：DELETE 后高 revision SET 复活、同 (order,revision) 两个 event_id 冲突、负 amount、SET 缺 amount、非法 kind、同 id 不同 amount 去重冲突、DELETE 携带 amount（含 None）、多订单按 order_id 升序、10^30 大整数总额不截断、输入未被修改。
- 隐藏验收由发起人事后独立运行，未访问未猜测。

## ERRORS / UNFINISHED_WORK
- 首次经连接器 OAuth 令牌写入返回 401；后用发起人提供的有效 PAT（scope=repo）写入成功，源码 commit `b67966b6dc2c3bbed0a6107bf86e783ed23bd283` 已 push。
- 无算法层面未完成项。

## FINAL_STATUS
ALGORITHM_COMPLETE=YES；TEST_REALLY_EXECUTED=YES；GIT_REALLY_WRITTEN=YES；GIT_READBACK=PASS；LIBRARY_WRITTEN=YES

## LIBRARY_PATH
/test/SCHED_CODE_BLIND_20261025/P02_DELIVERY.md

## LIBRARY_FILE_ID
q3RmeWpVwFQ2k5G79pKlKa

## LIBRARY_READBACK_STATUS
LIBRARY_READBACK_PASS（node-info 回读：title=P02_DELIVERY.md, kind=doc, parentId=ULpRMuAj5QYS83AQ6WuYCK, URL=https://www.workbuddy.cn/space/d/q3RmeWpVwFQ2k5G79pKlKa）

## MODEL_ID
MODEL_NOT_EXPOSED

## SUPERSEDED_OLD_BLOB_SHA
2bad9a4f57da6142290f2e28ae746ad73ea23e7f（旧 RETRY 轮次 P02.py）
6c92042ecfd1b85e6a89761c45f936ca46ceadc8（旧 RETRY 轮次 P02_REPORT.md）
