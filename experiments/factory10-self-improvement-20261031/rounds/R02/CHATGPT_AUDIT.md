# R02 F2｜ChatGPT独立审计｜2026-10-31
- Experiment: FACTORY10-SELF-IMPROVEMENT-20261031；本实验R02=F2首次基线。
- WorkBuddy job: `762c8f0887fc4188`，MCP状态DONE，463秒，实际返回15843字符，含BEGIN_FULL_REPORT/END_FULL_REPORT；Git WORKBUDDY_REPORT.md已写入并逐字回读，blob `f77061fc03d218c782960342e78adde3a0c9fd28`。
- 前一小时R01/F1：Job aab758d7c33d4631 DONE，但仅摘要、正式NOT_EVALUABLE；本轮不将其分数与F2相减。
- 同专题旧实验F2 R02：Job f77da8aaab28496d，旧审计81/100（22/18/16/15/10），仅HISTORICAL_REFERENCE；本轮新实验F2的R12才是正式同厂纵向比较。
- **本轮评分：76/100，CONDITIONAL_ACCEPT_FOR_RESEARCH / NOT_READY_FOR_EXECUTION。** WorkBuddy自评“六项全部RESOLVED”未获独立认可。

## 一、固定五维评分
| 维度 | 满分 | 得分 | 独立理由 |
|---|---:|---:|---|
| 证据与事实 |25|21|全文MCP回传、官方来源索引S1-S12与环境检查自述明确；但没有CLI原始stdout/退出码，S1被引用为“明确说不是安全沙箱”并非原文准确措辞；AGPL/漏洞样例有过度简化；S13/S14未核。|
| 工厂战略契合 |20|18|契合Markdown合同→代码→Git→审计→恢复，明确零安装路径和工具分层；成本“≈0”未计推理/运维/人工，GitHub连接器已授权在ChatGPT侧但Buddy只标CLAIMED。|
| 技巧与可执行性 |20|14|提供候选分层、权限模式和样例命令；但本机git/docker/scanner缺失，案例B的`-p --permission-mode dontAsk`与官方Headless“授权操作需要-y”存在版本/文档冲突，且`-y`官方等价bypassPermissions，不能未验证便认定组合有安全性；Case A纯`codebuddy -p`读网络亦可能被拒；B PR实际无法执行。|
| 五案例质量 |20|14|A-E均有输入/输出/正反例/回滚/阻塞/状态；A未冻结真实仓库/未运行，B权限未负例实测，C无OS隔离，D合成样本缺规则匹配证明且许可证不能仅靠import认定违规，E状态机/幂等仅概念级。|
| 风险、成本、真实性 |15|9|坦承NOT_TESTED/BLOCKED并区分授权；但“全部RESOLVED”过度自评；Case C建议`rm -rf .codebuddy/worktrees/*`可能删除其他工作树，不能作为安全回滚；无沙箱本机启用/OS拒绝证据。|
| **合计** | **100** | **76** | **研究文档可用于设计迭代，不代表已验证代码工厂或安全隔离。** |

