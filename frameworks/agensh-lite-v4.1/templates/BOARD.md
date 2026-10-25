# PROJECT BOARD（Controller-only Projection / 只读）

schema_version: 1.0
project_id: PROJECT-EXAMPLE
projection_version: PV-0001
projection_commit: UNKNOWN
generated_at: UNKNOWN
source_event_watermark: UNKNOWN
board_integrity: DRAFT_ONLY

## READY TASKS
| task_id | priority | dependency | spec_hash | last_event | claim_status |
|---|---|---|---|---|---|
| T-001 | P1 | none | HASH_PLACEHOLDER | EV-001 | NONE |

## ACTIVE CLAIMS
从独立 CLAIM/Controller 授租事件投影；不能手工在此修改。

## HOT FACT / FAIL / PATCH
当前各任务最新且有证据的摘要与证据链接；无信息不是证明任务不存在。

## SOURCE OF TRUTH
Git 事件文件 + 经授权的 Controller 状态；BOARD 可以随时重建。
