#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F8 RED-TEAM RUNNER  (assert-free -> safe under `python -O`)
============================================================
Runs >=8 negative cases (incl. R08 D1 estop-optimized-mode re-test) plus one
positive navigation MVE.  Exits 0 ONLY when every expectation is met.

IMPORTANT: this runner NEVER uses `assert` for gate verification.  All checks
use explicit `if / raise SystemExit`.  Therefore running it under
`python3 -O` exercises the SAME fail-closed logic as normal mode — proving the
R08 `assert not estop` bypass is gone.
"""
import json
import os
import sys
from datetime import datetime, timezone

import f8_contract as C

HERE = os.path.dirname(os.path.abspath(__file__))
IN = os.path.join(HERE, "inputs")


def load(name):
    with open(os.path.join(IN, name), "r", encoding="utf-8") as f:
        return json.load(f)


def fail(msg):
    print("RUNNER_FAIL: " + msg, file=sys.stderr)
    raise SystemExit(2)


# deterministic clock for reproducible expiry checks
NOW = datetime(2026, 11, 1, 0, 0, 0, tzinfo=timezone.utc)
DEVICE = "tb4-pilot-001"

auth_valid = load("auth_valid.json")
estop_off = {"estop": False}
estop_active = load("estop_active.json")
estop_missing = load("estop_missing.json")
estop_string = load("estop_string.json")
grid_valid = load("grid_valid.json")
grid_blocked = load("grid_blocked.json")
grid_badbounds = load("grid_badbounds.json")
cmd_nan = load("command_nan.json")
cmd_unknown = load("command_unknown_mode.json")

# Build a couple of adjacency variants inline (still frozen-class inputs).
auth_expired = load("auth_expired.json")
auth_string_false = load("auth_string_false.json")
auth_untrusted = load("auth_untrusted.json")
auth_device_mismatch = load("auth_device_mismatch.json")
auth_int_one = dict(auth_valid)
auth_int_one["authorized"] = 1  # truthy int, NOT strict bool


def case(name, expect_admit, command, auth, estop, tags):
    admitted, reason = C.run_case(name, command, auth, estop, DEVICE, NOW)
    ok = (admitted == expect_admit)
    verdict = "PASS" if ok else "FAIL"
    print("[%s] %-28s expect_admit=%-5s admitted=%-5s %s :: %s"
          % (verdict, name, expect_admit, admitted, ",".join(tags), reason[:90]))
    if not ok:
        fail("case '%s' mismatch: expected admit=%s got %s" % (name, expect_admit, admitted))
    # extra invariant for positive navigation
    if admitted and "nav" in tags:
        res = json.loads(reason)
        path = res["path"]
        if path[0] != command["start"] or path[-1] != command["goal"]:
            fail("positive path endpoints wrong")
        for (x, y) in path:
            if command["grid"][y][x] != C.GRID_FREE:
                fail("PATH CROSSES OBSTACLE at %s" % ([x, y],))
    return admitted, reason


print("=== F8 RED-TEAM (%s mode) ===" % ("OPTIMIZE" if sys.flags.optimize else "NORMAL"))
print("now=%s device=%s" % (NOW.isoformat(), DEVICE))

# ---- NEGATIVE cases (expect DENY / admitted=False) -------------------------
case("N1_estop_active",        False, grid_valid,     auth_valid,        estop_active,    ["estop", "core"])
case("N2_estop_missing",       False, grid_valid,     auth_valid,        estop_missing,   ["estop", "adjacent"])
case("N3_estop_string_true",   False, grid_valid,     auth_valid,        estop_string,    ["estop", "adjacent", "type"])
case("N4_auth_expired",        False, grid_valid,     auth_expired,      estop_off,       ["auth", "adjacent"])
case("N5_auth_string_false",   False, grid_valid,     auth_string_false, estop_off,       ["auth", "adjacent", "type"])
case("N6_auth_untrusted_src",  False, grid_valid,     auth_untrusted,    estop_off,       ["auth", "adjacent"])
case("N7_auth_device_mismatch",False, grid_valid,     auth_device_mismatch, estop_off,    ["auth", "adjacent"])
case("N8_auth_int_one",        False, grid_valid,     auth_int_one,      estop_off,       ["auth", "adjacent", "type"])
case("N9_cmd_velocity_nan",    False, cmd_nan,        auth_valid,        estop_off,       ["cmd", "adjacent"])
case("N10_cmd_unknown_mode",   False, cmd_unknown,    auth_valid,        estop_off,       ["cmd", "adjacent"])
case("N11_nav_no_path",        False, grid_blocked,   auth_valid,        estop_off,       ["nav", "adjacent"])
case("N12_nav_oob_start",      False, grid_badbounds, auth_valid,        estop_off,       ["nav", "adjacent"])
case("N13_net_disconnect",     False, grid_valid,     None,              estop_off,       ["auth", "adjacent", "default-deny"])

# ---- POSITIVE case (expect ADMIT, safe path) -------------------------------
case("P1_valid_nav",           True,  grid_valid,     auth_valid,        estop_off,       ["nav", "positive"])

print("=== ALL CASES PASS (fail-closed verified) ===")
raise SystemExit(0)
