BEGIN_FULL_REPORT

# R12 F2 软件与开源程序工厂 — 第二轮独立审计与隔离MVE研究报告

> 实验 FACTORY10-SELF-IMPROVEMENT-20261031；固定 R12=F2 第二轮
> 隔离目录 /tmp/factory10-self-improvement-20261031/R12/ （本轮新建，原不存在）
> 生成时间 2026-10-31（UTC）；模型由宿主固定，未切换
> 硬约束遵守：未改生产/未改Git配置/未安装插件/未切模型/未触密钥
> 网络检索：12/12（达上限）；子代理：0/1（未派发）
> 跨厂基线 R10 F10 = 62/100(V4 FAIL) 按 DELAYED_BASELINE；R11 F1 job=13434ad175b04267 仍 QUEUED，无 WORKBUDDY_REPORT，本轮不伪称其结果

## 0. 执行元信息与合规自检（可证伪）
| 项 | 结果 | 证据 |
|---|---|---|
| 生产桥接器/CodeBuddy配置/Git分支 | 未改 | 只写 /tmp 隔离目录；git MISSING 无法改 |
| 插件安装 | 0 | 仅只读 WebFetch + CLI --help |
| 模型切换 | 否 | 未调 --model |
| 密钥 | 未触 | 未读凭据；未登录/注册/领取 |
| 网络检索 | 12（达上限） | §4 S1–S12 |
| 子代理 | 0（≤1） | 未派发 |
| R12 目录 | 原不存在，本轮新建 | 存隔离MVE与冻结工件 |

环境只读实测（可复现）：codebuddy 2.177.0；git/docker/semgrep/uv MISSING；python3 3.13.5；node v20.20.2。`codebuddy --version` exit0；`codebuddy --help` exit0。

## A. 跨小时通用方法迁移（从 R10 F10 延迟基线，实际落实并复核）

### T1 — schema fail-closed + 相邻边界双模式（MVE-1）
R10缺陷：只覆盖预设样本、把异常当拒绝，致 12 次错误 ACCEPTED(exit0)。
R12落实：隔离 MVE `mve1_policy_parser.py` 实现权限政策解析器，**9 类有效负例**（≥8），normal 与 `python -O` 各执行。所有安全判定用 `if/raise` **不依赖 assert**（`python -O` 剥离 assert 否则 fail-open），两种模式输出 `optimize:0/1` 判定一致。

**运行结果**：9 非法 × 2 模式 = 18 次全部 REJECTED(exit2)；2 合法 × 2 模式 = 4 次 ACCEPTED(exit0)。**22/22 通过；≥16/16 拒绝达成；0 fail-open；0 未捕获异常**（CORRUPT_JSON 显式捕获）。9 类：EMPTY_INPUT/MISSING_FIELD/WRONG_TYPE/UNAUTHORIZED_PATH/GLOB_INJECTION(R02缺陷:危险通配清理)/BYPASS_PERMISSIONS_NS(R02缺陷:非沙箱bypass)/DUPLICATE_RULE/OVER_BUDGET/CORRUPT_JSON。

### T2 — 原始工件 SHA 三联 + 官方核验
完整源码(§A.1/§A.2)、冻结 JSON 输入(§A.3)、预期/实际 stdout、真实命令与退出码、环境、源码/输入/输出各自 SHA256(§A.4)。≥5 项高影响官方事实(§D F1–F8)逐条核验并标适用范围(2026-10-31)。

