# Agensh-Lite V4.2 · 弹性定时 Agent 池 / Controller MVP 施工指令

状态：IMPLEMENTATION-PLAN，尚非已上线运行系统。日期：2026-10-25。
源协议：../agensh-lite-v4.1/（必须阅读其 01–11、agents/COMMON.md、schemas/、tests/）。
Microsoft Agensh：microsoft/Agensh@0468a3e6a58b51dc2b84871fcaa0df22b0d1033e；按 MIT 许可证依法使用，引用见 V4.1 的 00_SOURCES_AND_ADOPTION.md。

## 首要修正：不是固定五个
目标为 N=2..5 个已启用 ChatGPT 定时 Agent，且 N 必须由配置/注册表计算，绝不在代码里假设固定有 A/B/C/D/E。用户可将未占用的计划任务名额用于 ChatGPT Work、审计或其他实验。不同配置均必须通过相同验收。五个时槽只是 N=5 时的一个示例。

核心目标：跨独立定时会话执行 GATHER → CLAIM → ACT → VERIFY → PUBLISH/HANDOFF；可继续已授权的长任务，也能在依赖满足时自由认领新任务；所有状态跨轮存储在 Git，可靠控制器处理并发、幂等与验收；无需用户本地电脑常开。

## 阅读顺序
1. config/agent_pool.example.json、docs/POOL_AND_SCHEDULING.md：弹性池配置、余量分配。
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
P0 只读探针 → P1 纯 Git 双 Agent 接力 → P2 原子 Controller+错误重放 → P3 N=2..5 动态池/热切换 → P4 WorkBuddy 测试接力/QA → P5 24h 影子运行。每阶段独立验收通过后才扩大权限或迁移现有任务。