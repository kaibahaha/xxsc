# Agensh-Lite V4.1｜五个 ChatGPT 定时 Agent 的 GitHub 自组织协作协议

**版本**：V4.1-DRAFT｜**生成日**：2026-10-25｜**模式**：Shadow / 候选规范，尚未启用生产任务。  
**现有体系**：ChatGPT 五个定时窗口（实际平台配置待核验）、WorkBuddy HY3/HY4/Step5、Codex、ChatGPT Work、Google Drive、GitHub、Controller。  
**目标 Git**：`kaibahaha/xxsc`，建议新增隔离分支，不触碰 `main` 和既有盲测分支。  
**参考**：Microsoft Research Agensh MIT 项目，固定来源 Commit `0468a3e6a58b51dc2b84871fcaa0df22b0d1033e`。本包为重新编写的适配设计，**不是微软官方版本，也不保证与微软源码行为一致**。

## 一句话架构
五个定时 Agent = 五个独立的、错峰唤醒的**协作工位**；GitHub 是**可读共享工作台与代码版本库**；Controller 是任务状态、原子租约、权限、验收的**权威控制面**；WorkBuddy/Codex 是实际运行与测试的执行面；Drive/Library 是源文件、归档与跨平台数据面。

## 必读入口
1. `00_SOURCES_AND_ADOPTION.md`：原始源码出处、逐模块可复制/需适配/不复制。
2. `01_ARCHITECTURE_AND_AUTHORITY.md`：微架构和状态权威边界。
3. `02_GITHUB_LAYOUT_AND_WRITES.md`：仓库目录、只能单写的 BOARD 投影、不可变消息文件。
4. `03_TASK_CLAIMS_AND_LEASES.md`：自组织认领、租约、并发冲突、fencing。
5. `04_UEM_EVENTS_AND_DELIVERY.md`：事件、ACK、游标、重试。
6. `05_SHARED_MEMORY_AND_CONTEXT.md`：FACT/FAIL/CLAIM/PATCH、检索、热冷记忆。
7. `06_LIFECYCLE_AND_HANDOFF.md`：唤醒、恢复、执行、交接、停止。
8. `07_QA_GATES_AND_PROVENANCE.md`：代码/媒体产物证据、测试与双端回读。
9. `08_FAILURE_SCENARIOS.md`：故障分类、熔断、Work 只搬运不代工。
10. `09_FIVE_AGENTS_SCHEDULING.md` 与 `agents/`：五个定时任务完整提示词。
11. `10_IMPLEMENTATION_ROADMAP.md` 和 `tests/`：上线阶段、离线验证和影子测试。
12. `templates/`、`schemas/`：规范化消息样板与 JSON Schema；`tools/validate_examples.py`：零依赖示例校验。

## 两条硬约束
- **不能把意图当成果**：CLAIM 不等于租约，提交文件不等于执行测试，通过文本检查不等于 QA 通过，自动任务 enabled 不等于真实运行。
- **默认不改现网**：本包仅标准文件和候选指令；不创建/修改/重启任何定时任务，不写现网 BOARD，不调用模型 API，不触碰既有测试结果。所有实际执行能力以工具探针+回读为准。

## 上手顺序
先在隔离分支创建项目目录并验证 A→Git、B→Git、Git→A/B 的读写与回读；再用独立 Task/Note/Event 文件完成两 Agent 接力；随后启用统一 Controller 投影和五工位错峰；最后加入 WorkBuddy/Codex QA。不能仅因 Markdown 文件存在就宣布运行系统已上线。
