#!/usr/bin/env python3
"""Offline RC1 content/schema checks only. No remote Git/Bridge/scheduler actions."""
from pathlib import Path
import json,hashlib,zipfile
from jsonschema import Draft202012Validator
root=Path(__file__).resolve().parents[1]
vols=sorted((root/'00_三卷候选').glob('*.md'))
assert len(vols)==3
assert all('version: V1.3-RC1' in p.read_text() and 'RC1_PROPOSED_NOT_EFFECTIVE' in p.read_text() for p in vols)
for p in vols: assert p.stat().st_size>4000
v1,v2,v3=[p.read_text() for p in vols]
for phrase in ['两条执行通道','微软','V1.2.1']:
    assert phrase in v1,phrase
for phrase in ['机器契约的唯一生效表','独立 ACK','连续水位不跨 Gap','Soft CLAIM','GCP Bridge','UNKNOWN','AGL_LITE_V1_2_1','GET /health','POST /v1/execute']:
    assert phrase in v2,phrase
for phrase in ['P1-01','P1-02','P1-03','P1-04','EX-01','EX-02','EX-03','REMOTE_NOT_RUN']:
    assert phrase in v3,phrase
z=root/'03_V121机器契约留存'
schemas={}
for name in ['task','event','message','ack','review','delivery','run']:
    schema=json.loads((z/'schemas'/f'{name}.schema.json').read_text())
    sample=json.loads((z/'examples'/f'{name}.valid.json').read_text())
    assert schema['properties']['schema_version']['const']=='AGL_LITE_V1_2_1'
    Draft202012Validator.check_schema(schema)
    vd=Draft202012Validator(schema)
    assert vd.is_valid(sample)
    wrong=dict(sample,schema_version='AGL_LITE_V1_3')
    assert not vd.is_valid(wrong)
    schemas[name]=schema
# preserve exact historic bytes vs original V1.3 ZIP
original=Path('/mnt/data/AGL_LITE_V1.3_微软源码对齐_宽容回合制_三卷重构候选包_20261028.zip')
if original.exists():
    with zipfile.ZipFile(original) as f:
        for rel in sorted(x.relative_to(z) for x in z.rglob('*') if x.is_file()):
            matches=[n for n in f.namelist() if n.endswith('/03_V121机器契约留存/'+rel.as_posix())]
            assert len(matches)==1,rel
            assert f.read(matches[0])==(z/rel).read_bytes(),rel
print(json.dumps({'result':'PASS_STATIC_ONLY','rc1_volumes':3,'old_schema_examples_valid':7,'wrong_schema_version_rejected':7,'p1_points_documented':4,'original_schema_files_byte_identical_when_zip_available':original.exists(),'remote_multiactor_git_tested':False,'gcp_bridge_tested':False,'scheduled_chatgpt_tested':False},ensure_ascii=False,indent=2))
