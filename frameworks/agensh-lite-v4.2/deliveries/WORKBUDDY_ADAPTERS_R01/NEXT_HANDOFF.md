# 交接（NEXT HANDOFF）

## 一句话状态

M02/M06/M08/M10 已实现并在真实 GitHub 与真实 git 对象上验证；核心 Controller 缺失，联合调试的下一步在 Codex 分支。

## 现在可以立刻做的事

```bash
# 1. 零依赖复跑（不需要网络与凭据）
cd factory && PYTHONPATH=. python3.11 -m pytest tests -q          # 期望 115 passed / 2 skipped

# 2. 端到端本地演示（自动建裸库、种子任务、写事件、认领、执行）
bash factory/tools/local_evidence.sh

# 3. 真实仓库只读探针（需 token）
export PYTHONPATH=factory GITHUB_TOKEN=***
python3.11 -m agl.cli probe --agent WORKBUDDY_01 --config /tmp/agl-r01-probe.json --transport api
```

`/tmp/agl-r01-probe.json` 是绑定 `dev/agl-v4.2-workbuddy-adapters` 的 6 人池配置；等价配置可用
`python3.11 -m agl.cli gen-pool --n 6 --out <path>` 生成后改 `ref` 与 `runtime_root`。

## 代码地图（只看这几处即可接手）

| 关注点 | 文件 |
|---|---|
| 不可变写入 / CAS / 回读 | `factory/agl/storage/github.py`、`transports.py` |
| 事件幂等、冲突、cursor | `factory/agl/storage/ledger.py` |
| provider 能力与只读熔断 | `factory/agl/adapters/providers.py`、`github_mailbox.py` |
| 准入 / 配额 / 配置前置校验 | `factory/agl/adapters/registry_view.py` |
| 排班与唤醒周期 | `factory/agl/poll.py` |
| 执行协议 | `factory/agl/execution.py` |
| 命令与门禁 | `factory/agl/cli.py` |
| 分支发布（git 协议不可用时的替代） | `factory/tools/publish_branch.py` |

## 未决事项（按优先级）

1. **接核心**：`agl.config` → `agl.events` → `agl.leases` → `agl.audit`，顺序与接线点见 `STUBS.md`。接 `leases` 前不要放开"共享写"。
2. **CI 激活**：需要 `workflow` scope；文件在 `factory/ci/agl-adapters-tests.yml`。
3. **示例配置去重**：上游两份 example 有重复 `agent_id`，`validate-config` 会拒绝（`BLOCKERS.md` B6）。
4. **配额实测**：ChatGPT/WorkBuddy/Codex 的真实配额与最小间隔；填 `capacity_verified=true` 后才会硬拒。
5. **云端 Runner**：目前只有本机 subprocess；接远程端点时保持 `TEST_RESULT` 字段不变（`commit_sha`、`exit_code`、日志 sha256、`environment_id`）。

## 不能做的事（避免踩坑）

- 不要用 `--apply` 打基线分支：适配器本身拒绝 `main/master`，但基线是普通分支，靠 `--branch` 与配置一致性校验保护。
- 不要把环境里的 `GITHUB_TOKEN` 传给"未认证"探针：`RestTransport(token="")` 才是显式未认证。
- 不要在缺少核心时把 `TEST_RESULT.status=PASS` 当成验收：`business_acceptance` 恒为 `PENDING_CORE`。
- 不要修改 `frameworks/agensh-lite-v4.1/`、`main`、盲测分支。

## 证据索引

| 文件 | 内容 |
|---|---|
| `INTEGRATION_TEST_RESULTS.txt` | 115 passed / 2 skipped 的完整 `-v` 输出 |
| `evidence/junit.xml` | 机器可读测试结果 |
| `evidence/real_roundtrip.log` | 真实写入 + 回读 + 重试 |
| `evidence/real_idempotent.log` | 同 run_id 重试不产生新提交 |
| `evidence/real_collision.log` | 同 event_id 冲突 exit 6 |
| `evidence/real_probe.log` | 三 provider 真实能力矩阵 |
| `evidence/real_poll_ack.log` | 任务→看板→认领→ACK→cursor |
| `evidence/local_evidence.log` | 本地 bare 仓库全流程 + N=2..20 + offsets |
| `git-bundle/workbuddy-adapters.bundle` | 本地 3 个语义提交的完整历史 |

## 恢复会话的最短路径

读 `REPORT.md` §2（提交链）→ `BLOCKERS.md` B1/B3（环境与核心依赖）→ `STUBS.md`（接线点）→ 跑一次 `pytest -q`。四条信息足够继续，不需要回看对话记录。
