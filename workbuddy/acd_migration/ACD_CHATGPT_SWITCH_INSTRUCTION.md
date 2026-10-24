# 转告 ChatGPT 的指令：定时任务申领改为从 git 读取

> 以下文字直接转给 ChatGPT（或粘贴为其定时任务的新指令）。

---

## 新指令（给 ChatGPT 的定时任务）

你原来的「从 Google Drive 账本领单」定时任务**改为从 GitHub 读取派单**。具体：

1. **申领来源切换**：不再扫描 Drive 账本 DOCX（`1h_9jKCPw8ecUFNKc9E3-nRrg6fWpzco6`）。改为**定时**（建议每 30 分钟）轮询 GitHub 仓库
   `kaibahaha/xxsc` 分支 `exp/p1-relay-dualwrite-20261023` 下的派单目录：
   - A 线：`workbuddy/a_orders/`
   - C 线：`workbuddy/c_orders/`
   - D 线：`workbuddy/d_orders/`
   读取最新的 `TASK-P1-GIT-{X}-YYYYMMDD-HHMM.md`（X = A/C/D）。

2. **按 QUESTION_NO 解题**：从派单文件里取 `QUESTION_NO` 字段决定做哪一题（A 线单题；C/D 线你只做 `ChatGPT 段` 那题，Buddy 段由 WorkBuddy 自解，不要碰）。
   物理题源 PDF 现在也在 git：`workbuddy/acd_migration/source_pdf/2025北京五十中高一10月月考物理（教师版）.pdf`，下载后按题号读题。

3. **回写位置（唯一交付地）**：把结果写回 git 同仓库
   - A：`results/chatgpt-a/P1-GIT-A-YYYYMMDD-HHMM.md`
   - C：`results/chatgpt-c/P1-GIT-C-YYYYMMDD-HHMM.md`
   - D：`results/chatgpt-d/P1-GIT-D-YYYYMMDD-HHMM.md`
   文件名 = 派单 `TASK_ID` 去掉 `TASK-` 前缀（例：派单 `TASK-P1-GIT-A-20261024-2130.md` → 结果 `P1-GIT-A-20261024-2130.md`）。
   结果文件开头必须包含：`TASK_ID=`、`SCHEDULE_ID=`、`GLOBAL_SEQ=`、`QUESTION_NO=`、`INPUT_COMMIT=`，并附 `GIT_ORDER_BLOB_SHA=`（派单文件的 blob SHA，用于验明你确实读了这份 git 派单）。

4. **等云端给绝对路径与说明**：迁移程序与完整指令已上传到 git 目录 `workbuddy/acd_migration/`（含 `ACD_THREE_LINE_INSTRUCTIONS.md` 三线派单全文、`MIGRATION_README.md` 重建步骤）。**在云端 Buddy 告诉你具体绝对路径与指令说明之前，先按上面的通用规则接 git；细节以云端给出的 `acd_migration/` 文件为准。**

5. **原 Drive 题保留为镜像**：`1h_9jKCPw8ecUFNKc9E3-nRrg6fWpzco6` 账本 DOCX 继续作为镜像/副本存放你过往的 Drive 成品，**不删除、不迁移**，与 git 主链并存。

6. **不要做的事**：不要写 Google Drive 作为交付（C/D 的 ChatGPT 段只回 git）；不要修改别人的派单与结果；不要按旧「Drive 镜像」句式执行任何 Drive 写入。

---

## 判定闭环

只有当 `results/chatgpt-{a,c,d}/` 出现对应 `P1-GIT-{X}-*.md` 且内容经独立回读验证（含正确 `GIT_ORDER_BLOB_SHA`），才算该单闭环。派单成功 ≠ 回写成功。
