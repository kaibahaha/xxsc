# 实际阻断与未测事项

| 状态 | 项目 | 解除条件/责任边界 |
|---|---|---|
| BLOCKED_ATOMIC_LEASE | 本次只有 LOCAL_SQLITE_ONLY 原子证明，无生产持久后端、租约权威发布/回读或云冷启动证据 | R02 配置受保护单主+持久卷或事务 DB，完成远端 100-way/fencing/crash/重启验收；禁止把 SQLite 放 Git/NFS |
| INTEGRATION_PENDING | WorkBuddy M02/M06/M08/M10 尚未与最终 2.0 合同跨分支集成运行 | 按 INTERFACES.md 固定源码 SHA，评审类型/receipt/错误映射，不覆盖双方文件 |
| BLOCKED_PROVIDER / NOT_TESTED | 真实 ChatGPT/WorkBuddy/Codex 的独立 schedule、触发和 Git mailbox/ACK 运行未探针 | 使用各平台真实权限与独立 run_id/时间/回执；模拟 ID 不等于 ACTIVE |
| BLOCKED_EXECUTOR（生产） | 没有真实跨平台 Runner/QA bridge 和生产证据核验器 | 注入验证凭证的 Authenticator，验证原 stdout/stderr/exit/spec/commit 的 EvidenceVerifier；默认 None 拒绝 QA |
| NOT_TESTED | GitHub Actions 单主实验、CI、24h shadow、真实计划 vs 实触发统计 | WorkBuddy M10/R02 建立隔离、获授权的实验；本单未创建或触发工作流/生产定时任务 |
| PENDING_INDEPENDENT_QA | 本单全部结果为作者 SELF_TESTED | 独立 QA 在 PR 最终 head 上重跑并核对相同源码 hash；禁止由作者自测替代 QA_GREEN |
| CONFIG_CONFLICT | 冻结 agent_pool.example.json 和 mixed_pool.example.json 有重复 WorkBuddy Agent ID/Provider 冲突 | 已有拒绝测试；由配置拥有者在后续单中修正，冻结文档未修改 |
| NOT_TESTED | Python 3.11、Windows、长账本与真实 API 限流/成本 | 本次实测 Linux/Python 3.12.14，N=20 功能配置；不声称无限吞吐 |

已知实现边界：每个事务回放全历史；诊断 snapshot 是受信内部接口；来源 hash 链不替代真实凭证和受保护 Git ref；外部副作用须 sink 幂等；不可用身份重新准入、FAIL 撤回、同 commit 重验和日志压缩/签名需显式后续策略。控制面不执行模型思考或外部 Runner。

没有 Git 写权限阻断：CLI push 已实测成功，连接器返回 admin/push/pull 权限；PR 已实际创建。未运行的能力不会因这些权限自动成立。