## A.1 MVE-1 完整源码（冻结）
```python
#!/usr/bin/env python3
# mve1_policy_parser.py  R12/F2 T1 — schema fail-closed permission-policy parser
import sys, json, os
MAX_BUDGET_TOKENS = 1_000_000
ALLOWED_ACTIONS = {"read", "write", "cleanup", "exec"}
FORBIDDEN_PATH_FRAGMENTS = ("/etc/", "/etc", "/home/", "/home", "/Users/",
    "/Users", "/root/", "/root", "~", "$HOME", "${", "..", "%HOME%")
def fail(category, detail):
    return {"status": "REJECTED", "category": category, "detail": detail}
def validate(policy):
    if policy is None or (isinstance(policy, dict) and len(policy) == 0):
        return fail("EMPTY_INPUT", "policy is null or empty object"), False
    if not isinstance(policy, dict):
        return fail("WRONG_TYPE", "top-level policy must be a JSON object"), False
    required = ["version", "allowed_root", "rules", "budget_tokens", "mode"]
    missing = [k for k in required if k not in policy]
    if missing:
        return fail("MISSING_FIELD", "missing required key(s): " + ",".join(missing)), False
    if not isinstance(policy["version"], str): return fail("WRONG_TYPE","version must be string"), False
    if not isinstance(policy["allowed_root"], str): return fail("WRONG_TYPE","allowed_root must be string"), False
    if not isinstance(policy["rules"], list): return fail("WRONG_TYPE","rules must be a list"), False
    if not isinstance(policy["budget_tokens"], int) or isinstance(policy["budget_tokens"], bool):
        return fail("WRONG_TYPE","budget_tokens must be integer"), False
    if not isinstance(policy["mode"], str): return fail("WRONG_TYPE","mode must be string"), False
    allowed_root = os.path.normpath(policy["allowed_root"])
    sandbox = bool(policy.get("sandbox", False))
    if policy["mode"] in ("bypassPermissions", "bypass") and not sandbox:
        return fail("BYPASS_PERMISSIONS_NS","mode=bypassPermissions requires sandbox=true; non-sandbox bypass is denied"), False
    if policy["budget_tokens"] > MAX_BUDGET_TOKENS:
        return fail("OVER_BUDGET","budget_tokens exceeds cap"), False
    seen_ids = set()
    for i, rule in enumerate(policy["rules"]):
        if not isinstance(rule, dict): return fail("WRONG_TYPE","rule[%d] must be object"%i), False
        rid = rule.get("id")
        if not isinstance(rid, str) or rid == "": return fail("MISSING_FIELD","rule[%d].id missing"%i), False
        if rid in seen_ids: return fail("DUPLICATE_RULE","duplicate rule id: %s"%rid), False
        seen_ids.add(rid)
        action = rule.get("action")
        if action not in ALLOWED_ACTIONS: return fail("WRONG_TYPE","rule[%d].action invalid"%i), False
        path = rule.get("path")
        if not isinstance(path, str) or path == "": return fail("MISSING_FIELD","rule[%d].path missing"%i), False
        low = path.lower()
        if any(frag.lower() in low for frag in FORBIDDEN_PATH_FRAGMENTS):
            return fail("UNAUTHORIZED_PATH","rule[%d] forbidden location: %s"%(i,path)), False
        if os.path.isabs(path):
            norm = os.path.normpath(path)
            if not (norm == allowed_root or norm.startswith(allowed_root + os.sep)):
                return fail("UNAUTHORIZED_PATH","rule[%d] escapes allowed_root: %s"%(i,path)), False
        if action in ("cleanup","write","exec") and ("**" in path or "/*" in path):
            return fail("GLOB_INJECTION","rule[%d] dangerous wildcard in %s: %s"%(i,action,path)), False
    return {"status":"ACCEPTED","category":"NONE","detail":"policy valid"}, True
def main(argv):
    if len(argv) < 2:
        print(json.dumps(fail("MISSING_FIELD","usage"))); return 2
    try:
        with open(argv[1],"r",encoding="utf-8") as f: text = f.read()
    except OSError as e:
        print(json.dumps(fail("IO_ERROR",str(e)))); return 2
    try: policy = json.loads(text)
    except json.JSONDecodeError as e:
        print(json.dumps(fail("CORRUPT_JSON","invalid JSON: %s"%e))); return 2
    result, ok = validate(policy)
    result["optimize"] = sys.flags.optimize
    print(json.dumps(result, ensure_ascii=False))
    return 0 if ok else 2
if __name__ == "__main__":
    sys.exit(main(sys.argv))
```

