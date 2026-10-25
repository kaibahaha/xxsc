# P1 修复回归与反例记录

源码固定于 `acc39e97ba4281197bcc65e2a7187a994e8b81f0`。完整执行命令、stdout/stderr、退出码见 REVIEW_FIX_R01_TEST_RESULTS.txt。

| 阶段 | 实际结果 | 证据 |
|---|---|---|
| P1-01 修复前，208e20f 基线 | 4 失败，exit 1；等待/重启后 QA 状态变 READY | REVIEW_FIX_R01_P101_BEFORE.txt/.xml |
| P1-01 核心修复后定向验证 | 新 4 + 原知识/QA 10 = 14 通过，exit 0 | 开发工具执行记录；正式全量日志覆盖同用例 |
| P1-02 修复前，已落 P1-01、尚未改 bootstrap | 2 失败，exit 1；新 Registry 重启发生 COMMAND_ID_COLLISION | REVIEW_FIX_R01_P102_BEFORE.txt/.xml |
| P1-02 核心修复后定向验证 | 2 通过，exit 0 | 开发工具执行记录；正式全量日志覆盖同用例 |
| 完整固定提交正式回归 | **原 90 + 新 26 = 116 通过，0 失败/错误/跳过，exit 0** | REVIEW_FIX_R01_TEST_RESULTS.txt、REVIEW_FIX_R01_RESULTS.xml |
| 本地演示及 whitespace 校验 | demo exit 0；git diff --check exit 0 | 同上原始日志 |

新增 26 项按 JUnit 分组：P1-01 15 项，P1-02 11 项。所有跨小时测试使用确定性逻辑时钟，没有真的睡眠一/两小时；真实底层为持久 SQLite、Python 线程与进程。Provider 身份仍为测试夹具。

| 不变量 | 新增覆盖 |
|---|---|
| 跨小时不丢 QA 候选 | 超过 3600 秒后 B 可合法申请 QA，原 candidate/spec/author 保留 |
| QA_GREEN 不依赖开发者在线 | 两小时后 C 申请 Review；作者 OFFLINE/DRAINING、重启、新库恢复均保留 qa_evidence |
| 五个验收阶段到期只撤权 | SUBMITTED/QA_PENDING/QA_GREEN/REVIEW_APPROVED/INTEGRATION_VERIFIED 分别实测，旧 epoch 拒绝、新 grant 正常 |
| 无新授权旁路 | 借别人的 token、错误 candidate commit、缺角色、缺读取范围、离线身份被拒绝；只读 QA 不能 SUBMIT 代码 |
| 并发仍排他 | 新增 100 路 QA 阶段申请只一个 GRANTED；原执行阶段 100 路争抢及独立进程测试继续通过 |
| 幂等重放不倒退业务状态 | 旧 QA 已接受命令重试只返回历史回执，不再应用变化，当前 REVIEW_APPROVED 和日志保持不变 |
| 冷启动不重新初始化 | 2→6、6→10、2→6→10 连续版本更新后重启，snapshot 和完整原日志前缀一致 |
| 启动配置不是授权 | 仅传入 10 人配置，持久 2 人状态不变，新 ID 不可申请；不能从模拟/生产模式切换获取权限 |
| 注册表修改受权、CAS、幂等 | 无 registry_admin 拒绝；过时 expected_version 拒绝；相同请求不重做；不同请求并发同版本仅一个成功 |
| 退场/恢复不复活 token | 停用后无新 lease，恢复须版本化授权，重新申请的 epoch 更高，旧 token 拒绝 |
| Provider 额度隔离且事务回滚 | WorkBuddy/Codex 可分别加入，ChatGPT 超自身额度拒绝；无效 quota 缩减不改变身份、任务、消息和 ACK |

原90项的全部测试函数/断言保持与基线一致，AST 校验记录见 REVIEW_FIX_R01_INTEGRITY.json。只改共享 move() 夹具以履行新的阶段授权协议；新增授权攻击测试直接调用 claim/transition，未通过夹具偷偷获取新 token。

执行回归不需要真实云凭据。真实 Git CAS/回执与云端授租未纳入本地 PASS，R02 项仍未完成。
