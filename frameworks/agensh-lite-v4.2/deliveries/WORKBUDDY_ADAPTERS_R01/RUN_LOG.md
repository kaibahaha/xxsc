# 运行日志（R01，UTC）

时间取自命令输出与提交时间；每条都能在同目录 `evidence/` 里找到原始文本。

| 时间 | 动作 | 结果 |
|---|---|---|
| 15:41:25Z | `git clone https://github.com/kaibahaha/xxsc.git` | 成功；`main` HEAD `a533d01` |
| 15:44Z | `git fetch origin`；校验冻结提交 | `2d4c1a6` 为 commit，标题 `dispatch: freeze V4.2 R01 ...`；`git ls-remote` 无 `dev/agl-*` 分支，故不存在覆盖历史 |
| 15:45Z | `git switch -c dev/agl-v4.2-workbuddy-adapters 2d4c1a6` | 新分支基于冻结提交 |
| 15:46–16:05Z | 阅读 README / ADAPTER_CONTRACT / REGISTRY / POOL / MODULES / ACCEPTANCE / V4.1 02·04·06·07 / 微软 `state.ts`、`board-service/main.py` | 提炼 `(dedup_key,agent)` 唯一键、1/5/30/120s 退避、cursor 单调、`shown` 台账 |
| 16:00–16:12Z | 编写 M02/M06/M08/M10 与测试 | `factory/` 38 文件 |
| 16:13Z | 首次全量 `pytest` | 113 passed, 1 failed（同 run_id 认领事件字节不稳定）→ 引入 run meta 固定 `observed_at` |
| 16:15Z | 复测 | 全部通过 |
| 16:17:00Z | 发布代码（Git Data API） | commit `02566162b99b`，38 文件，blob SHA 全部与本地 `git hash-object` 一致 |
| 16:18:25Z | 真实回读 1 | commit `6961e58`，blob `e8631eb`，sha256 `53d7339`，matches=true |
| 16:19:18Z | 真实回读 2（幂等基准） | commit `a0ae03b`，blob `54276eb`，sha256 `49ad3bb` |
| 16:19:25Z | 同 run_id 重试 | 返回同一 commit，HEAD 未变（无新提交） |
| 16:19:36Z | 事件 manifest 写入 | `246ad41` |
| 16:19:41Z | 事件投递 `EV-R01-COLLIDE-1` | `0954f21` |
| 16:20:0xZ | 同 event_id 不同 payload | `EVENT_ID_COLLISION`，exit 6；原文件未改 |
| 16:21:05Z | 能力探针写入（outbox） | `fec0b9a` |
| 16:21:22Z | 种子任务 | `34f316b`，回读 matches=true |
| 16:21:37Z | BOARD CAS 发布 | `c5d5dcd` |
| 16:21:42Z / 16:22:05Z | 轮询 planned / actual | `CLAIM_PROPOSED`，`TASK-R01-PROBE`，`CONTROLLER_UNAVAILABLE` |
| 16:22:09–16:22:22Z | run record / meta / `_last.json` | `86bc60c` / `ade2bc2` / `1ad98f2` |
| 16:22:30Z | ACK | `08e0b54`，`ack_result=DELIVERY_ACK` |
| 16:22:39Z | cursor 前进 / 回退尝试 | `ef19faa` / `MONOTONIC_NOOP` |
| **16:24:16Z** | **事故**：联网测试自动采用环境 token，写入基线分支 | 提交 `5c5e95c5de82`（仅 `factory/_probe/should-not-exist.json`） |
| 16:28Z | 核查父链 | `5c5e95c` 的父提交只有 `2d4c1a6`，未覆盖他人提交 |
| 16:29Z | 恢复基线 | `PATCH ref force` → `2d4c1a6`；越权文件 404 |
| 16:29:07Z | 本地 bare 仓库全流程重跑 | 回读 commit `cc1c494`，blob `5527bd0`，sha256 `0782ece`，matches=true |
| 16:30Z | 修复根因并提交 | 本地 `6055f2e`：token 显式未认证、worktree 子目录识别、回读载荷确定化 |
| 16:33Z | 重跑本地证据 | `run-sample-test` = PASS（exit 0）；错误 SHA = STALE（5）；无 runner = BLOCKED（3）；N=2/3/5/6/10/20 全 PASS |
| 16:35Z | 全量 `pytest`（带 token 环境） | **115 passed, 2 skipped**（匿名只读探针限流） |
| 16:36Z | 创建 PR | #2 `https://github.com/kaibahaha/xxsc/pull/2`（draft） |
| 16:40Z | 交付文档与 MANIFEST | 见本目录 |

## 关键命令（可复制）

```bash
cd factory && PYTHONPATH=. python3.11 -m pytest tests -v -rs
bash factory/tools/local_evidence.sh
python3.11 -m agl.cli offsets --k 5                    # -> [0, 12, 24, 36, 48]
python3.11 -m agl.cli plan-schedules --config config/pool_n6.valid.json --json
python3.11 -m agl.cli validate-config --config config/pool_n6.valid.json
```

## 观测到的环境噪声（不影响结论，但影响可复现性）

- `github.com:443` 间歇性完全不可达（多次 135s 超时），故一律优先 API。
- 匿名 `api.github.com` 60/h 配额在 20 分钟内耗尽，真实探针必须带 token。
- 同一台机器不同出口 IP（`81.70.150.155`、`49.232.230.217`）限流计数不同，说明走代理池。