## 二、官方来源交叉核验与新发现
1. `https://www.codebuddy.cn/docs/cli/worktree` 的“安全隔离”是工作目录改动隔离，并未提供OS级防越目录读写的保证。旧审计指出“worktree不等于防作弊安全边界”正确；本轮报告§4 S1声称官方“明确写出不是安全沙箱、权限与主Agent相同”是**过度精确的引述**，需改为“文档描述工作区隔离，未证明OS访问控制”；官方权限/沙箱分别见 `https://www.codebuddy.cn/docs/cli/permissions`、`https://www.codebuddy.cn/docs/cli/bash-sandboxing`。
2. `https://www.codebuddy.cn/docs/cli/permission-modes` 明确`dontAsk`对未预批准操作拒绝，`-y`等价`bypassPermissions`；`https://www.codebuddy.cn/docs/cli/headless`明确`-p`在执行需授权文件读写/命令/网络时要求`-y`，但官方也展示不带`-y`的`dontAsk`示例。**文档内部存在使用语境差异，不能未经真实CLI测试就声称Case B可按设计安全执行**。须隔离环境跑只读help与合成权限拒绝测试。
3. `https://www.codebuddy.cn/docs/cli/permissions` 说明`--add-dir`是增加信任目录而非强制隔离，Bash间接写入不被Edit规则挡住，外部OS边界必要；官方`Bash(git:*)`与路径`//tmp`有特殊语法，Case B应验证CLI接受的真实参数和优先级。
4. `https://docs.github.com/en/rest/apps/installations`支持GitHub App安装及按仓库授权；ChatGPT的GitHub连接器本轮实际读写此实验分支，WorkBuddy本机无git/未授权GitHub插件，不能把二者混淆。
5. `https://www.gnu.org/licenses/gpl-faq.en.html`要求按复制、修改、分发及网络服务条件分别判断GPL/AGPL义务。报告Case A“GPLv3修改须同源”“AGPLv3网络服务须提供对应源码”措辞过宽，需按具体覆盖作品、触发条件、义务范围及例外收窄；无许可证不得自动当成可复用。
6. Case D“`from aggplib import *`=AGPL违规”不成立：使用许可证组件不等于违反义务；`requests==2.31.0`无已知CVE与`sk-1a2b3c...`能被扫描器检出均未经规则版本验证。应采用明确的CVE/规则ID、版本化正负夹具、真实退出码。不能用6个设计样本宣称检测能力。
7. Case C建议`rm -rf .codebuddy/worktrees/*`作为回滚不安全，可能误删其他任务的worktree。应按创建时记录的唯一worktree ID/path，调用官方受控移除工具或逐一检查后清理，禁止全目录通配删除。
8. §3将OS级Bash sandbox标为“立即可用”，仅凭官方存在`/sandbox`并未验证本机bubblewrap及策略有效性，需改为`AVAILABLE_IN_DOCS / ENV_NOT_VERIFIED`。Case E状态机缺failed/cancelled/expired等边界，未实测远端超时和重叠防护。

## 三、SAME_FACTORY_REMEDIATION：历史六项问题独立复核
| 历史缺陷 | WorkBuddy自评 | ChatGPT复核 | 理由/下次验收 |
|---|---|---|---|
| F2-P0-01 工作区≠安全隔离 |RESOLVED|**RESOLVED（概念层）**|本轮明确工作区与OS隔离区别、C标BLOCKED；实际OS盲测仍未验证，不能宣称安全通过。|
| F2-P0-02 无人值守权限过宽 |RESOLVED|**PARTIAL**|提出dontAsk与白名单，但`-p`/`-y`兼容和真实拒绝日志缺失；须实际权限负例。|
| F2-P1-03 GPL/AGPL一刀切 |RESOLVED|**PARTIAL**|提供五类许可矩阵方向，但GPL/AGPL义务仍过度概括，需法律触发条件矩阵。|
| F2-P1-04 工具缺失未披露 |RESOLVED|**RESOLVED（证据分级）**|五案例均明确READY/BLOCKED/DESIGN_ONLY/NOT_TESTED，环境命令自述可复查；不等于案例可运行。|
| F2-P1-05 门禁“100%检出”无实测 |RESOLVED|**PARTIAL**|不再虚报检出率，但合成样本设计有假阳性/假阴性与许可证推断错误，须规则ID与退出码。|
| F2-P2-06 商业优先级/成本 |RESOLVED|**PARTIAL**|按可用性排序，但零成本未计人工/云资源；ChatGPT连接器实际已写Git，WorkBuddy未授权需继续分开计。|
- historical_defects_count=6; **resolved_count=2（概念/披露层）**; partial_count=4; recurred_count=0（按旧错误原句未直接复述口径）；new_issues=4组（权限命令可执行性、样本真实性、沙箱可用性、危险回滚）。
- 解决率严格口径2/6=33.3%，**不是旧F2 81分→新F2 76分的“倒退5分”因果证据**：研究焦点、证据覆盖、评分严格程度均不同。R02本实验基线76/100，R12同厂第二轮再做可比差值。

