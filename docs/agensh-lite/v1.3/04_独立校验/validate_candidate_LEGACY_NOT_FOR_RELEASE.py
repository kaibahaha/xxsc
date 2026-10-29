#!/usr/bin/env python3
"""Documentation/snapshot-only validation. NOT an agent runtime or Git authorization test."""
from pathlib import Path
from copy import deepcopy
import hashlib, json, re, sys
from jsonschema import Draft202012Validator
BASE=Path(__file__).resolve().parents[1]
contract=BASE/'03_V121机器契约留存'
orig=Path('/mnt/data/agensh_v121_l0')  # optional source-identity check when original Library files are mounted
types=('task','event','message','ack','review','delivery','run')
passes=0
negatives=0
results=[]
for kind in types:
  schema=json.loads((contract/'schemas'/f'{kind}.schema.json').read_text())
  sample=json.loads((contract/'examples'/f'{kind}.valid.json').read_text())
  Draft202012Validator.check_schema(schema)
  validator=Draft202012Validator(schema)
  assert validator.is_valid(sample),(kind,'positive')
  passes+=1
  results.append((kind,'positive','PASS'))
  for field in schema.get('required',[]):
    bad=deepcopy(sample);bad.pop(field,None)
    assert not validator.is_valid(bad),(kind,'missing required accepted',field)
    passes+=1; negatives+=1
  bad=deepcopy(sample);bad['schema_version']='NOT_REAL_VERSION'
  assert not validator.is_valid(bad),(kind,'invalid version accepted')
  passes+=1; negatives+=1
# Additional targeted V1.2.1 schema checks, as *schema-only* evidence
event_schema=json.loads((contract/'schemas'/'event.schema.json').read_text())
event=json.loads((contract/'examples'/'event.valid.json').read_text())
E=Draft202012Validator(event_schema)
first=deepcopy(event);first['event_type']='TASK_CREATED';first['expected_state']='ABSENT';first['requested_state']='PROPOSED'
assert E.is_valid(first),('first task creation should validate',list(E.iter_errors(first)))
passes+=1
bad=deepcopy(first);bad['event_type']='TASK_READY';assert not E.is_valid(bad)
passes+=1
bad=deepcopy(event);bad['target_kind']='ACK';assert not E.is_valid(bad)
passes+=1
# VERIFIED needs a structural proof bundle; this tests shapes only, NOT real remote readback.
delivery_schema=json.loads((contract/'schemas'/'delivery.schema.json').read_text())
delivery=json.loads((contract/'examples'/'delivery.valid.json').read_text())
D=Draft202012Validator(delivery_schema)
dbad=deepcopy(delivery); dbad['status']='VERIFIED'
assert not D.is_valid(dbad),'VERIFIED without readback unexpectedly accepted'
passes+=1; negatives+=1
dgood=deepcopy(delivery); dgood.update({'status':'VERIFIED','readback_hash':'a'*64,'comparison_hash':'a'*64,'hash_basis':'RAW_BYTES_SHA256','readback_ref':'EXAMPLE:git/sha','readback_at_utc':'2026-10-28T00:00:00Z'})
assert D.is_valid(dgood),list(D.iter_errors(dgood))
passes+=1
# File identity / old primary volumes retained and unchanged against published baseline manifest
source_manifest=json.loads((contract/'extraction_manifest.json').read_text())
old_candidates=list(orig.glob('纲领02_*V1.2.1*')) if orig.exists() else []
source_sha_verified=bool(old_candidates)
if source_sha_verified:
 assert hashlib.sha256(old_candidates[0].read_bytes()).hexdigest()==source_manifest['source_sha256']
 passes+=1
# Structural: 3 candidate volumes; 50 source rows; twice-positive no-hidden-authorization clauses
vols=list((BASE/'00_三卷候选').glob('*.md'))
assert len(vols)==3
for p in vols:
 t=p.read_text()
 assert 'PROPOSED_NOT_EFFECTIVE' in t and '2026-10-28' in t and t.count('## ') >= 3
 assert '微软' in t
 passes+=1
source=(BASE/'01_逐项对照与变更'/'微软Agensh论文源码与LiteV13规则逐项对照_20261028.md').read_text()
rows=re.findall(r'^\| MS-(\d\d) \|',source,re.M)
assert rows==[f'{n:02d}' for n in range(1,51)],rows
passes+=1
must=(BASE/'00_三卷候选'/'纲领02_Git消息协作与定时运行_V1.3_DRAFT.md').read_text()
for phrase in ['早醒','晚醒','不因','字数','去重','上下文','未完']:
 assert phrase in must,phrase
 passes+=1
print(json.dumps({'result':'PASS_STATIC_ONLY','checks_passed':passes,'schema_positive':7,'schema_negative_required_and_version':negatives,'original_contract':'V1.2.1 unchanged semantics','source_sha_verified_when_available':source_sha_verified,'v13_runtime_implemented':False,'remote_git_or_scheduler_tested':False},ensure_ascii=False,indent=2))
