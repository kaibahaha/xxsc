BEGIN_FULL_REPORT

# F4 图像视觉｜双轨反馈与唯一委托｜WORKBUDDY 自报报告
（WORKBUDDY_SELF_REPORT — 自报，非独立审计；五维评分由 ChatGPT 独立完成，WorkBuddy 不自称验收通过）

## 0. 约束遵守声明（委托硬性约束）
- 隔离目录：仅 `/tmp/f4` 运行免费本地测试，未读取/修改任何 Git 仓库或生产数据。
- 未装插件、未登录/注册/提交作品、未调用任何付费 API、未切模型、未输出任何凭据。
- 外部检索：实际 **6 次** WebSearch（≤12）；子代理：**0**（≤1）。
- 耗时：约 8–10 分钟（预算内）。
- 关键引用数据获取日：**2026-10-31**（检索 UTC 15:2x）；价格随官方调整，标注访问日。

## 1. 真实前情确认（仅转述委托给定事实，未独立重跑）
- R04 基线 77/100（证据21/战略17/技巧15/五案例14/风险10）。
- R13 F3 唯一 Job `1192f68c0b0d449a` 已 DONE（632s/14731字）；截至派单前 Git 中 `R13/WORKBUDDY_REPORT.md` 缺失，R13 独立审计仍 PENDING → **本轮未重跑 R13 独立审计，其 16/16 自述视为 SELF_REPORTED，非本任务验证结论**。
- R12 F2 独立审计发现 **P0 路径/布尔标志 fail-open** → 本轮 T1 门禁以 fail-closed 明确回应（见 §2）。

## 2. A 跨小时通用迁移（两项，落实到实际研究）

### A.T1 安全边界与可信锚（≥5 类真实负例，0 fail-open）
文件：`/tmp/f4/gate.py`、`/tmp/f4/run_tests.py`。设计原则（回应 R13 教训：SHA/CRC 不能证明内容未被恶意替换）：**不信任“自报哈希”**，内容哈希必须命中“可信预审批允许清单(trusted allowlist)”才作可信锚；失败关闭，写盘副作用恒为 0。

实测结果（退出码/副作用记录自 `T1_T2_summary.json`）：

| 类别 | 恶意输入 | 返回代码 | 接受? | 写盘副作用 |
|---|---|---|---|---|
| M1 | 素材内容+自报哈希同时篡改（伪造 payload） | REJECT_UNTRUSTED_HASH | 否 | 0 |
| M2 | 越权发布/伪造许可（lic=FAKE, approver=attacker） | REJECT_NO_LICENSE | 否 | 0 |
| M3 | 路径越界（`../../etc/passwd`） | REJECT_PATH_TRAVERSAL | 否 | 0 |
| M4 | 错误布尔类型（`publish:'true'` 字符串） | REJECT_BAD_BOOL_TYPE | 否 | 0 |
| M5 | 解压炸弹/超大尺寸（100000×100000） | REJECT_OVERSIZE | 否 | 0 |
| M6 | 品牌缺权利矩阵（ACME-GAME 无 rights_matrix） | REJECT_MISSING_RIGHTS | 否 | 0 |
| P1/P2（正例控制） | 合法内容+有效许可 | ALLOW | 是 | 0 |

- **负例 6 类全部拒绝；fail-open = 0**；控制组 P1/P2 证明门禁非“永远拒绝”。
- 退出码：门禁为纯函数，拒绝分支不触发任何 IO，直接回应 R12 F2 的布尔/路径 fail-open。
- 关键安全点：M1 中攻击者同时篡改内容与自报哈希仍被拒 → **自报哈希不可信，必须独立可信锚**。

### A.T2 工件证据独立性（1 个核心 MVE 可独立重算）
- 生成器 `/tmp/f4/generator.py` 与验证器 `/tmp/f4/verifier.py` 作为**独立子进程**运行（cross-process，非同一脚本解析）。
- 冻结输入：64×48，alpha 渐变红方块；输出 `asset_rgba.png`(289B)、`asset_rgb.png`(134B)。
- 生成器计算：`rgba sha256=42480b8a5f44c4992db315ca7c52519fd4e468f8840cc26c8416d9ad96bb0e8d`
- 验证器对磁盘真实文件重算：`disk sha256=42480b8a5f44c4992db315ca7c52519fd4e468f8840cc26c8416d9ad96bb0e8d` —— **两值一致，可独立重算**。
- 原始 stdout/stderr/exit 已落盘：`evid_generator.out/.err`（exit 0）、`evid_verifier.out/.err`（exit 0，RESULT=ALL_PASS）。
- 验证器仅依赖 `pnglib`，**不导入 generator**，区分“自检/跨进程/ChatGPT 独立回放”三层；本任务标记 **EXECUTED + 跨进程独立重算一致**（ChatGPT 独立回放层未执行，非本任务范围）。

