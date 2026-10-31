# R14 F4 图像视觉｜ChatGPT独立复核（2026-11-01 00:23 CST）
## 三方分离
WORKBUDDY_SELF_REPORT：唯一Job f2c3385cea0c43d9 DONE 594s，9340字符，报告声称六类负例拒绝、RGBA PNG跨进程校验通过、五案例仅部分执行。
CHATGPT_INDEPENDENT_AUDIT：通过MCP取全文，Git WORKBUDDY_REPORT.md commit 66988d0650cabecd6e443b8e9c7142a87df5ecc3/blob 70297a05c04c598852bc43c477ff048f5e519111，独立回读全文一致。检查报告事实并访问官方页面；**未取得/tmp/f4源代码、输入、输出文件或日志，因此远端6个负例、SHA、RGBA和文字安全区均未由ChatGPT独立重放**。
FINAL_ACCEPTANCE：**FAIL_FACT_GATE / PARTIAL_RESEARCH_ONLY / PRODUCTION_NOT_READY**；不能仅凭Job DONE或报告文字认定研发验收通过。
## 五维评分（同厂R04=77，21/17/15/14/10）
证据18/25；战略18/20；操作技巧16/20；五案例14/20；风险真实性9/15；**总分75/100**，较R04 **-2**；五维Δ=(-3,+1,+1,0,-1)。因R14强调安全门禁而R04强调结构PNG，难度与内容不同，分差不是严格因果结论。
## ≥5项高影响事实抽查（官方链接、核验日期2026-11-01）
1. **P0 F4-PRICE-01：GPT Image 2模型费率**。WorkBuddy §3 F1将图入$8/M、图出$30/M、文本入$5/M标为GPT Image 2；官方 https://developers.openai.com/api/docs/pricing 列gpt-image-2图入**$4/M**、图出**$15/M**、文本入**$2.50/M**；$8/$30/$5对应2.5型号或其他计费档位。属于**型号-费率错配，RECURRED**，直接影响成本估算；必须保留官方页面快照/日期、明确standard/batch。部分官网帮助页的GPT-Image-2.0费率与API文档不同，不能混同ChatGPT企业用量与API计费。
2. **P1 F4-LICENSE-02：ComfyUI GPL-3.0**。报告将“闭源商用受限”泛化为商业使用受限。GPL允许商业使用；若分发GPL程序/派生作品，才可能触发源码及同许可证义务，是否构成派生、网络服务场景另需具体法律判断。官方源码许可证 https://github.com/comfyanonymous/ComfyUI/blob/master/LICENSE 。结论：**PARTIAL/误导性许可解释**。
3. Canva美国年度价格：报告Pro $144/年、Business $250/人/年，官方 https://www.canva.com/pricing/ 支持，**PASS**；不适用于其他地区税费。
4. Adobe Firefly Standard $9.99/月2000积分、Pro $19.99/月4000积分，官方 https://www.adobe.com/products/firefly.html 支持，**PASS**；套餐更新需按访问日复核。
5. Stability Community License $1M年营收门槛，官方 https://stability.ai/news-updates/license-update 支持原则性门槛，**PASS_WITH_SCOPE**；须明确适用具体模型、注册及条款，不能等同Stability API赠金资格。
6. PNG跨进程SHA值42480b8a...：仅报告自述，源文件及stdout未进入Git，**NOT_VERIFIABLE**；不能认定INDEPENDENTLY_VERIFIED。
**fact_check_sample_count=6; material_fact_error_count=2（含许可证误导）; fact_gate_verdict=FAIL；无法核验的执行工件另列。**
## SAME_FACTORY_REMEDIATION
|旧缺陷|本轮实际行动|独立裁决|
|---|---|---|
|R04跨模型混价|列F1-F10官方矩阵|**RECURRED**：GPT Image 2价仍错配GPT Image 2.5档|
|R04同脚本自检冒充独立|自述生成器和验证器不同子进程|**PARTIAL**：措辞改进，但原始源码/工件不在Git，无法独立回放|
|R04 PNG结构≠商业质量|自述alpha、文字安全区和6负例|**PARTIAL**：合成资产质检不等于AI生成品质、OCR、版权、生产场景|
resolved_count=0, partial_count=2, recurred_count=1; key_error_recurrence_rate=1/3 (仅上述三项口径)，不可将自述6/6算独立验证。
## 五案例与MVE
A-E均有设计/部分门禁，但**0/5商业案例端到端真实运行**。门禁与PNG实验WORKBUDDY_SELF_REPORTED_EXECUTED，独立执行证据未随Git交付；core_mve_status=SELF_REPORTED_EXECUTED; core_mve_independent_replay=NO; artifact_reproducibility_verdict=NOT_INDEPENDENTLY_REPRODUCED。red_team_test_count=6 SELF_REPORTED，independent_pass_count=0，blocked_count=6未复现。claims_overstated_count=至少1（F1错价）；production_readiness=NOT_READY。
## NEXT
R15 F5必须继承：T1 所有价格/型号/计费周期双重公式校验，抽5条关键事实，0错；T2 执行声称必须交付源代码+冻结输入+stdout/stderr+SHA，无法传输时明确SELF_REPORTED，不称独立复现。不能照搬F4商业结论到F5。