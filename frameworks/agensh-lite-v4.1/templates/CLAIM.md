# CLAIM 提案 / 非有效排他租约

project_id: PROJECT-EXAMPLE
task_id: T-001
claim_event_id: EV-REPLACE
owner_agent: A
scope: 某独立模块或方案
base_commit: REPLACE
spec_hash: REPLACE
claimed_at: REPLACE_ISO8601
soft_expires_at: REPLACE_ISO8601
state: CLAIM_PROPOSED
lease_ref: NONE
fencing_epoch: NONE

若无 Controller 成功 `LEASE_GRANTED` + epoch 回执，禁止修改其他人共享源码和权威状态。
