# 05｜共享知识看板：FACT / OBSERVED / FAIL / CLAIM / PATCH_SUMMARY

## 源码语义
`shared_lessons.py` 支持五种 gist、CLAIM 过期、保守语义去重和 FAIL 候选失效；`main.py` 持久储存/快照游标/grep；`board_client.ts` 使用增量 snapshot、失败时全量 fallback，并对 board 不可达显式标 UNKNOWN；`group_messages.ts` 把早期群消息落 JSONL，最近32条保持就近可读。这些不是 ChatGPT 网页自带的保证，需在 Git 上适配。

| 类型 | 何时写 | 必须包含 | 不得替代 |
|---|---|---|---|
| OBSERVED | 实际观察到运行结果 | source_ref、how_observed、观察时点 | 推测/模型常识 |
| FACT | 有证据的稳定结论 | claim、evidence_ref、scope、confidence | 业务独立验收 |
| FAIL | 某路径经过验证失败 | hypothesis、failed_test、scope、affected_commit | 全局永久禁止所有类似方案 |
| CLAIM | 正在推进工作的声明 | task_id、owner、scope、expires_at、lease_ref | 排他锁 |
| PATCH_SUMMARY | 实际代码或方案产物 | files、idea、evidence、commit_sha 或产物 ID | QA_GREEN |

## 短摘要与长详情
建议 summary <= 160 字（**V4.1 自定**，不是微软的100字符限制），长正文留 evidence/detail_uri。`board_grep` 的 AND/OR 和 `board_unfold` 可在 Git 索引式检索中实现最小替代：结构化过滤 `type, task_id, path, commit, run`，复杂全文检索留后续。最小 P0 上下文必须含权威状态、自己的 HANDOFF、有效租约、当前关联 FACT/FAIL；目录树和全部历史仅按需加载。

## HOT / WARM / COLD
HOT：本次任务、最新经验证事件、当前租约和 P0 安全政策；WARM：最近一两轮 HANDOFF、尚未解决的 FAIL、活跃 CLAIM、冲突事件；COLD：完整事件 JSONL、历史 Markdown、测试日志、旧 SHA。压缩不得删证据；返回索引和可展开 URI，不直接把全部历史复制进 prompt。

## 消费语义与 Board 不可用
- 读取成功但没有新事件：`EMPTY_INCREMENT`；读取失败或游标缺损：`BOARD_UNKNOWN`；这两者不同。
- 遇到未知状态，不接受新 CLAIM，只允许低风险本地分析和已有有效 lease 下的工作；任何权威状态变更停止。
- 恢复后先全量/限定窗口回补，再推进 cursor；若无法确认水位，进行完整 ID 差分。
- 若本轮产出知识、失败或进度却没有 NOTE/HANDOFF，则触发强制回写提醒；不能为回写而编造结论。

## FAIL 影响规则
FAIL 影响的对象为 `task_id + spec_hash + implementation_commit + test_id` 对应候选，且应写原始失败日志。即使微软源码可用文本信号推测 checkpoint，本系统也不因带 `passed` 的文字自动提升为 QA，必须独立校验日志/运行环境/版本。FAIL 的优先作用是阻止重复无意义尝试，并触发候选撤回/重验。
