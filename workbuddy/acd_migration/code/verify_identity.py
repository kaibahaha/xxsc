# -*- coding: utf-8 -*-
"""只读核对：当前 WorkBuddy Git 身份（classic PAT，kaibahaha 账号）对两座仓库的真实权限。"""
import os
import requests

BASE = os.path.dirname(os.path.abspath(__file__))
tok = open(os.path.join(BASE, "state", "github_token.txt"), "r", encoding="utf-8").read().strip()
s = requests.Session()
s.trust_env = False
h = {"Authorization": "Bearer %s" % tok, "Accept": "application/vnd.github+json"}

# 当前身份
r = s.get("https://api.github.com/user", headers=h, timeout=30)
me = r.json() if r.status_code == 200 else {}
print("IDENTITY login=%s id=%s" % (me.get("login"), me.get("id")))

for full in ("OutsiderVictor/xxsc", "kaibahaha/xxsc"):
    r2 = s.get("https://api.github.com/repos/%s" % full, headers=h, timeout=30)
    j = r2.json() if r2.status_code == 200 else {}
    print("%s -> http=%s private=%s id=%s default_branch=%s"
          % (full, r2.status_code, j.get("private"), j.get("id"), j.get("default_branch")))

# 可见仓库列表（证明身份边界）
r3 = s.get("https://api.github.com/user/repos?per_page=100", headers=h, timeout=30)
print("VISIBLE_REPOS count=%s"
      % (len(r3.json()) if r3.status_code == 200 else r3.status_code))
