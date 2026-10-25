# Microsoft Agensh 固定版本源码采用记录

实际 clone：`https://github.com/microsoft/Agensh.git` 到 `/workspace/Agensh`，detach 于 `0468a3e6a58b51dc2b84871fcaa0df22b0d1033e`。已实际读取工单/dispatch 指定文件；逐文件实际 SHA256 和行数见 MICROSOFT_SOURCE_HASHES.json（由 shell/Python 对原始文件计算）。未运行微软多容器系统，不能宣称其端到端验证通过。

| 固定 commit 内路径 | 本次核实内容 | 采用/排除与目标 |
|---|---|---|
| prompts/agents.txt | GATHER/CLAIM/ACT/VERIFY/PATCH、协作碰撞、共享板 | 借鉴设计；改为跨 Provider、GitHub、显式权限和不自动 merge 的合同。原有自主 merge main 指令明确排除 |
| board-service/shared_lessons.py | 五种知识、3600s 软 CLAIM、近期替换与完整历史、保守去重、FAIL/checkpoint | 接口重写到 memory.py/context.py；软 CLAIM 不当锁；FAIL 精确 task/spec/commit/test；不复制文本 passed 正则作为 QA |
| board-service/main.py | MySQL 持久化、hydrate、board_cursor、pending lease、shown、snapshot、grep/unfold | 借鉴设计；原 API 不移植。短事务日志与 ACK 后连续 cursor；不照搬 snapshot 读取即推进 cursor 的行为 |
| board-service/verifier.py | 格式/占位证据词校验，不运行测试 | 借鉴边界；替换为结构证据 + 受信实际日志 verifier。未把字符串检验当 runtime QA |
| board-service/gquery.py | AND/OR/括号解析和参数化 SQL LIKE | 已读，明确排除复杂表达式 parser；首版结构化知识检索更小且保留冷索引 |
| mini-router/src/uem.ts | 通用事件字段 | 按接口重写 Event/UEM；增加 provider、multi-target、版本/attempt/epoch/provenance |
| mini-router/src/state.ts | per-agent 去重、状态、有限退避、sending 重启恢复、source cursor | 借鉴设计；Python 统一账本与事务回执。未移植 MySQL/TS 或后台重试循环 |
| mini-router/src/board_client.ts | 增量读与全量 fallback、UNKNOWN 与 EMPTY 分离 | 借鉴语义到 Board fence；实际 Git 回退读取由 WorkBuddy 实现，不假装本核心已连远端 |
| mini-router/src/dispatcher.ts | serialized dispatch、成功后记账失败不能重做执行、批次回执 | 借鉴处理证据/ACK_ONLY 与 sink key；不复制 ACP prompt/中途注入/常驻调度 |
| mini-router/sql/01-events-schema.sql | event/agent 唯一键、事件状态、独立 source cursor | 参考事务约束；新写 SQLite 单一 hash-chain journal schema，不复制 MySQL 表作为云后端 |
| mini-router/sql/02-mattermost-db.sql | Mattermost database 初始化 | 已读，明确排除，与 GitHub MVP 无关 |
| mini-router/sql/03-board-schema.sql | append-only gist/detail/expiry 与索引 | 借鉴冷热历史和到期只影响 live view 的原则 |
| LICENSE | MIT，Copyright (c) Microsoft Corporation. | 原文复制到 factory/agl/contracts/MICROSOFT_LICENSE.txt |

源码采用分类：本交付无上游源文件逐行直接移植；Python 实现为本项目重新实现的数据契约和事务模型。为保留采用来源和授权义务，仍附微软 MIT 原文、原版权和固定 commit 入口。MIT 不代表微软认证，也不覆盖其论文文本。

明确未部署/复制为必要依赖：Gitea、Mattermost、Copilot ACP、secret-service、shim、原 MySQL 服务和研究集群。没有主张云端 webhook、原生 loadSession、mid-turn 注入在 ChatGPT/WorkBuddy 已存在。
