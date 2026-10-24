# P1-GIT-A/C/D 路径与编号权威对齐参考（给 ChatGPT）

> 用途：WorkBuddy 让 ChatGPT 对齐 A/C/D 三线的 **Drive / Git 绝对路径** 与 **任务文档编号**。
> 权威仓库统一为 `kaibahaha/xxsc` @ 分支 `exp/p1-relay-dualwrite-20261023`
> （已确认无 `OutsiderVictor/xxsc` 残留；协作者仅 kaibahaha，ChatGPT 以 kaibahaha 身份读写）。

---

## 0. Git 仓库身份（全局统一）

| 项 | 值 |
|---|---|
| 仓库 | `kaibahaha/xxsc` |
| 分支 | `exp/p1-relay-dualwrite-20261023` |
| 协议文档 | `docs/03-testing/2026-10-23-P1-Git-Drive-dualwrite-protocol.md` |
| 实验截止 | `2026-10-25T12:00:00+08:00`（之后只报只读统计，不再派单/写 git） |
| 派单频率 | 每 30 分钟一格（整点 / 半点） |

**教师版 PDF 来源（A / C/D 的 ChatGPT 段读题用）：**
- PHYSICS：`2025北京五十中高一10月月考物理（教师版）.pdf`，Google Drive file id `1p6pOP5mWVN9-gYBBxtn3uB7RjUOm6jl5`（题号 1..24）
- MATH：`2025-2026学年北京市十一实验中学高一（上）第一次段考数学试卷.pdf`，Google Drive file id `1siyRIDyk_7VYvJVE7wFIC400Nqi9OvCV`（题号 1..22，备用）
- ⚠️ 当前 git 派单只引用 **PHYSICS**（1..24）；MATH 为 Drive 旧 relay 体系备用，git 派单不主动使用。

---

## 1. 三线绝对路径表

| 线路 | 在 Drive 的绝对路径 | 在 Git 的绝对路径（分支 `exp/p1-relay-dualwrite-20261023`） |
|---|---|---|
| **A** | **派单：无（git-only，2026-10-24 拍板取消 Drive 领取，见第 6 节）**<br>结果镜像文件夹：`12qx-6ixnWJbdbBGZB0JUevDNuR0gi9uL`（V4.0 已有，仅镜像、非派单源） | 派单：`workbuddy/a_orders/TASK-P1-GIT-A-YYYYMMDD-HHMM.md`<br>ChatGPT 回写结果：`results/chatgpt-a/TASK-P1-GIT-A-YYYYMMDD-HHMM.md`<br>WorkBuddy ACK：`workbuddy/acks/P1-GIT-A-YYYYMMDD-HHMM-<RUN_ID>.json` |
| **C** | 账本 DOCX file id `1h_9jKCPw8ecUFNKc9E3-nRrg6fWpzco6`<br>URL：`https://drive.google.com/file/d/1h_9jKCPw8ecUFNKc9E3-nRrg6fWpzco6/view`<br>（WorkBuddy 以 `WORKBUDDY_C` ASSIGN 块写入；Buddy 段交付 + ChatGPT 段镜像同名文件） | 派单：`workbuddy/c_orders/TASK-P1-GIT-C-YYYYMMDD-HHMM.md`<br>ChatGPT 回写结果：`results/chatgpt-c/TASK-P1-GIT-C-YYYYMMDD-HHMM.md`<br>WorkBuddy ACK：`workbuddy/acks/P1-GIT-C-YYYYMMDD-HHMM-<RUN_ID>.json` |
| **D** | 同上账本 DOCX（file id `1h_9jKCPw8ecUFNKc9E3-nRrg6fWpzco6`），WorkBuddy 以 `WORKBUDDY_D` ASSIGN 块写入 | 派单：`workbuddy/d_orders/TASK-P1-GIT-D-YYYYMMDD-HHMM.md`<br>ChatGPT 回写结果：`results/chatgpt-d/TASK-P1-GIT-D-YYYYMMDD-HHMM.md`<br>WorkBuddy ACK：`workbuddy/acks/P1-GIT-D-YYYYMMDD-HHMM-<RUN_ID>.json` |

**Git 文件完整 URL 示例（A，00:30 槽）：**
`https://github.com/kaibahaha/xxsc/blob/exp/p1-relay-dualwrite-20261023/workbuddy/a_orders/TASK-P1-GIT-A-20261024-0030.md`

