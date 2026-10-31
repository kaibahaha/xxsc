# R16 F6 研究报告工厂｜派单前状态
- planned_at: 2026-11-01 01:25 Asia/Shanghai (R01=2026-10-31 10:25，每小时一轮；R16=F6第二轮)。
- actual_dispatch_at: NOT_YET; state=PREPARED_NOT_SUBMITTED; job_id=NOT_SUBMITTED; score=NOT_EVALUABLE; same_factory_baseline=R06 65/100 (17/17/12/11/8)。
- R15前轮唯一job=2b73e0b468c74b33 DONE 416s/14060字符；Git完整报告、独立审计和质量门禁已回读；R15 71/100、FACT_AND_SAFETY_GATE_FAIL，未获生产许可。
- 云端预检查HTTP200, CodeBuddy reachable, running=0, queued=0, quota_cooldown=null, unresolved_orphan_count=2, possible_remote_overlap=true。历史孤儿不等于当前队列堵塞；仅可派只读隔离研究。
- 先检查本轮Git是否已有Job ID和WorkBuddy最近任务，禁止重复派单；必须在计划时刻后真实提交；FEEDBACK全文必须在submit prompt中实际注入，不能只给Git URL。
- 旧实验README与新实验R06/R15报告、审计、适配均已读取；R06 65/100、R15 71/100，跨厂分数不得作因果比较。
- 无注册、付费、插件安装、模型切换、生产或其他分支修改；未创建新定时任务。