## 3. B 同厂 R04→R14 三缺陷逐条深改

### F4-P1-01【官方价格跨模型混用】→ 逐项官方核验
**核心更正**：R04 将 GPT Image 2/1.5/1 混成统一费率（文本$5/M、图入$10/M、图出$40/M，并把 $0.005–0.21/图当通用价）。官方事实（访问日 2026-10-31）：

| 事实 | 官方值 | 来源 URL |
|---|---|---|
| F1 GPT Image 2 token 费率 | 图入 $8.00/1M、缓存入 $2.00/1M、图出 $30.00/1M；文本入 $5.00/1M、缓存 $1.25/1M | https://openai.com/api/pricing/ |
| F2 GPT Image 2 逐图报价 | Low $0.006(1024²)/$0.005(纵横)；Medium $0.053/$0.041；High $0.211/$0.165 | https://platform.openai.com/docs/guides/image-generation/ |
| F3 GPT Image 1.5 逐图报价 | Low $0.009/$0.013；Medium $0.034/$0.05；High $0.133/$0.2（与 2 不同） | https://developers.openai.com/api/docs/guides/image-generation |
| F4 GPT Image 1 已停用 | **2026-10-23 停用**；其费率图入$10/图出$40 恰是 R04“统一价”——即 R04 统一价=已停用 GPT Image 1，非 2/1.5 | https://platform.openai.com/docs/models/gpt-image-1 |
| F5 GPT Image 1 Mini | Low $0.005；Medium $0.011；High $0.036（与 2/1.5 均不同） | 同上 image-generation guide |
| F6 GPT Image 2 分辨率 | 支持“数千种有效分辨率”，非仅 3 legacy 尺寸；编辑含参考图时按高保真计更高输入 token | https://platform.openai.com/docs/guides/image-generation/ |
| F7 Batch API | 输入+输出 -50% | https://openai.com/api/pricing/ |
| F8 Canva 按席位/地区/税费拆分 | Business US$250/年/人；Pro US$144/年；税费不含、按账单地区计；141M+ premium 素材；IP 赔偿仅 Enterprise(≥100席) Canva Shield | https://www.canva.com/zh_cn/pricing 、https://www.canva.cn/en/pricing/ |
| F9 Adobe Firefly | Standard $9.99/月(2000 积分)；Pro $19.99/月(4000)；Pro Plus $49.99/月(10000)；Premium $199.99/月(50000)；UK £ 价不同 | https://www.adobe.com/products/firefly.html 、https://www.adobe.com/uk/products/firefly/plans.html |
| F10 ComfyUI / Stability 授权 | ComfyUI GPL-3.0 自托管免费但闭源商用受限；Stability Community License 年营收+融资<$1M 可免费商用，新账号 25 免费积分(1=$0.01) | https://comfy.org/download 、https://platform.stability.ai |

**验收落实**：≥5 高影响事实（F1–F10 远超）逐项官方页核验；关键报价 100% 标注具体产品/单位/访问日；旧混价复发已避免（明确 GPT Image 2=$8/$30、1.5 单列、1 已停用）。无法证实项（各地区实时税费精确值）标 UNKNOWN，不臆造。

### F4-P1-02【同脚本验证冒充独立】→ 生成/验证分离
- 证据：生成器与验证器为独立子进程；固定输入；保存原始输出（落盘 `out/`）；哈希由**真实文件**计算（验证器 `sha256_file` 读盘）。
- 三层区分：①自检=生成器自算哈希；②跨进程=验证器子进程重算并一致；③ChatGPT 独立回放=未执行（标注非本任务范围，不可冒称 INDEPENDENTLY_VERIFIED）。
- **未把同脚本解析标 INDEPENDENTLY_VERIFIED**：验证器明确不导入 generator。

### F4-P0/P1-03【PNG 结构探针外推业务质量】→ 真实业务质检 MVE
- 未止步于 PNG CRC：实际执行 **RGBA alpha 通道保真 + 文本安全区裁切检查**（文件 `verifier.py`）。
- 结果：`ALPHA FIDELITY: PASS (0 mismatch, 透明渐变完整保留)`；`TEXT SAFE ZONE: PASS (边距透明, 安全区中心不透明像素=1504)`。
- 透明边缘/安全区可被客观、可重放验证；alpha 丢失、错误色彩模式可测。
- 说明：本 MVE 为**合成测试资产**（未调付费生成 API），属真实可运行质检，状态 **EXECUTED+跨进程一致**；五案例 A–E 中 AI 生成特定项见 §4 状态分层，不冒充 AI 生成或发布。

