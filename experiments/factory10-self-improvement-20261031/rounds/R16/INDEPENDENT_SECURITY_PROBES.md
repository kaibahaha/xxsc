# R16 F6 独立安全反例｜2026-11-01 Asia/Shanghai
## 证据来源与复现等级
- 唯一WorkBuddy Job 135fcff83e044e3b DONE，真实正文30439字符；Git WORKBUDDY_REPORT.md blob c59a67c9dfec3b9ee088cdc312edfdcaf6d4c6d2，完整回读。
- 真实MVE源码已从报告原始代码块无修改提取到 artifacts/evidence_gate_r16.py（14375字符），冻结输入 artifacts/frozen_cases_r16.jsonl（3801字符），Git各自回读PASS。ChatGPT在独立JavaScript SHA256实现中用标准向量sha256('abc')=ba7816bf...验算，再计算文件真实SHA256：源码 313071e5ac6aeabff24fbba7e052ca70659b880a3949099e67d11d6195444e19、输入 fcc03db36a1a3d2cc47d0985c80b19a00f47b63fe99ca2a368390dc1de587ddf，与Buddy报告声称一致。此项为真实内容哈希独立复算，不等于完整Python脚本逐字节运行。
- ChatGPT在独立Python环境按报告源码逐函数重实现`admit_evidence`、`_validate_source`、`_validate_rights`、`_validate_date`、`_validate_path`、`_evidence_hash`的决策逻辑，并对冻结合法样本施加相邻变式。该测试为**独立逻辑复刻/边界探针**，不是从Git直接运行原始脚本；完整原脚本normal/-O字节级重放仍为NOT_INDEPENDENTLY_REPLAYED。
## 10项独立边界探针
|编号|输入相对于合法样本的变更|实际结果|安全判定|
|---|---|---|---|
|P0|原始合法样本|ADMIT|对照通过|
|N15|source_url=https://nature.com.evil.example/forged|ADMIT|**FAIL_OPEN P0**，hostname为nature.com.evil.example而非nature.com|
|N16|source_url=https://evil.example/x?ref=nature.com|ADMIT|**FAIL_OPEN P0**，域名仅在查询参数出现|
|N17|source_url=javascript:nature.com|ADMIT|**FAIL_OPEN P0**，非HTTPS且无合法主机名|
|N18|claim='This retracted paper proves its disputed findings'|ADMIT|**P0逻辑缺陷**，门禁未核验claim与来源事实/撤稿状态|
|N19|authorized=True, rights='copyright_restricted'|ADMIT|**P0逻辑缺陷**，自报布尔与受限版权标签不能构成真实发布授权|
|N20|claim=''|ADMIT|P1，空声明无最小字段约束|
|N21|version=''|ADMIT|P1，空版本虽为str却不代表有效版本|
|N22|claim=None|ADMIT|P1，缺声明仍可发布|
|N23|source_url=http://www.nature.com/articles/nature12968|ADMIT|P1，未强制HTTPS|
- 上述输入均未修改磁盘或联网，使用Python标准库在隔离环境测试；无生产副作用。与Buddy的14类自选负例全部拒绝不矛盾：新攻击覆盖其遗漏的域名解析、版权授权证明、语义真实性与空字段。
## 根因与修复要求
1. `_validate_source` 使用`any(domain in url for domain in reg['domains'])`，只做字符串子串包含；应以`urllib.parse.urlsplit`解析，限定`scheme=='https'`，`hostname`精确匹配批准域名或经审批的子域名；拒绝userinfo、恶意端口、URL编码绕过、空host、重定向到外站。必须增加N15/N16/N17/N23。
2. `authorized`是调用方可自报的布尔值，没有经认证的审批者签名/来源可信锚；`rights='copyright_restricted'`被允许进入发布门。应将证据入库与对外发布分成不同状态，发布须绑定经过核验的授权主体、权利范围、可追溯审批与原始证据，默认拒绝受限版权全文发布。必须增加N19。
3. `claim`可以为空/None/任意虚假陈述，`publication_date`只检查日期合法而不比对原论文实际日期，`version`空字符串通过；应校验schema必填、claim非空、版本非空，并在外部事实核验通过前标DOCUMENTED/UNVERIFIED而不是ADMIT_FOR_PUBLICATION。撤稿DOI不可作为有效研究结论来源。增加N18/N20/N21/N22。
4. 现有SHA只覆盖claim、source_url、publication_date三个自报字段，不能证明内容可信，也未绑定rights/authorized/version；哈希是完整性检查而非权威证明。须引入受信任外部来源证据和审计签名/可信快照。
## 独立结论
- 原14类负例Buddy自述PASS，未直接运行原脚本，故原测试计SELF_REPORTED；真实源码/冻结输入SHA256经独立验证。
- 新增9项非对照变式均被逻辑复刻ADMIT，其中至少4项构成严重的安全/真实性fail-open；**FINAL_SECURITY_GATE=FAIL / P0_OPEN≥2**。不能用于发布或生产，必须由下一轮R17继承域名可信锚、权限真实性和语义证据的边界红队。
