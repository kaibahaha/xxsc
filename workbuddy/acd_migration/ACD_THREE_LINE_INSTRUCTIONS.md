# ACD 三线定时任务指令全文（迁移版）
> 本文件由 `p1git_dispatch.py::build_order()` 真实渲染产出，是云端 Buddy 重建 A/C/D 三条定时任务时各自派单指令的**权威全文**。
> 渲染示例槽位：A/C/D 各取一例（题号随 GLOBAL_SEQ 滚动，结构不变）。

---

## 线 A 派单指令全文

```markdown
# P1-GIT-A-20261024-2130 | CHATGPT_A 物理顺序解题派单（git-only 测试，不写 Drive）

## 1. 元信息

| 字段 | 值 |
|---|---|
| TASK_ID | `P1-GIT-A-20261024-2130` |
| ASSIGNEE | `CHATGPT_A` |
| DISPATCHER | `WORKBUDDY`（P1-GIT-A 工位 V1.1） |
| 计划时刻（北京） | `2026-10-24T21:30:00+08:00` |
| CREATED_AT | `2026-10-24T21:30:00+08:00` |
| SCHEDULE_ID | `CHATGPT_A_2026-10-24T21:30:00+08:00` |
| GLOBAL_SEQ | `56` |
| QUESTION_NO | `Q8` |
| SOURCE_KEY | `PHYSICS` |
| 教师PDF来源ID（Google Drive） | `1p6pOP5mWVN9-gYBBxtn3uB7RjUOm6jl5` |
| 教师PDF文件名 | `2025北京五十中高一10月月考物理（教师版）.pdf` |
| INPUT_COMMIT | `SAMPLE_INPUT_COMMIT` |
| REPO / BRANCH | `kaibahaha/xxsc` / `exp/p1-relay-dualwrite-20261023` |
| 协议 | `docs/03-testing/2026-10-23-P1-Git-Drive-dualwrite-protocol.md` |
| 实验截止 | `2026-10-25T12:00:00+08:00` |

## 2. OBJECTIVE（解题要求，git-only）

独立求解 **2025北京五十中高一10月月考物理（教师版）.pdf 第 8 题（Q8）**，来源教师版 PDF：
`2025北京五十中高一10月月考物理（教师版）.pdf`（Google Drive file ID `1p6pOP5mWVN9-gYBBxtn3uB7RjUOm6jl5`）。

要求：
1. 完整读题后给出**分步推导**，写明所用物理规律与公式；
2. 给出**最终答案**：选择题只写大写字母 `A/B/C/D`；计算/解答题写数值+单位或表达式；
3. 不得向 WorkBuddy 索取答案，不得引用他人结果；

## 3. INPUT_FILES

- 教师版 PDF（Google Drive）：`2025北京五十中高一10月月考物理（教师版）.pdf`（file id `1p6pOP5mWVN9-gYBBxtn3uB7RjUOm6jl5`）
- 本派单文件：`workbuddy/a_orders/TASK-P1-GIT-A-20261024-2130.md`（分支 `exp/p1-relay-dualwrite-20261023`）
- 实验协议：`docs/03-testing/2026-10-23-P1-Git-Drive-dualwrite-protocol.md`

## 4. ACCEPTANCE_CRITERIA（git-only，不写 Drive）

1. 结果文件名 `results/chatgpt-a/P1-GIT-A-20261024-2130.md`，正文开头标注 `TASK_ID`、`SCHEDULE_ID`、`GLOBAL_SEQ`、`QUESTION_NO`、`INPUT_COMMIT`；
2. **仅回写 git**：`results/chatgpt-a/P1-GIT-A-20261024-2130.md`（分支 `exp/p1-relay-dualwrite-20261023`）；本次不要求写入 Google Drive；
3. 正文完整，不使用占位符；若读不到题图，依据题干文字作答并注明「未读图」。

## 5. RESULT_EXPECTED_PATH

- GitHub（唯一交付地）：`results/chatgpt-a/P1-GIT-A-20261024-2130.md`

## 6. OUTPUT_CONTRACT

```
TASK_ID=P1-GIT-A-20261024-2130
SCHEDULE_ID=CHATGPT_A_2026-10-24T21:30:00+08:00
GLOBAL_SEQ=56
QUESTION_NO=Q8
INPUT_COMMIT=SAMPLE_INPUT_COMMIT
RESULT=results/chatgpt-a/P1-GIT-A-20261024-2130.md
```

## 7. 隔离声明

WorkBuddy 只负责发布本指令、提交派单、回读 A 结果与写自己的 ACK；
不替 A 解题，不修改 A 的原始答案，不覆盖任何 C/D 派单、结果或既有代码。

```

