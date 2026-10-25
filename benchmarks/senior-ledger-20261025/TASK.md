# SENIOR-LEDGER-20261025 — 高级工程师级 Python/SQLite 综合修复题

## 背景

你接手一个小型支付账务服务 MiniLedger。它使用 SQLite 文件持久化账户余额、转账请求及复式记账流水。代码能够跑简单演示，但面临并发、故障、重复请求及审计篡改时会发生真实资金错误。

**任务**：在不修改对外 API 和冻结原题的前提下提交修复后的完整实现、回归测试、技术说明。你是维护工程师，不是从零重写一段示例伪代码。

## 冻结输入（全部只读）

仓库：`kaibahaha/xxsc`
分支：`exp/senior-ledger-20261025`
项目根目录（仓库内绝对路径）：`/benchmarks/senior-ledger-20261025/`
入口源码：`src/mini_ledger/__init__.py`、`errors.py`、`db.py`、`service.py`
公开测试：`tests/test_public.py`、`pyproject.toml`

**禁止读取**历史 `results`、先前盲测答案、其他 Agent 工作目录，禁止向其他模型委托编程。

## 不可改变的公共 API

```python
from mini_ledger import Ledger, InvalidRequest, NotFound, Conflict, InsufficientFunds, InvariantViolation
ledger = Ledger(path: str, *, on_before_commit=None)
ledger.create_account(account_id: str, initial_balance: int = 0) -> None
ledger.balance(account_id: str) -> int
ledger.snapshot() -> dict[str, int]
ledger.transfer(request_id: str, source: str, target: str, amount: int) -> dict
ledger.audit() -> dict
```

异常类必须保留名称及目前继承层级，可添加内部私有函数，但不能新增必选参数；所有方法同时适用于重新实例化读取同一 SQLite 文件的场景。

## 精确业务规范

1. **验证**：所有 ID 必须是包含非空白字符的 `str`（允许含空格但不能全空白；保留原字符串，不能自动 trim），金额、初始余额必须是严格 Python 整数而非 `bool`。转账额在 `[1, 2^63-1]`，初始余额在 `[0, 2^63-1]`。非法参数统一抛 `InvalidRequest`，不能留下持久化副作用。 `path` 必须非空字符串。
2. **账户**：`create_account` 创建新账户并设置 `opening_balance` 和当前 `balance`；重复 ID 统一 `Conflict`。未知账户的 `balance`、转账源/目标抛 `NotFound`。 `snapshot` 按账户 ID 字典序返回余额，不能泄露数据库游标等中间对象。
3. **转账原子性**：`source != target`，否则 `InvalidRequest`；转账必须一次数据库事务实现“扣源账户、加目标账户、写 transfer 请求记录、写恰好两条 journal 复式分录”。这五项中任何一个步骤失败都必须整个事务回滚，所有读写从事务内部的同一一致状态执行。不能使用转账期间跨多个事务的 read-modify-write。
4. **借贷守恒**：余额不允许负数；扣款不足抛 `InsufficientFunds` 且不得改变任何数据。收款后余额超出 SQLite 有符号64位上限抛 `Conflict` 且整体回滚。转账总余额不变，不能吞掉溢出异常并当作成功。
5. **严格幂等**：`request_id` 在整个数据库内全局唯一。首次成功保存 `(source,target,amount)` 和 `status='committed'`。同一个 ID 再次调用且三项 payload 完全相同，必须直接返回与第一次完全相同的回执，**即使之后源账户余额不够**也一样；重复请求不能再扣款或写额外流水。同一个 ID 对应不同 payload 必须抛 `Conflict`，无副作用。
6. **回执**：必须返回且只返回 `{ 'request_id': str, 'source': str, 'target': str, 'amount': int, 'status': 'committed' }`。
7. **竞争安全**：同一个 SQLite 文件上可有多个 `Ledger` 实例以及多个线程、多个进程独立连接。并发相同 `request_id` 只能成功扣款一次；并发不同 `request_id` 不能超额扣款。合理等待 SQLite 写锁，常见短暂竞争下不应以 `database is locked` 代替业务结果；不能依赖全局 Python 锁作为唯一正确性手段。
8. **故障注入**：`on_before_commit(request_id)` 只在**第一次成功**新转账的所有 DML 已执行后、真正 `COMMIT` 之前调用一次。如回调抛出任意异常，完整回滚并原样传播异常，之后同 ID 可以正常重试；重复幂等调用不执行该回调。
9. **审计**：`audit()` 返回且只返回 `{ 'accounts': int, 'transfers': int, 'total_balance': int }`。它必须在一次一致性读取下校验：(a) 每个账户 `balance = opening_balance + SUM(journal.delta)`；(b) 每条 committed transfer 恰有两条 journal，分别为 `(source,-amount)` 与 `(target,+amount)`；(c) 没有孤儿 journal 或未 committed 的 transfer；(d) 所有账户余额都在 `[0,2^63-1]`。任一不变量被破坏统一抛 `InvariantViolation`，**只能只读报错，不得偷偷修复/删除记录**。有真实转账且无篡改时返回正确账户数、转账数与当前余额合计。
10. **持久化**：全程 Python 3.11 标准库 + SQLite，不依赖网络、付费 API 或第三方库。数据库连接要安全关闭；允许修改 SQLite 连接/事务参数与增加必要索引；不要改变列名、删除历史数据或破坏与现有 starter 数据库的兼容性。 `Ledger(path)` 重建实例、重启进程后可正确回放查询及幂等行为。