## A.2 MVE-2 完整源码（冻结）
```python
#!/usr/bin/env python3
# mve2_task_contract.py  R12/F2 P1-F2-R12-03 — factory task-contract / execution-policy validator
import sys, json, os
ISOLATION_ROOT = os.environ.get("R12_ISOLATION_ROOT",
    "/tmp/factory10-self-improvement-20261031/R12/_task_tmp")
def reject(category, detail):
    return {"status":"REJECTED","category":category,"detail":detail}
def validate_contract(c):
    if not isinstance(c, dict): return reject("WRONG_TYPE","contract must be object"), False
    for k in ("job_id","scenario","lease_ttl","cleanup_paths"):
        if k not in c: return reject("MISSING_FIELD","missing "+k), False
    if not isinstance(c["job_id"], str) or c["job_id"]=="": return reject("WRONG_TYPE","job_id"), False
    if not isinstance(c["lease_ttl"], int) or c["lease_ttl"]<=0: return reject("WRONG_TYPE","lease_ttl"), False
    if not isinstance(c["cleanup_paths"], list): return reject("WRONG_TYPE","cleanup_paths"), False
    for p in c["cleanup_paths"]:
        if not isinstance(p, str): return reject("WRONG_TYPE","path str"), False
        if "*" in p or "?" in p: return reject("GLOB_INJECTION","wildcard cleanup forbidden: "+p), False
        norm = os.path.normpath(p)
        if not (norm.startswith(ISOLATION_ROOT+os.sep) or norm==ISOLATION_ROOT):
            return reject("CLEANUP_ESCAPE","cleanup escapes isolation root: "+p), False
    return {"status":"ACCEPTED","category":"NONE","detail":"valid"}, True
def simulate(c):
    sc = c.get("scenario"); trace=["QUEUED"]
    if sc=="happy": trace+=["RUNNING","DONE"]
    elif sc=="rate_limit": trace+=["RUNNING","COOLDOWN_429","RUNNING","DONE"]
    elif sc=="lease_expire": trace+=["RUNNING","ORPHAN","REQUEUED","RUNNING","DONE"]
    elif sc=="unknown_remote": trace+=["RUNNING","UNKNOWN_REMOTE"]
    elif sc=="hard_fail": trace+=["RUNNING","FAILED"]
    else: return {"status":"REJECTED","category":"UNKNOWN_SCENARIO","detail":sc}, False
    return {"status":"ACCEPTED","category":"NONE","trace":trace,"final":trace[-1]}, True
def cleanup(c):
    res, ok = validate_contract(c)
    if not ok: return res, False
    owned = c.get("_created_files", []); planned=[]
    for p in c["cleanup_paths"]:
        if p in owned: planned.append(p)
        else: return reject("CLEANUP_NOT_OWNED","not created by this task: "+p), False
    return {"status":"ACCEPTED","category":"NONE","detail":"simulated cleanup %d files (no real delete)"%len(planned),"would_remove":planned}, True
def main(argv):
    if len(argv)<3:
        print(json.dumps(reject("MISSING_FIELD","usage"))); return 2
    cmd, path = argv[1], argv[2]
    try:
        with open(path,"r",encoding="utf-8") as f: c=json.load(f)
    except json.JSONDecodeError as e:
        print(json.dumps(reject("CORRUPT_JSON","%s"%e))); return 2
    except OSError as e:
        print(json.dumps(reject("IO_ERROR",str(e)))); return 2
    if cmd=="validate": res,ok=validate_contract(c)
    elif cmd=="simulate": res,ok=simulate(c)
    elif cmd=="cleanup": res,ok=cleanup(c)
    else: res,ok=reject("UNKNOWN_COMMAND",cmd),False
    res["optimize"]=sys.flags.optimize
    print(json.dumps(res, ensure_ascii=False))
    return 0 if ok else 2
if __name__=="__main__":
    sys.exit(main(sys.argv))
```

