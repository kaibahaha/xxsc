# 11｜能力登记、身份、许可证与风险边界

## 权限分离
`allowed_reads`、`allowed_writes`、`allowed_actions`、`credential_principal`、`repo/branch/path` 必须按 Agent 登记；GitHub Web 连接器会话权限不等于后台定时任务权限，WorkBuddy SDK/Webhook 不等于已经连接的云端执行器。本地 4060Ti 设备关机后，任何本机 API Server 都不可达，除非有独立云服务；不得臆造桥。

## Prompt 不是硬隔离
不同 Agent 即使被指示写独立路径，若 OAuth token 实际可写全仓库，仍需由 Controller、Git branch protection、GitHub App 安装范围或中间执行器在实际接口层强制权限。由 Scheduler 触发只是动作入口，不是安全边界。

## 许可
Microsoft Agensh 使用 MIT 许可。我们保留官方项目及 Commit 引用；如复制完整实现代码，随代码带原 LICENSE 及版权声明。本文重新起草的中文改编规则不代表 Microsoft 认证。论文不因代码 MIT 自动成为 MIT 文本授权。

## 模型/API成本
ChatGPT 定时任务的实际工具可用性、运行时长、模型与额度，以当前账户及每次真实调度结果为准；不按一次聊天里可用的工具外推所有定时任务都可以调用。默认不调用付费 API，不开启自动超预算重试。先测量每有效成果成本，再扩展。