**Drive 账本 DOCX 示例行（Buddy 段）：** `EVENT_TYPE=ASSIGN / TASK_ID=WORKBUDDY_C / SCHEDULE_ID=WORKBUDDY_C_2026-10-24T00:30:00+08:00 / QUESTION_NO=Q22 / STATUS=ASSIGNED`

---

## 2. 任务文档编号规则（必须严格沿用派单文件，缺失/冲突记 `BLOCKED/REWORK`，不得猜测）

### 2.0 编号权威链（对齐 ChatGPT A V4.0，澄清后无冲突）

| 字段 | 用途 | 是否决定 A 解哪道题 |
|---|---|---|
| `QUESTION_NO`（**派单文件内的字段**） | 有效 WorkBuddy 派单指定的题号 | **是** |
| `GLOBAL_SEQ` | WorkBuddy 每 30 分钟派单的序号，仅派单元数据 | 否 |
| `SCHEDULED_A_RUN` | ChatGPT A 每小时 `:35` 的实际计划轮次，属 ChatGPT 自己的调度 | 否 |

规则（ChatGPT A 必须遵守）：
1. **必须实际读取有效派单文件**，从文件里取 `QUESTION_NO`，并核验 `ASSIGNEE=CHATGPT_A`、学科、PDF ID、到期时间后才执行；
2. **禁止仅凭 `GLOBAL_SEQ` 反推题号**——WorkBuddy 的「SEQ=14→Q14」只是它写派单那一刻的计算，写进文件后**以文件里的 `QUESTION_NO` 字段为准**；
3. `GLOBAL_SEQ` / `SCHEDULED_A_RUN` 只作元数据，不覆盖 ChatGPT A 的每小时调度。

### 2.1 字段生成规则（WorkBuddy 侧）

- **SLOT（计划时刻）**：把当前北京时间向下取整到 `:00` / `:30` 边界。
- **GLOBAL_SEQ**：`1 + floor((SLOT − 2026-10-23T18:00:00+08:00) / 30分钟)`
- **TASK_ID**：`P1-GIT-{LINE}-{YYYYMMDD}-{HH}{MM}`，其中 `MM ∈ {00, 30}`
  - 例：`P1-GIT-A-20261024-0030`、`P1-GIT-C-20261024-0030`、`P1-GIT-D-20261024-0030`
  - Git 内文件名 = `TASK-{TASK_ID}.md`
- **SCHEDULE_ID**：`CHATGPT_{LINE}_<SLOT_ISO>`，`SLOT_ISO = YYYY-MM-DDTHH:MM:SS+08:00`
  - 例：`CHATGPT_A_2026-10-24T00:30:00+08:00`
- **ASSIGNEE**：`CHATGPT_{LINE}`（A→CHATGPT_A，C→CHATGPT_C，D→CHATGPT_D）
- **QUESTION_NO**：
  - **A**：`Q = ((GLOBAL_SEQ − 1) mod 24) + 1`（物理题 1..24 顺序循环）
  - **C/D 接力两题**（Buddy 段 + ChatGPT 段；两题不同、依次错开 1 题；C 偏移 8、D 偏移 16）：
    - `q_buddy = ((GLOBAL_SEQ − 1 + Q_OFFSET) mod 24) + 1`
    - `q_chat  = ((GLOBAL_SEQ − 1 + Q_OFFSET + 1) mod 24) + 1`
    - `Q_OFFSET = {A:0, C:8, D:16}`
  - 例（SEQ=14）：A→Q14；C→Buddy Q22 / ChatGPT Q23；D→Buddy Q6 / ChatGPT Q7
- **INPUT_COMMIT**：本派单文件提交到 git 时的 commit SHA（WorkBuddy 回写，ChatGPT 原样带回）。

---

## 3. ChatGPT 回写契约（OUTPUT_CONTRACT）

结果文件正文开头必须含（A 用单题号；C/D 用 ChatGPT 段的 `q_chat`）：

```
TASK_ID=P1-GIT-<LINE>-YYYYMMDD-HHMM
SCHEDULE_ID=CHATGPT_<LINE>_YYYY-MM-DDTHH:MM:SS+08:00
GLOBAL_SEQ=<n>
QUESTION_NO=Q<n>          # A 单题号；C/D 用 ChatGPT 段的 q_chat
INPUT_COMMIT=<sha>
RESULT=results/chatgpt-<line>/TASK-P1-GIT-<LINE>-YYYYMMDD-HHMM.md
```

