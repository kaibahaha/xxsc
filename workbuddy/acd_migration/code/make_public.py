# -*- coding: utf-8 -*-
"""把 kaibahaha/xxsc 从私有改为公开（用户已确认），并验证 raw 直读是否恢复。"""
import os
import requests

BASE = os.path.dirname(os.path.abspath(__file__))
tok = open(os.path.join(BASE, "state", "github_token.txt"), "r", encoding="utf-8").read().strip()
s = requests.Session()
s.trust_env = False
h = {"Authorization": "Bearer %s" % tok,
     "Accept": "application/vnd.github+json",
     "User-Agent": "p1-visibility/1.0"}

r = s.patch("https://api.github.com/repos/kaibahaha/xxsc",
            headers=h, json={"private": False}, timeout=30)
print("PATCH private=false -> http=%s" % r.status_code)
if r.status_code == 200:
    j = r.json()
    print("NOW private=%s  visibility=%s  default_branch=%s"
          % (j.get("private"), j.get("visibility"), j.get("default_branch")))
else:
    print("body=%s" % r.text[:300])

# 验证 raw 直读（公开仓不需要 Bearer）
url = ("https://raw.githubusercontent.com/kaibahaha/xxsc/"
       "exp/p1-relay-dualwrite-20261023/workbuddy/a_orders/"
       "TASK-P1-GIT-A-20261023-2220.md")
r2 = s.get(url, timeout=30)
print("RAW_ANON http=%s bytes=%d" % (r2.status_code, len(r2.text)))
if r2.status_code == 200:
    for line in r2.text.splitlines()[:6]:
        print("  | " + line)
