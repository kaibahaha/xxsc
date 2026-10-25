# V4.2/R01｜Codex + WorkBuddy 双工位正式开发派单

状态：AUTHORIZED_FOR_ISOLATED_DEVELOPMENT（只授权隔离开发分支/验收测试，不授权上线、生产调度或合并 main）
项目：kaibahaha/xxsc
工单基线分支：exp/agensh-lite-v4.2-controller-mvp-20261025
规范主目录：frameworks/agensh-lite-v4.2/
微软来源：microsoft/Agensh@0468a3e6a58b51dc2b84871fcaa0df22b0d1033e
注意：工单基线 SHA 由发布此文档的最终 Git commit 确定；执行者必须在领取时记录实际精确 SHA，不得以可变分支名代替记录。

## 只分两张互不重叠的首轮开发工单
- AGL-CODEX-CORE-R01：Codex 主责 M01/M03/M04/M05/M07/M09，Controller/协议/并发一致性/事件重放。看 workorders/AGL-CODEX-CORE-R01/TASK.md。
- AGL-WB-ADAPTERS-R01：WorkBuddy 主责 M02/M06/M08/M10，GitHub 原生仓储适配、按需轮询/调度、云端 Runner 能力探针、CLI/CI。看 workorders/AGL-WB-ADAPTERS-R01/TASK.md。

## 指令优先级
用户最新口头指令（跨平台 N>=2、总数无人工固定上限） > 本轮工单 > docs/AGENT_ADAPTER_CONTRACT.md、docs/MULTI_PROVIDER_AGENT_REGISTRY.md、docs/POOL_AND_SCHEDULING.md > docs/PROJECT_MODULES.md、tests/ACCEPTANCE_MATRIX.md > 旧 V4.1 方案。若存在相互矛盾的硬约束须列出裁决，不得悄悄沿用旧 N<=5 限制。

## 手动认领方式（当前无 Controller，因此这是工单记录而非 lease）
1. 阅读本轮 TASK.md 以及全部 REQUIRED_READS；先通过 GitHub 真实读取验证 repo/branch/基线 SHA。
2. 从冻结的工单基线创建自身独立开发分支；如分支已存在，检查其创建历史后再继续，禁止强推。
3. 在自身分支写 workorders/claims/<TASK_ID>/<AGENT_ID>/<RUN_ID>.md，含 STARTED、时间、基线 SHA、分支、承诺的文件边界；提交并写后回读。
4. 工作只能在该独立分支、自己负责的路径下进行。工单完成后 PR 指向上述工单基线分支（不是 main）。
5. 把源码、测试、操作日志、真实 Git commit SHA、读回证据、已知阻断放入指定 deliveries 目录；没有真实运行的内容标 NOT_RUN/UNKNOWN/BLOCKED。

## 二者协作防冲突
同一 Git 基线并行开发；Codex 拥有 core/schema/events/leases/state/memory/handoff/audit；WorkBuddy 拥有 storage/adapters/poll/execution/cli/integration harness。不要互相编辑对方文件。统一数据协议见 workorders/INTERFACE_HANDOFF.md。第一次交付以独立模拟可运行测试 + 冻结契约为主；集成时通过另一轮受控 PR 解决依赖，**禁止两个分支谁先做完就强推共享分支**。

## 审查与合并
用户把两个 PR/精确提交 SHA 发给负责验收的 ChatGPT 聊天，我会重新用 GitHub 工具逐文件看源码、测试、日志、回读、检查清单，给逐项 PASS/FAIL/BLOCKED 与修改要求。写作成果不等于代码可运行、PR 创建不等于 QA 通过。没有显式合并授权不合并 main 或生产代码。

## 禁止
禁止改 main、历史盲测分支、V4.1 源规范；禁止未经用户批准创建 ChatGPT 定时任务、GitHub 线上定时 workflow/云端收费实例，禁止执行真实付费 API；不得绕权限检查或上传密钥；离线模拟不许写成真实跨平台接力完成。