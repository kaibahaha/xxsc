# 00｜微软源码目录细颗粒度拆解与采纳矩阵

固定证据基线：`microsoft/Agensh@0468a3e6a58b51dc2b84871fcaa0df22b0d1033e`（MIT）；GitHub https://github.com/microsoft/Agensh；论文 https://arxiv.org/abs/2609.26781；复现指南 https://github.com/microsoft/Agensh/blob/main/REPRODUCE.md 。2026-10-25 通过连接器只读取得真实源码。**借鉴机制**与**已经接入我们系统的能力**须分别表述。

| 具体上游位置 | 已核实的程序行为 | V4.1 对应交付 | 处理 |
|---|---|---|---|
| `prompts/agents.txt` | 通用自组织指令、观测→CLAIM→实现→验证→合并→PATCH_SUMMARY | `agents/COMMON.md`、A–E 指令 | 改写采用，不照搬 ProgramBench 目标 |
| `prompts/kickoff.txt`, `idle.txt`, `deadline-45m.txt`, `deadline-5m.txt` | 新任务、空闲提醒、截止冻结/收尾 | `06_LIFECYCLE_AND_HANDOFF.md` | 改写采用；定时窗口不能假定持续60分钟 |
| `board-service/shared_lessons.py` | 五种 gist、默认 3600s CLAIM、保守去重、FAIL 使特定补丁候选失效 | `05_SHARED_MEMORY_AND_CONTEXT.md`, note schema | 改写采用，FAIL 生效范围必须绑定 task+commit |
| `board-service/verifier.py` | 格式/占位词校验，**不运行测试** | `07_QA_GATES_AND_PROVENANCE.md` | 只复刻文本门禁，不误称真实 QA |
| `board-service/main.py` | append-only 入库、近期视图、snapshot 游标、grep/unfold、消息领取/确认 | `02/04/05`, templates | 用 Git 不可变文件+Controller 索引替代；原 API 不直接可用 |
| `board-service/gquery.py`, `unfold.py` | AND/OR 检索、长详情展开 | `05`, evidence refs | 先索引检索，暂不搬 SQL 解析器 |
| `mini-router/src/uem.ts`, `uem_render.ts` | UEM 六字段、批量渲染 | `04_UEM_EVENTS_AND_DELIVERY.md`, JSON schema | **直接借鉴数据形状** |
| `mini-router/src/state.ts`, `sql/01-events-schema.sql` | 每 agent 去重、pending/sending/sent/failed/retrying、batch、退避、恢复 | `04`, event/receipt schema | 改写采用，Git 无 SQL 事务，不能宣称相同保证 |
| `mini-router/src/board_client.ts` | 增量 snapshot→全量回退、UNKNOWN≠EMPTY、无知识回写时提醒 | `05/06`, agent 指令 | 强烈建议复制语义 |
| `mini-router/src/group_messages.ts` | 最新32条直接显示，积压 JSONL 冷存 | `05`, archive 规则 | 借鉴冷热策略，不机械使用32条 |
| `mini-router/mcp-notice-shim.cjs` | MCP tool result 注入实时 DM/板通知 | `04`, 后续 adapter backlog | **不直接复用**；网页定时 Agent 未证实中途注入 |
| `mini-router/src/acp_socket_channel.ts`, `agent/acp-bridge.py` | ACP session/load 恢复与 Copilot 工作进程 | `06`, 手工 checkpoint/handoff | 模式借鉴，**无原生 Session 复用** |
| `secret-service/`, `agent/config/` | Worker 凭据与 MCP 配置 | `11_SECURITY_AND_LIMITS.md` | 暂不部署；GitHub 权限必须另管 |
| `docker/`, `scripts/`, `REPRODUCE.md` | 多容器长驻研究实验 | `10_IMPLEMENTATION_ROADMAP.md` | 不复制重服务和 1024 Agent 部署 |

上述文件的源码入口：https://github.com/microsoft/Agensh/blob/0468a3e6a58b51dc2b84871fcaa0df22b0d1033e/prompts/agents.txt、https://github.com/microsoft/Agensh/blob/0468a3e6a58b51dc2b84871fcaa0df22b0d1033e/board-service/shared_lessons.py、https://github.com/microsoft/Agensh/blob/0468a3e6a58b51dc2b84871fcaa0df22b0d1033e/mini-router/src/state.ts、https://github.com/microsoft/Agensh/blob/0468a3e6a58b51dc2b84871fcaa0df22b0d1033e/mini-router/src/board_client.ts、https://github.com/microsoft/Agensh/blob/0468a3e6a58b51dc2b84871fcaa0df22b0d1033e/mini-router/src/group_messages.ts。

## 额外复刻的“隐藏关键点”
1. **每 Agent 独立消费水位**：全局单游标会让 A 消费后 B 看不到消息；Git 投影游标按 (agent_id, source) 管理。
2. **读取失败 != 队列为空**：标 `BOARD_UNKNOWN`，禁止新抢单，只处理此前已持有、且仍有效的租约。
3. **事件投递成功 != 业务任务成功**：ACK 只能说明 agent 收到事件；`QA_GREEN` 必须另有实际测试证据。
4. **FAIL 不能全球禁用整个思路**：上游失效语义按发布者候选处理；V4.1 绑定 task+spec+commit+evidence 后裁决。
5. **压缩积压不删历史**：hot 提供最近/关联信息，warm 为当前失败与认领，cold 是 append-only 历史及不可变证据。
6. **每轮强制写回**：有发现写 FACT/FAIL/OBSERVED；仍在工作更新 HANDOFF；空轮明确 `NO_ELIGIBLE_TASK`，不制造伪知识。
7. **原子租约 != 软 CLAIM**：Git 没有跨多个文件的事务，只有 Controller 成功回执可授予权威执行权。
8. **成本与阶段门槛**：开发稿不是生产合约，只有经冻结的 Policy/Capabilities 和成功的读写探针可进入活动运行。

## 第三方报告的两处修正
“board-service 可直接给五个网页 Agent 用”不严谨：服务模型无关，但 MySQL、认证网络和 ChatGPT 定时连接器/直连 HTTP 的能力尚需实测；本包先移植协议。 “规模开销线性”是粗略预算估算，不是相同总 Token 消耗的实测规律。

## 授权与来源
本包为原创适配说明、短字段名称和协议约定；未批量复制微软源码。微软原项目 MIT 许可，若日后复制源文件或显著派生具体代码，应保留其 LICENSE 与版权声明。论文材料的授权单独核实，不能把 MIT 自动扩展到论文。见 `NOTICE.md`。
