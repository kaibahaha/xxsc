# R22 F2｜ChatGPT独立隔离安全原型与红队实测（非WorkBuddy报告）
## 证据身份与执行环境
- WorkBuddy唯一job=1b6feeaf3f514af1 **FAILED_OOM/90s**，无正文/无MVE。以下是ChatGPT在独立容器内另行执行的**小型安全原型**，不是WorkBuddy结果，不替代五案例或R22正式质量评分，不证明真实CodeBuddy/OS沙箱/生产网关已安全。
- 运行环境：容器Python 3.13；执行 `python /mnt/data/factory10_r22_independent/run_redteam.py`；脚本仅创建本实验隔离目录、合成JSON及临时symlink，不触生产、真实用户仓库、远端Bridge、密钥或插件。
- Git本轮原始工件：`artifacts/policy_gate.py`（2199字节）、`artifacts/run_redteam.py`（2501字节）、`artifacts/frozen_inputs.json`（3672字节）、`artifacts/redteam_log.json`（5787字节）。以上四份均Git创建后独立回读exact PASS；源文件及输入/输出原始字节已落在本实验R22目录，不能把远端Buddy工件混入。
## 实际执行结果（从容器子进程采集）
- 14种冻结输入：1合法+13非法；每个以普通Python与`python -O`运行一次，共**28次真实子进程执行，28/28符合预期**。合法2次exit=0/ACCEPTED，非法26次exit=2/REJECTED，stderr全部空；具体每例原始stdout、stderr、退出码见`artifacts/redteam_log.json`。
- 非法13类：relative_path、unknown_mode、negative_budget、sandbox_string_true、empty_rules、symlink_escape、prefix_collision、duplicate_id、budget_bool、wildcard_cleanup、bypass_mode、unknown_action、empty_input。至少5项针对R12真实失效边界：相对路径、未知mode、负预算、sandbox字符串、空规则；另有symlink、目录前缀冲突等相邻边界。
- 关键设计：外部可信root参数而非合同自报root；仅绝对路径；Path.resolve+is_relative_to；严格schema/mode/预算/规则；拒绝bypassPermissions和未知sandbox字段；显式返回非零，不依赖assert。实际原型**没有执行写/删/网络/真实Agent授权**，所以只能验证解析器拒绝行为，不能证明生产权限边界、竞态/TOCTOU、清理归属、真实OS sandbox、并发或商业运行。
## 容器实际文件SHA256（从文件字节计算）
|file|SHA256|
|---|---|
|policy_gate.py|7974ab9232d53c2775ecc05a81435ed1914344abdfc85ecf0b11d298cbeb06b7|
|run_redteam.py|d7069d3069506912593845827de309b3cf19c404a19ae526cb18c1671f3825f1|
|frozen_inputs.json|65ced3c6dde3d9e3ba26a54c492f323b8daa8a11f849bcc160d0e3ae2f5950ab|
|redteam_log.json|7702e285acba2ca0800c6d8344fa55941374dfd2470ca1aec4b9b98b3658346e|
- 以上是**容器文件的SHA256**；Git回读验证的是Git blob内容与本次写入字串一致，尚未对Git远端字节另算SHA256，故不宣称跨环境独立哈希复算完成。4文件字符数与容器字节数一致（全ASCII）。压缩归档仅为附加便携副本，不代替Git原始工件。
## 审计结论
- 独立原型安全负例：**PASS_28_OF_28_FOR_TESTED_PARSER_ONLY**；R12旧解析器10/10 fail-open缺陷在这个**新原型的对应冻结输入**上被阻断，属于设计级局部修复证据，**不构成R12生产P0关闭**，因为没有WorkBuddy本轮报告、真实执行路径/OS沙箱与可信身份、并发/清理验证。
- D1=PARTIAL_PROTOTYPE_ONLY，D2=NOT_TESTED（simulate/cleanup可信归属尚未实现），D3=NOT_TESTED（许可证/供应链真实扫描尚未运行）；同厂正式resolved_count=0，不能声称三项整改全部解决。R22固定100分仍NOT_EVALUABLE。
- 下一步：远端OOM恢复后，在后续轮次只读检查；对本原型添加外部可信root固定配置、创建者归属与安全清理、TOCTOU相邻边界、真实CLI拒绝与授权审计；不可未经许可部署生产。