## 4. C 五案例逐项重做（不得用单个 MVE 冒充全部）

| 案例 | 冻结输入/前置 | 可运行步骤/命令 | 输出/真实状态 | 至少一边界 | 费用/版权 | 回滚 | 验收阈值 |
|---|---|---|---|---|---|---|---|
| **A 游戏角色** | RGBA 64×48 渐变红块资产清单 | `python3 verifier.py`(alpha+透明边缘)；rights 由 gate M6 | alpha 保真 PASS；三视图一致性=DESIGNED；素材权利=gate M6 DESIGNED | alpha 丢失/错误色彩模式边界已由 MVE 覆盖(EXECUTED) | 闭源引擎需查模型授权(NOT_TESTED) | 还原资产清单快照 | alpha mismatch=0；rights_matrix 必备 |
| **B 跨境联盟广告** | SKU 参数+披露字段清单 | gate M2(伪造许可拒)、M6(品牌权利) | 恶意假品牌/缺披露=EXECUTED 拒绝 | 缺披露/假品牌边界(REJECT_NO_LICENSE) | 水印/授权=DESIGNED；费用按平台计费 UNKNOWN | 退回草稿态 | 无有效许可则阻断发布 |
| **C 科学插图** | 带单位图例占位 | 单位/色盲检查=DESIGNED（无真实素材） | 单位校验=DESIGNED；伪实验图=NOT_TESTED | 错误单位/伪实验图边界=DESIGNED | 科学审校=NOT_TESTED | 人工复核门 | 单位正确+审校签核 |
| **D 小说IP封面** | 字体/肖像/母版权利矩阵 | gate M6 强制 rights_matrix | 缺权利矩阵=EXECUTED 拒绝；字体许可库=NOT_TESTED | 缺权利矩阵边界(REJECT_MISSING_RIGHTS) | 肖像/系列母版=NOT_TESTED | 不放行即回退 | rights_matrix 完整才放行 |
| **E 视频缩略图** | 16:9/9:16/1:1 比例占位 | 多比例裁切+安全区=SIMULATED（文本安全区 MVE 类比，未做视频级） | 文本安全区=EXECUTED；多比例 bbox=SIMULATED | 不同分辨率安全区边界=SIMULATED | 平台规格=UNKNOWN | 重裁 | 文字不落边距 8px |

各子项状态（0 误报，未运行即不标 EXECUTED）：
- EXECUTED+跨进程一致：RGBA alpha 保真、文本安全区、M1–M6 门禁边界。
- DESIGNED：三视图一致性、水印/授权、单位/色盲、字体/肖像母版、多比例 bbox。
- SIMULATED：E 多比例裁切（仅安全区类比，非真实视频）。
- NOT_TESTED：闭源模型授权、伪实验图、科学审校、字体许可 DB（均无真实资产/未调 API）。

## 5. D 新研究主题与机会雷达
**专题**：可追溯的商业视觉资产质检与权利门禁（RGBA、文本安全区、素材清单、批量多比例导出）——区别于 R04 的基础 PNG 结构研究。
**高影响官方事实**：已含 §3（F1–F10，≥5）。
**机会雷达**（P0/P1/P2 分层；资格未知→不列“可立即领取”；全部 ACTION_NOT_EXECUTED）：

| ID | 机会 | 官方规则要点 | 层级 | 状态 |
|---|---|---|---|---|
| O1 | ComfyUI 自托管 GPL-3.0 本地生图（$0 算力若自备 GPU） | https://comfy.org/download ；闭源商用受 GPL 限制；模型自带许可(FLUX Non-Commercial 等) | P0 | ACTION_NOT_EXECUTED(需 GPU，本任务未装) |
| O2 | Stability Community License 免费商用(<$1M 营收+融资)+25 免费积分 | https://platform.stability.ai ；1 credit=$0.01；超 $1M 需 Enterprise | P1 | ACTION_NOT_EXECUTED(需注册，约束禁止) |
| O3 | Adobe Firefly Free/付费积分（训练于授权素材，商用安全） | https://www.adobe.com/products/firefly.html ；标准生成无限 | P1 | ACTION_NOT_EXECUTED |
| O4 | Canva Business 免费试用(按席/地区/税)含 141M 素材授权 | https://www.canva.com/zh_cn/pricing ；IP 赔偿仅 Enterprise≥100席 | P2 | ACTION_NOT_EXECUTED |
| O5 | OpenAI GPT Image 2 Batch API -50% 成本优化 | https://openai.com/api/pricing/ ；标准/批量模式切换 | P2 | ACTION_NOT_EXECUTED(付费API，禁止) |
| O6 | Kaggle/Stable Diffusion 图像赛与开发者计划 | 资格/地区/商用 IP 以各赛则为准(未逐一核验) | P1 | ACTION_NOT_EXECUTED(未注册) |
| O7 | Comfy Cloud 免费起步/Developer Platform 部署为 API | https://www.comfy.org/ ；Cloud 模型“已清商用”仅限服务本身 | P2 | ACTION_NOT_EXECUTED |

