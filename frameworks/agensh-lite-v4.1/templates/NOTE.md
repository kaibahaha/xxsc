# NOTE（短摘要+长详情）

```json
{
  "schema_version": "1.0", "type": "FAIL", "event_id": "EV-EXAMPLE",
  "project_id": "PROJECT-EXAMPLE", "task_id": "T-001",
  "producer": "A", "summary": "实测输入X导致候选版本Y崩溃",
  "detail_ref": "repo@commit:06_evidence/T-001/RUN-001/fail.txt",
  "evidence_ref": "repo@commit:06_evidence/T-001/RUN-001/test.log",
  "spec_hash": "REPLACE_SHA256", "affected_commit": "REPLACE_COMMIT",
  "created_at": "REPLACE_ISO8601", "status": "PROPOSED"
}
```

上游五种类型为 `FACT / OBSERVED / FAIL / CLAIM / PATCH_SUMMARY`；本系统不把 CLAIM 当排他锁；文本检查不等于执行测试。
