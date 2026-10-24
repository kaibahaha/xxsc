# ACD → WorkBuddy 云端迁移 README

> 目的：把本地 ACD（A/C/D 三线 git 派单+回写）系统整体迁移到 WorkBuddy 云端。
> 云端 Buddy 拉取本目录下的程序与指令，在云端重建派单循环；ChatGPT 侧申领改为从 git 读取。
> 唯一变化：试卷 PDF 也放进 git（见 `source_pdf/`），云端据此解题与分配给 ChatGPT，不再依赖 Google Drive 原件。

## 1. 仓库与分支

- 仓库：`kaibahaha/xxsc`
- 分支：`exp/p1-relay-dualwrite-20261023`
- 本迁移包根目录：`workbuddy/acd_migration/`
- 原有派单/结果（运行时数据，仍在）：`workbuddy/{a,c,d}_orders/`、`results/chatgpt-{a,c,d}/`、`workbuddy/acks/`

## 2. 目录结构（本迁移包）

```
workbuddy/acd_migration/
├── MIGRATION_README.md                  # 本文件
├── ACD_THREE_LINE_INSTRUCTIONS.md       # A/C/D 三线派单指令全文（build_order 真实渲染）
├── code/                                # 全部本地程序代码
│   ├── p1git_dispatch.py                # 核心：单线派单（--line A|C|D），含 build_order/ACK/回读
│   ├── p1git_loop.py                    # 常驻循环：每 30 分钟对齐边界派 A→C→D（替代 WorkBuddy 定时任务）
│   ├── p1git_scheduler.py               # 旧 WorkBuddy 自动化调度器（参考，已被 loop 取代）
│   ├── list_orders.py / dump_results.py / stat_all.py   # 只读核查工具
│   ├── verify_slot.py / verify_0900.py / verify_readback.py  # 闭环核验工具
│   ├── device_auth.py / pat_setup.py / accept_invite.py / check_invites.py
│   ├── make_public.py / probe_repos.py / probe_now.py
│   └── verify_identity.py / verify_ov_token.py / wait_and_dispatch.py
├── instructions/                        # 指令/参考文档
│   ├── P1_ACD_PATHS_AND_NUMBERING_REF.md    # ACD 绝对路径+编号规则权威参考
│   ├── P1_ACD_BACKUP_INSTRUCTION.md         # 备份/接管指令
│   ├── P1GIT-A接入回执_20261023.md
│   └── P1GIT-A架构纠正_只读核对报告_20261023.md
└── source_pdf/                          # 试卷 PDF（迁移唯一新增项）
    ├── 2025北京五十中高一10月月考物理（教师版）.pdf   # ACD 物理题源（TEACHER_PDF）
    └── 2025-2026学年北京市十一实验中学高一（上）第一次段考数学试卷.pdf  # 同批 Drive 试卷（镜像）
```

> 未上传项（本机本地、不上传）：`state/github_token*.txt`（密钥，云端自备）、`state/runs.jsonl`/日志/pid/tickets（运行时状态）、`repo/`(git 工作副本)、`__pycache__`、`start_scheduler.vbs`(Windows 专用)、`_staging/dl_pdfs.py`(Drive 下载器，云端无需)。

## 3. 云端重建步骤

1. **准备 GitHub token**：云端 Buddy 用自己的 classic PAT（`ghp_` 或 `github_pat_`，scope `repo`）访问 `kaibahaha/xxsc`。可放环境变量 `GITHUB_TOKEN`，或落到 `code/` 同级 `state/github_token.txt`（脚本优先读取）。
2. **拉取程序**：把 `workbuddy/acd_migration/code/` 下所有 `.py` 取到云端工作区（需 Python 3 + `requests` 库）。
3. **启动派单**：直接跑常驻循环
   `python p1git_loop.py`（自动每 30 分钟派 A/C/D，自带去重；或单次 `python p1git_dispatch.py --line A`）。
   频率：整点/半点一格；`STOP_AT=2026-10-25T12:00+08:00` 后转只读（可按需改长）。
4. **⚠️ 唯一必改项——PDF 来源**：`code/p1git_dispatch.py` 里 `TEACHER_PDF` 现指向 Google Drive file id。云端改为从本仓库读取：
   - 物理解题用 `workbuddy/acd_migration/source_pdf/2025北京五十中高一10月月考物理（教师版）.pdf`
   - 将其 `gdrive_file_id` 字段替换为该 PDF 在 git 的 raw URL（或云端先 download 到本地再用本地路径）。
   - 其余字段（`question_range [1,24]`、`source_key PHYSICS`、`filename`）不变。
5. **ChatGPT 申领切 git**：见 `ACD_CHATGPT_SWITCH_INSTRUCTION.md`（转告 ChatGPT 的指令）。

## 4. 关键不变项

- 编号规则、目录布局、OUTPUT_CONTRACT（结果文件头 `TASK_ID/SCHEDULE_ID/GLOBAL_SEQ/QUESTION_NO/INPUT_COMMIT`）与本地完全一致，详见 `instructions/P1_ACD_PATHS_AND_NUMBERING_REF.md`。
- A = git-only（不写 Drive）；C/D = 接力（Buddy 自解 Qbuddy + ChatGPT 接手 Qchat），ChatGPT 段只回写 git，不镜像 Drive。
- `drive_probe()` / Buddy 段 Drive 交付依赖 `C:\Users\Administrator\.workbuddy\gdrive\gdrive_core`，云端若无此模块可跳过——Drive 账本 DOCX（`1h_9jKCPw8ecUFNKc9E3-nRrg6fWpzco6`）仅作镜像副本，git 为主链。

## 5. 绝对路径速查（给云端 Buddy / ChatGPT）

- 迁移包根：`https://github.com/kaibahaha/xxsc/tree/exp/p1-relay-dualwrite-20261023/workbuddy/acd_migration`
- 程序：`.../workbuddy/acd_migration/code`
- 指令全文：`.../workbuddy/acd_migration/ACD_THREE_LINE_INSTRUCTIONS.md`
- 试卷 PDF：`.../workbuddy/acd_migration/source_pdf`
- 运行时派单：`.../workbuddy/a_orders`、`.../workbuddy/c_orders`、`.../workbuddy/d_orders`
- 运行时回写：`.../results/chatgpt-a`、`.../results/chatgpt-c`、`.../results/chatgpt-d`
