import json,subprocess,sys,hashlib
from pathlib import Path
base=Path('/mnt/data/factory10_r22_independent')
root=base/'testroot';root.mkdir(exist_ok=True)
outside=base/'testroot-evil';outside.mkdir(exist_ok=True)
link=root/'link'
if not link.exists() and not link.is_symlink(): link.symlink_to(outside,target_is_directory=True)
good={'version':'1','rules':[{'id':'r1','action':'read','path':str(root/'safe.txt')}],'budget_tokens':100,'mode':'dontAsk'}
cases={'valid':good}
def case(name,change):
 v=json.loads(json.dumps(good));change(v);cases[name]=v
case('relative_path',lambda x:x['rules'][0].update(path='sensitive_file'))
case('unknown_mode',lambda x:x.update(mode='anything'))
case('negative_budget',lambda x:x.update(budget_tokens=-999))
case('sandbox_string_true',lambda x:x.update(sandbox='false'))
case('empty_rules',lambda x:x.update(rules=[]))
case('symlink_escape',lambda x:x['rules'][0].update(path=str(root/'link'/'secret')))
case('prefix_collision',lambda x:x['rules'][0].update(path=str(outside/'secret')))
case('duplicate_id',lambda x:x['rules'].append(dict(x['rules'][0])))
case('budget_bool',lambda x:x.update(budget_tokens=True))
case('wildcard_cleanup',lambda x:x['rules'][0].update(path=str(root/'*'),action='cleanup'))
case('bypass_mode',lambda x:x.update(mode='bypassPermissions'))
case('unknown_action',lambda x:x['rules'][0].update(action='deleteAll'))
cases['empty_input']={}
(base/'frozen_inputs.json').write_text(json.dumps({'trusted_root':str(root),'cases':cases},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
log=[]
for mode in ([],['-O']):
 for name,fixture in cases.items():
  cp=subprocess.run([sys.executable,*mode,str(base/'policy_gate.py'),str(root)],input=json.dumps(fixture),text=True,capture_output=True,timeout=3)
  expected=0 if name=='valid' else 2
  passed=cp.returncode==expected and ('ACCEPTED' in cp.stdout if name=='valid' else 'REJECTED' in cp.stdout)
  log.append({'case':name,'mode':'-O' if mode else 'normal','expected_exit':expected,'actual_exit':cp.returncode,'stdout':cp.stdout.strip(),'stderr':cp.stderr.strip(),'pass':passed})
(base/'redteam_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('total',len(log),'passed',sum(x['pass'] for x in log),'failed',[(x['case'],x['mode']) for x in log if not x['pass']])
for p in (base/'policy_gate.py',base/'run_redteam.py',base/'frozen_inputs.json',base/'redteam_log.json'):
 print(p.name,p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest())
