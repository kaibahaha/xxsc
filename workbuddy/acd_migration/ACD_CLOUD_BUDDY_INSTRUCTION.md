# ACD 派单系统 → WorkBuddy 云端重建指令（给云端 Buddy）

> 本文档可直接全文转给云端 Buddy。它拉取本仓库里的程序与指令，在云端独立重建 A/C/D 三线派单循环，并接管与 ChatGPT 的 git 协同。
> 唯一新增变化：试卷 PDF 已随包上传到 git，云端不再依赖 Google Drive 原件。

---

## 0. 目标（一句话）

在云端拉起一个常驻进程，每 30 分钟（北京时间整点/半点）向 git 提交 A/C/D 三线派单；ChatGPT 改为从 git 读取派单、解题、把结果回写 git。

---

## 1. 仓库与分支（绝对路径）

- 仓库：`kaibahaha/xxsc`（私有，需 classic PAT，scope=repo）
- 分支：`exp/p1-relay-dualwrite-20261023`
- Web 根：`https://github.com/kaibaha/xxsc/tree/exp/p1-relay-dualwrite-20261023`
- Raw 前缀：`https://raw.githubusercontent.com/kaibaha/xxsc/exp/p1-relay-dualwrite-20261023`

> 说明：`kaibahaha` 是 OWNER，可用环境变量 `P1GIT_OWNER` 覆盖（默认即此值，一般不用改）。

---

## 2. 你要拉取的文件清单

迁移包根目录：`workbuddy/acd_migration/`

### 2.1 程序（必拉，`code/` 下）
| 文件 | 作用 |
|---|---|
| `code/p1git_dispatch.py` | 核心：单线派单（`--line A/C/D`），含 build_order / ACK / 回读校验 |
| `code/p1git_loop.py` | 常驻循环：每 30 分钟对齐边界顺序派 A→C→D（替代定时任务，主驱动） |
| `code/p1git_scheduler.py` | 旧 WorkBuddy 自动化调度器（参考用，已被 loop 取代，可不跑） |
| `code/list_orders.py` / `dump_results.py` / `stat_all.py` | 只读核查工具 |
| `code/verify_slot.py` / `verify_readback.py` | 闭环核验工具 |
| 其余 `code/*.py`（device_auth / pat_setup / probe_* / verify_* 等） | 诊断/鉴权辅助，按需 |

Raw 示例（dispatch）：
`https://raw.githubusercontent.com/kaibaha/xxsc/exp/p1-relay-dualwrite-20261023/workbuddy/acd_migration/code/p1git_dispatch.py`

### 2.2 试卷 PDF（必拉，`source_pdf/`，迁移唯一新增项）
| 文件 | 作用 |
|---|---|
| `source_pdf/2025北京五十中高一10月月考物理（教师版）.pdf` | **ACD 物理题源**（TEACHER_PDF，题号 1..24 顺序循环） |
| `source_pdf/2025-2026学年北京市十一实验中学高一（上）第一次段考数学试卷.pdf` | 同批 Drive 试卷（镜像，数学题用） |

> 中文文件名 Raw URL 需 URL-encode（浏览器/工具通常自动处理）。也可 clone 整仓后在本地路径取。

### 2.3 指令与参考（`instructions/` + 根）
| 文件 | 作用 |
|---|---|
| `ACD_THREE_LINE_INSTRUCTIONS.md`（根） | A/C/D 三线派单指令全文（build_order 真实渲染，照此发单） |
| `instructions/P1_ACD_PATHS_AND_NUMBERING_REF.md` | 绝对路径 + 编号规则权威参考 |
| `instructions/P1_ACD_BACKUP_INSTRUCTION.md` | 备份/接管指令 |
| `MIGRATION_README.md`（根） | 迁移总说明 |

---

## 3. 云端重建步骤

### 步骤 1 · 环境
- Python 3（3.10+ 验证过），安装 `requests`：`pip install requests`
- 工作区建一个目录，例如 `~/acd_cloud/`，把 `code/` 下 `.py` 放进去。

