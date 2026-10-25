# R01 Review P1 修复报告

本轮仅修复 P1-01/P1-02。PR #1 保持 Draft，不请求合并；云端授租/真实 Git CAS、后续验收证据门禁和配置样例清理由 R02 继续负责。

- Review：https://github.com/kaibahaha/xxsc/pull/1#pullrequestreview-5643961756 。已通过 GitHub 接口读取正文，回执见 REVIEW_FIX_R01_REVIEW.json。
- 修复前 PR HEAD：`208e20f70e8c8f38ca6da87751534ab1e8d6dc09`。首次核验和推送前 fetch 均确认无新增远端提交；未覆盖其他人的修改。
- P1-01 提交：`6c48167`；完整修复源码/测试提交：**`acc39e97ba4281197bcc65e2a7187a994e8b81f0`**。后续提交仅归档本轮证据，最终 PR HEAD 由完成后的 Git/API 回读报告，避免报告自引用提交 SHA。
- 正式运行：2026-10-25T16:06:51Z；托管开发容器 Linux，Python 3.12.14，SQLite 3.53.1；实际 pytest **116 passed in 5.84s，exit_code=0**。原有 90 项 + 新增 26 项，均无失败/错误/跳过。环境与分组统计见 REVIEW_FIX_R01_ENVIRONMENT.json；原始输出及 JUnit 分别为 REVIEW_FIX_R01_TEST_RESULTS.txt、REVIEW_FIX_R01_RESULTS.xml。

## P1-01：阶段事实不能随执行租约过期被清零

根因：旧 `expire_tasks()` 对所有非空过期租约调用 `invalidate()`；后者混合了撤销写入权与删除候选结果的操作。原开发 lease 一直延续到 DONE，导致等待 QA 或 Review 跨小时后，状态变 READY，candidate_commit/author/qa_evidence 被清空。

最小修复：

1. task_state.py:45 的 `revoke_lease()` 仅增加 epoch/version、撤销 lease/lease_phase；:70 的 `retire_authority()` 对 SUBMITTED、QA_PENDING、QA_GREEN、REVIEW_APPROVED、INTEGRATION_VERIFIED 和 DONE 保留业务事实。执行阶段未完成工作仍按旧规则回 READY；`invalidate()` 只用于真正的重置路径。
2. task_state.py:61 的到期恢复和旧 journal 升级只撤销等待阶段的旧授权，不修改已提交/验收的事实。旧记录中无 lease_phase 的开发 token 即使尚未到期，也会在恢复时撤销，不能拿来跨阶段写入。
3. controller.py:233 的现有 `claim()` 接口支持申请当前验收阶段授权：绑定当前 task version/spec/candidate commit、角色、准入、读范围、独立身份、WIP、短期限和新 epoch；DTO 字段不变。开发执行仍检查开发能力和写范围；QA/Review 角色不因此获得开发写权限。
4. controller.py:300 的状态推进要求当前授权持有人、当前阶段、epoch、version、spec 和 commit。完成提交或一个验收阶段即释放其 token；下个阶段需要新的 claim，等待本身不占租约。不通过无限续租绕过：TTL 上限仍为 3600 秒。
5. controller.py:128 的注册表权限/健康修改撤销受影响身份的旧授权，复用阶段保留逻辑；原开发 Agent 离线不会撤销别人已经确认的 QA/Review。

修复前：四个新增测试真实失败，分别见到 QA_PENDING/QA_GREEN 被退回 READY；日志/JUnit 为 REVIEW_FIX_R01_P101_BEFORE.txt/.xml。修复后：同四项加五阶段授权过期、token 所有权、candidate 绑定、读权限、100 路阶段抢租、旧回执重试等共 15 项全过。时钟跨越一/两小时由注入的逻辑时钟确定性推进，实际执行的是本地事务/线程/进程；没有谎称真实等待两小时或真实云平台接力。

## P1-02：首次初始化不能冒充注册表配置升级

根因：构造器固定复用 `bootstrap` ID，且请求 hash 包含可变注册表与 quotas。已有数据库扩容后，以新的 6/10 人配置重启会发生 COMMAND_ID_COLLISION；简单更换 bootstrap ID 又可能误覆盖持久状态。

最小修复：

1. leases.py:65 的事务初始化路径在同一个 `BEGIN IMMEDIATE` 锁内检查空账本。仅空库执行 bootstrap；已有库校验 genesis 并只返回已持久化运行模式，不再比较可变启动请求、更不重写状态或追加第二次初始化。普通命令幂等碰撞检测保持不变。
2. controller.py:17 的构造器加载已存在的权威状态；新传入 Registry 只是意图，不能私自加人、停人、改权限或 quota。模拟/生产模式固定于持久库，启动时请求改模式会被拒绝。
3. controller.py:157 新增 `apply_registry(..., expected_version=..., quotas=...)`：registry_admin 鉴权后进行版本 CAS、受审计 upsert、完整合并校验和 provider/account 独立配额验证。缺省行不会删除历史身份，停用和恢复都必须显式提交。旧 journal 缺版本时按隐式版本 1 读取，首次受权变更再持久版本，不做启动写入迁移。
4. controller.py:175 的单个 register 保留旧签名，新增可选 expected_version；相同身份相同内容返回 DUPLICATE，不产生新身份，不推进配置版本；冲突内容拒绝。降级专用 update_health 也沿用共享注册表版本。完整配置更新/恢复必须通过强制版本检查的 apply_registry。旧兼容 API 只提供单项增加/降级，不允许静默覆盖或无版本恢复权限。
5. controller.py:128 复用现有 AgentRegistry 配额/准入校验，不引入第二套注册表。已存在 ID 不可重绑定 provider/account/principal；任何有效权限/准入修改都撤销旧 token；停用后恢复也不能复活旧 epoch。TASK/EVENT/ACK/HANDOFF/历史 lease 日志保留。

修复前：2→6 和 6→10 两个扩容后重启用例真实失败，均为 COMMAND_ID_COLLISION；日志/JUnit 为 REVIEW_FIX_R01_P102_BEFORE.txt/.xml。此时只落了 P1-01 补丁，bootstrap/registry 尚未修复。修复后两项及批量配置、版本冲突、幂等、停用/恢复、独立 quota、权限、并发 CAS、模式保护等共 11 项全过。

## 回归完整性与交接

原有四个测试模块的全部 `test_*` 函数 AST 与 208e20f 基线相同；没有删测试、删断言或降低期望。唯一原测试文件改动是共享 `move()` 调用夹具：在验收阶段显式申请当前授权，再调用 transition。新增旧 epoch/借用 token 等安全测试直接调用核心，不经该自动申请夹具，避免它掩盖迟到结果缺陷。核对结果见 REVIEW_FIX_R01_INTEGRITY.json。

实际修改生产逻辑仅 controller.py、task_state.py、leases.py；复用 registry.py，未改 WorkBuddy Adapter/CLI/Runner。同步更新本方 contracts/README.md 说明授权与注册表版本语义；Python DTO/schema 字段没有重构。

下一步：WorkBuddy 按当前阶段重新 claim 并绑定 candidate commit，配置升级调用 versioned apply_registry；先 recover/读取状态，再 Board 对账和申请当前授权。真实 probe、Git receipt/CAS、外部 Runner 和后续 Gate 原证据核验仍见 REVIEW_FIX_R01_BLOCKERS.md；本次不能签发云端/独立 QA_GREEN。
