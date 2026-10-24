# -*- coding: utf-8 -*-
"""只读探查 v4：xxsc 仓库的默认分支与分支列表。"""
import os
import requests

BASE = os.path.dirname(os.path.abspath(__file__))
tok = open(os.path.join(BASE, "state", "github_token.txt"), "r", encoding="utf-8").read().strip()
s = requests.Session()
s.trust_env = False
h = {"Authorization": "Bearer %s" % tok,
     "Accept": "application/vnd.github+json",
     "User-Agent": "p1-probe/1.0"}

r = s.get("https://api.github.com/repos/kaibahaha/xxsc", headers=h, timeout=30)
j = r.json() if r.status_code == 200 else {}
print("REPO http=%s default_branch=%s private=%s"
      % (r.status_code, j.get("default_branch"), j.get("private")))

r2 = s.get("https://api.github.com/repos/kaibahaha/xxsc/branches?per_page=50",
           headers=h, timeout=30)
print("BRANCHES http=%s -> %s"
      % (r2.status_code,
         [b.get("name") for b in r2.json()] if r2.status_code == 200 else r2.text[:150]))

r3 = s.get("https://api.github.com/repos/kaibahaha/xxsc/contents/README.md",
           headers=h, timeout=30)
print("README http=%s" % r3.status_code)
