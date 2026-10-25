# AGL-CODEX-CORE-R01 实际交付报告

> P1 Review 后续已修复：请优先读取 REVIEW_FIX_R01_REPORT.md 与 contracts/README.md 的当前阶段授权/版本化注册表约定；本文件其余内容保留首轮交付记录。

状态：**SELF_TESTED / INTEGRATION_PENDING / BLOCKED_ATOMIC_LEASE（云端）**。

已交付可运行 Python 核心及 90 项实际通过测试，失败 0、跳过 0，pytest exit_code=0，耗时 2.75s。源码和测试提交为 `001a7f2db4ea9d1ef3c6e164456d900a0cb7d41c`，完整输出见 TEST_RESULTS.txt，机器可读结果见 pytest-results.xml。之后的提交仅归档交付证据；本报告不尝试自引用其所在提交 SHA。最终分支 SHA 可从 PR head 和 Git 回读取得。

PR：https://github.com/kaibahaha/xxsc/pull/1 （Draft，未合并）；head `dev/agl-v4.2-codex-controller`，base `exp/agensh-lite-v4.2-controller-mvp-20261025`；冻结基线 `2d4c1a6fc0792a1182777262b41bfb4c09c0b5d2`。手动认领提交 `f3c1c18`，首版合同提交 `4728f69`，最终合同随上述源码提交冻结。

实际环境：本次托管云开发容器 `/workspace/xxsc`，Linux 6.18.55 x86_64 / glibc 2.41，Python 3.12.14，SQLite 3.53.1，pytest 9.1.1。运行核心仅依赖标准库；V4.1 导入边界及测试使用 jsonschema 4.26.0。Python 3.11 未实际运行测试。开发容器测试通过不代表云端 Controller 已部署。

| 模块 | 实际代码 | 已验证能力 |
|---|---|---|
| M01 | factory/agl/config.py、schemas.py、registry.py、contracts/ | 动态池、独立身份/权限/健康、Provider/account 配额、严格路径与 ref、版本与 V4.1 导入 |
| M03 | events.py、controller.py、leases.py | 事件碰撞检测、多目标处理回执与 ACK、按 Agent/source 连续水位、因果 ACK 门禁 |
| M04 | controller.py、task_state.py、leases.py | DAG、优先级与老化、WIP、短事务授租、版本/epoch/期限、角色验收门禁 |
| M05 | memory.py、context.py | 五类知识、同版本 FAIL 阻断、有限 HOT/WARM 与完整 COLD 索引 |
| M07 | handoff.py、context.py | 不可变交接、冷启动恢复、失效 attempt 只读与重新认领 |
| M09 | audit.py、replay.py、leases.py | 哈希链审计、确定重放、新库恢复、孤儿回收、未知写入对账、relay grace 纯判定 |

最低验收实际证据：

- N=2/3/4/5/6/8/10/12/20 配置测试通过；另测 3 ChatGPT+2 WorkBuddy+1 Codex，及 3 ChatGPT+7 WorkBuddy 的 10 人池。身份是模拟数据，未声称真实 Provider 已准入。
- 100 个线程、独立 SQLite 连接、三种 Provider 争抢同一任务，只产生一个有效 GRANTED；另测 12 个独立进程承载 24 个请求。
- 到期、旧 epoch、旧 grant/renew 重试、非持有者、时钟倒退、权限/依赖不符均不能推进任务。
- 重复事件、碰撞、跨目标 ACK、乱序 ACK、丢 ACK 后重启 ACK_ONLY、随机故障重放、新数据库恢复均通过。
- 真正执行子进程在 append 后/commit 后 os._exit(73)，分别验证回滚和持久恢复；不是只抛异常模拟进程退出。
- 正面 QA 状态机测试执行了本地 Python 子进程并核验日志 hash；任务 SHA 与 Provider 身份是隔离测试夹具。它不构成本交付的独立 QA，也不构成真实外部 Runner 接入。

Git clone/fetch/分支创建/commit/push 均真实执行；连接器实际报告仓库 pull/push/admin 权限。GitHub API 已独立回读合同文件，原始内容和 blob SHA 在 GITHUB_SOURCE_READBACK.json；PR 创建回执在 PR_CREATED.json。最终交付还将通过新的 fetch/逐文件哈希核验，结果随最终回复报告。

未改 main、冻结协议或 WorkBuddy Adapter/CLI/执行代码；未创建定时任务、生产服务、付费资源。SQLite/WAL/SHM 未入 Git。没有把本交付标为 QA_GREEN、没有冒充生产上线。

阻断与后续：见 BLOCKERS.md 和 NEXT_HANDOFF.md。完整跨平台验收、Git mailbox 运行闭环、独立 QA、GitHub Actions 实验及 24h 影子运行均未完成，不能将 V4.2 全矩阵签绿。
