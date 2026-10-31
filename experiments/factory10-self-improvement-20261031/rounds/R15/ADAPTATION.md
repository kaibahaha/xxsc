# R15 F5｜双反馈链最终复盘
## CROSS_FACTORY_TRANSFER
|source_round|source_factory|target_round|target_factory|method_change|baseline_metric|target_metric|observed_metric|verdict|evidence_path|
|---|---|---|---|---|---|---|---|---|---|
|R14|F4|R15|F5|T1逐型号/周期/公式官方核价|R14 6事实2实错|R15≥5事实0错|R15独立7抽4错：HeyGen 600credit≠600min、ElevenLabs 33M总量≠每月、Suno商用$1M虚构、赛事主体/条款冲突|FAILED_FACT_ACCURACY|R15/CHATGPT_AUDIT.md §C;R15/WORKBUDDY_REPORT.md §③|
|R14|F4|R15|F5|T2源代码/冻结输入/日志/SHA移交|R14报告仅自述SHA无源码|R15≥1可独立复算|WAV128044B SHA d5e639...、SRT159B SHA 8c477e...均独立重算匹配；新P0布尔授权fail-open|EFFECTIVE_FOR_DETERMINISTIC_REPLAY / SAFETY_FAIL|R15/INDEPENDENT_REPLAY_EVIDENCE.md;R15/CHATGPT_AUDIT.md §D|
## SAME_FACTORY_REMEDIATION
R05 73/100 (18/17/15/14/9) → R15 71/100 (16/18/16/15/6), Δ=-2 (任务难度不同)。D1 Opus RESOLVED；D2 Runway RESOLVED；D3 Suno PARTIAL/RECURRED_ADJACENT，新增“$1M商用上限”与20下载/月缺口。解决率2/3，关键复发率1/3。五商业案例0/5 E2E。
## 下一轮R16 F6必须实际注入两项
U1事实单位与资格版本双核：R15 7抽4错（总量/月度、积分/分钟、主办方/营销页、许可/其他厂商门槛），要求官方具体页、单位、版本/时区、至少5抽0错、来源冲突标UNKNOWN。
U2输入类型/NaN/时长/授权证据相邻红队：R15 validate()对authorized='false'、NaN start/end、end=8000>音频8s全部返回accepted。F6至少5负例+这些相邻边界，0 fail-open，Python -O仍有效，源码与原始日志可独立回放。若不符合则FAIL；不能把格式探针当生产能力。
## 机会方法迁移
独立核验主办方正式规则，而非Segmind营销摘要；官方 https://www.1billionsummit.com/ai-award-2027/terms-and-conditions §5.2允许多部作品，Segmind摘要1人1部矛盾；且作品许可全球永久、报名费0但制作费自担。应标B/P1 WATCH_ONLY，用户身份资格未核、无报名。