#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
P1-GIT-A 本地精确调度器（每小时北京时间 :20 触发一次派单）
Windows 任务计划程序在本机被安全策略禁用时的等价实现（协议第3条允许的本地 Python 方案）。
"""
import os
import sys
import time
import subprocess
import json
from datetime import datetime, timedelta, timezone

BASE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(BASE, "state")
LOGS = os.path.join(STATE, "logs")
os.makedirs(LOGS, exist_ok=True)

PY = sys.executable
if PY.lower().endswith("pythonw.exe"):
    PY = PY[:-11] + "python.exe"
DISPATCH = os.path.join(BASE, "p1git_dispatch.py")

CST = timezone(timedelta(hours=8))
SCHED_MINUTE = 20


def log(msg):
    line = "[%s] %s" % (datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S"), msg)
    try:
        with open(os.path.join(LOGS, "scheduler.log"), "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def main():
    with open(os.path.join(STATE, "scheduler.pid"), "w", encoding="utf-8") as f:
        f.write(str(os.getpid()))
    log("SCHEDULER START pid=%s minute=%s" % (os.getpid(), SCHED_MINUTE))
    fired = {}   # key: YYYYMMDDHH -> True

    while True:
        now = datetime.now(CST)
        key = now.strftime("%Y%m%d%H")
        if now.minute == SCHED_MINUTE and not fired.get(key):
            fired[key] = True
            log("TRIGGER -> %s" % now.strftime("%Y-%m-%dT%H:%M:%S+08:00"))
            try:
                p = subprocess.run([PY, DISPATCH], cwd=BASE, capture_output=True,
                                   text=True, timeout=900)
                log("DISPATCH rc=%s out_tail=%s err_tail=%s" % (
                    p.returncode, (p.stdout or "")[-400:], (p.stderr or "")[-400:]))
            except Exception as e:
                log("DISPATCH EXCEPTION %s" % e)
        if now.minute != SCHED_MINUTE:
            fired.pop(key, None)
        time.sleep(15)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        log("FATAL %s" % __import__("traceback").format_exc())