### 步骤 2 · 取仓库内容（二选一）
- **方案 A（推荐，可 git 回读）clone 私有仓**：
  ```
  git clone https://x-access-token:<你的PAT>@github.com/kaibahaha/xxsc.git
  cd xxsc
  git checkout exp/p1-relay-dualwrite-20261023
  # 所需程序在 workbuddy/acd_migration/code/，PDF 在 workbuddy/acd_migration/source_pdf/
  ```
- **方案 B（轻量，纯 Raw 下载）**：用 §2 的 raw URL 逐个下载 `.py` 和 PDF 到工作区。

### 步骤 3 · GitHub token
- 用你自己的 classic PAT（`ghp_` / `github_pat_`，scope `repo`）访问 `kaibahaha/xxsc`。
- 二选一配置：
  - 环境变量：`export GITHUB_TOKEN=<你的PAT>`
  - 或落到 `code/` 同级 `state/github_token.txt`（脚本 `GITHUB_TOKEN` → `GH_TOKEN` → `state/github_token.txt` → `code/.github_token` 顺序读取）
- ⚠️ token 不要提交进 git、不要写进任何会被上传的文件。

### 步骤 4 · ⚠️ 唯一必改项——PDF 来源
`code/p1git_dispatch.py` 第 61–66 行 `TEACHER_PDF` 现指向 Google Drive file id。云端改为读 git 里的 PDF：
```python
TEACHER_PDF = {
    "source_key": "PHYSICS",
    "filename": "2025北京五十中高一10月月考物理（教师版）.pdf",
    # 改为本地路径（clone 后）或 git raw URL：
    "local_path": "<你的工作区>/source_pdf/2025北京五十中高一10月月考物理（教师版）.pdf",
    "question_range": [1, 24],
}
```
其余字段（`question_range [1,24]`、`source_key PHYSICS`、`filename`）**不变**。数学题用 `source_pdf/` 下那份数学 PDF，逻辑同。

### 步骤 5 · 启动派单
- 主驱动（常驻循环，替代定时任务）：
  ```
  python p1git_loop.py
  ```
  自动每 30 分钟对齐整点/半点边界，顺序派 A→C→D；自带本地+远端双去重，重复触发无害。
- 单次补派（调试用）：`python p1git_dispatch.py --line A`（A/C/D 同理）

---

## 4. 运行关键参数（不要动）

- 派单频率：每 30 分钟一格（整点/半点），由 `main()` 向下取整实现。
- `STOP_AT = 2026-10-25T12:00+08:00`：到点后派单转只读、循环空转。要延长就改这个值（或删掉判断）。
- 编号锚点 `ANCHOR = 2026-10-23T18:00+08:00`，`GLOBAL_SEQ = 1 + floor((SLOT-ANCHOR)/30m)`。云端沿用同锚点，会与历史连续，**不会重头编号**。
- 去重：以 `workbuddy/{a,c,d}_orders/TASK-P1-GIT-{X}-YYYYMMDD-HHMM.md` 文件名判重，已存在即 `DUPLICATE_SKIP`。

---

## 5. 派单 / 回写目录与编号规则（核心不变项）

### 派单落盘（你写）
- A：`workbuddy/a_orders/TASK-P1-GIT-A-YYYYMMDD-HHMM.md`
- C：`workbuddy/c_orders/TASK-P1-GIT-C-YYYYMMDD-HHMM.md`
- D：`workbuddy/d_orders/TASK-P1-GIT-D-YYYYMMDD-HHMM.md`

### 结果回写目录（ChatGPT 写，你只回读校验）
- A：`results/chatgpt-a/`
- C：`results/chatgpt-c/`
- D：`results/chatgpt-d/`
- 结果文件名 = 派单 TASK_ID **去掉 `TASK-` 前缀**，例如 `P1-GIT-A-20261024-1830.md`

