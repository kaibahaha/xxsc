# R12 F2 软件与开源程序工厂｜同厂R02定向整改反馈包
- 实验 FACTORY10-SKILL-24H-20261030；计划Phoenix 2026-10-29 21:00 / 北京2026-10-30 12:00；本轮固定R12/F2，不因R11补跑而变更。
- **同厂旧版R02**：Job `f77da8aaab28496d` DONE；报告 `rounds/R02/WORKBUDDY_REPORT.md`、审计 `rounds/R02/CHATGPT_AUDIT.md`、状态 `rounds/R02/STATUS.md`、反馈及ADAPTATION均已Git读取；**81/100**，五维**22/25、18/20、16/20、15/20、10/15**。本轮必须与R02比较同厂Δ、五维差和关键P0复发率（ChatGPT在取得正文后计算，WorkBuddy不自行宣布提升）。
- **R02保留优点**：37项EVIDENCE_LOG、CLI v2.177.0/209项市场缓存与0已装的分层（均为WorkBuddy自述远端CLI）、21组候选/Top5命令、五案例输入输出/负例/回滚字段完整；E25/E26/E30已纠正R01误否定原生scheduler。应保留来源级别、CLI负例和候选能力矩阵，不能把本地缓存视为安装或把ChatGPT GitHub连接器授权推定到WorkBuddy。

## R02真实缺陷逐条整改（原断言→原因→动作/官方来源→验收）
1. **P0-1 工作区≠安全沙箱**：R02案例C原话“Agent_i 只可见 dir_i 与 FROZEN_TASK.md；--add-dir 限定”，与官方 `https://www.codebuddy.cn/docs/cli/worktree` 和 `https://www.codebuddy.cn/docs/cli/permissions`矛盾；worktree仅隔离Git工作树，--add-dir扩大信任范围，不是OS访问控制。R12必须提出独立用户/容器/VM或MAC权限+只读挂载+独立凭据；明确无法在本机无docker情况下验证的BLOCKED。**验收**：尝试越目录读取、访问其他Agent答案和共享缓存的负例，要求由系统权限拒绝并附日志；不能用提示词拒绝替代。
2. **P0-2 headless自动写入授权过宽**：R02案例B建议 `codebuddy -p ... -y --permission-mode acceptEdits --allowedTools "Bash,Read,Edit,Write"`，仅禁Bash(git push)不足防越权；官方 `https://www.codebuddy.cn/docs/cli/headless`、`https://www.codebuddy.cn/docs/cli/permission-modes`。R12给最小工具/命令允许集、分支保护、GitHub App按仓库授权、PR人工审批和隔离runner方案。**验收**：git push、访问凭据、错误分支、危险网络请求四类负例均由系统/服务端拒绝；不执行实际生产写入。
3. **P1-3 GPL/AGPL过度禁止**：R02案例A将GPL/AGPL统一“禁止直接复制”，不符 `https://www.gnu.org/licenses/gpl-faq.en.html`。R12应按SPDX许可证+复制/修改/再分发/链接/网络服务/商业销售场景建立MIT、Apache-2.0、GPLv3、AGPLv3、无许可证矩阵。**验收**：每类列条件义务/阻断/人工法律复核，不能一刀切；许可UNKNOWN不得直接复制。
4. **P1-4 运行环境阻塞**：R02 E21称无git、uv/uvx、docker、扫描器；A/B/C/D命令未能实际运行。R12先用只读CLI help/which核查最新环境，给无需本机git的GitHub只读API路线及审批后可部署路线；不得因为缓存里有插件就宣称已安装。**验收**：五例逐案依赖、阻塞状态、替代路径和成本；运行未发生一律PLAN/BLOCKED。
5. **P1-5 供应链门禁“100%检出”无实测**：R02案例D以少数示例声称100%负例检出目标，且AKIA样本不证明真实密钥覆盖。R12用合成凭据/已知脆弱依赖/无害代码夹具，记录每类≥3正负样本、误报/漏报、扫描器版本、CI实际block与warn区分；未安装则只设计夹具，不能称PASS。**验收**：测试矩阵及可重放源码/输入/stdout/exitcode或NOT_TESTED。
6. **P2-6 商业优先级**：R02 Top5工具选型未考虑本环境缺git/docker、ChatGPT已连接GitHub可用、CodeBuddy市场插件未安装及实际费用。R12按“零安装GitHub只读→Markdown合同→静态审计→隔离测试→PR审批→CI发布”重排并给可核成本/权限表；未知价格标UNKNOWN。

