#!/usr/bin/env python3
"""Zero-network structural smoke check. Never confuses schema-shape validation with real runtime tests."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
checks=[('task','example_task'),('event','example_event'),('note','example_note'),('receipt','example_receipt')]
for schema_name,example_name in checks:
    schema=json.loads((root/'schemas'/f'{schema_name}.schema.json').read_text(encoding='utf8'))
    item=json.loads((root/'examples'/f'{example_name}.json').read_text(encoding='utf8'))
    missing=set(schema['required'])-set(item)
    extra=set(item)-set(schema['properties'])
    assert not missing and not extra,(schema_name,sorted(missing),sorted(extra))
    for key,desc in schema['properties'].items():
        if key not in item: continue
        val=item[key]
        if 'enum' in desc: assert val in desc['enum'],(schema_name,key)
        types=desc.get('type',[])
        if isinstance(types,str): types=[types]
        if val is None: assert 'null' in types,(schema_name,key)
        elif isinstance(val,bool): assert 'boolean' in types,(schema_name,key)
        elif isinstance(val,int): assert 'integer' in types or 'number' in types,(schema_name,key)
        elif isinstance(val,str): assert 'string' in types,(schema_name,key)
        elif isinstance(val,list): assert 'array' in types,(schema_name,key)
    print('SCHEMA_SHAPE_PASS',schema_name,example_name)
print('NOTE: only checks example structure; not actual GitHub write/readback, leases, QA, or tools.')
