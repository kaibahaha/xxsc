# 01｜Agensh-Lite V4.1 总体架构及权威边界

## 核心思路
遵循“智能分布式，状态集中治理”：Agent 对知识、任务拆解和实现方案自组织；Controller 对任务有效性、租约、预算、验收和投影实行确定性裁决。这里的“无中央编排器”仅指没有一个大模型持续给每个 Worker 分配微任务；不是取消权限管理与数据库事实权威。

## 角色矩阵
| 角色 | 可自主做什么 | 必须请求/依赖什么 | 不允许 |
|---|---|---|---|
| ChatGPT A–E | 读取 Git 状态、做研究/文档/方案/代码草案、提出 CLAIM、提交角色产物与审查 | Controller 授权方可修改共享业务状态；代码验证需外部真实执行 | 自报运行测试成功、直接覆盖 BOARD、替他人标已完成 |
| WorkBuddy DEV | 获权 worktree 编码和执行命令 | 任务 lease+fencing、测试与回读 | 以现有聊天任务指令当做无限云端 API 权限 |
| Codex | 复杂编程/评估、真实测试（环境可用时） | 受限 scope、预算、独立 QA | 直接合并生产主分支 |
| QA / Integrator | 运行独立验证、证据归档、可控集成 | 测试环境及权限白名单 | 开发者自测冒充独立 QA |
| ChatGPT Work Relay | 仅搬运已经合法产生、完整核验的工件和回执 | source identity、grace、目标权限 | 代替未做完的业务成果或抢节拍 |
| Controller | 分配短租约、CAS 状态推进、队列排序、生成 BOARD 投影 | 审计事件+真实运行证据 | 编造业务结论、无限启动模型 |

## Git 与 Drive/Library 数据主权
- Git SHA 与工单 `spec_hash` 是版本对齐依据，主要存代码、不可变消息、证据索引、审查文档；Google Drive 存业务原件、协作附件、跨平台镜像；Library 存 ChatGPT 产物源，三者不互相冒充。
- Git `BOARD.md` 是 Controller 根据事件生成的 **可重建投影**；不可同时当五个人共同编辑的数据库。
- 每个 Agent 只能写自身 `outbox/<agent_id>/` 和本人 `runs/<agent_id>/`；未授权时写本地候选，不能称 Git 交付。
- 任何历史执行/写入只有 API、文件 ID、Git commit 与独立回读佐证时才能算 OBSERVED。

## 权威状态分层
`Task`：READY→CLAIMED→RUNNING→SUBMITTED→QA_PENDING→QA_GREEN→REVIEW_APPROVED→INTEGRATION_VERIFIED→DONE；失败/阻断是显式分支。`Artifact/Transport`：CREATED→SOURCE_VALID→TARGET_WRITTEN→READBACK_VERIFIED→ACK_RECORDED。`Event`：created→published→observed→validated→accepted。三条状态机不合并为一个 done。

## 保留旧版本
现存《多Agent无人值守工厂统一架构与运行总规范 V4.0》等系列文档不覆盖。冲突优先级：平台权限与安全检查 > 人工批准配置 > 真实工具可用性 > 已冻结项目协议 > V4.0 生产约束 > 本 V4.1 候选稿。生产切换要求独立影子测试和显式批准。
