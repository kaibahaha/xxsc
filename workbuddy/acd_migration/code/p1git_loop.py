# -*- coding: utf-8 -*-
"""P1-GIT 常驻循环派单器（替代 WorkBuddy 自带定时任务）。

设计：
- 一个常驻进程自我循环，每 30 分钟对齐到整点/半点边界，依次派 A/C/D 三线的当前 slot。
- 不依赖外部调度器 firing，比 WorkBuddy 定时任务靠谱（后者休眠/重连后不恢复触发）。
- 复用 p1git_dispatch.py --line，dispatch 自身按 TASK_ID 对本地+远端双去重 -> 重复 fire 无害。
- 策略：只派"当前边界"这一格，不回填历史漏槽（与 2026-10-24 用户决定一致）。
- STOP_AT 沿用 p1git_dispatch 的 2026-10-25 12:00（到点后 dispatch 自动 READ_ONLY，循环空转）。

运行：python p1git_loop.py  (建议 Bash run_in_background)
"""
import os, sys, time, subprocess, traceback
from datetime import datetime, timedelta, timezone

BASE = os.path.dirname(os.path.abspath(__file__))
LOGS = os.path.join(BASE, "state", "logs")
os.makedirs(LOGS, exist_ok=True)

# 必须用带 requests 的 Python（managed 3.13 venv 无 requests，故用系统 Python310）
PY = r"C:/Users/Administrator/AppData/Local/Programs/Python/Python310/python.exe"
DISPATCH = os.path.join(BASE, "p1git_dispatch.py")
CST = timezone(timedelta(hours=8))
LINES = ("A", "C", "D")
PIDFILE = os.path.join(BASE, "state", "p1git_loop.pid")
LOOPLOG = os.path.join(LOGS, "p1git_loop.log")


def log(msg):
    line = "[%s] %s" % (datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S"), msg)
    try:
        print(line, flush=True)
    except Exception:
        pass
    try:
        with open(LOOPLOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def dispatch_line(line):
    try:
        p = subprocess.run([PY, DISPATCH, "--line", line], cwd=BASE,
                           capture_output=True, text=True, timeout=900)
        tail = (p.stdout or "")[-260:]
        log("DISPATCH line=%s rc=%s | %s" % (line, p.returncode, tail.replace("\n", " ")))
    except Exception as e:
        log("DISPATCH EXC line=%s %s" % (line, e))


def main():
    with open(PIDFILE, "w", encoding="utf-8") as f:
        f.write(str(os.getpid()))
    log("LOOP START pid=%s lines=%s interval=30min (替代 WorkBuddy 定时任务)" %
        (os.getpid(), ",".join(LINES)))
    while True:
        now = datetime.now(CST)
        grid = (now.minute // 30) * 30
        slot = now.replace(minute=grid, second=0, microsecond=0)
        log("TICK slot=%s" % slot.strftime("%Y-%m-%dT%H:%M"))
        # 三线顺序派（dispatch 内部 A:0/C:7/D:15 错峰，规避 409）
        for line in LINES:
            dispatch_line(line)
        # 睡到下一个 30 分钟边界
        nxt = slot + timedelta(minutes=30)
        delta = (nxt - datetime.now(CST)).total_seconds()
        if delta < 1:
            delta = 1
        log("SLEEP %ds -> %s" % (int(delta), nxt.strftime("%Y-%m-%dT%H:%M")))
        time.sleep(delta)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        log("FATAL %s" % traceback.format_exc())
