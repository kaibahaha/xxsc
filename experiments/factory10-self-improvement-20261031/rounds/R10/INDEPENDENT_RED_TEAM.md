# R10 F10｜ChatGPT独立红队复放记录（V4）
- 执行日期：2026-10-31；独立环境：ChatGPT隔离Python 3.13.5；非WorkBuddy远端环境。测试对象来自本实验Git WORKBUDDY_REPORT.md §5 Python代码块，逐字提取为 f10_consistency_validator.py；采用独立合成JSON输入，**不是WorkBuddy原始8份冻结输入**。
- 方法：本地shell真实运行 python3 f10_consistency_validator.py fixture.json 与 python3 -O f10_consistency_validator.py fixture.json，每例两模式，记录退出码、stdout/stderr结构；共15类×2=30次。无网络/付费API/真稿件/生产写入。
- Git报告源码块7092字符（ASCII）；对Git精确读取源码块独立SHA256：不附末尾LF ec14e7f26956f0b382d2acf41d8934b26f4ff295a44d2bd1df0bfec38821b617；附单LF a681c6ca4c06612d6470a5efd8f69f6fd0c3dacf45aa2e931ab48a23a105717c；WorkBuddy报告§7自报 222568b773ab19adcf0eb5b429a07186f362d10c43a89b9527e444f979830cf4。**两种通常文件结尾方式均不一致**，所以“报告完整源码与自报SHA一致”独立复核FAIL。远端实际文件可能不同，但Git报告无法证明一致。
- 报告§5仅列8个输入文件名与SHA，**未附JSON完整字节**；§7未附 run_mve.py 源码和 mve_run_summary.json 原始内容，无法独立核对8个输入SHA或WorkBuddy原始运行结果。以下是ChatGPT以报告源码自行构造的独立相邻输入，不得冒充WorkBuddy冻结输入原样复放。

## 独立测试矩阵（normal / python -O）
|类别|合成输入与期望|normal exit|python -O exit|独立结论|
|---|---|---:|---:|---|
|positive|合法授权声明+角色+章节+有效引用；预期接受|0 VALID|0 VALID|PASS|
|neg_missing_char_id|删除角色id；预期拒绝|2 REJECTED|2 REJECTED|PASS|
|neg_empty_graph|characters=[]；预期拒绝|2 REJECTED|2 REJECTED|PASS|
|neg_invalid_ref|references=['ghost']；预期拒绝|2 REJECTED|2 REJECTED|PASS|
|neg_wrong_type|birth_year='2219'；预期拒绝|2 REJECTED|2 REJECTED|PASS|
|neg_missing_auth|删除meta.authorization；预期拒绝|2 REJECTED|2 REJECTED|PASS|
|neg_empty_text|text=''；预期拒绝|2 REJECTED|2 REJECTED|PASS|
|NEW-01 root_array|根JSON=[]；预期结构化拒绝|1 AttributeError|1 AttributeError|FAIL_UNSTRUCTURED|
|NEW-02 empty_chapters|chapters=[]；章节一致性验收不能VALID|0 VALID|0 VALID|FAIL_OPEN_CONTRACT|
|NEW-03 missing_chapters|删除chapters；同上|0 VALID|0 VALID|FAIL_OPEN_CONTRACT|
|NEW-04 duplicate_id|重复角色id；唯一身份应阻断|0 VALID_WITH_WARNINGS|0 VALID_WITH_WARNINGS|FAIL_OPEN_CONTRACT|
|NEW-05 age_conflict|2247年/2219出生/声称40岁；高严重冲突应阻断|0 VALID_WITH_WARNINGS|0 VALID_WITH_WARNINGS|FAIL_OPEN_CONTRACT|
|NEW-06 wrong_chapter_text_type|text=123；文本类型必须拒绝|0 VALID|0 VALID|FAIL_OPEN_SCHEMA|
|NEW-07 unhashable_ref|references=[{id:'char_001'}]；预期结构化拒绝|1 TypeError|1 TypeError|FAIL_UNSTRUCTURED|
|NEW-08 source_boolean|meta.authorization.source=true；授权来源需有效文本/可信凭据|0 VALID|0 VALID|FAIL_OPEN_AUTHORIZATION|

**统计**：原定6类负例×2=12/12正确结构化拒绝；合法正例×2=2/2接受。新增8类×2=16次：12次错误接受/只警告退出0，4次未捕获异常退出1。**R09缺字段教训部分迁移成功，但R10仍未形成完整fail-closed门禁。**

## 复现输入生成说明（独立构造）
基准JSON：{"meta":{"title":"Frozen sample","setting_year":2247,"authorization":{"text_usage":"granted","source":"synthetic-owned"}},"characters":[{"id":"char_001","birth_year":2219,"age_ref":28}],"chapters":[{"text":"The door opened.","references":["char_001"]}]}。
在基准上分别执行上表字段删除/替换；root_array用[]；duplicate_id在characters追加原角色副本；source_boolean将source设true。保存为UTF-8 JSON，执行报告§5源码即可重放。动态时间戳不用于逐字输出比对，核对exitcode/status/error_code即可。

## 缺陷等级与整改要求
- **P0-GATE-01（生产阻断）**：授权标识仅由用户输入自述，且source=true可通过，不能证明文本版权/许可真实存在；不得将该程序用于真实授权判定或生产发布门禁。必须引入外部可信授权台账/签名/人工审批，验证schema及权限来源；本次只算合成数据格式门禁。
- **P1-ARTIFACT-01**：Git报告源码SHA与自报SHA不一致，且8份原始冻结JSON、run_mve.py、原始run_summary未附；必须将真实字节以本实验路径提交、SHA独立核对，失败时不得声称INDEPENDENTLY_VERIFIED。
- **P1-SCHEMA-02**：根JSON非object、引用项非hashable导致未捕获异常；文本数字类型被VALID；对顶层、章节、引用类型全面做结构化校验。
- **P1-SEMANTICS-03**：缺/空章节、重复角色id、重大年龄矛盾仍exit0；按“章节一致性发布门禁”合同必须阻断高严重缺陷，低严重警告与阻断分级清晰。
- **P1-FACT-04**：候选列表含2019年已终止的Adobe Story，不能作为2026可部署现行候选；官方公告 https://blog.adobe.com/en/publish/2018/01/22/adobe-exits-scriptwriting-software-business-end-adobe-story-cc 。
- **P1-EVIDENCE-05**：Top5只有链接/费用表，缺完整实际命令/工作流与权限实测；B/C/D/E案例没有逐案可执行步骤、成本数值、异常和回滚证据。
- 下一轮R11跨厂迁移最多2项：T1 全类型/缺字段/空集合/异常统一fail-closed，T2 源码SHA+原始输入+输出字节三联复核及过期产品清除；必须进入R11实际MCP prompt，不能只写Git。
