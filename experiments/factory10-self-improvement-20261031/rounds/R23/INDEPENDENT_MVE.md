# R23 F3｜ChatGPT独立隔离MVE｜游戏采矿车HTML+Node｜与WorkBuddy失败完全分账
- 实验性质：**ChatGPT独立构建和实际运行**；WorkBuddy唯一job 2b219729ac404238 FAILED_OOM，故**不是Buddy报告、不是Buddy执行证据**。不改生产/桥接器/模型/账号/授权；不安装npm依赖。
- 环境：独立容器 Node v22.16.0、Python 3.13.5；标准库 node:fs/node:vm/node:test/node:assert/node:child_process/node:crypto；操作系统与浏览器未作为正式游戏发布环境验证。
- 工厂核心MVE：单个 `artifacts/game.html` 内联GameCore+DOM按钮，4×4采矿网格；玩家从(0,0)出发到(1,1)采两矿，回基地卸矿，gold=2胜利；`artifacts/fixture.json`冻结7动作；`run.cjs`从HTML提取实际内联JS，通过Node VM运行核心逻辑，写 `output.json`，不伪称浏览器UI执行。
## 原始可复现工件（均已通过GitHub独立回读，Git blob SHA与本地git hash-object逐字节一致）
|文件|本地SHA256（实际文件计算）|Git blob SHA（与本地git hash-object相同）|
|---|---|---|
|game.html|7f0576b2dcee07e47d9d0f1fb30288dcbc6d03171f3c7cff15835ab1ad1abc4a|994e8a7e097ed7860df98bb4a663422c2a51c9ed|
|fixture.json|6635a9ff7f6d81bce1de9d2aed7b512d270e4cefb24c5b1baffb95f270933e4b|0d759d6925c549d7a02b8f1a4cd28cdc35522a7b|
|run.cjs|2374dfe4cfa0d68a864ab650df144801b5c407a59025f847e8b78c485485a2b7|fb260e07b1270c9fff84edd8bda23853e6dc8cc5|
|test.cjs|2387b0624a287bb3578f60adb6401134a92ab7da32b456bccd7881cfd5ce677a|3d506f1f2d0ed1e039f48cb4e93a66393027e983|
|output.json|2bd8350705c87b446d1cb925d9e88245a4cdf68d4bfdf9a5c9b4798281444f6d|6c2fa7252a217fd23f51c1863abf13c9f76195ca|
|run.stdout|942c1acd37c38cdde8932b7c09b03849adb2a714c1701f5303c0377367a95429|f41a26e9c9f3e91daf1d6ed390e6f7be4c4a60f2|
|test.stdout|26b9057875b259384ae8153344cfb634aee4375a11ff4900f2676d2e66c1acde|d78a05e33cffec5c180fb4712fc0de8807bfc429|
|cli.cjs|9232f8a29d0b90b6feed815f51dce8a1ed3d7fa610b3d2152a247aa7246ca150|7c57676955d3cb8e18074de89fc4bbfb795b6dfc|
|redteam_cases.json|a71eec548482e65c6b9bea5a48f19dc74f5e2e56e49b986f41784619e273ecdc|b8b63382812826a5eb4fa722e959c62bcca8312a|
|redteam_runner.cjs|de781017591cf066e803ba86878bb028292588393c0d35fe389e63076afe3897|d3b9a5396b03be15bf0b7fcffc5e5f8c104199f2|
|redteam.stdout|d2540c038c02a22b12b3ef7b277b43b703e4658f43289d1cc157cadd55aefbdc|73e0660ef78cda352b1614673deb78f6bc948537|
- `SHA256SUMS` 与 `REDTEAM_SHA256SUMS` 是容器内sha256sum真实输出；同目录保存所有原始stdout、空stderr、退出码0文件和冻结输入。Git各文件逐项创建后重新fetch_file并exact回读PASS；本地git hash-object与Git blob逐项一致，证明Git源字节等于实测源字节。不能用Git blob SHA1代替SHA256；二者独立记录。
## 真正运行的命令与原始输出
```sh
cd artifacts
node run.cjs >run.stdout 2>run.stderr; echo $? >run.exit
node --test test.cjs >test.stdout 2>test.stderr; echo $? >test.exit
node redteam_runner.cjs >redteam.stdout 2>redteam.stderr; echo $? >redteam.exit
sha256sum game.html fixture.json run.cjs test.cjs output.json run.stdout run.stderr test.stdout test.stderr >SHA256SUMS
sha256sum cli.cjs redteam_cases.json redteam_runner.cjs redteam.stdout redteam.stderr >REDTEAM_SHA256SUMS
```
- `run.exit=0`；`run.stdout`原文：`FINAL={"x":0,"y":0,"energy":6,"cargo":0,"gold":2,"ore":0,"seen":[1,2,3,4,5,6,7],"turn":7}`，`SHA256=2bd8350705c87b446d1cb925d9e88245a4cdf68d4bfdf9a5c9b4798281444f6d`。真实输出文件哈希与日志相同。
- `test.exit=0`；`test.stdout` TAP原文包含 `1..16`、`# tests 16`、`# pass 16`、`# fail 0`；16项中2正例、14个异常/边界断言，负例验证`assert.throws`和原state JSON不变。此处异常是JS throw，**不是每项独立子进程退出码**。
- `redteam.exit=0`；`redteam_runner.cjs`用12个冻结负例分别spawn独立Node CLI，全部`actual_exit=2`、stdout为空、stderr为`REJECTED:<原因>`；runner末行`REDTEAM_TOTAL=12 PASS=12 FAIL=0`。12类涵盖缺ID、错误ID类型、负ID、未知动作、非法方向、越界、无矿、空载卸矿、能量耗尽、重复事件、空动作、损坏状态。原始逐例状态与退出码均在`redteam.stdout`，未触碰外部文件/账号；仅runner生成本目录测试输出。错误处理用显式throw，不依赖可关闭assert作生产安全门禁。
## 验收范围与未证实边界
- 已证实：**Node执行的纯JS游戏规则**、7动作确定性、16单测、12独立进程负例、原始字节SHA和Git回读。按V4证据级别，ChatGPT独立原型逻辑层=INDEPENDENTLY_VERIFIED（由独立执行器和Git字节回读）；仅该toy逻辑。
- 未证实：HTML在真实浏览器的DOM点击/视觉/触控（UI NOT_TESTED）；真实Game Jam提交、游戏商用许可、AI素材权利、玩家留存、在线多用户作弊防护、服务器身份鉴权、抗同源日志篡改、支付/发布回滚。无浏览器E2E截图，不能称游戏整体端到端生产就绪。
- 此MVE是隔离独立成果，**不得计入R23 WorkBuddy五维评分、Buddy红队通过数、Buddy缺陷RESOLVED**。R23正式研究状态仍JOB_FAILED_OOM/NOT_EVALUABLE。
- 下轮复测建议：使用浏览器实际点按并断言胜负/错误提示；加入可信服务器状态或签名才讨论防作弊；另在R24 F4研究中继续官方事实门禁，不机械迁移F3行业结论。