---

## 线 C 派单指令全文

```markdown
# P1-GIT-C-20261024-2130 | CHATGPT_C 接力解题派单（Buddy 做 Q16，ChatGPT 做 Q17）

## 1. 元信息

| 字段 | 值 |
|---|---|
| TASK_ID | `P1-GIT-C-20261024-2130` |
| ASSIGNEE | `CHATGPT_C` |
| DISPATCHER | `WORKBUDDY`（P1-GIT-C 工位 V1.1） |
| 计划时刻（北京） | `2026-10-24T21:30:00+08:00` |
| CREATED_AT | `2026-10-24T21:30:00+08:00` |
| SCHEDULE_ID | `CHATGPT_C_2026-10-24T21:30:00+08:00` |
| GLOBAL_SEQ | `56` |
| QUESTION_NO (Buddy 段) | `Q16` |
| QUESTION_NO (ChatGPT 段) | `Q17` |
| SOURCE_KEY | `PHYSICS` |
| 教师PDF来源ID（Google Drive） | `1p6pOP5mWVN9-gYBBxtn3uB7RjUOm6jl5` |
| 教师PDF文件名 | `2025北京五十中高一10月月考物理（教师版）.pdf` |
| INPUT_COMMIT | `SAMPLE_INPUT_COMMIT` |
| REPO / BRANCH | `kaibahaha/xxsc` / `exp/p1-relay-dualwrite-20261023` |
| 协议 | `docs/03-testing/2026-10-23-P1-Git-Drive-dualwrite-protocol.md` |
| 实验截止 | `2026-10-25T12:00:00+08:00` |

## 2. RELAY 接力结构（两题两段）

- **第 1 段 · Buddy 自解**：WorkBuddy 选 **第 16 题（Q16）**，独立完成并交付到 Drive 账本 DOCX `1h_9jKCPw8ecUFNKc9E3-nRrg6fWpzco6`（地址与原来一致，不另建镜像）。
- **第 2 段 · ChatGPT 接手**：再选 **第 17 题（Q17）**，由 ChatGPT 读取本派单后在 git 完成并回写。
- 两题不同、互不影响；Buddy 不替 ChatGPT 作答，ChatGPT 不修改 Buddy 的交付。
- **交付覆盖规则（2026-10-24 起生效）**：ChatGPT 段**只回写 git，不额外镜像 Drive**。本规则取代 `TASK-P1-GIT-C/D-20261024-0030` 及更早订单中的「ChatGPT 段（Drive 镜像）：同文件名写入 C/D 资料夹」一句；历史订单不改写，一切以本派单为准。覆盖规则明确前，不得按旧句执行任何 Drive 写入。

## 3. OBJECTIVE · Buddy 段（自解 Q16）

WorkBuddy 独立求解 **2025北京五十中高一10月月考物理（教师版）.pdf 第 16 题（Q16）**，来源教师版 PDF：
`2025北京五十中高一10月月考物理（教师版）.pdf`（Google Drive file ID `1p6pOP5mWVN9-gYBBxtn3uB7RjUOm6jl5`）。

要求：完整读题后给出分步推导与最终答案；结果交付到 Drive 账本 DOCX `1h_9jKCPw8ecUFNKc9E3-nRrg6fWpzco6`（与 ChatGPT 段同任务目录，与原来一致）。

## 4. OBJECTIVE · ChatGPT 段（接手 Q17，git 回写）

ChatGPT 独立求解 **2025北京五十中高一10月月考物理（教师版）.pdf 第 17 题（Q17）**，来源同上教师版 PDF。

要求：
1. 完整读题后给出**分步推导**，写明所用物理规律与公式；
2. 给出**最终答案**：选择题只写大写字母 `A/B/C/D`；计算/解答题写数值+单位或表达式；
3. 不得向 WorkBuddy 索取答案，不得引用他人结果；

## 5. INPUT_FILES

- 教师版 PDF（Google Drive）：`2025北京五十中高一10月月考物理（教师版）.pdf`（file id `1p6pOP5mWVN9-gYBBxtn3uB7RjUOm6jl5`）
- 本派单文件：`workbuddy/c_orders/TASK-P1-GIT-C-20261024-2130.md`（分支 `exp/p1-relay-dualwrite-20261023`）
- 实验协议：`docs/03-testing/2026-10-23-P1-Git-Drive-dualwrite-protocol.md`

## 6. ACCEPTANCE_CRITERIA

1. Buddy 段：WorkBuddy 完成 Q16 并交付到 Drive 账本 DOCX 1h_9jKCPw8ecUFNKc9E3-nRrg6fWpzco6（地址与原来一致，不另建镜像）；
2. ChatGPT 段：结果文件名 `results/chatgpt-c/P1-GIT-C-20261024-2130.md`，正文开头标注 `TASK_ID`、`SCHEDULE_ID`、`GLOBAL_SEQ`、`QUESTION_NO`、`INPUT_COMMIT`；
3. ChatGPT 段结果**回写 git**：`results/chatgpt-c/P1-GIT-C-20261024-2130.md`（分支 `exp/p1-relay-dualwrite-20261023`）——**唯一交付地，不额外镜像 Drive**；本要求取代 20261024-0030 及更早订单中的「Drive 镜像」一句，历史订单不改写、以本派单为准；
4. 只提交自己的结果文件，不修改 WorkBuddy 的 `workbuddy/c_orders/`、不修改另一段的派单与既有结果；
5. 正文完整，不使用占位符；若读不到题图，依据题干文字作答并注明「未读图」。

## 7. RESULT_EXPECTED_PATH

- Buddy 段（Drive）：账本 DOCX 1h_9jKCPw8ecUFNKc9E3-nRrg6fWpzco6 / `P1-GIT-C-20261024-2130.md`（与原来一致）
- ChatGPT 段（git，唯一交付地）：`results/chatgpt-c/P1-GIT-C-20261024-2130.md`（分支 `exp/p1-relay-dualwrite-20261023`）；**只回写 git，不额外镜像 Drive**（本规则取代 20261024-0030 及更早订单中的「ChatGPT 段（Drive 镜像）：同文件名写入 C/D 资料夹」一句，以本派单为准）

## 8. OUTPUT_CONTRACT（ChatGPT 段）

```
TASK_ID=P1-GIT-C-20261024-2130
SCHEDULE_ID=CHATGPT_C_2026-10-24T21:30:00+08:00
GLOBAL_SEQ=56
QUESTION_NO=Q17
INPUT_COMMIT=SAMPLE_INPUT_COMMIT
RESULT=results/chatgpt-c/P1-GIT-C-20261024-2130.md
```

## 9. 隔离声明

WorkBuddy 只负责发布本指令、提交派单、回读 ChatGPT 段结果与写自己的 ACK；
不替 ChatGPT 作答，不修改 ChatGPT 的原始答案，不覆盖任何其它派单、结果或既有代码。

```

