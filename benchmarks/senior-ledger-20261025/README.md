# Senior coding benchmark — MiniLedger 事务与并发修复

**难度**：高级工程师级（目标 8.5–9/10）。**单道综合题**，并非四个独立编程题。

这是一个有意包含缺陷的 Python 3.11 / SQLite 多模块项目。要求在**保留公开 API** 的前提下修复实际业务问题，提供可执行代码、真实测试日志和提交证明。不得把 README 或 starter 标成答案。

## 从哪里开始

1. 先读 [`TASK.md`](TASK.md)：完整规范、评分权重、禁止事项。
2. 再读 [`AGENT_PROMPT.md`](AGENT_PROMPT.md)：可直接给新窗口/定时任务的执行指令。
3. 源码在 `src/mini_ledger/`；公开测试在 `tests/test_public.py`。
4. **仅能在指定隔离结果目录交付，不得修改冻结题目。**

## 快速运行公开测试

在本目录下：

```bash
PYTHONPATH=src python3.11 -m unittest discover -s tests -p 'test_public.py' -v
```

Starter 初始状态**故意不能全部通过**；这是题目的一部分。不要把它当成环境故障。

## 评测范围

数据验证、事务原子性、SQLite 多连接并发、幂等冲突、余额守恒、崩溃回滚、不可变账目核验、测试可重复性、可审计交付。

评分以独立复测为准，模型自述 PASS 不能代替运行证据。