## 四、跨小时通用方法迁移 R01→R02（实际注入与效果）
| method_change | R01基线 | R02目标 | R02实测 | 结论 |
|---|---|---|---|---|
| M1 全文MCP可读、Git可回读 | 远端382行仅1517字摘要、NOT_EVALUABLE | 100%正文回传与Git回读 | R02 MCP返回15843字符、BEGIN/END齐全；Git WORKBUDDY_REPORT.md 16123字符，blob f77061fc...，全文逐字回读 | **EFFECTIVE（交付层）** |
| M2 官方版本核验与五案例负例+回滚 | R01案例正文不可读 | 关键主张≥90%可追溯，5/5含负例/回滚 | 5/5案例字段具备；官方链接索引S1-S12，但若干断言与官方细节不符、样例未执行 | **PARTIAL_EFFECTIVE（形式与透明度），实际正确性未达标/≥90%不可独立证实** |

R02比R01更可审计，证明**交付机制**改善，不证明跨工厂研究准确性必然提升。未直接观察WorkBuddy CLI stdout或实际权限沙箱日志，不能冒充独立远端实测。

## 五、五案例逐案审计与R12整改要求
- A 开源解构：保留冻结commit/SPDX矩阵，但必须给真实仓库commit、依赖树/许可证原始文件、CLI/urllib实测退出码；许可证义务按具体行为判断；不能以“网络可达”替代目标仓可读取。
- B Markdown合同→PR：安全设计方向保留，必须在隔离环境核对`-p`+`dontAsk`+`-y`的实际权限优先级与白名单参数；以合成越目录/越权写/push失败日志为证；不能仅凭禁令保证安全；缺git则BLOCKED。
- C 多Agent盲测：OS隔离仍BLOCKED；不把worktree当安全边界；移除`rm -rf .codebuddy/worktrees/*`，以独立身份/容器/网络权限拒绝日志验收。
- D 供应链门禁：正负样本应来自真实规则ID和受影响版本；许可证义务不可用import判违规；未装scanner时只做测试协议，不能宣称门禁通过。
- E 桥接器恢复：保留固定快照/Job幂等/写回读分离；增加failed/cancelled/expired、远端仍运行的orphan风险、429冷却、队列TTL、进程重启后持久化恢复；只允许隔离模拟，不触生产。

## 六、R03 F3跨专题继承：最多2项
- **M1证据强度分层**：所有核心能力/插件/引擎声称必须区分“官方文档存在 / 本环境真实安装 / 已实际执行 / 已通过独立验收”；涉及权限/隔离/许可证/计费时至少给出一个官方反例或失败边界；目标≥90%核心断言有官方URL与版本，且不把设计当实测。
- **M2可执行案例的反例质量**：五案例5/5含明确输入/输出/失败/回滚/成本/授权/运行状态；负例必须能对应真实工具、规则或确定性模拟，不用“看似异常”的字符串冒充测试成功；目标5/5字段齐全，至少1个案例有真实可复现的只读命令或确定性测试输出（若未执行标NOT_TESTED）。
- 下一轮F3游戏互动重点验证游戏引擎运行/模拟随机种子、资产许可、玩家行为与NPC逻辑、自动化试玩；不要机械复用F2的Git/PR业务细节。

## 七、最终判断
**76/100：完整报告交付已真实改进，内容仍有需整改的技术准确性与安全边界问题。** 本轮未安装/授权/修改生产；Git已保存WorkBuddy真实完整报告并回读，ChatGPT审计独立完成。R12必须逐项回测上述六项历史缺陷与新问题；R03应继承M1/M2研究方法而非F2业务结论。
