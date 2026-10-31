# R11 F1｜FEEDBACK_TO_BUDDY｜派单前冻结（2026-10-31 20:25 Asia/Shanghai）
**实验** FACTORY10-SELF-IMPROVEMENT-20261031；**本轮** R11 / F1 API与模型服务工厂；**同厂正式基线** R01 / job aab758d7c33d4631 / 后补完整报告Git blob c6d0137ad338f031399c065190621be0d9e65d43；ChatGPT独立79/100（证据22、战略18、技巧14、案例14、风险11），审计blob beb95d74f58af7e76131ac5a7a28c9636daabad5。**跨小时来源** R10 F10 / job 6899942694c048bb / 62/100仅作跨专题方法证据，绝不比较总分因果。R10最终报告、审计、适应和状态均已Git读取。R01五案例A-E全部设计级，真实端到端0/5；R11重点转为可独立复放的API计费/权限故障注入，而不是重复架构介绍。

## A. 跨小时通用方法迁移（恰好2项，必须逐字注入MCP prompt）
**T1 完整schema与fail-closed相邻负例**。R10审计 rounds/R10/CHATGPT_AUDIT.md §D：原定6类负例×normal/-O均拒绝，但新增8类×两模式16次中12次非法输入错误exit0、4次抛出非结构化异常；布尔授权来源true也被接受，不能证明授权。根因假设：只为预设用例编程，没有完整输入契约和相邻边界。R11修复：核心MVE定义严格schema（根对象、必填字段、空值、数字/布尔区分、身份可信来源、重复ID、越界额度、负数费用、异常恢复、幂等），所有无效输入必须结构化拒绝、非零退出且无副作用；Python正常与 -O 各至少8个负例，并至少一个专门测试R10的布尔来源/空字段fail-open类比。目标16/16负例拒绝且合法正例通过；任一无效输入exit0或非结构化崩溃即FAIL；不得把单元模拟说成真实生产安全。
**T2 原始工件SHA三联+官方当前产品存续核验**。R10审计§C/D：报告源码SHA自报222568...，Git源码块实际无LF ec14e7... / 有LF a681c6... 均不符；8份冻结JSON与runner原文缺失；Adobe Story 2019已停用仍被列为2026可用候选，9项抽核1项实质错。根因假设：原始源码/输入/输出在摘要转录中不一致，未核产品当前存续。R11修复：真实MVE源码、冻结输入、runner、原始stdout/stderr、exitcode、输出工件均交付实际字节或完整可复制正文，SHA256由真实文件计算；给出文件→SHA→运行命令→输出映射。对≥5项高影响主张用官方具体文档核验当前版本、日期、费用单位、商业许可和存续状态；不可核标NOT_VERIFIABLE。目标原始工件SHA一致1/1，事实实质错误0/≥5；任一SHA不符/停用产品当现行即FAIL。上一轮方法质量结果：T1 PARTIAL_EFFECTIVE、T2 FAILED_ARTIFACT/PARTIAL_FACT；本轮先实施，效果须等独立复验。

## B. 同厂R01具体缺陷登记与最高优先级整改（3项；不得用跨厂方法代替）
**P0-F1-01｜--fallback-model命令与运行模式冲突**。R01报告§5.5原文：“`--fallback-model`、`security-scan --auto` 在官方CLI文档中未找到对应项（UNVERIFIED是否真实语法）”；R01独立审计明确旧实验F2 E33曾报告 `codebuddy --help` 列出 `--fallback-model`（可能只在`--print`有效），存在版本/模式差异。根因：把“文档未找到”误当“CLI不存在”，没有完整help和版本锁定。修复：在当前云端只读执行 `codebuddy --version`、`codebuddy --help`、必要时相关子命令help；记录精确原始行、版本、交互/--print/--serve的适用模式；用官方 https://www.codebuddy.cn/docs/cli/reference 和版本发布说明交叉核对；`security-scan --auto`同样验证，不得执行未知危险命令。验收：返回“存在/不存在/仅某模式/无法确认”的可复核矩阵，命令与版本匹配；不改配置，不切模型。
**P0-F1-02｜多租户预算未证明fail-closed**。R01报告§4案例C仅DESIGNED，称“数据库故障 → L2 fail-open”，又建议外加账本或provider限额，未实现；官方 https://docs.litellm.ai/docs/proxy/users 明确无数据库时预算不执行，并描述 `fail_closed_budget_enforcement` 选项及条件。根因：设计级建议没有代码级身份信任、原子扣减、并发重试/DB故障实测。修复：在隔离目录实现**最小确定性Python预算门禁MVE**，输入冻结JSON请求{tenant_id,authenticated,request_id,cost_cents,db_available,remaining_cents}，拒绝缺字段/布尔数字/未认证/DB不可达/余额不足/重复request_id/负值/越界；采用明确整数美分，不依赖assert，不触真实API、DB、云额度。至少8负例×normal/-O、1合法正例、1重复请求与1并发边界；原始stdout/stderr/退出码/SHA及实际可复制代码完整交付。验收：非法请求均拒绝且账本不变化，DB故障结构化503/非零，正常授权通过；明确SIMULATED，不得称LiteLLM已部署或多租户商业生产就绪；说明LiteLLM实际功能需版本/部署验证。
**P1-F1-03｜Sigstore/cosign OIDC验证命令不可复跑**。R01报告§4案例E给 `cosign verify --key oidc ...`，审计指出占位语法不可直接执行；且混合了CodeBuddy网关密码、企业OAuth、Sigstore证书身份。根因：签名验证模式与OIDC信任域混淆，未给证书身份/issuer/可信根和离线测试证据。修复：查 https://docs.sigstore.dev/cosign/verifying/verify/ 或官方当前文档，明确keyed与keyless验证命令、证书身份/issuer、制品摘要、失败退出条件，提供安全可复跑的**无密钥/公开样本**验证或明确DOCUMENTED；不安装未知工具、不签真实产物。验收：不得再出现 `--key oidc` 作为完整命令；至少2类错误身份/摘要负例，若没执行标DESIGNED。
**可选深化（不替代前三项）**：R01§4案例D“Collector中断本地telemetry 100%落盘”仅设计无故障注入；R01§1.2“CODEBUDDY_IS_SANDBOX变量存在证明OS隔离”逻辑不成立；R01§4案例B的HTTP 401/403只是预期而非真实调用。所有此类能力必须按DOCUMENTED/DESIGNED/SIMULATED/EXECUTED/INDEPENDENTLY_VERIFIED分级。

