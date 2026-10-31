#!/usr/bin/env python3
# R22 F2 independent read-only contract policy prototype, not production sandbox
import json, os, sys
from pathlib import Path
ALLOWED_MODES = {"default", "dontAsk"}
ALLOWED_ACTIONS = {"read", "write", "exec", "cleanup"}
def validate(contract, trusted_root):
    def deny(code): return {"status":"REJECTED","code":code}
    if not isinstance(contract,dict) or not contract: return deny("EMPTY_OR_TYPE")
    if set(contract)!={"version","rules","budget_tokens","mode"}: return deny("SCHEMA_KEYS")
    if contract["version"]!="1": return deny("VERSION")
    if not isinstance(contract["mode"],str) or contract["mode"] not in ALLOWED_MODES: return deny("MODE")
    budget=contract["budget_tokens"]
    if type(budget) is not int or not 1<=budget<=1000000: return deny("BUDGET")
    rules=contract["rules"]
    if not isinstance(rules,list) or not rules: return deny("RULES")
    root=Path(trusted_root).resolve(strict=True)
    if not root.is_dir(): return deny("ROOT")
    seen=set()
    for rule in rules:
        if not isinstance(rule,dict) or set(rule)!={"id","action","path"}: return deny("RULE_SCHEMA")
        rid=rule["id"]
        if not isinstance(rid,str) or not rid or rid in seen: return deny("RULE_ID")
        seen.add(rid)
        if rule["action"] not in ALLOWED_ACTIONS: return deny("ACTION")
        path=rule["path"]
        if not isinstance(path,str) or not path or not os.path.isabs(path): return deny("PATH_ABSOLUTE")
        if "*" in path or "?" in path or "\x00" in path: return deny("PATH_META")
        try:
            resolved=Path(path).resolve(strict=False)
            if not resolved.is_relative_to(root): return deny("PATH_ESCAPE")
        except (OSError,ValueError,RuntimeError): return deny("PATH_INVALID")
    return {"status":"ACCEPTED","code":"OK"}
def run():
    contract=json.loads(sys.stdin.read())
    result=validate(contract,sys.argv[1])
    print(json.dumps(result,sort_keys=True))
    return 0 if result["status"]=="ACCEPTED" else 2
if __name__=="__main__":
    try: sys.exit(run())
    except (json.JSONDecodeError,OSError,ValueError,IndexError):
        print('{"code":"INPUT_ERROR","status":"REJECTED"}')
        sys.exit(2)
