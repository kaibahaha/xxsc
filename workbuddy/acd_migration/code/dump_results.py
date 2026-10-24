# -*- coding: utf-8 -*-
"""只读：拉取 results/chatgpt-{a,c,d} 里结果文件的实际落盘内容（截断显示）。"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p1git_dispatch as m
import requests

s = requests.Session(); s.trust_env = False
hdr = {"Authorization": "Bearer %s" % m.TOKEN, "Accept": "application/vnd.github+json"}
base = "https://api.github.com/repos/%s/%s" % (m.OWNER, m.REPO)
BR = m.BRANCH

targets = [
    ("A", "results/chatgpt-a", "P1-GIT-A-20261024-1000.md"),
    ("A", "results/chatgpt-a", "P1-GIT-A-20261024-0030.md"),
    ("C", "results/chatgpt-c", "P1_C_WB-C-20261024T113632-220.md"),
    ("D", "results/chatgpt-d", "P1_D_WB-D-20261024T115651-405.md"),
]

for line, d, name in targets:
    path = "%s/%s" % (d, name)
    r = s.get("%s/contents/%s?ref=%s" % (base, path, BR), headers=hdr, timeout=30)
    print("=" * 70)
    if r.status_code != 200:
        print("[%s] %s -> HTTP%s" % (line, path, r.status_code))
        continue
    import base64
    txt = base64.b64decode(r.json()["content"]).decode("utf-8", "ignore")
    print("[%s] %s (%d bytes)" % (line, path, len(txt.encode("utf-8"))))
    print("-" * 70)
    print(txt[:1800])
    if len(txt) > 1800:
        print("...（后略，共 %d 字符）" % len(txt))