### 语义（照此发单，详见 ACD_THREE_LINE_INSTRUCTIONS.md）
- **A 线**：git-only，单题。ChatGPT 读派单 → 解 `QUESTION_NO` 题 → 回写 git。**不写 Drive**。
- **C/D 线**：接力。Buddy（你/云端）自解 `Qbuddy` 一题；ChatGPT 接手 `Qchat` 一题。**ChatGPT 段只回写 git，不镜像 Drive**。
- 题号公式：`QUESTION_NO = ((GLOBAL_SEQ-1) mod 24)+1`；C/D 接力偏移 `OFF={A:0,C:8,D:16}`。
- **权威字段是派单文件里的 `QUESTION_NO`**，禁止从 SEQ 反推题号。

### 结果文件头（OUTPUT_CONTRACT，ChatGPT 回写规范）
必须含：`TASK_ID` / `SCHEDULE_ID` / `GLOBAL_SEQ` / `QUESTION_NO` / `INPUT_COMMIT` / `GIT_ORDER_BLOB_SHA`（派单文件 blob 指纹，用于验明读了哪份 git 派单）。

---

## 6. 与 ChatGPT 协同（切 git 申领）

- ChatGPT 原来的「从 Drive 账本领单」改为 **从 git 读取派单**（指令全文见 `ACD_CHATGPT_SWITCH_INSTRUCTION.md`，由用户转告 ChatGPT）。
- ChatGPT 每 30 分钟轮询 `workbuddy/a_orders/`、`c_orders/`、`d_orders/` 读最新 `TASK-P1-GIT-{X}-*.md`，取 `QUESTION_NO` 解题，结果回写 `results/chatgpt-{a,c,d}/`。
- 物理 PDF 在 git：`workbuddy/acd_migration/source_pdf/2025北京五十中高一10月月考物理（教师版）.pdf`，告诉 ChatGPT 从这里取题。
- **原 Google Drive 账本 DOCX（`1h_9jKCPw8ecUFNKc9E3-nRrg6fWpzco6`）保留作镜像副本，不删不迁**，与 git 主链并存。ChatGPT 仍可保留 Drive 副本，但不作为交付地。

---

## 7. 闭环判据（什么算成功）

派单成功 ≠ 闭环。只有 `results/chatgpt-{a,c,d}/` 出现对应结果文件、且结果内 `GIT_ORDER_BLOB_SHA` 与派单实际 blob 比对一致、答案 `ANSWER_MATCH=MATCH`、`STATUS=COMPLETED`，才算该槽闭环。

只读核验：`python verify_slot.py <HHMM>`（或 `stat_all.py` 看三线总览）。

---

## 8. 注意事项（务必看）

1. **PDF Raw URL 中文需编码**：若用 Raw 下载，文件名含中文/括号要 URL-encode，否则 404。
2. **token 安全**：PAT 只放环境变量或本地 `state/github_token.txt`，**绝不提交 git**。
3. **接管前停掉原本地循环**：本机（零刻）目前还有常驻循环在跑（`p1git_loop.py`）。云端接管后，请用户停掉本机那个进程，避免两个独立进程都对齐边界派单（虽有去重保护不会重复写文件，但状态各自独立、日志混乱）。停止方式：本机结束 `p1git_loop.py` 进程即可。
4. **STOP_AT 到点转只读**：`2026-10-25 12:00` 后不再派新单；如需持续运行改长该值或删除判断。
5. **Drive 模块可跳过**：Buddy 段若涉及 Drive 交付依赖（如 `gdrive_core`），云端无此模块可跳过——git 为主链，Drive 仅镜像。
6. **回读校验用 REST API 直连**：脚本已 `SESSION.trust_env=False` 直连 `api.github.com` / `raw.githubusercontent.com`，云端若走代理反而可能失败，保持直连。

---

## 9. 一句话总结给云端 Buddy

拉 `workbuddy/acd_migration/` 下的 `code/` + `source_pdf/` + 指令文档 → 配 PAT → 把 `p1git_dispatch.py` 的 `TEACHER_PDF` 改读本地 git PDF → `python p1git_loop.py` 常驻 → 每 30 分钟派 A/C/D → ChatGPT 从 git 申领并回写 `results/chatgpt-*`。原 Drive 账本保留作镜像，不动。
