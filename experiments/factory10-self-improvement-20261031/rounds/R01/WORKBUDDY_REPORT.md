# R01 F1 WorkBuddy MCP真实返回｜SUMMARY_ONLY

- job_id: aab758d7c33d4631
- MCP status: done
- provenance: 以下是get_workbuddy_result实际返回的完整文本；WorkBuddy声称远端另有382行报告，但该全文未通过MCP返回，故本文件仅为原始返回摘要，不能冒充完整报告。
- remote_full_report_claimed_path: /tmp/factory10-self-improvement-20261031/R01/WORKBUDDY_REPORT.md

---

报告已完成并保存至隔离目录。以下是可追溯的结果摘要。

## 交付物
- 主报告：`/tmp/factory10-self-improvement-20261031/R01/WORKBUDDY_REPORT.md`（382 行，中文）
- **RESULT_STATUS: COMPLETE**

## 约束遵守（已核验，零违规）
全程**只读**：仅用 `codebuddy --version` / `--help`（mcp/plugin/config 子命令）与随包官方文档 + 4 次 Web 检索。**未安装、未授权、未切模型、未改生产桥接器、未读凭据、未创建任何子定时任务**。所有样例均用占位符 `sk-xxx`/`${VAR}`，无真实 token，未提交 Git。

## 关键整改（三个 P0 已用官方一手证据纠正）
- **SF01（P0）**：旧报告称“CodeBuddy 无内建 scheduler” → **证伪**。官方文档证实自 v2.57.0 起即有 `CronCreate/CronList/CronDelete` 工具、`/loop`、REST `/api/v1/scheduled-tasks`（U1/U2/U3）；持久任务由 daemon 接管（v2.156.0），默认 30 天有效期（v2.168.3）。反例：顶层无 `scheduler` 子命令 ≠ 无调度。
- **SF02（P0）**：旧报告把 `codebuddy --serve` 当“通用多模型推理网关” → **证伪**。`http-api.md` 全量端点**无 `/v1/chat/completions`**；`/api/v1/runs`(Gateway Protocol) 与 ACP 是**Agent 控制面**，非推理面。`/chat/completions` 仅作 `models.json` 的**上游 url**。真正推理网关是 L2（LiteLLM 类，U6/U7）。
- **SF03（P0）**：旧报告称“models.json 配 apiKey 即额度隔离” → **证伪**。`models.md` 字段仅模型定义，**无租户身份/RPM·TPM 预算/账本**。多租户需 L2 虚拟密钥 + 预算 DB；且 LiteLLM **无 DB 时 fail-open**（原文引述），必须 fail-closed 兜底。
- SF04/SF05/SF06 亦给出文档级核验与费用严格区分（“CLI/插件免费”因文档未标价而标 UNVERIFIED，不谎称）。

## 报告内含
- ① 日期/环境/命令原始输出；② **9 条官方一手 URL**（U1–U9，含 codebuddy.cn/ai、Tencent Cloud、LiteLLM、ACP、E2B）+ 未验证清单（U-1~U-6）；③ ChatGPT 侧/WorkBuddy 侧 插件·Skill·MCP 的可用性/安装/授权/费用严格区分表；④ F1 四层模块化架构 + 5 案例（A–E，各含输入/最小命令/输出/失败注入/回滚/权限成本/量化验收）；⑤ SF01–SF06 逐项“旧问题→修复→新证据→验收”表 + A–E 逐案复盘；⑥ 2 个通用方法改进候选（M1 三段式证据、M2 每案例必含负例+回滚）及指标；并标注 NO_PREVIOUS_HOUR、不与旧实验混号。

未亲自实测的内容（L2 部署、预算账本跑通、端到端 trace 抽样、SBOM/签名流水线、桥接器内部态）均明确标 **UNVERIFIED**，未做断言。