- **A**：仅 git，不写 Drive。
- **C/D ChatGPT 段**：写 git `results/chatgpt-{c,d}/<TASK_ID>.md`；如需镜像 Drive，用同名文件写入上方账本 DOCX（`1h_9jKCPw8ecUFNKc9E3-nRrg6fWpzco6`）。
- 只提交自己的结果文件，不修改 WorkBuddy 的 `workbuddy/*_orders/`、不改其它线路派单与既有结果。

---

## 4. 一个真实待对齐点（请 ChatGPT 注意）

- Drive 旧 relay（`relay_lib.py`）的 C/D 选题是 **随机**（50% 物理 / 50% 数学，随机题号），
  与 git 派单的 **GLOBAL_SEQ 物理顺序** 不同步。
- **对齐口径：以 git 派单里的 Q 题号为准**（ChatGPT 段用 `q_chat`）；
  Buddy 段在 Drive 账本里的选题是独立随机的，不与 git 题号一一对应，属设计差异，不要求强行一致。

---

## 5. 派单位置 ≠ 成果交付位置（重要区分）

- **派单入口**（上面表格）与**结果交付/镜像目录**是两回事，不能混用。
- 账本 DOCX（`1h_9jKCPw8ecUFNKc9E3-nRrg6fWpzco6`）**只是 C/D 的派单总账**，不是结果镜像目录。
- **A 的结果镜像文件夹**（ChatGPT A V4.0 已定义，WorkBuddy 确认沿用）：Drive folder id `12qx-6ixnWJbdbBGZB0JUevDNuR0gi9uL`。
  - 更正：WorkBuddy 此前说「还缺结果文件夹 ID」对 A 不成立——A 的结果镜像文件夹 V4.0 已有，即上面的 `12qx-6ixnWJbdbBGZB0JUevDNuR0gi9uL`。
- **C/D 的结果镜像文件夹**：待定（见第 7 节）。

---

## 6. 派单入口决策（2026-10-24 拍板）

**决定：A 正式改为 Git-only——取消 Drive 领取派单，只从 `kaibahaha/xxsc` 的 Git 实验分支 `exp/p1-relay-dualwrite-20261023` 领取。**

- 依据：①用户 2026-10-24 00:38 权威指令「A 只有 git 有、不进 Drive，目的是测试 ChatGPT 能否读取 git 并完成」；②实测 Drive relay（`relay_lib.py` 的 `run_round`）**只接受 `WORKBUDDY_C`/`WORKBUDDY_D`，从不产生 A 派单**——A 事实上从未在 Drive 出现过，本决定只是把现实正式化。
- 性质：这是对 ChatGPT A V4.0「Git+Drive 双源领取」规则的**一次新修订**（记作 A V4.1）。
- 影响范围：**仅派单入口**。不影响 Library 冻结归档，也不影响 A 的 Git/Drive 成果镜像（结果仍可写 git `results/chatgpt-a/` 并镜像 Drive `12qx-6ixnWJbdbBGZB0JUevDNuR0gi9uL`）。
- ChatGPT A 行为变化：**不再去 Drive 找 A 派单**，只读 git 的 `workbuddy/a_orders/TASK-P1-GIT-A-*.md`。

---

## 7. 结果交付与镜像（最终，2026-10-24 闭环）

- **A**：结果回写 git `results/chatgpt-a/`，并镜像到 Drive 文件夹 `12qx-6ixnWJbdbBGZB0JUevDNuR0gi9uL`（V4.0 已有）。
- **C/D**（2026-10-24 拍板）：**Drive 地址与原来一致，不额外镜像**。
  - Buddy 段：交付到 Drive 账本 DOCX `1h_9jKCPw8ecUFNKc9E3-nRrg6fWpzco6`（原地址不变，**不另建结果镜像文件夹**）。
  - ChatGPT 段：**只回写 git** `results/chatgpt-{c,d}/`，**不镜像到 Drive**。
- Git 派单流与 Drive 随机派题流是**不同订单流**，不能只凭题号合并；ChatGPT 段以 git 派单的 `QUESTION_NO` 为准（见 2.0 / 第 4 节）。
