# 本轮剩余阻断与 R02 范围

两项指定 P1 的本地修复/反例/完整回归已交付，不表示生产/云端已验收。

| 状态 | 待办 | 交接 |
|---|---|---|
| BLOCKED_ATOMIC_LEASE / INTEGRATION_PENDING | GitHub 真实 HEAD/CAS/readback 与 Controller 权威授租未接通；本地 Board digest 不能代替真实 projection 回执 | WorkBuddy M02/R02 实物集成，保持 LOCAL_SQLITE_ONLY 标签，不能把本地 GRANTED 发布成跨云权威 |
| R02_GATE_EVIDENCE | Review/Integration/DONE 仍为权限+非空 evidence_refs，未核验各自独立真实原证据 | 本轮只强化阶段 token 所有权/阶段绑定，没有伪装已完成 P2；独立审查/集成/验收回执核验留给 R02 |
| R02_CONFIG_COMPATIBILITY | 两份冻结示例仍存在重复 ID/Provider 兼容问题 | 配置拥有者后续修正；原拒绝测试保留，不能视为可部署示例 |
| BLOCKED_PROVIDER / BLOCKED_EXECUTOR（生产） | 真实 Provider probe/鉴权、外部 Runner、云 cold-start、24h shadow、独立 QA 仍缺实际证据 | 仍沿用首轮 BLOCKERS，不启动定时器、云服务或收费资源 |
| INTERFACE_HANDOFF | WorkBuddy 必须按当前阶段申请新 epoch，使用版本化注册表命令 | 详见 contracts/README.md；现有 DTO 字段不变。lease_phase 在 task 投影中；ClaimProposal.commit_sha 对验收阶段必须匹配 candidate_commit |

运维/升级注意：

- 构造器的新 Registry 不会自动授权新增/停用/恢复身份或改变 quotas。已有状态是权威；以 registry_admin 调用 apply_registry，并给当前 registry_version。缺省行不代表删除，停用必须明确提交 desired_enabled/health/admission。
- 旧兼容 register_agent/update_health 支持可选 expected_version；完整配置变更、恢复/提升权限走强制 CAS 的 apply_registry。实际准入 probe refs 必须由受信集成服务核验；本核心不编造真实 probe。
- 旧 R01 journal 中尚存的等待阶段开发 token 在 recover/首个权威操作中撤销，事实保留；先 recover，再回读版本/Board 对账和重新申请，避免拿旧 expected_version 请求。
- 先前版本已经实际清空且写入历史的证据不会被凭空自动恢复；需从真实历史回执/工件经受权状态修复。本补丁保护后续到期和旧格式未受损 journal，不伪造已经丢失的业务确认。
- 阶段 grant 不授权开发写入；外部 Git Adapter 仍须对所有副作用实施 scope 与 fencing。历史命令重试只返回当时回执，不代表现在仍持有授权。
- 当前 per-transaction 全历史回放与本地存储边界不变；不是云容量/吞吐保证。

未修改 main、WorkBuddy Adapter/CLI/Runner 或生产配置；PR #1 保持 Draft、未合并。本轮通过级别为 SELF_TESTED，未签发本交付的独立 QA_GREEN。