## C. R01五案例逐案修订，不允许只改标题
A【多模型路由】保留Agent控制面 vs LLM推理网关分层；新增版本化CLI只读验证，设计429/超时/回退的输入、期望响应、成本、回滚；若未真调标DESIGNED。
B【API契约】保留OpenAPI差异、401/403/409/429/500；提供冻结OpenAPI示例、测试命令、预期/实际状态码、CI拒绝断言与回滚；无运行服务不得称真实接口通过。
C【多租户预算】升级为本轮核心MVE，给完整可复制源码/输入/原始输出/哈希、普通/-O安全负例、并发与幂等、成本/权限/回滚；模拟≠真实LiteLLM。
D【可观测性】保留job_id→trace_id→Git commit关联；给脱敏与Collector断连的测试输入、原始证据或未执行原因、丢包/恢复策略、隐私与存储成本。
E【供应链/灰度】纠正cosign签名/证书身份，分离网关密码、企业OAuth、Sigstore；给错误身份、摘要不匹配、灰度5%→20%→100%回滚条件，未安装工具标DOCUMENTED/DESIGNED。
五案例每项必须写：输入、账号/权限、步骤、冻结命令、预期输出、实际输出或NOT_TESTED、异常/边界、计费、商用许可、回滚、验收标准、状态等级。提交“R01历史问题→修复动作→新证据→独立可核验结果”对照表，不得自称全RESOLVED。

## D. 本轮独立机会雷达V4.1/V4.2（必须交付两份Markdown内容）
额外研究F1 API与模型服务领域**全球头部**免费API/云额度/开发者计划、国际黑客松/竞赛/研究计划、Beta/模型试用、可商用合作。优先官方规则且适合个人/小团队；关注AWS Activate Founders（官方2026-06-04指南$1,000起、网站/成立年限要求）、Google for Startups Start（官方$2,000且MVP/24个月/此前额度限制）、Microsoft for Startups、NVIDIA Inception、Hugging Face推理免费额度等，不能将最高奖励当普通个人可领。严格核验地区/实体/网站/信用卡/自动计费/有效期/资格/IP/截止时区，3–8项高质量，低价值过滤。提供OPPORTUNITY_RADAR.md与ACTION_CHECKLIST.md可直接落Git的完整正文，机会状态和用户人工操作卡；不得登录、领取、注册、提交、消耗额度。未核实标UNVERIFIED。
特别关注：AWS Founders官方2026-06-04指南 https://aws.amazon.com/aws-startups/learn/applying-for-aws-activate-credits-a-step-by-step-guide/；Google Start官方 https://cloud.google.com/startup/pre-funded；LiteLLM官方预算 https://docs.litellm.ai/docs/proxy/users。上述只是研究线索，不能代替当期核验。

## E. 任务约束与输出验收
最多12次外部检索、1子代理，8–12分钟收敛；只读官方资料与本机help；允许隔离目录的Python安全模拟，不安装插件、不改生产、不切模型、不创建自动化、不访问用户凭据、不提交付费资源、不修改Git其他实验。**WorkBuddy必须通过MCP返回完整报告正文，不得仅摘要或远端路径**；报告目标15k–22k字符内，长则分段且保证ChatGPT可取到全文。必须含五案例、官方事实≥5项、核心MVE及≥5类实际红队负例、工件SHA、三方状态区分、同厂三项整改、跨厂两项迁移、机会清单及人工行动。不能证明则明确NOT_VERIFIABLE/NOT_TESTED。
最终评分固定证据25、战略20、技巧20、五案例20、风险真实性15；与R01 79分同厂比较五维差值，但研究难度不同须说明。Git仅允许kaibahaha/xxsc的exp/factory10-skill-plugin-20261030分支、experiments/factory10-self-improvement-20261031/范围；**本轮研究代理不自行修改Git**，报告返回后由ChatGPT GitHub连接器写入并回读。
