#!/usr/bin/env python3
# 只读：统计 kaibahaha/xxsc 实验分支上的派单/回执/结果文件（权威统计）
import os, json, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.abspath(__file__))
TOKEN = open(os.path.join(ROOT, "state", "github_token.txt"), "r", encoding="utf-8").read().strip()
BRANCH = "exp/p1-relay-dualwrite-20261023"
OWNER, REPO = "kaibahaha", "xxsc"

def list_dir(path):
    url = "https://api.github.com/repos/%s/%s/contents/%s?ref=%s" % (OWNER, REPO, path, BRANCH)
    req = urllib.request.Request(url, headers={
        "Authorization": "Bearer " + TOKEN,
        "Accept": "application/vnd.github+json",
        "User-Agent": "p1git-stat",
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, json.loads(r.read().decode("utf-8", "ignore"))
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode("utf-8", "ignore"))
        except Exception:
            return e.code, []

for label, path in [("派单 a_orders", "workbuddy/a_orders"),
                    ("回执 acks", "workbuddy/acks"),
                    ("A结果 results/chatgpt-a", "results/chatgpt-a")]:
    st, items = list_dir(path)
    if st != 200 or not isinstance(items, list):
        print("%-22s http=%s (空或不存在)" % (label, st))
        continue
    files = [it["name"] for it in items if it.get("type") == "file"]
    print("%-22s 共 %d 个文件：" % (label, len(files)))
    for f in sorted(files):
        print("   -", f)
