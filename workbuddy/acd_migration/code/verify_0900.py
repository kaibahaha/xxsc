# -*- coding: utf-8 -*-
"""P1-GIT 09:00 槽只读核验（不写 git、不派单、不读 token）。
用法：PY verify_0900.py
输出：三线派单实况、字段原文、commit、ACK、回写状态。
"""
import os, sys, json, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import p1git_dispatch as m  # noqa: E402
import requests  # noqa: E402

SLOT = "20261024-0900"
CST = datetime.timezone(datetime.timedelta(hours=8))
s = requests.Session(); s.trust_env = False
hdr = {"Authorization": "Bearer %s" % m.TOKEN, "Accept": "application/vnd.github+json"}
base = "https://api.github.com/repos/%s/%s" % (m.OWNER, m.REPO)
BR = m.BRANCH

print("===== 核验时间: %s =====" % datetime.datetime.now(CST).strftime("%Y-%m-%dT%H:%M:%S+08:00"))
print("仓库: %s/%s  分支: %s" % (m.OWNER, m.REPO, BR))

# 1) runs.jsonl 中 0900 槽记录
print("\n----- [1] runs.jsonl 0900 槽记录 -----")
rows = []
p = os.path.join(m.STATE_DIR, "runs.jsonl")
if os.path.exists(p):
    for l in open(p, encoding="utf-8"):
        l = l.strip()
        if not l:
            continue
        try:
            rows.append(json.loads(l))
        except Exception:
            pass
slot_rows = [r for r in rows if (r.get("task_id") or "").endswith(SLOT)]
if not slot_rows:
    print("  （无 0900 槽记录 -> 自动化 09:00 未运行或未写日志）")
for r in slot_rows:
    print("  %s | state=%s | actual_at=%s | commit=%s" % (
        r.get("task_id"), r.get("state"), r.get("actual_at"),
        (r.get("commit_sha") or "")[:12]))

# 2) 远端派单文件 + 字段原文 + commit sha
for line in ("A", "C", "D"):
    rel = "workbuddy/%s_orders/TASK-P1-GIT-%s-%s.md" % (line.lower(), line, SLOT)
    print("\n----- [2.%s] 派单 %s -----" % (line, rel))
    code, txt = m.raw_get(rel)
    if code != 200:
        print("  远端读取 HTTP%s -> 该槽未派单" % code)
        continue
    fields = {}
    qlist = []
    for ln in txt.splitlines():
        if ln.startswith("| TASK_ID"):
            fields["TASK_ID"] = ln.split("`")[1]
        elif ln.startswith("| ASSIGNEE"):
            fields["ASSIGNEE"] = ln.split("`")[1]
        elif ln.startswith("| SCHEDULE_ID"):
            fields["SCHEDULE_ID"] = ln.split("`")[1]
        elif ln.startswith("| GLOBAL_SEQ"):
            fields["GLOBAL_SEQ"] = ln.split("`")[1]
        elif ln.startswith("| QUESTION_NO"):
            qlist.append(ln.split("`")[1])
    fields["QUESTION_NO"] = qlist
    r = s.get("%s/commits?sha=%s&path=%s&per_page=1" % (base, BR, rel), headers=hdr, timeout=30)
    csha = r.json()[0]["sha"] if (r.status_code == 200 and r.json()) else "?"
    cmsg = r.json()[0]["commit"]["message"].splitlines()[0] if (r.status_code == 200 and r.json()) else ""
    print("  commit_sha: %s" % csha)
    print("  commit_msg: %s" % cmsg[:90])
    for k, v in fields.items():
        print("  %s: %s" % (k, v))
    # 覆盖规则句是否在文中
    has_override = "只回写 git，不额外镜像 Drive" in txt
    print("  覆盖规则句存在: %s" % ("是" if has_override else "否（异常！）"))

# 3) ACK 文件
print("\n----- [3] ACK（workbuddy/acks/ 中含 0900） -----")
r = s.get("%s/contents/workbuddy/acks?ref=%s" % (base, BR), headers=hdr, timeout=30)
if r.status_code == 200:
    names = [it["name"] for it in r.json() if SLOT in it["name"]]
    if names:
        for n in names:
            print("  ", n)
            c2, t2 = m.raw_get("workbuddy/acks/%s" % n)
            if c2 == 200:
                for ln in t2.splitlines():
                    if '"state"' in ln or '"ack_state"' in ln or "RESULT" in ln.upper():
                        print("      ", ln.strip()[:120])
    else:
        print("  （无 0900 槽 ACK）")
else:
    print("  acks 目录 HTTP%s" % r.status_code)

# 4) ChatGPT 回写检查
print("\n----- [4] results/chatgpt-* 回写检查（闭环判据） -----")
for line in ("a", "c", "d"):
    d = "results/chatgpt-%s" % line
    r = s.get("%s/contents/%s?ref=%s" % (base, d, BR), headers=hdr, timeout=30)
    if r.status_code != 200:
        print("  %-20s -> HTTP%s（目录不存在，无回写）" % (d, r.status_code))
        continue
    names = [it["name"] for it in r.json()]
    hit = [n for n in names if SLOT in n]
    print("  %-20s -> %d 个文件；0900 槽结果文件: %s" % (
        d, len(names), hit if hit else "无（未回写）"))

print("\n===== 核验结束 %s =====" % datetime.datetime.now(CST).strftime("%H:%M:%S"))