## 交付范围

必须在仓库**原题同分支的独立结果路径**创建文件（如果需要多 Agent 对比，可分别换不同 RUN_ID/目录，但不能复写他人提交）：

`/results/senior-ledger-20261025/workbuddy/src/mini_ledger/{__init__.py,errors.py,db.py,service.py}`

`/results/senior-ledger-20261025/workbuddy/tests/test_regression.py`

`/results/senior-ledger-20261025/workbuddy/REPORT.md`

`/results/senior-ledger-20261025/workbuddy/RUN_LOG.md`

复制原文件也需交付完整代码，不能只交 patch/截图。尽量不改 API；若无变动也可以交付其原内容。允许增加**额外 `.py` 文件**，但原四个模块必须齐备。

## 复测与本地运行

将自己的交付目录当作 Python `src/` 根，运行题目冻结的 `tests/test_public.py` 与你自行编写的 `tests/test_regression.py`；公开测试从冻结目录读取，不能修改测试使其通过。

若拥有真实 Python 工具，必须执行并在 `RUN_LOG.md` 中保留原始命令、退出码、测试数及完整的失败堆栈。没有真实执行工具只能标 `NOT_EXECUTED`，不许虚构 PASS。提交后回读 Git Blob SHA，报告每文件 commit SHA，并在最终汇总中列明各阶段真实完成时刻。

## 评分（100分）

| 项目 | 分值 |
|---|---:|
| 输入/边界/API 兼容性 | 10 |
| 转账原子性/持久化/故障回滚 | 25 |
| 并发竞争、幂等及溢出 | 25 |
| 账目审计/篡改检测 | 20 |
| 自编回归测试质量 | 10 |
| Git 写入/回读、证据与报告真实性 | 10 |

公开测试只检验基本路径，隐藏评测将包含独立构造的多线程、多进程竞争、故障点、异常时间序列与篡改测试。公开测试全通过不等于隐藏全通过。

## 失败处理

不要修改冻结题目，不能覆盖或删除别人结果、不能写主分支或生产目录。单文件成功就应尽早提交、独立回读，避免一次性积压到最后。连接器写入被拒时不得绕过安全策略，记录真实错误并在定时任务最终回复里给出**完整未提交源码**。不许用不存在的路径或预期 commit 假冒成果。
