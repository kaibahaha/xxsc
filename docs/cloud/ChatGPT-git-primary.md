# 致 ChatGPT A / C / D 工作者：以 Git 为主通道，Drive 仅作镜像与备份

> 本指令自 V1.2（2026-10-24）起生效，取代此前任何把 Google Drive 作为派单源/主交付通道的规则。
> **一句话：从 git 拿任务、向 git 交任务；Google Drive 只是历史镜像与备份，不再是主通道，也不要再作为领取派单的来源。**

---

## 1. 权威仓库（全局统一）

| 项 | 值 |
|---|---|
| 仓库 | `kaibahaha/xxsc` |
| 分支 | `exp/p1-relay-dualwrite-20261023` |
| 协议文档 | `docs/03-testing/2026-10-23-P1-Git-Drive-dualwrite-protocol.md`（历史协议，仅参考；以本指令与派单文件为准） |
| 派单频率 | 每 30 分钟一格（整点 / 半点） |
| 教师 PDF | **已在仓库内**：`papers/2025北京五十中高一10月月考物理（教师版）.pdf`（PHYSICS，题号 1..24，主用）<br>`papers/2025-2026学年北京市十一实验中学高一（上）第一次段考数学试卷.pdf`（MATH，题号 1..22，备用） |

> ⚠️ **不再从 Google Drive 读取教师 PDF 与派单**。所有题源 PDF 随仓库提交于 `papers/`，直接从仓库取。

---

## 2. 三线目录（全部在 git，Drive 仅镜像）

| 线路 | 领取派单（git） | 你回写结果（git，唯一交付地） |
|---|---|---|
| **A** | `workbuddy/a_orders/TASK-P1-GIT-A-YYYYMMDD-HHMM.md` | `results/chatgpt-a/TASK-P1-GIT-A-YYYYMMDD-HHMM.md` |
| **C** | `workbuddy/c_orders/TASK-P1-GIT-C-YYYYMMDD-HHMM.md` | `results/chatgpt-c/TASK-P1-GIT-C-YYYYMMDD-HHMM.md` |
| **D** | `workbuddy/d_orders/TASK-P1-GIT-D-YYYYMMDD-HHMM.md` | `results/chatgpt-d/TASK-P1-GIT-D-YYYYMMDD-HHMM.md` |

- **派单入口 = git 的 `workbuddy/*_orders/`**，不是 Drive。
- **结果交付 = git 的 `results/chatgpt-*`**，这是唯一交付地；不需要、也不要求再镜像到 Drive。
- Drive 旧账本 DOCX（`1h_9jKCPw8ecUFNKc9E3-nRrg6fWpzco6`）与旧结果文件夹（如 `12qx-...`）**仅作历史镜像与备份**，请勿向其中写入新交付，也不要把它们当作派单来源。

---

## 3. 领取与执行（严格执行）

1. **拉取**：`git clone` / `git pull` `kaibahaha/xxsc` @ `exp/p1-relay-dualwrite-20261023`。
2. **找派单**：读取对应线路的 `workbuddy/{a,c,d}_orders/TASK-P1-GIT-{LINE}-*.md`，选**最新且尚未认领**的一份。
3. **核验字段**：确认 `ASSIGNEE=CHATGPT_{LINE}`、学科、`SOURCE_KEY`、PDF 仓库路径、实验截止时间后再执行。
4. **取题号**：**以派单文件内的 `QUESTION_NO` 字段为准**（A 单题号；C/D 取 ChatGPT 段的 `QUESTION_NO`）。**禁止仅凭 `GLOBAL_SEQ` 反推题号**——`GLOBAL_SEQ` 只是元数据。
5. **读题**：从仓库 `papers/` 读取对应教师 PDF，完整读题（含题图；读不到图则依据题干文字作答并注明「未读图」）。
6. **解题**：给出分步推导（写明所用规律与公式）+ 最终答案（选择只写 `A/B/C/D`；计算/解答写数值+单位或表达式）。不得向 WorkBuddy 索取答案，不得引用他人结果。

---

## 4. 回写契约（OUTPUT_CONTRACT）

在 `results/chatgpt-{line}/TASK-P1-GIT-{LINE}-YYYYMMDD-HHMM.md` 的**正文开头**必须含：

```
TASK_ID=P1-GIT-<LINE>-YYYYMMDD-HHMM
SCHEDULE_ID=CHATGPT_<LINE>_YYYY-MM-DDTHH:MM:SS+08:00
GLOBAL_SEQ=<n>
QUESTION_NO=Q<n>          # A 单题号；C/D 用 ChatGPT 段的 q_chat
INPUT_COMMIT=<sha>
RESULT=results/chatgpt-<line>/TASK-P1-GIT-<LINE>-YYYYMMDD-HHMM.md
```

- 只提交**自己的**结果文件，不修改 WorkBuddy 的 `workbuddy/*_orders/`、不修改另一线的派单与既有结果、不覆盖任何其它代码。
- 交付方式：通过 GitHub（REST Contents API 或 git push）写入上述 git 路径即可；**不要再写 Drive**。

---

## 5. C/D 接力补充说明

- C/D 派单含两段题：Buddy 段（Q_buddy，由负责 Buddy 段的 WorkBuddy relay 在 git 完成，交付 `results/chatgpt-{c,d}/buddy-<TASK_ID>.md`）+ ChatGPT 段（Q_chat，由你完成，交付 `results/chatgpt-{c,d}/<TASK_ID>.md`）。
- 你（ChatGPT）**只做 ChatGPT 段（Q_chat）**，回写上述 git 路径；Buddy 段不是你的职责。
- 两段题号不同、互不影响；你不得修改 Buddy 段的交付。

---

## 6. 隔离与兜底

- 不替 WorkBuddy 作答，不修改其派单与原始答案，不覆盖任何其它派单、结果或既有代码。
- 若仓库不可达、token 失效、读不到题图等：在结果文件与回执中如实标注，不要伪造 `INPUT_COMMIT` 或 `commit_sha`。
- 本指令与任意历史规则冲突时，**以本指令与派单文件为准**。
