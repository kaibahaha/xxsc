# 可运行验证

仓库根执行，推荐临时虚拟环境：

```sh
python -m pip install pytest jsonschema
PYTHONDONTWRITEBYTECODE=1 python -m pytest factory/tests/core -v -ra
PYTHONDONTWRITEBYTECODE=1 python -m factory.agl.contracts.demo
sha256sum -c frameworks/agensh-lite-v4.2/deliveries/CODEX_CORE_R01/MANIFEST.sha256
```

实测前两条运行结果见 TEST_RESULTS.txt：90 passed，demo 重放一致/ACK_ONLY/Board UNKNOWN，两条 exit_code=0。最后的 manifest 验证由交付归档流程执行，最终 Git 回读后再次检查。

进一步手工检查：在 test_events_recovery.py 中查看真实 os._exit(73) 后重开数据库的两个案例；查看 test_git_journal_export_restore_new_database，导出 records -> 固定已核验 head -> 新空库 restore -> Controller 冷启动，对账前拒绝 claim。所有测试数据库来自 tmp_path，不可提交这些运行时文件。

本模块没有接管 WorkBuddy CLI；demo 仅用于 review，不会启动 Provider、真实调度或持久服务。