## A.3 冻结输入样例（原始字节）
- `fixtures/f05_glob_injection.json`: `{"version":"1","allowed_root":"/tmp/scope","rules":[{"id":"r1","path":"/tmp/scope/**","action":"cleanup"}],"budget_tokens":100,"mode":"dontAsk"}` → GLOB_INJECTION
- `fixtures/f06_bypass_ns.json`: mode=bypassPermissions 无 sandbox → BYPASS_PERMISSIONS_NS
- `fixtures/v01_valid_dontask.json`: 合法 dontAsk → ACCEPTED
- `contracts/c06_bad_cleanup_wild.json`: cleanup 含 `.../R12-006/*` → GLOB_INJECTION
- `contracts/c07_bad_cleanup_escape.json`: cleanup=`.codebuddy/worktrees/` → CLEANUP_ESCAPE

## A.4 原始运行输出（节选）+ 退出码 + SHA 三联
- `python3 mve1_policy_parser.py fixtures/f05_glob_injection.json` → `{"status":"REJECTED","category":"GLOB_INJECTION",...,"optimize":0}` EXIT=2；`python3 -O` 同判定 `"optimize":1` EXIT=2
- `python3 mve2_task_contract.py validate contracts/c07_bad_cleanup_escape.json` → `{"status":"REJECTED","category":"CLEANUP_ESCAPE",...}` EXIT=2
- `python3 mve2_task_contract.py simulate contracts/c02_rate_limit.json` → `{"status":"ACCEPTED","trace":["QUEUED","RUNNING","COOLDOWN_429","RUNNING","DONE"],"final":"DONE"}` EXIT=0

**SHA256（原始字节，三联一致可复现）：**
| 工件 | SHA256 |
|---|---|
| mve1_policy_parser.py | a04576e3f035fb05d5859f4da0eda46dc17f882a3d4143f9f670cb41e2214af9 |
| mve2_task_contract.py | 76c5417df2e6ecc5b1b2644c7fc7abec2a1a63a3a3828470175b3dd265b96295 |
| fixtures/f05_glob_injection.json | 550a58badca06ac8587420da25f8607c5d5350b751d1d95777c32d1589694157 |
| fixtures/f06_bypass_ns.json | 9af85a8005684f3957dd44a905969eae4b3d59bb28dee2fa15d52b207681c1ef |
| fixtures/v01_valid_dontask.json | 25832e81839d8ef89aca4b21c594c4632d8bcd51504ee92d4a0af62791bb21c2 |
| contracts/c06_bad_cleanup_wild.json | c74125be0d061b06ea8e15a6f210a3b3eb727a5fa56dd409ef6664d7b3e93d0a |
| contracts/c07_bad_cleanup_escape.json | ffa3960fd2b03f0d510798087638fec77e55ebcc63068af51c5b64d31b624262 |
| run_log.txt (MVE-1 全输出) | 74314cf45c8f25daa094e2324aa3ee12d561e579a784c0109da7c301747a99c1 |
| run_log_mve2.txt (MVE-2 全输出) | a8a2f93f14c0d93f3816e3ce51db1496b1422d9eb5813b0bcd889700d59d3d65 |

## B. 同厂 R02 独立审计：三项 P0/P1 专项整改

