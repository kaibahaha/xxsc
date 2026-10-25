---
schema_version: '1.0'
project_id: PROJECT-EXAMPLE
task_id: T-001
revision: 1
status: READY
priority: P1
spec_hash: REPLACE_SHA256
base_commit: REPLACE_GIT_SHA
allowed_agents: [A, B, C, D, E]
requires_real_runtime_test: true
---
# 任务描述

## Objective
明确、可验收的业务目标。

## Preconditions
目标分支与关联文件、依赖事件、已知失败。

## Deliverables
独立文件+元数据+哈希/回读；测试与评审需要额外证据。

## Acceptance Criteria
可重复核查的成功标准和失败标准。未经 QA 不写 DONE。
