#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GitHub OAuth Device Flow（官方公开 client，无需预置密钥）
拿到 token 后写入 state/github_token.txt，并立刻跑一次首轮派单。
token 只落盘，不打印明文。
"""
import os
import sys
import time
import json
import subprocess
import requests

BASE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(BASE, "state")
os.makedirs(STATE, exist_ok=True)
TOKEN_FILE = os.path.join(STATE, "github_token.txt")

CLIENT_ID = "Iv1.b507a08c87ecfe98"   # gh CLI 公开 client_id
SCOPE = "repo,read:user"
PY = r"C:\Users\Administrator\.workbuddy\binaries\python\envs\default\Scripts\python.exe"


def log(m):
    print("[%s] %s" % (time.strftime("%H:%M:%S"), m), flush=True)


def main():
    r = requests.post("https://github.com/login/device/code",
                      headers={"Accept": "application/json"},
                      data={"client_id": CLIENT_ID, "scope": SCOPE}, timeout=30)
    log("device/code http=%s" % r.status_code)
    if r.status_code != 200:
        print(r.text[:300])
        return 2
    d = r.json()
    user_code = d["user_code"]
    verify = d.get("verification_uri", "https://github.com/login/device")
    interval = int(d.get("interval", 5))
    expires = int(d.get("expires_in", 900))
    device_code = d["device_code"]

    print("=" * 60, flush=True)
    print("请在浏览器打开： %s" % verify, flush=True)
    print("输入授权码：     %s" % user_code, flush=True)
    print("授权 scope:      %s" % SCOPE, flush=True)
    print("=" * 60, flush=True)

    deadline = time.time() + expires
    fail_streak = 0
    while time.time() < deadline:
        time.sleep(interval)
        try:
            t = requests.post("https://github.com/login/oauth/access_token",
                              headers={"Accept": "application/json"},
                              data={"client_id": CLIENT_ID, "device_code": device_code,
                                    "grant_type": "urn:ietf:params:oauth:grant-type:device_code"},
                              timeout=30)
            j = t.json()
        except Exception as e:
            fail_streak += 1
            log("network blip (%d): %s" % (fail_streak, type(e).__name__))
            if fail_streak > 20:
                log("too many network failures, abort")
                return 5
            continue
        fail_streak = 0
        if "access_token" in j:
            tok = j["access_token"]
            with open(TOKEN_FILE, "w", encoding="utf-8") as f:
                f.write(tok)
            log("AUTH OK, token saved (len=%d, prefix=%s***)" % (len(tok), tok[:4]))
            who = requests.get("https://api.github.com/user",
                               headers={"Authorization": "Bearer %s" % tok,
                                        "Accept": "application/vnd.github+json"}, timeout=30)
            log("authenticated as: %s" % who.json().get("login") if who.status_code == 200 else "whoami failed")
            return 0
        err = j.get("error")
        if err == "authorization_pending":
            log("waiting for user authorization ...")
            continue
        if err == "slow_down":
            interval += 5
            continue
        log("auth error: %s" % err)
        return 3
    log("device code expired")
    return 4


if __name__ == "__main__":
    sys.exit(main())
