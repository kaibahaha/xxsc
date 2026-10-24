# -*- coding: utf-8 -*-
"""只读核验指定 30 分钟槽的三线派单/ACK/回写状态。用法: verify_slot.py <HHMM>
不写 git、不派单、不读 token 明文。"""
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p1git_dispatch as m
import requests

slot = sys.argv[1] if len(sys.argv) > 1 else "0900"
s = requests.Session(); s.trust_env = False
hdr = {"Authorization": "Bearer %s" % m.TOKEN, "Accept": "application/vnd.github+json"}
base = "https://api.github.com/repos/%s/%s" % (m.OWNER, m.REPO)
BR = m.BRANCH

print("===== 核验时间: %s =====" % m.now_cst().strftime("%Y-%m-%dT%H:%M:%S+08:00"))
print("仓库: %s/%s  分支: %s  目标槽: %s" % (m.OWNER, m.REPO, BR, slot))

print("\n----- [1] runs.jsonl %s 槽记录 -----" % slot)
rows = []
p = os.path.join(m.STATE_DIR, "runs.jsonl")
if os.path.exists(p):
    for line in open(p, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except Exception:
            pass
hits = [r for r in rows if slot in (r.get("task_id") or "")]
if hits:
    for r in hits:
        print("  ", r.get("task_id"), "|", r.get("state"), "|",
              r.get("actual_at") or r.get("planned_at"), "| commit:",
              (r.get("commit_sha") or "")[:10])
else:
    print("  （无 %s 槽记录 -> 自动化未运行或未写日志）" % slot)

for line in ("A", "C", "D"):
    tag = "[2.%s]" % line
    path = "workbuddy/%s_orders/TASK-P1-GIT-%s-20261024-%s.md" % (line.lower(), line, slot)
    print("\n----- %s 派单 %s -----" % (tag, path))
    code, txt = m.raw_get(path)
    if code == 200:
        r = s.get("%s/commits?sha=%s&path=%s&per_page=1" % (base, BR, path), headers=hdr, timeout=30)
        csha = r.json()[0]["sha"] if r.status_code == 200 and r.json() else "?"
        fields = {}
        qlist = []
        for ln in txt.splitlines():
            for key in ("TASK_ID", "ASSIGNEE", "SCHEDULE_ID", "GLOBAL_SEQ"):
                if ln.startswith("| %s " % key):
                    fields[key] = ln.split("`")[1] if "`" in ln else ln
            if ln.startswith("| QUESTION_NO"):
                qlist.append(ln.split("`")[1] if "`" in ln else ln)
        print("  远端读取 HTTP200 | commit: %s" % csha)
        for k in ("TASK_ID", "ASSIGNEE", "SCHEDULE_ID", "GLOBAL_SEQ"):
            print("  %s: %s" % (k, fields.get(k, "(未解析)")))
        print("  QUESTION_NO: %s" % (qlist if qlist else "(未解析)"))
        print("  ---- 正文前 20 行 ----")
        print("\n".join("  " + x for x in txt.splitlines()[:20]))
    else:
        print("  远端读取 HTTP%s -> 该槽未派单" % code)

print("\n----- [3] ACK（workbuddy/acks/ 中含 %s） -----" % slot)
r = s.get("%s/contents/workbuddy/acks?ref=%s" % (base, BR), headers=hdr, timeout=30)
if r.status_code == 200:
    acks = [it["name"] for it in r.json() if slot in it["name"]]
    print("  " + ("\n  ".join(acks) if acks else "（无 %s 槽 ACK）" % slot))
else:
    print("  HTTP%s" % r.status_code)

print("\n----- [4] results/chatgpt-* 回写检查（闭环判据：按派单 TASK_ID 对应结果文件名） -----")
# 结果文件名规则（与派单 RESULT_EXPECTED_PATH 一致）：P1-GIT-{LINE}-YYYYMMDD-HHMM.md
# 注意：结果文件没有 TASK- 前缀（派单文件才有），勿用派单文件名直接当结果文件名查。
for line in ("a", "c", "d"):
    d = "results/chatgpt-%s" % line
    r = s.get("%s/contents/%s?ref=%s" % (base, d, BR), headers=hdr, timeout=30)
    expect = "P1-GIT-%s-20261024-%s.md" % (line.upper(), slot)
    if r.status_code == 200:
        names = [it["name"] for it in r.json()]
        hit = expect in names
        print("  %-22s -> %d 个文件；期望结果 %s -> %s" % (
            d, len(names), expect, "已回写 ✅" if hit else "未回写 ❌"))
    else:
        print("  %-22s -> HTTP%s（目录不存在）；期望结果 %s -> 未回写 ❌" % (d, r.status_code, expect))

print("\n===== 核验结束 %s =====" % m.now_cst().strftime("%H:%M:%S"))