### P0-F2-R12-01 — 无人值守 CLI 权限与 OS 隔离不可混淆
**原始证据(R02)**：§5-B 混用 `codebuddy -p -y` 与 `--permission-mode dontAsk`；Case C 将 worktree 当盲测隔离；无真实权限拒绝 stdout/exit。
**官方核验(只读,2026-10-31)**：
- `--help`：`--dangerously-skip-permissions ... Bypass permission prompts (HIGH/CRITICAL still ask)`，`-y`≡`--permission-mode bypassPermissions`。
- permission-modes：`dontAsk`=未预批准动作直接拒绝（严格非宽松）；bypassPermissions 不使前置 deny/ask 失效；full pass 需 `CODEBUDDY_IS_SANDBOX=1`。
- headless：`-y` 是非交互必需；仅 `-y` 仍可能问 HIGH/CRITICAL；真正不询问需沙箱环境变量。
- worktree FAQ：「子代理隔离是安全沙箱吗？**不是**。子代理在文件层面隔离，但权限与主 Agent 相同，理论上可操作 worktree 之外的文件...防止文件冲突，而非安全限制」。
- bash-sandboxing：OS 级(bubblewrap/Seatbelt) FS+网络隔离；逃生舱 `dangerouslyDisableSandbox`；域前置可绕网络过滤。
**版本化矩阵**：`-p`(非交互打印,无授权则受限) / `-y`(≡bypass,高危,非沙箱非安全) / `dontAsk`(严格拒绝,需allowlist) / `allowedTools`(进程级allow,复合命令可绕单deny) / OS边界(需沙箱/容器,worktree≠边界)。
**真实只读证据**：`--version`=2.177.0(exit0)、`--help`(exit0) 已附。**合成越权执行态**：本环境无外部 OS 强制边界(无docker、无bubblewrap确认)，按约束 BLOCKED，**未对真实仓库做 live 拒绝**（避免碰生产）。越权以 MVE-2 CLEANUP_ESCAPE/GLOB_INJECTION 在隔离解析层验证(exit2)。状态：**PARTIAL_VERIFIED / live拒绝 BLOCKED（诚实，不称安全生产通过）**。

### P1-F2-R12-02 — 许可证触发条件及供应链门禁假阳性
**原始证据(R02)**：Case A 把 GPL/AGPL 义务写普遍；Case D `from aggplib import *` 推断违规、`requests==2.31.0` 称有CVE、`sk-...` 称必检出——无规则ID/版本/真实退出码。
**官方核验**：GNU GPL FAQ：编辑/翻译=修改；静/动链接=组合作品；**内用不分发=无发布义务**；AGPL§13 延伸网络义务(本轮 fetch 该段截断，标待独立复核)。OpenSource.org：MIT/Apache-2.0 宽松；GPL 强 copyleft；AGPL 网络 copyleft。
**场景矩阵**：MIT/Apache 自由(留声明)；GPL 分发改同源；AGPL 网络服务须供源码；无许可仅只读研究。
**3正3负夹具**：正 `sk-...`(secret)/`requests==2.19.1`(需OSV库)/`from aggplib import *`(仅AGPL+网络才触发,非import=违规)；负 `os.getenv`/`requests==2.31.0`(无CVE于本机)/`MIT`。**工具态**：semgrep MISSING → NOT_TESTED/DESIGNED，明确不称检出。
**通过**：≥5 官方事实无实质错；0 个"import=违规"错误（已纠正）。

### P1-F2-R12-03 — 危险回滚、工件复现与真实商业成本
**原始证据(R02)**：Case C 建议 `rm -rf .codebuddy/worktrees/*`；Case E 仅概念状态机缺 failed/429/孤儿/UNKNOWN_REMOTE；"≈0成本"未计模型/人工/云/维护。
**修复(MVE-2,实跑)**：零安装 stdlib 任务合同/执行策略验证器，不调生产Bridge、不跑危险清理；5边界(happy/rate_limit/lease_expire/unknown_remote/hard_fail)×normal/-O 真实跑(22/22)；状态转移表覆盖 QUEUED→RUNNING→DONE/FAILED/ORPHAN/COOLDOWN_429/UNKNOWN_REMOTE/REQUEUED；回滚只清唯一隔离临时文件并验归属。
**成本公式**：周人力=Σ(工时×单价UNKNOWN)；算力=Σ(模型调用×单价UNKNOWN,外部锚 Copilot Pro $10/月)；服务费=CI/扫描 UNKNOWN；维护=审计工时 UNKNOWN。零安装本地路径=0，但**整体≠0**（模型/人工/云/维护单列 UNKNOWN）。

