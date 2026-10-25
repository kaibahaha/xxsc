# Agensh-Lite V4.2 · 跨平台开放式 Agent 池 / Controller MVP 施工指令

状态：IMPLEMENTATION-PLAN，尚非已上线运行系统。日期：2026-10-25。
源协议：../agensh-lite-v4.1/（必须阅读其 01–11、agents/COMMON.md、schemas/、tests/）。
Microsoft Agensh：microsoft/Agensh@0468a3e6a58b51dc2b84871fcaa0df22b0d1033e；按 MIT 许可证依法使用，引用见 V4.1 的 00_SOURCES_AND_ADOPTION.md。

## 最新需求：至少2个 Agent，数量无系统级上限
ChatGPT、WorkBuddy、Codex、ChatGPT Work（有真实权限时）及其他厂商可以混合加入共享任务池。**总池 N>=2（含2）且没有全局 max_active=5 上限**。每个 Provider 的配额、调度、鉴权、执行能力独立管理；ChatGPT 五个名额仅是一个用户待核实的平台配额示例，不是全系统上限。每个 Agent 须注册独立身份/能力/触发方式，并在探针核实后获得准入资格。配置的 desired_enabled 不是已上线证据。示例：3 ChatGPT + 2 WorkBuddy + 1 Codex = N=6。

核心目标：跨独立定时会话执行 GATHER → CLAIM → ACT → VERIFY → PUBLISH/HANDOFF；可继续已授权的长任务，也能在依赖满足时自由认领新任务；所有状态跨轮存储在 Git，可靠控制器处理并发、幂等与验收；无需用户本地电脑常开。

## 阅读顺序
先读 `docs/AGENT_ADAPTER_CONTRACT.md` 与 `config/mixed_pool.example.json`，两者是本次用户修正后的必读合同。
1. config/agent_pool.example.json、docs/POOL_AND_SCHEDULING.md、docs/MULTI_PROVIDER_AGENT_REGISTRY.md：开放式异构注册、配额与排班。
2. docs/PROJECT_MODULES.md：10 个开发模块、拆分、接口与验收定义。
3. docs/CLOUD_CONTROLLER.md：Git+Controller 可行实现边界、正确性与故障回退。
4. dispatch/CODEX_MASTER_TASK.md：Codex 技术设计/高复杂度模块任务指令。
5. dispatch/WORKBUDDY_BUILD_TASK.md：WorkBuddy 工程实现/集成/测试任务指令。
6. tests/ACCEPTANCE_MATRIX.md：必须出具真实自动化日志的验收矩阵。

## GitHub 仓库绝对逻辑定位
REPO=kaibahaha/xxsc
DEVELOPMENT_BRANCH=exp/agensh-lite-v4.2-controller-mvp-20261025
ROOT=/frameworks/agensh-lite-v4.2/
REFERENCE_PROTOCOL=/frameworks/agensh-lite-v4.1/
PROPOSED_RUNTIME_ROOT=/factory/
不得改 main、此前 SENIOR-LEDGER 盲测分支或微软原仓库。

## 当前不是已部署
此次只提交开发计划与模板；没有创建实际 ChatGPT 定时任务、没有接通 ChatGPT → WorkBuddy 云端 webhook、没有宣布代码测试通过。开发者须从零建设并以真实运行日志证明所声称能力。若云端执行能力/权限不存在，记录 BLOCKED_CONNECTOR、不得伪造成功。

## 单一版本路线
P0 只读探针 → P1 纯 Git 双 Agent 接力 → P2 原子 Controller+错误重放 → P3 N>=2 动态异构池/热切换 → P4 ChatGPT→WorkBuddy 跨平台接力/QA → P5 24h 影子运行。每阶段独立验收通过后才扩大权限或迁移现有任务。