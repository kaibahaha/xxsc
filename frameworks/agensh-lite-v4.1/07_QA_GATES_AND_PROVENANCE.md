# 07｜交付、真实测试、审查、媒体工件与证据溯源

## 事实等级
`PROPOSED`=仅设计；`GENERATED`=已生成文本/文件；`SOURCE_VERIFIED`=原件真实存在且回读；`GIT_VERIFIED`=Git 提交及同分支回读匹配；`RUNTIME_TESTED`=指定环境真实执行并有日志；`QA_GREEN`=独立 QA 在**同一 commit/spec**确认通过；`BUSINESS_ACCEPTED`=有权审批者验收。**禁止跃迁**。

## 代码和 QA
ChatGPT 可以编写代码、审查 diff，但不能默认具备定时任务中的容器/命令执行、Codex App Server 调用、Webhook 触发权限。实际运行必须由已经实测可用的 WorkBuddy/Codex/CI 等受权执行端完成。提交 `TEST_REQUESTED`，附 `repo`, `branch`, `commit_sha`, `spec_hash`, `test_command`, `expected_results`, `max_budget`；执行者回传实际 stdout/stderr/exit code/hash；独立 QA 对应同版本给出 verdict。过期 SHA 的测试 `STALE_TEST`。

## 研究/图像/UI/游戏/音频/视频
每种交付用同样的身份证据：`task_id`, `artifact_id`, `mime`, `source_uri`, `source_sha256`, `generation_method`, `source_app`, `quality_gate`, `preview_uri`。工具支持图像生成不代表每种定时任务能调用图像工具，也不代表能直接导出音频/视频到 Git。**未实际成功执行及读取原始文件时只能提交设计稿或生成指令，不能标媒体产物交付成功。**

## Git ↔ Drive ↔ Library 目标分别 ACK
对同一工件分别记录 `source_valid`, `git_verified`, `drive_verified`, `library_verified`。通过 GitHub 读写不证明 Google Drive 已同步，更不能据此推断本地电脑开机。hash 层级：raw_bytes_sha256（有原始字节）、canonical_text_sha256（规范化提取文本）、git_blob_sha、commit_sha、Docs revision ID；这些不能互代。

## Work 补交防抢节拍
仅当真实源已 SOURCE_VALID、原生允许写入尝试/宽限到期且差异对账证实目标缺失，才进入 relay eligible。审计记载 `source_ready_at`, `native_attempt_at`, `native_outcome`, `grace_until`, `relay_copy_at`, `readback_at`, `recovery_agent`；未见原始失败日志只能写 UNKNOWN，不能因为 Work 最终提交了就说原机器人失败。

## 同一证据不可被循环引用
三个 Agent 对同一个结果复述并不能构成独立测试；每条检验需记录 `producer`, `verifier`, `independence_group`, `runtime_environment`, `tested_sha`。如只有作者自测，结论是 SELF_TESTED，不是 INDEPENDENT_QA_GREEN。
