#!/usr/bin/env python3
# 只读探针：确认当前 WorkBuddy Git 身份对目标仓库的权限（不改任何东西）
import os, json, base64, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
TOKEN = ""
tp = os.path.join(ROOT, "state", "github_token.txt")
if os.path.exists(tp):
    TOKEN = open(tp, "r", encoding="utf-8").read().strip()

def api(path):
    url = "https://api.github.com" + path
    req = urllib.request.Request(url, headers={
        "Authorization": "Bearer " + TOKEN,
        "Accept": "application/vnd.github+json",
        "User-Agent": "p1git-probe",
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, json.loads(r.read().decode("utf-8", "ignore"))
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read().decode("utf-8", "ignore"))
        except Exception:
            body = {}
        return e.code, body
    except Exception as e:
        return -1, {"error": str(e)}

st, me = api("/user")
print("WHOAMI        :", st, "login=", me.get("login"), "id=", me.get("id"))
for repo in ["OutsiderVictor/xxsc", "kaibahaha/xxsc"]:
    st, body = api("/repos/" + repo)
    print(f"REPO {repo:22s}: http={st} id={body.get('id')} visibility={body.get('visibility')} perms={body.get('permissions')}")
