#!/usr/bin/env python3
"""Agensh-Lite V1.3 release-only static validation. NOT remote/runtime acceptance."""
from pathlib import Path
from copy import deepcopy
from jsonschema import Draft202012Validator
import json,hashlib,sys
root=Path(__file__).resolve().parents[1]
vols=sorted((root/'00_现行纲领').glob('*.md'))
assert len(vols)==3, ('three volumes required',len(vols))
for vol in vols:
    s=vol.read_text(encoding='utf-8')
    assert 'version: V1.3\n' in s and 'DESIGN_BASELINE_APPROVED_REMOTE_NOT_RUN' in s
    assert 'V1.3-RC1 候选' not in s and 'RC1_PROPOSED_NOT_EFFECTIVE' not in s
v1,v2,v3=[v.read_text(encoding='utf-8') for v in vols]
assert 'Gather' in v1 and 'Claim' in v1 and 'Git' in v1
assert '连续水位不跨 Gap' in v2 and '独立 ACK' in v2
assert 'Soft CLAIM' in v2 and 'AGL_LITE_V1_2_1' in v2
assert 'GCP/MCP' in v3 and 'REMOTE_NOT_RUN' in v3
c=root/'03_V121机器契约留存'
count=0
for kind in ('task','event','message','ack','review','delivery','run'):
    schema=json.loads((c/'schemas'/f'{kind}.schema.json').read_text(encoding='utf-8'))
    sample=json.loads((c/'examples'/f'{kind}.valid.json').read_text(encoding='utf-8'))
    Draft202012Validator.check_schema(schema)
    v=Draft202012Validator(schema)
    assert schema['properties']['schema_version']['const']=='AGL_LITE_V1_2_1'
    assert v.is_valid(sample),kind
    invalid=deepcopy(sample);invalid['schema_version']='AGL_LITE_V1_3'
    assert not v.is_valid(invalid),kind
    count+=2
# Verify complete package manifest (this script itself is included)
manifest=root/'SHA256_MANIFEST.tsv'
rows=manifest.read_text(encoding='utf-8').splitlines()
assert rows[0]=='relative_path\tsha256\tbytes'
assert len(rows)==len([p for p in root.rglob('*') if p.is_file()]), 'manifest should include all except self'
for line in rows[1:]:
    rel,digest,size=line.split('\t')
    p=root/rel
    assert p.is_file(),rel
    b=p.read_bytes()
    assert hashlib.sha256(b).hexdigest()==digest and len(b)==int(size), rel
print(f'RELEASE_STATIC_PASS: 3 volumes; {count} schema positive/version-negative checks; {len(rows)-1} file hashes; REMOTE_NOT_RUN')
