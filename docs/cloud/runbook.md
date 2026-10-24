# P1-GIT A/C/D · 云端运行手册（V1.2，已弃用 Google Drive）

> 本手册供 **云端 WorkBuddy**（腾讯云沙箱）在无人值守下运行 P1-GIT A/C/D 派单工位。
> 配套脚本：`p1git_dispatch.py`（仓库根目录）。本仓库即唯一真相源与唯一交付通道。

---

## 0. 一句话背景

- 原本地派单工位（V1.1）每 30 分钟向 GitHub 实验分支提交一份解题派单，并只读探测 Google Drive。
- **云端沙箱无法连接 Google Drive**，因此 V1.2 的唯一功能变化是：**彻底弃用 Drive**——
  教师 PDF 改为随仓库提交（见 `papers/`），所有派单/交付/回读都在 git 完成，Drive 仅作历史镜像。
- 序列锚点 `ANCHOR = 2026-10-23T18:00:00+08:00` 保持不变，云端续跑时 `GLOBAL_SEQ` / `QUESTION_NO` 与既有序列无缝衔接。

---

## 1. 仓库与分支（全局统一）

| 项 | 值 |
|---|---|
| 仓库 | `kaibahaha/xxsc` |
| 分支 | `exp/p1-relay-dualwrite-20261023` |
| 派单工位脚本 | `p1git_dispatch.py`（仓库根目录） |
| 依赖 | `requests`（见 `requirements.txt`）；**不再需要** google-* 库 |
| 派单频率 | 每 30 分钟一格（整点 / 半点） |
| 教师 PDF | `papers/2025北京五十中高一10月月考物理（教师版）.pdf`（PHYSICS，题号 1..24，主用）<br>`papers/2025-2026学年北京市十一实验中学高一（上）第一次段考数学试卷.pdf`（MATH，题号 1..22，备用） |

---

## 2. 云端沙箱启动步骤（每次任务触发时由云端 WorkBuddy 执行）

1. **取代码**：把 `kaibahaha/xxsc` @ `exp/p1-relay-dualwrite-20261023` 克隆（或拉取）到一个**持久化目录**（如 `/home/runner/p1git-xxsc`）。
   若目录已存在则 `git fetch origin` + `git reset --hard origin/exp/p1-relay-dualwrite-20261023`。
2. **装依赖**：确认 Python3 可用；执行 `pip install -r requirements.txt`（通常只需 `requests`）。
3. **配凭据**：必须提供 `GITHUB_TOKEN`（仓库读写用的 classic PAT），以环境变量注入：
   `export GITHUB_TOKEN=****`。
   - 若云端通过 GitHub 连接器取 token，请先从中取出 PAT 再 export；
   - 也可把 PAT 存入任务「密钥/环境变量」后由运行时注入。**没有 token 则无法写仓库。**
4. **跑派单**（按线路选择其一）：
   ```bash
   cd /home/runner/p1git-xxsc
   export P1GIT_REPO_DIR=/home/runner/p1git-xxsc      # 仓库根目录（脚本订单/结果相对它）
   export P1GIT_STATE_DIR=/tmp/p1git_state            # 可写目录，避免污染仓库
   # A 线路：
   python p1git_dispatch.py --line A
   # C 线路：
   python p1git_dispatch.py --line C
   # D 线路：
   python p1git_dispatch.py --line D
   ```
5. **读结果**：脚本退出后，把 `last_report.json`（在 `P1GIT_STATE_DIR` 内）的 8 行摘要原样汇报。

---

## 3. 环境变量速查

| 变量 | 必填 | 说明 |
|---|---|---|
| `GITHUB_TOKEN` | 是 | 仓库读写 classic PAT；无则无法派单 |
| `P1GIT_REPO_DIR` | 否 | 克隆后的仓库根目录（含 `workbuddy/`、`results/`、`papers/`）；缺省回退当前工作目录 |
| `P1GIT_STATE_DIR` | 否 | 可写状态目录（`runs.jsonl`/`last_report.json`）；缺省回退系统临时目录 |
| `P1GIT_OWNER` | 否 | 仓库归属，默认 `kaibahaha` |
| `P1GIT_STOP_AT` | 否 | 形如 `2026-10-25T12:00:00+08:00`；**不设则云端持续运行（默认无硬性截止）** |