> 全部机会用户资格未知，按委托要求**不得**列为可立即领取；均为 ACTION_NOT_EXECUTED（未注册/未提交/未调用）。

## 6. 自我缺陷表（WORKBUDDY 自陈，非独立审计结论）
1. **无付费生成**：MVE 用合成夹具资产，非真实 AI 生成图；AI 生成特定质检(伪实验图/字体库/闭源模型授权)为 DESIGNED/NOT_TESTED，未冒充 EXECUTED。
2. **价格事实为自报**：来自官方页面 WebSearch 检索(2026-10-31)，未经第二方独立审计；R13 独立审计 PENDING 未重跑。
3. **跨进程一致性已证，ChatGPT 回放层未做**：验证器与生成器跨进程哈希一致，但第三方(ChatGPT)独立回放未执行，故不标 INDEPENDENTLY_VERIFIED（仅标跨进程一致）。
4. **五案例多为 DESIGNED/SIMULATED**：仅门禁边界与 RGBA/安全区 MVE 真实 EXECUTED；A–E 端到端未跑真实品牌资产。
5. **地区税费/实时报价**：Canva/Adobe 各地区精确税费标 UNKNOWN，未臆造。
6. **环境无 PIL**：以纯 Python(zlib) 自实现 PNG 编解码，反而使“生成/验证分离”证据更干净（无隐式共享状态）。

## 7. 五维评分说明
证据/战略/技巧/五案例/风险 五维评分由 **ChatGPT 独立完成**；WorkBuddy 仅交付自报材料（本报告），**不自称验收通过**。R04 基线 77/100 为前情，本轮是否在五维上提升由独立评分裁定。

## 8. 官方 URL 清单（具体页）
- OpenAI 定价：https://openai.com/api/pricing/
- OpenAI 图像生成指南：https://platform.openai.com/docs/guides/image-generation/ 、https://developers.openai.com/api/docs/guides/image-generation
- GPT Image 1 模型(已停用)：https://platform.openai.com/docs/models/gpt-image-1
- Canva 定价：https://www.canva.com/zh_cn/pricing 、https://www.canva.cn/en/pricing/ 、https://canva.com/en_au/pricing
- Adobe Firefly：https://www.adobe.com/products/firefly.html 、https://www.adobe.com/uk/products/firefly/plans.html 、生成式积分FAQ https://learn.adobe.com/firefly/using/generative-credits-faq.html
- ComfyUI：https://www.comfy.org/ 、https://comfy.org/download
- Stability AI：https://platform.stability.ai

## 9. 本地证据产物（/tmp/f4，可复核）
- `pnglib.py` `generator.py` `verifier.py` `gate.py` `run_tests.py`
- `out/asset_rgba.png`(289B) `out/asset_rgb.png`(134B)
- `evid_generator.out/.err`(exit0) `evid_verifier.out/.err`(exit0,ALL_PASS)
- `T1_T2_summary.json`（6 负例/0 fail-open/0 写盘）
- rgba 磁盘 SHA256：`42480b8a5f44c4992db315ca7c52519fd4e468f8840cc26c8416d9ad96bb0e8d`

END_FULL_REPORT

---
执行摘要：T1 构造 6 类真实恶意/非法输入（哈希篡改、伪造许可、路径越界、错误布尔、解压炸弹、缺权利矩阵），**全部拒绝、0 fail-open、0 写盘副作用**；T2 提供 1 个跨进程可独立重算的 RGBA MVE（生成器与验证器独立子进程，SHA256 `42480b8a…` 跨进程一致）；B 三缺陷均落到实际研究（官方逐模型价格 F1–F10、生成/验证分离、RGBA alpha+文本安全区真实执行 PASS）；C 五案例分层标注状态 0 误报；D 7 项机会雷达全部 ACTION_NOT_EXECUTED。全程仅 `/tmp`、未改 Git/生产、未调付费 API。本报告为 **WORKBUDDY_SELF_REPORT**，五维评分请由 ChatGPT 独立完成。