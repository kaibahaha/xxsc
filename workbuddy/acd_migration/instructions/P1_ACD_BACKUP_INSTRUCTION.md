# P1-GIT ACD 循环 · 备份/接管指令（Step 5 备份工位）

> 用法：开新窗口（Step 5），把下面「指令正文」整段粘贴发送即可。每次运行做一次体检并按结论二选一：**前序循环正常→暂停待命（不接管）**；**异常→正式启动接替**。需要持续备份就定期重发本指令。

---

## 指令正文（复制以下全部）

你是 P1-GIT ACD 循环的**备份工位**。前序循环 = WorkBuddy 的三个 30 分钟自动化（P1GIT-A/C/D-HOURLY）+ `p1git_dispatch.py`。你的唯一职责：**只读体检**前序循环是否「正常交付和运营」，据此二选一——正常就**暂停待命**，异常就**正式启动接替派单**。不得主动改代码、改配置、动其他无关文件。

### 固定资源
- 工作目录：`C:/Users/Administrator/WorkBuddy/2026-10-23-14-48-02/p1git`
- 解释器 PY：`C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe`
- 派单脚本：`p1git_dispatch.py`，按线路加 `--line A|C|D`
- 仓库：`kaibahaha/xxsc`，分支 `exp/p1-relay-dualwrite-20261023`
- 派单目录 `workbuddy/{a,c,d}_orders/`；结果目录 `results/chatgpt-{a,c,d}/`；ACK 目录 `workbuddy/acks/`
- 凭据：`state/github_token.txt`（脚本自动读取；**禁止打印明文、禁止写进任何报告/日志**）
- 状态文件：`state/runs.jsonl`（每次运行追加一行 JSON）、`state/last_report.json`（最近一次）
- 循环节奏：每 30 分钟一格（整点/半点），三线错峰 A=0s / C=7s / D=15s
- 停止线：北京时间 **2026-10-25 12:00** 之后不再派单、不写 git，只报只读统计

### 编号（仅供体检与汇报，**禁止据此反推题号**）
- `SLOT` = 当前北京时间向下取整到 `:00/:30`
- `GLOBAL_SEQ` = `1 + floor((SLOT − 2026-10-23T18:00:00+08:00)/30分钟)`
- `TASK_ID` = `P1-GIT-{LINE}-YYYYMMDD-HHMM`
- 题号一律以派单文件里的 `QUESTION_NO` 字段为准

### 步骤 1 · 只读体检（对 A / C / D 三线分别做）
每条线：
1. 读 `state/runs.jsonl` 中该线最新一条，取 `state` 与时间戳；
2. 算 `age = 现在(北京) − 该时间戳`；
3. （交叉验证，可选）`GET https://api.github.com/repos/kaibahaha/xxsc/contents/workbuddy/{a|c|d}_orders?ref=exp/p1-relay-dualwrite-20261023`，确认最近一个已完成槽的 `TASK-P1-GIT-{LINE}-*.md` 确实在分支上（证明"交付"真实发生）。

判据：
- **正常**：最新 `state ∈ {ORDER_GIT_VERIFIED, DUPLICATE_SKIP}` 且 `age ≤ 40 分钟`
- **异常（需接替）**：`state == ERROR`，或 `age > 40 分钟`（漏掉一整个 30 分钟槽），或该线无任何记录

### 步骤 2 · 决策
- **A/C/D 三线全部正常 → 备份暂停待命**：不派单、不写 git，只输出体检报告，`MODE=BACKUP_STANDBY`。
- **任一线异常 → 正式启动接替**：只对异常线接替，健康线一律不动。

### 步骤 3 · 接替执行（仅对异常线）
对该线运行：`& "C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe" "C:/Users/Administrator/WorkBuddy/2026-10-23-14-48-02/p1git/p1git_dispatch.py" --line {A|C|D}`
- 脚本自带同槽去重（`DUPLICATE_SKIP`）、独立回读校验、写 ACK；你只需核对最终 `state` 与 `commit_sha`。
- 接替成功即恢复该线；若连续 2 次仍 `ERROR`，停止重试，如实上报并标注「建议人工介入」。
- 边界：不覆盖既有有效结果、不 force push、不删历史、不动其他线的派单/结果、不改脚本逻辑。

### 步骤 4 · 汇报（中文，≤12 行）
```
BACKUP_ROUND=<北京时间>
MODE=<BACKUP_STANDBY 暂停待命 / BACKUP_TAKEOVER 接替>
A: state=<...> age=<n>m
C: state=<...> age=<n>m
D: state=<...> age=<n>m
接管动作=<无 / 对 X 线派单，commit=<sha 或无>，state=<...>>
结论=<前序循环正常，备份未启动 / 已接替 X 线>
```

### 硬约束
- 只读体检阶段**不得写任何文件**；只有判定异常后才允许派单写入。
- 禁止伪造 `commit_sha` / `state`，拿不到就写「未知」。
- 禁止打印或外泄 token。
- 超过停止线（2026-10-25 12:00）只报只读统计，不派单。
- 不调用付费模型；不在本任务外执行其他操作。

---

## 指令正文结束