## C. R02 五案例逐项保留与修订
| 案例 | 历史问题 | 修复 | 新证据 | 验收 |
|---|---|---|---|---|
| A 开源解构 | 一刀切禁复制 | 五许可矩阵+未知→人工 | §B2 官方事实 | REVISED(READY/DESIGNED) |
| B 合同→PR | 混用dontAsk/-y;无拒绝 | 版本化矩阵;安全隔离才测 | §B1 CLI文档+--help | REVISED(live BLOCKED) |
| C 多Agent盲测 | worktree当安全 | 区分隔离层;删通配rm | worktree文档"非沙箱" | REVISED(BLOCKED) |
| D 供应链门禁 | "100%检出"仅设计 | 3正3负+规则ID | semgrep MISSING | REVISED(NOT_TESTED) |
| E 桥接器恢复 | 仅概念状态机 | MVE-2真实5边界 | 22/22双模式 | REVISED(SIMULATED) |

## D. 本轮研究差异与硬约束
聚焦：零安装、安全边界明确、可复现的开源代码工厂任务合同与策略门禁（MVE-1/MVE-2 已交付）。
市场机会：开源维护者/小团队/企业内网代码审计与可复现CI；零安装只读解析成本0易试点，合规CI门禁需托管扫描(云成本UNKNOWN)；收费按仓库/月或审计人时(UNKNOWN,待试点)。
Skill/插件/MCP 分层：① CodeBuddy Read/Grep/Glob+py3(官方有/本机有/真执行/SHA验收)；② 权限模式/沙箱(官方有/部分--help/未live/未验收)；③ semgrep(官方有/MISSING/否/NOT_TESTED)；④ GitHub Actions托管(官方有/需审批/否/WAIT_USER)；⑤ ChatGPT连接器写Git(CLAIMED/未授权/否/WAIT_USER)。
官方文档≥8(S1–S12，2026-10-31 均成功抓取)。
**≥5 事实(F1–F8，0实质错)**：F1 `-y`≡bypassPermissions(v2.177.0,全模式)；F2 `dontAsk`=严格拒绝非宽松；F3 headless需`-y`,full pass需CODEBUDDY_IS_SANDBOX=1；F4 worktree非安全沙箱子代理可触外文件；F5 `--add-dir`不加载.target .codebuddy,Edit-deny不挡python -c,deny永远优先；F6 OS沙箱=bubblewrap/Seatbelt,域前置可绕；F7 GPL编辑=修改/静动链接=组合/内用不分发无义务；F8 Copilot Free≤2000补全/月仅个人、JetBrains OSS仅非商业、GSoC组织注册关闭。

## E. V4.1/V4.2 全球 F2 资源机会
| # | 机会 | 资格/规则 | 费用 | 商业/IP | P级 | 分 | 评级 | 行动 |
|---|---|---|---|---|---|---|---|---|
| O1 | GitHub Copilot Free | 个人无组织访问;≤2000补全/月 | $0 | 商用需Pro/Business($19/seat/月) | P1 | 4/5 | B | WAIT_USER |
| O2 | JetBrains OSS许可 | 非商业OSS免费;成熟项目个案审 | $0(非商业) | **仅personal non-commercial** | P1 | 4/5 | B | WAIT_USER |
| O3 | GitHub Sponsors | 维护者需税表+银行;103地区 | 平台费0%(通用政策,切片未逐字) | 收款为收入,IP不变 | P2 | 4/5 | A | 可行动(若已维护者) |
| O4 | Student Developer Pack | 须验证真实学生;教育/个人 | $0 | 禁商业生产 | P1 | 3/5 | B | WAIT_USER |
| O5 | GSoC 2026 | 官网"Org registration closed" | stipend(未载) | 学生贡献 | P2 | 0/5 | REJECT | 不可当开放 |

未登录/注册/领取/提交，未存凭据。O5 依反馈"已截止"且 fetch 显示组织注册关闭 → REJECT。O1/O2/O4 资格未达列 WAIT_USER；仅 O3 对已成维护者列"立即行动"(开通收款不涉领取外部资源)。

## F. 最终交付

