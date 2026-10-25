# 02｜GitHub 看板、目录、不可变写入协议

## 推荐目录（在 GitHub 独立隔离分支下）
```
frameworks/agensh-lite-v4.1/      # 本协议文档，冻结后只读
projects/<PROJECT_ID>/
  00_policy/                     # Controller 单写配置、身份、能力、允许的路径
  01_tasks/<TASK_ID>/TASK.md     # 用户授权的任务，不可变或版本化
  02_claims/<TASK_ID>/<EVENT_ID>.json   # 提议性软 CLAIM，非租约
  03_events/<YYYYMMDD>/<EVENT_ID>.json # 每个事件新文件，不更新旧事件
  04_notes/<TYPE>/<EVENT_ID>.json      # FACT/FAIL/OBSERVED/PATCH_SUMMARY
  05_outbox/<AGENT_ID>/<RUN_ID>/      # 每工位唯一可写范围
  06_evidence/<TASK_ID>/<RUN_ID>/     # 测试/图片/媒体证据索引
  07_receipts/<TARGET>/<EVENT_ID>.json# Git/Drive/Library 分目标 ACK
  08_projections/BOARD.md             # Controller 唯一写者；只读消费
  08_projections/CURRENT.json
  09_runs/<AGENT_ID>/<RUN_ID>.md       # 真实唤醒/运行记录
  10_archive/                          # append-only 历史
```
## 写入四不原则
- 任何 Agent 不直接修改同一个 BOARD.md；各自仅创建独立事件文件；Controller 汇总后以 CAS 或受保护集成提交发布 BOARD 投影。
- 不覆盖同事的事件、不强推、不直接改 `main`、不在未知 SHA 上盲写。
- 新文件名必须包含 `EVENT_ID` 或 `RUN_ID`；目标已存在时读内容+hash，对等价内容做幂等 ACK，不因冲突产生第二份业务事件。
- 每笔 `READ→VALIDATE→WRITE→INDEPENDENT_REREAD→ACK`，返回 Commit SHA、Blob SHA、readback hash 后才能宣布 Git Verified。

## BOARDS 的职责
`BOARD.md` 最多列任务摘要、有效 CLAIM、最新 FAIL 与已验证交付的索引、当前投影版本和构建时间；它不替代原件。上游源 ID、提交 SHA、目标路径、协议版本单独留存。若投影不可用、过期或读取失败：`UNKNOWN`，不能当 EMPTY。

## 分支政策
文档草拟用 `exp/agensh-lite-v4.1-20261025`（建议）；不得直接接管既有 `exp/senior-ledger-*`、`exp/scheduled-model-*` 等盲测分支。生产迁移仅能通过独立 PR、QA 与用户批准。支持仓库读写≠所有计划任务都已继承相同权限。

## Git 锁边界
GitHub Contents API 只能提供单文件基于 blob SHA 的条件更新，无法天然提供跨 TASK+CLAIM+EVENT 三文件原子事务；所以 L0 阶段只把 CLAIM 作为提示与协商，L1 才由常驻 Controller/数据库做原子授租。
