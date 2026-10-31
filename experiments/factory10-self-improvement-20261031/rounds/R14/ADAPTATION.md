# R14 F4｜双反馈链完成后修正
## CROSS_FACTORY_TRANSFER
|source_round|source_factory|target_round|target_factory|method_change|baseline_metric|target_metric|observed_metric|verdict|evidence_path|
|---|---|---|---|---|---|---|---|---|---|
|R13|F3|R14|F4|T1可信锚+至少5类恶意负例|R13自述16 Node测试但无原始工件|≥5类、0 fail-open、可重放|WorkBuddy自述6类全拒绝；源码/原始日志未Git交付|INJECTED_BUT_NOT_INDEPENDENTLY_VERIFIED|R14/WORKBUDDY_REPORT.md;R14/CHATGPT_AUDIT.md|
|R13|F3|R14|F4|T2生成/验证分离并交付完整工件|R13缺真实源文件|≥1可独立回放MVE|报告称独立子进程、PNG289B SHA42480...；无源文件或原始工件|PARTIAL_METHOD_ONLY|R14/WORKBUDDY_REPORT.md;R14/CHATGPT_AUDIT.md|
## SAME_FACTORY_REMEDIATION
R04 77/100→R14 75/100 (-2, 非严格可比)；三缺陷0 RESOLVED/2 PARTIAL/1 RECURRED。型号定价仍错配：gpt-image-2官方API $4/$15而报告称$8/$30；另GPL许可解释过宽。
## R15跨小时改进（≤2，须完整注入实际prompt）
**T1 逐产品/模型/计费周期的权威核价和可重算算术**：R14自述已修R04混价但把GPT Image 2写成$8/$30（官网API价$4/$15），说明表格完整不等于正确。F5要求Opus、Runway、Suno、ElevenLabs、HeyGen至少5项逐条核官方页面+计费单位+日期+复算公式，目标5项0实质错误；若≥1错则T1 FAIL，未知标UNKNOWN。
**T2 原始工件可移交并独立复现**：R14报告声称6恶意输入拒绝、RGBA SHA一致，但仅远端/tmp/f4有源文件，Git只有文字。F5须把合法、可共享的最小源码、冻结输入、命令、退出码、原始输出、SHA256作为报告内可复制附录或在允许路径交付；目标至少1个音视频核心MVE可由ChatGPT独立重放，五商业案例不得冒充完成。若只有自述，则NOT_VERIFIED。
## NEXT
R15检验T1/T2与同厂R05 73/100基线，禁止跨厂总分当因果。