## R02五案例逐案反馈（每案必须逐项回应）
- **A 开源仓库解构**：保留只读架构/许可证/SBOM-lite，输入owner/repo+冻结commit，输出ARCHITECTURE/DEPENDENCY/LICENSE/SOURCE_LOCK；补五种许可证场景与缺LICENSE负例、第三方依赖层级、版本漂移、时间/费用、回滚到冻结SHA；禁止冒称非标准SBOM为SPDX/CycloneDX。
- **B Markdown合同→PR**：保留CONTRACT.md AC1–AC5→PATCH.diff→TEST_RESULTS→PR_REVIEW→Git readback；重做最小权限和人工审批，测试失败/越权/错误分支/重试重复提交负例；未授权只提供方案，不自动push。
- **C 多Agent盲测**：重做隔离：冻结题目哈希、不同系统身份与不可见答案、独立runner/容器或VM；输出匿名结果/隔离访问拒绝日志/评分；无OS级隔离标普通并行对比，不得声称可信盲测。
- **D 安全供应链门禁**：保留负例驱动，合成密钥/漏洞/许可证样本集，输出GATE_MATRIX/误报漏报/RULE_VERSION；至少3正负样本/类、真正CI阻断、签名与回滚；无扫描器标BLOCKED。
- **E 桥接器可靠性只读审计**：最贴近当前项目，输入冻结源码SHA与submit→queued→running→done/failed→Git commit/readback事件流；输出EVENT_LOG/DEDUP/STATE_TRANSITION；模拟429、重启interrupted、任务未提交CodeBuddy、队列积压、重复submit、Git写入成功但回读失败；必须不触碰生产桥接器或其他实验。时间、token/调用成本UNKNOWN需采样，回滚只在隔离模拟器。
五案例每案至少：目标、真实Skill/插件及连接状态、具体输入、操作/精确命令、输出、正反测试、阈值、权限与费用、回滚、执行状态、依赖阻塞。每案必须明确旧版不足是否已修复。

## 跨厂方法调整（只迁移方法）
- R10 F10最新完整研究76/100（18/19/15/15/9）：完整MCP正文已补交，但自述RUN的源码/输入/日志仍指向**其他实验路径**且未在本实验Git可复现；把NO FAKES Act提案当现行法，外部官方来源与本地缓存混计。R03 F3 83/100也有源码缺失；这些只用于F2方法改进，不能替代R02同厂旧报告。
- **M1 官方/现行来源先行**：所有重要安全/法律/CLI断言提供现行官方URL、版本、适用范围；外部官方、本地CLI、缓存分别计数，至少10条外部一手来源。
- **M2 工件必须可独立重放**：任何声称RUN须在报告正文内完整附最小源码、固定输入、原始stdout、exitcode、环境版本，不能只指私有目录；否则SELF_REPORTED_NOT_REPRODUCED。至少两个小型只读模拟（可用Python标准库，不安装）。
- **M3 安全与权限负例实证**：区分Git工作区、OS权限、GitHub App授权、CI执行、模型Agent权限；五案例都含越权/失败/成本/回滚/PLAN或RUN状态。不得安装插件、切模型、改任何生产或其他实验、泄露凭据。
**本轮深挖目标**：R02两个P0修复、GPL/AGPL许可精确性、可重复盲测隔离方案、桥接器队列/429与Git幂等只读模拟；候选≥12、Top5详细manifest/调用语法/依赖/费用/安全、五案例互不重复。报告必须输出“R02原句→本轮修订→证据→已解决/部分/未解决”追踪表，并列新增缺陷及未验证项。