# -*- coding: utf-8 -*-
"""独立验证：已提交的派单能否从 GitHub 远程回读（私有仓 raw 不通时的 Contents API 回退是否生效）。"""
import importlib.util
import os

BASE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "pd", os.path.join(BASE, "p1git_dispatch.py"))
pd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pd)

print("OWNER/REPO = %s/%s  BRANCH=%s" % (pd.OWNER, pd.REPO, pd.BRANCH))
print("TOKEN = %s" % (pd.TOKEN[:4] + "***(len=%d)" % len(pd.TOKEN) if pd.TOKEN else "<none>"))

rel = "workbuddy/a_orders/TASK-P1-GIT-A-20261023-2120.md"
code, text = pd.raw_get(rel)
print("READBACK %s -> http=%s bytes=%d" % (rel, code, len(text or "")))
if code == 200 and text:
    for line in text.splitlines()[:16]:
        print("  | " + line)
else:
    print("  body=%s" % (text or "")[:200])
