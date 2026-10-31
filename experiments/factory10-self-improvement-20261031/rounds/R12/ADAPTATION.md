# R12 F2｜ADAPTATION（双轨整改预注册，非结果自评）
## 跨小时通用方法：R11仍排队，采用R10延迟基线
R11 F1 job=13434ad175b04267未返回、Git无WORKBUDDY_REPORT；状态DELAYED_BASELINE，不能从R11虚构方法结果。采用最近已完成R10 F10独立审计中的两项可跨工厂迁移方法，已逐字写入R12/FEEDBACK_TO_BUDDY.md并真实注入唯一MCP prompt。
## CROSS_FACTORY_TRANSFER
|source_round|source_factory|target_round|target_factory|method_change|baseline_metric|target_metric|observed_metric|verdict|evidence_path|
|---|---|---|---|---|---|---|---|---|---|
|R10 (DELAYED_BASELINE; R11 PENDING)|F10 小说叙事|R12|F2 软件开源|T1 完整schema、相邻边界、normal/-O fail-closed|R10新增8类×2：12次exit0错误接受、4次非结构化异常|R12≥8类×2，非法拒绝≥16/16，0 fail-open、0副作用|PENDING|ACTUALLY_INJECTED / NOT_VERIFIED|rounds/R10/CHATGPT_AUDIT.md;rounds/R12/FEEDBACK_TO_BUDDY.md|
|R10 (DELAYED_BASELINE; R11 PENDING)|F10 小说叙事|R12|F2 软件开源|T2 原始源码/输入/输出SHA三联、当前官方版本/许可核验|R10源码SHA不一致、8冻结输入缺字节；9事实1错|R12原始SHA3/3一致、≥5官方事实0实质错|PENDING|ACTUALLY_INJECTED / NOT_VERIFIED|rounds/R10/CHATGPT_AUDIT.md;rounds/R12/FEEDBACK_TO_BUDDY.md|
## SAME_FACTORY_REMEDIATION
正式R02 F2基线76/100（21/18/14/14/9），真实报告/独立审计Git已回读。选择三项有明确证据的高价值缺陷：
- P0-F2-R12-01：headless -p/-y/dontAsk权限模式缺真实拒绝证据、worktree≠OS隔离；本轮核官方版本/只读help/≥3类拒绝，未运行标NOT_TESTED。
- P1-F2-R12-02：GPL/AGPL义务触发条件过度概括、import即违规、CVE/密钥扫描缺真实规则；本轮按行为矩阵与3正3负夹具复核。
- P1-F2-R12-03：rm -rf .codebuddy/worktrees/*危险回滚、Case E仅概念、≈0成本漏人力；本轮安全唯一临时目录清理、队列故障模型、真实工件与成本公式。
五案例A–E逐案修订要求已在FEEDBACK中完整列出。缺陷状态PENDING，不将反馈发出视为解决。
## 假设与证伪
- H1：引入相邻边界双模式将减少非法输入fail-open；任一非法exit0/无结构化错误即证伪。
- H2：源码+输入+输出原始SHA与官方版本核对可减少“报告声称已验证但无法复放”；任一SHA不一致、官方过期候选即证伪。
- 研究报告未返回前observed_metric=PENDING；不以跨厂总分或报告长度作因果证据。
- NEXT: R13 F3先追R12真实Job，再从最新完成的1–3轮选最多2项通用方法；R22 F2再同时对比R02/R12。