---

## 线 D 派单指令全文

```markdown
# P1-GIT-D-20261024-2130 | CHATGPT_D 接力解题派单（Buddy 做 Q24，ChatGPT 做 Q1）

## 1. 元信息

| 字段 | 值 |
|---|---|
| TASK_ID | `P1-GIT-D-20261024-2130` |
| ASSIGNEE | `CHATGPT_D` |
| DISPATCHER | `WORKBUDDY`（P1-GIT-D 工位 V1.1） |
| 计划时刻（北京） | `2026-10-24T21:30:00+08:00` |
| CREATED_AT | `2026-10-24T21:30:00+08:00` |
| SCHEDULE_ID | `CHATGPT_D_2026-10-24T21:30:00+08:00` |
| GLOBAL_SEQ | `56` |
| QUESTION_NO (Buddy 段) | `Q24` |
| QUESTION_NO (ChatGPT 段) | `Q1` |
| SOURCE_KEY | `PHYSICS` |
| 教师PDF来源ID（Google Drive） | `1p6pOP5mWVN9-gYBBxtn3uB7RjUOm6jl5` |
| 教师PDF文件名 | `2025北京五十中高一10月月考物理（教师版）.pdf` |
| INPUT_COMMIT | `SAMPLE_INPUT_COMMIT` |
| REPO / BRANCH | `kaibahaha/xxsc` / `exp/p1-relay-dualwrite-20261023` |
| 协议 | `docs/03-testing/2026-10-23-P1-Git-Drive-dualwrite-protocol.md` |
| 实验截止 | `2026-10-25T12:00:00+08:00` |

## 2. RELAY 接力结构（两题两段）

- **第 1 段 · Buddy 自解**：WorkBuddy 选 **第 24 题（Q24）**，独立完成并交付到 Drive 账本 DOCX `1h_9jKCPw8ecUFNKc9E3-nRrg6fWpzco6`（地址与原来一致，不另建镜像）。
- **第 2 段 · ChatGPT 接手**：再选 **第 1 题（Q1）**，由 ChatGPT 读取本派单后在 git 完成并回写。
- 两题不同、互不影响；Buddy 不替 ChatGPT 作答，ChatGPT 不修改 Buddy 的交付。
- **交付覆盖规则（2026-10-24 起生效）**：ChatGPT 段**只回写 git，不额外镜像 Drive**。本规则取代 `TASK-P1-GIT-C/D-20261024-0030` 及更早订单中的「ChatGPT 段（Drive 镜像）：同文件名写入 C/D 资料夹」一句；历史订单不改写，一切以本派单为准。覆盖规则明确前，不得按旧句执行任何 Drive 写入。

## 3. OBJECTIVE · Buddy 段（自解 Q24）

WorkBuddy 独立求解 **2025北京五十中高一10月月考物理（教师版）.pdf 第 24 题（Q24）**，来源教师版 PDF：
`2025北京五十中高一10月月考物理（教师版）.pdf`（Google Drive file ID `1p6pOP5mWVN9-gYBBxtn3uB7RjUOm6jl5`）。

要求：完整读题后给出分步推导与最终答案；结果交付到 Drive 账本 DOCX `1h_9jKCPw8ecUFNKc9E3-nRrg6fWpzco6`（与 ChatGPT 段同任务目录，与原来一致）。

## 4. OBJECTIVE · ChatGPT 段（接手 Q1，git 回写）

ChatGPT 独立求解 **2025北京五十中高一10月月考物理（教师版）.pdf 第 1 题（Q1）**，来源同上教师版 PDF。

要求：
1. 完整读题后给出**分步推导**，写明所用物理规律与公式；
2. 给出**最终答案**：选择题只写大写字母 `A/B/C/D`；计算/解答题写数值+单位或表达式；
3. 不得向 WorkBuddy 索取答案，不得引用他人结果；

## 5. INPUT_FILES

- 教师版 PDF（Google Drive）：`2025北京五十中高一10月月考物理（教师版）.pdf`（file id `1p6pOP5mWVN9-gYBBxtn3uB7RjUOm6jl5`）
- 本派单文件：`workbuddy/d_orders/TASK-P1-GIT-D-20261024-2130.md`（分支 `exp/p1-relay-dualwrite-20261023`）
- 实验协议：`docs/03-testing/2026-10-23-P1-Git-Drive-dualwrite-protocol.md`

## 6. ACCEPTANCE_CRITERIA

1. Buddy 段：WorkBuddy 完成 Q24 并交付到 Drive 账本 DOCX 1h_9jKCPw8ecUFNKc9E3-nRrg6fWpzco6（地址与原来一致，不另建镜像）；
2. ChatGPT 段：结果文件名 `results/chatgpt-d/P1-GIT-D-20261024-2130.md`，正文开头标注 `TASK_ID`、`SCHEDULE_ID`、`GLOBAL_SEQ`、`QUESTION_NO`、`INPUT_COMMIT`；
3. ChatGPT 段结果**回写 git**：`results/chatgpt-d/P1-GIT-D-20261024-2130.md`（分支 `exp/p1-relay-dualwrite-20261023`）——**唯一交付地，不额外镜像 Drive**；本要求取代 20261024-0030 及更早订单中的「Drive 镜像」一句，历史订单不改写、以本派单为准；
4. 只提交自己的结果文件，不修改 WorkBuddy 的 `workbuddy/d_orders/`、不修改另一段的派单与既有结果；
5. 正文完整，不使用占位符；若读不到题图，依据题干文字作答并注明「未读图」。

## 7. RESULT_EXPECTED_PATH

- Buddy 段（Drive）：账本 DOCX 1h_9jKCPw8ecUFNKc9E3-nRrg6fWpzco6 / `P1-GIT-D-20261024-2130.md`（与原来一致）
- ChatGPT 段（git，唯一交付地）：`results/chatgpt-d/P1-GIT-D-20261024-2130.md`（分支 `exp/p1-relay-dualwrite-20261023`）；**只回写 git，不额外镜像 Drive**（本规则取代 20261024-0030 及更早订单中的「ChatGPT 段（Drive 镜像）：同文件名写入 C/D 资料夹」一句，以本派单为准）

## 8. OUTPUT_CONTRACT（ChatGPT 段）

```
TASK_ID=P1-GIT-D-20261024-2130
SCHEDULE_ID=CHATGPT_D_2026-10-24T21:30:00+08:00
GLOBAL_SEQ=56
QUESTION_NO=Q1
INPUT_COMMIT=SAMPLE_INPUT_COMMIT
RESULT=results/chatgpt-d/P1-GIT-D-20261024-2130.md
```

## 9. 隔离声明

WorkBuddy 只负责发布本指令、提交派单、回读 ChatGPT 段结果与写自己的 ACK；
不替 ChatGPT 作答，不修改 ChatGPT 的原始答案，不覆盖任何其它派单、结果或既有代码。

```

---

## 云端适配说明（唯一变化）

- **试卷 PDF 来源改为 git**：原指令中 `教师PDF来源ID（Google Drive）` 与 `Google Drive file ID` 两行，在云端应指向本仓库 `workbuddy/acd_migration/source_pdf/` 下的 PDF（raw 路径见 MIGRATION_README）。云端 Buddy 下载该 PDF 后即可按 `QUESTION_NO` 解题与分配给 ChatGPT，无需再访问 Google Drive。
- **ChatGPT 申领改为从 git 读取**：ChatGPT 的定时任务不再从 Drive 账本领单，改为定时扫描 `workbuddy/{a,c,d}_orders/` 目录、读取最新 `TASK-P1-GIT-{X}-*.md`、按 `QUESTION_NO` 解题、回写 `results/chatgpt-{a,c,d}/`。详见 MIGRATION_README 与转告 ChatGPT 的指令。
- **原 Drive 题保留为镜像**：`1h_9jKCPw8ecUFNKc9E3-nRrg6fWpzco6` 账本 DOCX 继续作为镜像/副本存放，不影响 git 为主链。
