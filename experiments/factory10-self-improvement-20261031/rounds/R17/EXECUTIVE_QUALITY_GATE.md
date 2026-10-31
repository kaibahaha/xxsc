# R17 F7｜执行质量门禁（报告待返回）
- 本轮研究目标：科研DOI/撤稿/许可证可信锚、统计负例真实阻断、字节级复现与全球AI for Science机会。
- WorkBuddy自述：尚无，唯一job 4314c14e9faa4d80 已提交，PENDING。
- ChatGPT独立核验：R16/R07历史缺陷与本轮FEEDBACK已Git读取/写入/回读；本轮研究正文未返回。
- FACT_GATE=NOT_EVALUABLE；CASE_STATUS_COUNTS=NOT_EVALUABLE；MVE=NOT_VERIFIED；RED_TEAM=NOT_EXECUTED；ARTIFACT_REPRODUCIBILITY=NOT_VERIFIED；SAME_FACTORY_SCORE_DELTA=NOT_EVALUABLE；FINAL_ACCEPTANCE=PENDING；PRODUCTION_READINESS=NOT_ASSESSED。
- 不存在已经验收的本轮科研能力或已获得资源。下一步按原job追单后更新，不重复派单。


## FINAL R17 F7｜独立验收结论
- WorkBuddy唯一Job 4314c14e9faa4d80 DONE 291s，完整正文25909字符 Git commit 2e095bcb32abb88fe4aa9ee0cdb3df692da761fc / blob 04ae3615ef0d8f36cb04993c089990d30562da48 回读PASS。
- ChatGPT独立官方事实8抽3实错 → **FACT_GATE_FAIL**；5案例A DOCUMENTED/B EXECUTED_SELF_REPORTED/C NOT_TESTED/D SIMULATED_SELF_REPORTED/E EXECUTED_SELF_REPORTED，完整商业E2E独立复现0/5。
- 核心MVE：Buddy自报11负例通过，但ChatGPT忠实逻辑复刻10个新增边界中8个错误ADMIT、2个正确拒绝；包含版权rights缺失、伪DOI、伪撤稿、human_approved="false"等P0。**RED_TEAM_FAIL**。
- 工件：Buddy自报源码SHA b5aee31b…；报告源码单末尾换行SHA独立复算f4f33662…、无末尾换行b7b9289b…；4份冻结JSON原文和完整stdout/stderr均未交付。**ARTIFACT_INTEGRITY_FAIL / ORIGINAL_RUNTIME_NOT_REPLAYED**。源码提取已Git回读，但不等于Buddy原文件一致。
- 同厂R07 68/100（17/17/13/13/8）→ R17 **62/100（16/18/12/12/4）**，Δ=-6；D1 PARTIAL、D2 RECURRED、D3 PARTIAL，resolved=0/3、recurred=1/3。难度与核验覆盖有差异，不能把分数变化当模型能力因果。
- 跨小时R16→R17：T1 hostname部分有效但授权/DOI信任链FAIL；T2许可分层部分实施但官方事实FAIL。FINAL_ACCEPTANCE=**FAIL**；production_readiness=**NOT_READY**，禁止自动科研发布或用于授权审批。
- 机会：IEEE 2027与OpenAlex免费API官方核验，但用户资格/账号状态未知；注册0、资源到账0。其余Buddy机会无当期官方核验，观察而非可行动。
- R18 F8优先整改严格布尔/可信审批/默认拒绝，以及真实冻结输入+原始日志+源码SHA完整交付；具体复现证据见INDEPENDENT_SECURITY_PROBES.md。
