# P1-GIT A / C / D · 云端定时任务提示词（直接粘贴为云端自动化）

> 用途：把下面三段分别注册为**云端（云上模式）**定时任务，频率 `FREQ=MINUTELY;INTERVAL=30`，
> 各自独立。每条的 `--line` 不同（A / C / D）。卡片会带「云端」标识，电脑关机也能跑。
> 详细沙箱适配见同目录 `runbook.md`。
>
> ⚠️ 注册前请确保云端任务已注入 `GITHUB_TOKEN`（仓库读写 classic PAT）到环境变量；
> 若用 GitHub 连接器取 token，先在提示词里要求「从连接器取出 PAT 并 export 为 GITHUB_TOKEN」。

---

## ① 云端任务：P1-GIT-A（每 30 分钟）

```
P1-GIT-A 云端派单工位（V1.2，git-only，已弃用 Google Drive）。每 30 分钟（整点/半点）触发一次。

目标：从 GitHub 拉取实验分支，运行派单脚本向仓库提交一份 CHATGPT_A 物理顺序解题派单，独立回读校验，并把 8 行摘要汇报出来。你只派单、回读、写 ACK，不替 A 解题。

执行步骤：
1. 仓库：kaibahaha/xxsc @ 分支 exp/p1-relay-dualwrite-20261023。把仓库克隆（或拉取）到持久目录，例如 /home/runner/p1git-xxsc；已存在则 git fetch origin && git reset --hard origin/exp/p1-relay-dualwrite-20261023。
2. 依赖：python3 + requests。若缺，先 pip install -r requirements.txt（通常只需 requests）。
3. 凭据：必须有 GITHUB_TOKEN（classic PAT，仓库读写）。从你的 GitHub 连接器取出 PAT 并 export GITHUB_TOKEN=****；或确认任务环境变量已注入。没有 token 就如实汇报「等待有效 PAT」并停止，不要伪造 SHA。
4. 运行（在仓库根目录）：
   export P1GIT_REPO_DIR=/home/runner/p1git-xxsc
   export P1GIT_STATE_DIR=/tmp/p1git_state
   python p1git_dispatch.py --line A
5. 读取 P1GIT_STATE_DIR/last_report.json，原样按下面 8 行格式汇报（中文）：
   ROUND=<北京时间>
   STATE=<ORDER_GIT_VERIFIED / DUPLICATE_SKIP / ERROR / READ_ONLY_AFTER_STOP>
   TASK_ID=<...> SEQ=<n> Q=<n>
   COMMIT=<sha 或 无>
   回读=<...>
   A结果=<A_RESULT_GIT_VERIFIED / A_RESULT_NOT_SEEN / A_RESULT_PENDING_WORK_RELAY>
   失败原因=<无则写"无">

约束：只发布指令、提交派单、回读、写自己的 ACK；不替 A 解题、不修改 A 的原始答案、不动 C/D 派单与既有结果；不 force push、不删历史；不调用付费模型；不在本任务外执行其他操作。STATE=ERROR 时按 runbook 第 6 节如实汇报，不要猜仓库名、不要改分支。
```

---

## ② 云端任务：P1-GIT-C（每 30 分钟）

```
P1-GIT-C 云端派单工位（V1.2，接力版，已弃用 Google Drive）。每 30 分钟（整点/半点）触发一次。

目标：运行派单脚本向仓库提交一份 CHATGPT_C 接力解题派单（Buddy 段 Q_buddy + ChatGPT 段 Q_chat），独立回读校验，并 8 行摘要汇报。你只派单、回读 ChatGPT 段、写 ACK，不替任何一方解题。

执行步骤：同 P1-GIT-A，仅第 4 步改为：
   python p1git_dispatch.py --line C

汇报格式（中文，8 行内）：
   ROUND=<北京时间>
   STATE=<ORDER_GIT_VERIFIED / DUPLICATE_SKIP / ERROR / READ_ONLY_AFTER_STOP>
   TASK_ID=<...> SEQ=<n> Q=<Qbuddy/Qchat>
   COMMIT=<sha 或 无>
   回读=<...>
   失败原因=<无则写"无">

约束：只发布指令、提交派单、回读、写自己的 ACK；不替 C 解题、不动 A/D 派单与既有结果；不 force push、不删历史；不调用付费模型；不在本任务外执行其他操作。C 接力说明见仓库 docs/cloud/runbook.md 第 4 节：Buddy 段由独立 relay 在 git 完成（交付 results/chatgpt-c/buddy-<TASK_ID>.md），ChatGPT 段由 ChatGPT 在 git 完成（交付 results/chatgpt-c/<TASK_ID>.md）。
```

---

## ③ 云端任务：P1-GIT-D（每 30 分钟）

```
P1-GIT-D 云端派单工位（V1.2，接力版，已弃用 Google Drive）。每 30 分钟（整点/半点）触发一次。

目标：运行派单脚本向仓库提交一份 CHATGPT_D 接力解题派单（Buddy 段 Q_buddy + ChatGPT 段 Q_chat），独立回读校验，并 8 行摘要汇报。你只派单、回读 ChatGPT 段、写 ACK，不替任何一方解题。

执行步骤：同 P1-GIT-A，仅第 4 步改为：
   python p1git_dispatch.py --line D

汇报格式（中文，8 行内）：
   ROUND=<北京时间>
   STATE=<ORDER_GIT_VERIFIED / DUPLICATE_SKIP / ERROR / READ_ONLY_AFTER_STOP>
   TASK_ID=<...> SEQ=<n> Q=<Qbuddy/Qchat>
   COMMIT=<sha 或 无>
   回读=<...>
   失败原因=<无则写"无">

约束：只发布指令、提交派单、回读、写自己的 ACK；不替 D 解题、不动 A/C 派单与既有结果；不 force push、不删历史；不调用付费模型；不在本任务外执行其他操作。D 接力说明见仓库 docs/cloud/runbook.md 第 4 节：Buddy 段由独立 relay 在 git 完成（交付 results/chatgpt-d/buddy-<TASK_ID>.md），ChatGPT 段由 ChatGPT 在 git 完成（交付 results/chatgpt-d/<TASK_ID>.md）。
```

---

## 注册提示

- 在 WorkBuddy 小程序 / App 中选择**云上模式**创建定时任务，粘贴上面对应段落。
- 频率：`FREQ=MINUTELY;INTERVAL=30`（与本地一致，保证序列续接）；想省额度可改 `FREQ=HOURLY;INTERVAL=1`，但会与既有 30 分钟序列错位。
- 三条任务各自独立；脚本内置错峰（C 延后 7s、D 延后 15s）降低同分支 409。
- 云端任务**不支持**推送到企业微信，结果回写到仓库与 `last_report.json`。
