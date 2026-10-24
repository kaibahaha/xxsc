# -*- coding: utf-8 -*-
"""只读全量统计：kaibahaha/xxsc 实验分支 A/C/D 三线派单/ACK/结果 + 最近提交。
不写 git、不派单、不打印 token 明文。"""
import os, sys, json
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p1git_dispatch as m
import requests

s = requests.Session(); s.trust_env = False
hdr = {"Authorization": "Bearer %s" % m.TOKEN, "Accept": "application/vnd.github+json"}
base = "https://api.github.com/repos/%s/%s" % (m.OWNER, m.REPO)
BR = m.BRANCH

print("===== 统计时间: %s =====" % m.now_cst().strftime("%Y-%m-%dT%H:%M:%S+08:00"))
print("仓库: %s/%s  分支: %s" % (m.OWNER, m.REPO, BR))

def list_dir(path):
    r = s.get("%s/contents/%s?ref=%s" % (base, path, BR), headers=hdr, timeout=30)
    if r.status_code != 200:
        return r.status_code, []
    return r.status_code, [it for it in r.json() if it.get("type") == "file"]

# ---------- [1] 派单 ----------
orders = {}   # line -> [names]
for line in ("a", "c", "d"):
    path = "workbuddy/%s_orders" % line
    code, files = list_dir(path)
    orders[line] = sorted(f["name"] for f in files)
    print("\n----- [1] 派单 workbuddy/%s_orders -----" % line)
    if code != 200:
        print("  HTTP%s（目录不存在）" % code)
    elif not orders[line]:
        print("  （空）")
    else:
        for n in orders[line]:
            print("   -", n)

# ---------- [2] ACK ----------
print("\n----- [2] ACK workbuddy/acks -----")
code, files = list_dir("workbuddy/acks")
if code != 200:
    print("  HTTP%s（目录不存在）" % code)
else:
    acks = sorted(f["name"] for f in files)
    if not acks:
        print("  （空）")
    for n in acks:
        print("   -", n)

# ---------- [3] 结果 ----------
results = {}  # line -> [names]
print("\n----- [3] 结果 results/chatgpt-{a,c,d} -----")
for line in ("a", "c", "d"):
    d = "results/chatgpt-%s" % line
    code, files = list_dir(d)
    results[line] = sorted(f["name"] for f in files)
    if code != 200:
        print("  %-22s HTTP%s（目录不存在）" % (d, code))
    else:
        print("  %-22s %d 个文件" % (d, len(results[line])))
        for n in results[line]:
            print("     -", n)

# ---------- [4] 闭环配对 ----------
print("\n----- [4] 闭环配对（派单 TASK-P1-GIT-X-HHMM  <->  结果 P1-GIT-X-HHMM） -----")
def hhmm(n):
    # TASK-P1-GIT-A-20261024-1000.md -> 1000 ; P1-GIT-A-20261024-1000.md -> 1000
    parts = n.replace(".md", "").split("-")
    return parts[-1] if parts else ""

for line in ("a", "c", "d"):
    L = line.upper()
    o_slots = {}
    for n in orders[line]:
        if n.startswith("TASK-P1-GIT-%s-" % L):
            o_slots[hhmm(n)] = n
    r_slots = set(hhmm(n) for n in results[line] if n.startswith("P1-GIT-%s-" % L))
    print("  %s 线：派单 %d 单 / 结果 %d 份" % (L, len(o_slots), len(r_slots & set(o_slots))))
    for slot in sorted(o_slots):
        ok = slot in r_slots
        print("    %-6s %s  派单:%s" % (slot, "闭环✅" if ok else "未回写❌", o_slots[slot]))

# ---------- [5] 最近提交 ----------
print("\n----- [5] 分支最近 15 次提交 -----")
r = s.get("%s/commits?sha=%s&per_page=15" % (base, BR), headers=hdr, timeout=30)
if r.status_code == 200:
    for c in r.json():
        print("  %s  %s  %s" % (c["sha"][:10], c["commit"]["committer"]["date"], c["commit"]["message"].splitlines()[0][:80]))
else:
    print("  HTTP%s" % r.status_code)

# ---------- [6] 本地 runs.jsonl ----------
print("\n----- [6] 本地 runs.jsonl 派单日志 -----")
p = os.path.join(m.STATE_DIR, "runs.jsonl")
if os.path.exists(p):
    n = 0
    for ln in open(p, encoding="utf-8"):
        ln = ln.strip()
        if ln:
            n += 1
    print("  共 %d 条记录" % n)
else:
    print("  文件不存在")

print("\n===== 统计结束 %s =====" % m.now_cst().strftime("%H:%M:%S"))
