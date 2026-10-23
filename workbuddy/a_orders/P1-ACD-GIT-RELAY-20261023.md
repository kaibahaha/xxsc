# P1-ACD-GIT-RELAY-20261023 | A/C/D Git 双写调度说明

## 原有流程（保持不变）

1. WorkBuddy 发布 C/D 任务到 Drive。
2. ChatGPT 按原定时任务读取待办，完成任务，并把完整 Markdown 结果交付到资料夹。
3. 原 Word/资料夹定时任务把已完成的 C/D 结果复制到 Drive 指定目录。
4. C/D Google Docs 缺失补交、A/C/D Drive 镜像、固定审计日志继续执行。
5. 所有动作只复制、不删除；失败必须记录并留待下轮补缺。

## 新增 Git 双写流程

在 ChatGPT 已将结果成功交付到资料夹之后，WorkBuddy 的 A/C/D Git 搬运任务再执行：

- A、C、D 均从“资料夹中已完成且尚未 Git 搬运”的 Markdown 读取。
- 不从 Git 历史审计记录反推成功，不把 Drive 原始任务单当作 Git 结果源。
- 源文件必须完整、已完成、身份明确；复制原始 Markdown 内容，不改写、不总结、不重建。
- 写入实验分支：
  - REPO: `kaibahaha/xxsc`
  - BRANCH: `exp/p1-relay-dualwrite-20261023`
  - A -> `results/chatgpt-a/`
  - C -> `results/chatgpt-c/`
  - D -> `results/chatgpt-d/`
- 每个源文件只允许写入对应的 A/C/D 目录；不得删除或覆盖无关文件。
- 每次 Git 写入后必须取得真实 commit SHA，并从该分支重新读取目标文件。
- 只有在源资料夹文件与 Git 读回内容逐字/逐字节一致，且 filename、TASK_ID/RESULT_ID、完成标记均核对通过后，才可记为 PASS。
- Git 写入失败、权限不足、源文件不完整或读回不一致：记为 BLOCKED/REWORK，写入固定审计日志，保留源文件，下一轮继续补缺。

## 子任务与审计

WorkBuddy 负责为每个新结果创建对应的 `TASK-P1-GIT-A/C/D-*.md` 子任务单、执行 Git 搬运、保存 commit/read-back 证据并更新审计日志。不得仅凭退出码、任务注册、目录存在、历史日志或自报结果判定成功。

## 截止

- DEADLINE_BEIJING: `2026-10-25T12:00:00+08:00`

本文件只是调度说明，不是结果文件；原 Drive/资料夹流程仍是主流程，Git 是 A/C/D 的新增镜像出口。