---

## 4. 三条线路的分工（务必遵守隔离）

| 线路 | 派单目录 | ChatGPT 回写结果目录 | 备注 |
|---|---|---|---|
| A | `workbuddy/a_orders/TASK-P1-GIT-A-*.md` | `results/chatgpt-a/TASK-P1-GIT-A-*.md` | git-only，ChatGPT 解题 |
| C | `workbuddy/c_orders/TASK-P1-GIT-C-*.md` | `results/chatgpt-c/TASK-P1-GIT-C-*.md` | 接力：Buddy 段(Q_buddy) + ChatGPT 段(Q_chat) |
| D | `workbuddy/d_orders/TASK-P1-GIT-D-*.md` | `results/chatgpt-d/TASK-P1-GIT-D-*.md` | 接力：Buddy 段(Q_buddy) + ChatGPT 段(Q_chat) |

- **A**：纯派单 + 回读 + ACK；不替 A 解题。
- **C/D**：派单中指定两段题号——`Buddy 段`（由负责 Buddy 段的 WorkBuddy relay 在 git 完成，交付 `results/chatgpt-{c,d}/buddy-<TASK_ID>.md`）+ `ChatGPT 段`（ChatGPT 在 git 完成）。
  - 本工位（派单脚本 / 云端 A/C/D 任务）**只发派单、回读 ChatGPT 段、写 ACK**，不替任何一方解题。
  - Buddy 段求解由独立的 relay 负责；若云端未单独部署 relay，则该段暂无人解（交付目标已改为 git，待 relay 接手）。

---

## 5. 频率与并发

- 建议：每条线路独立云端定时任务，频率 `FREQ=MINUTELY;INTERVAL=30`（与本地一致）。
  若想省额度可改为每小时（`FREQ=HOURLY;INTERVAL=1`），但会与既有 30 分钟序列错位——如需严格续接请保持 30 分钟。
- 脚本内置错峰（C 延后 7s、D 延后 15s）以降低同分支 HEAD 并发 409；三条任务仍各自独立。
- 远端分支 `exp/p1-relay-dualwrite-20261023` 可能被本地 V1.1 派单（仍在跑，每 30 分钟）同时推送；REST API 的 409/5xx 已在脚本内退避重试，正常无碍。

---

## 6. 故障处理

- `state=ERROR` 且 `failure_reason` 含 `ENSURE_REPO_FAILED` / `GIT_PUSH_FAILED` / `NO_WRITE_CHANNEL`：如实汇报，不要猜仓库名、不要 force push、不要改分支。
- 无 `GITHUB_TOKEN`（缺凭据）：明确汇报「等待有效 PAT」，不要伪造 commit SHA。
- 只有仓库可达且需 AI 判断的复杂冲突，才标注「建议升级 Codex App Server」，由用户决定。

---

## 7. 与本地 V1.1 的差异清单（便于审计）

| 项 | V1.1（本地） | V1.2（云端） |
|---|---|---|
| 教师 PDF 来源 | Google Drive file id | 仓库 `papers/`（随仓库提交） |
| Drive 只读探测 `drive_probe` | 有 | **已删除** |
| C/D Buddy 段交付 | Drive 账本 DOCX `1h_...` | git `results/chatgpt-{c,d}/buddy-<TASK_ID>.md` |
| ChatGPT 段交付 | git（不镜像 Drive） | git（不变） |
| 停止派单时间 | 2026-10-25T12:00+08:00 硬截止 | 可配（`P1GIT_STOP_AT`），默认持续 |
| 运行位置 | 本机 Python + 本地克隆 | 云端沙箱 + 云端克隆 + `GITHUB_TOKEN` 环境变量 |
| 依赖 | requests + google-* | 仅 requests |