### NEXT_AGENT_INSTRUCTIONS
1. 独立复核 AGPLv3 §13 网络触发逐字条款(本轮 fetch 截断)，补 gnu.org 原文，禁泛称无差别义务。
2. 待 R11 F1(job=13434ad175b04267) 出报告后，独立核验 ChatGPT 连接器写Git能力，再更新 Case B；勿沿用"CLAIMED"。
3. 在具 OS 强制边界(bubblewrap/容器)环境，对 MVE 做真实拒绝执行并复算 SHA。
4. 用 GitHub Actions 托管 semgrep/CodeQL 跑 3正3负，回填规则ID/退出码替换 NOT_TESTED。
5. 用试点数据填 UNKNOWN 单价，形成可报价成本表。
6. 严禁重复 R11/R12 派单；桥接器 1 running/2 queued、1 unresolved orphan 未变。

### 五案例状态表
| 案例 | 等级 | 状态 |
|---|---|---|
| A 开源解构 | DESIGNED/READY | 静态解析可跑 |
| B 合同→PR | DESIGNED(live BLOCKED) | 无git/无OS边界 |
| C 多Agent盲测 | BLOCKED | 无docker |
| D 供应链门禁 | NOT_TESTED | semgrep MISSING |
| E 桥接器恢复 | SIMULATED | MVE-2 22/22,不触生产 |

### 红队 ≥5
RT1 若 MVE 用 assert 做安全判定，`-O` 将 fail-open；已用 if/raise 验证 optimize0/1 一致。
RT2 恶意策略 allowed_root=/ + cleanup /** 被 GLOB_INJECTION+CLEANUP_ESCAPE 双拦。
RT3 R02 `rm -rf .codebuddy/worktrees/*` 被 MVE-2 通配+越界+归属三拒(exit2)。
RT4 权限层 deny 不挡 python -c 间接写 → 仅权限模式不足，需 OS 沙箱。
RT5 沙箱网络过滤可被域前绕过 → 非完整网络边界。
RT6 `-y`≡bypassPermissions，误当"安全无人值守"即越权；R02 案例B口径混乱。
RT7 AGPL§13 逐字未核验，禁把"网络服务须供源码"当无差别义务。

### 成本/权限/许可证矩阵
- 成本：零安装本地=0；模型/人工/云/维护=UNKNOWN(不再"0元")。
- 权限：`dontAsk`=严格拒绝；`-y`=bypass(高危,需sandbox)；OS边界=沙箱/容器,worktree≠边界。
- 许可：MIT/Apache宽松；GPL分发改同源；AGPL网络供源码；无许可仅只读研究。

### 机会雷达
O1 Copilot Free(B,WAIT_USER) O2 JetBrains OSS(B,WAIT_USER) O3 Sponsors(A,可行动) O4 Student(B,WAIT_USER) O5 GSoC2026(REJECT)。新候选：Sponsors收款、Copilot Pro商用层级、OSV/GHSA API(门禁真实化)。

### 人工行动卡
C1 WAIT_USER：确认商用 Copilot 层级与报价。C2 WAIT_USER：JetBrains OSS 仅非商业，评自身商业性。C3 可行动：若已为开源维护者开通 Sponsors。C4 WAIT_USER：真实学生方可申 Student Pack。C5 DO_NOT：勿提交 GSoC 2026。C6 WAIT_USER：独立验连接器写Git(待R11)。

### 自述 vs 独立验证分离
自述：完成 MVE-1(22/22)、MVE-2(22/22)、12 官方核验、五案例修订、机会雷达。
独立验证锚点：重算 §A.4 九个 SHA；重跑 `python3 mve1_policy_parser.py fixtures/f05_glob_injection.json` 与 `-O` 应同 exit2；重跑 `python3 mve2_task_contract.py validate contracts/c07_bad_cleanup_escape.json` 应 exit2。任何不符即失败。

RESULT_STATUS: COMPLETE_WITH_HONEST_NOT_TESTED
（live 权限拒绝/供应链扫描/真实PR 因缺 OS 边界与 git/scanner 诚实标 BLOCKED/NOT_TESTED，未自称全部 RESOLVED；R11 F1 未伪称结果）

END_FULL_REPORT