# R13 F3｜动态RSI跨厂方法适应性记录（派单前）
- 实验：FACTORY10-SKILL-24H-20261030；计划Phoenix 2026-10-29 22:00 / 北京2026-10-30 13:00；同厂第二轮R13对照R03，不改变固定24轮调度。
- 已真实读取同厂R03完整WORKBUDDY_REPORT/CHATGPT_AUDIT/STATUS/ADAPTATION：Job `5b8ee940847e42f2`，83/100（20/19/16/16/12），核心P0为“宣称完整源码却只给原则、原始日志缺失”和“SHA完整性与防恶意重算混淆”；P1为物理模拟未校准、单HTML与多JS矛盾、授权/费用/发布未验证。
- 最近可评价的跨厂样本：R10/F10 76/100（18/19/15/15/9）同样存在远端RUN源码不在本实验可重放、法律状态误判；R03/F3 83分存在工件缺失；R11/R12真实Job仍QUEUED/0字，属于延迟证据，不能从其推断质量趋势。
- 观察→原因假设→本轮方法调整（最多三项）：
  1. **M1可复制工件**：自述RUN不等于第三方可复现→凡称RUN，直接在MCP正文附完整最小源代码、固定输入、三次独立进程原始stdout/stderr、exit code、版本与SHA；验收“RUN中可独立重放比例”，缺工件不得标PASS。
  2. **M2证据/授权分层**：R10法律地位误判与R03缓存/credits混淆→关键事实附当期官方链接、适用范围、核验日期；分别列E0执行、E1官方、E2市场缓存、E3推断及CONNECTED/MARKET_CACHED/AUTH_REQUIRED；验收无无证据的“已装/已授权/已运行/现行法律”断言。
  3. **M3信任边界+案例一致性**：R03普通SHA误作防篡改、单HTML与多JS输出冲突→五案例各给至少一个能否定主张的负例、真实工件清单、失败回滚与成本；验收5/5案例字段齐全，至少2项负例具备可复制步骤。
- 实际注入要求：上述M1–M3和R03专项反馈的完整事实与验收，必须与本轮`FEEDBACK_TO_BUDDY.md`全文一起写入WorkBuddy submit prompt；不可仅发Git链接。
- 待验证：R13报告是否完整返回；同厂总分Δ和五维Δ；P0复发率；M1–M3按报告证据判已解决/部分/未解决/无法判断。**当前PENDING/NOT_EVALUABLE，尚未派单时不得写已生效**。
- 下一轮R14/F4：优先追R11–R13现有Job，补交已完成原文/审计；F4首圈R04 429失败，若仍无报告则记录MISSING_BASELINE，不得伪造同厂评分；跨厂只继承验证方法，不复制F3游戏业务内容。

## 派单后真实状态回填
- 本轮反馈4242字符已从Git回读，并作为完整原文实际嵌入WorkBuddy MCP Stable `submit_workbuddy_task` prompt（总5216字符），唯一Job `24a8fbd31257441a`；M1–M3及R03六项整改均已真实传达，不只是写在Git。
- MCP get_result首查[running]/0字，但list_jobs明确QUEUED/0字；桥接器HTTP200、后端可达、单执行槽、active_jobs=6。R11/R12同样QUEUED，不能判定R13研究质量。
- 方法执行状态：PROMPT_INJECTED / RESULT_PENDING / EFFECT_NOT_EVALUABLE；待R13完整报告及ChatGPT独立审计后逐项回填，不虚构改善。
