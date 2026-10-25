# 开发完成后的独立审查与验收｜V4.2 R01

审查对象仅限工单 dev 分支的真实提交、PR、源码、测试和独立回读，不依赖作者总结自述。

## 受理条件
Codex PR：base exp/agensh-lite-v4.2-controller-mvp-20261025，head dev/agl-v4.2-codex-controller；交付 deliveries/CODEX_CORE_R01/。
WorkBuddy PR：base 同上，head dev/agl-v4.2-workbuddy-adapters；交付 deliveries/WORKBUDDY_ADAPTERS_R01/。
必须把 exact commit SHA、PR URL、交付目录、真实 pytest 命令与返回码交给用户以便转交验收。没有 PR 时仍可对 exact branch commit 只读预审，但记 NOT_SUBMITTED_FOR_REVIEW。

## 验收维度
- A SPEC: 是否按目前最优先需求保持 N>=2、无固定全局最大、各 provider 独立 quota/schedule/admission；不写死五个 ChatGPT。
- B CODE: 有真正可安装运行的 Python 代码和单元测试，而非全是 Markdown；import、README、packaging 真实一致。
- C CORRECTNESS: 100 并发 Claim、lease/fencing、老 epoch 迟到、ACK 丢失、Git 冲突、replay/board source of truth、权限隔离；能复现反例则 FAIL。
- D INTEGRATION: 两分支约定类型兼容，尤其 Schema/AgentAdapter/Storage 接口；未合并前标 INTEGRATION_PENDING，不能各自通过就宣称全厂上线。
- E EVIDENCE: pytest 日志、命令 exit_code、Git blob/commit、readback hash、真实与模拟区分；不可用项 UNKNOWN/BLOCKED，不伪造测试。
- F SAFETY: 只在允许开发分支写，未改 main / 旧盲测；无 secrets / 强推 / 未获授权自动化/付费部署。
- G HANDOFF: PR diff 可复查、MANIFEST、Blockers、下一阶段可执行衔接步骤。

## 判定
每项 PASS/FAIL/BLOCKED/NOT_TESTED，并在报告附上对应具体文件、Git blob SHA 或代码定位；若无测试环境则区分“代码审查通过但未验证运行”。两份 PR 首次独立验收后，再发 V4.2 R02 集成测试单；不直接宣称 ChatGPT→WorkBuddy 实际定时任务闭环或上线。

## 用户通知
用户提供两条 PR URL 或精确 Git 分支/commit，ChatGPT 在收到通知的当前对话进行实际 GitHub 只读验收；若用户另需无人工催促的定时巡检，必须明确授权并创建独立自动化。本工单本身不代表自动开始监视/定时回审。