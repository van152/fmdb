#!/usr/bin/env python3
"""Independent structural and source-regression verifier for t110 outputs."""
import json, runpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
ns=runpy.run_path(str(ROOT/'scripts/t110_master_l3_schema.py'))
m=json.loads((OUT/'master_67tables_l3.json').read_text(encoding='utf-8'))
c=json.loads((OUT/'coverage_milestone.json').read_text(encoding='utf-8'))
assert m['status']=='complete' and len(m['tables'])==67
assert (OUT/'master_67tables_l3.json').stat().st_size < 15*1024*1024
assert all(x['in_slot_off'] == x['mem_off']-x['obj_off'] and 0 <= x['in_slot_off'] < x['wire_len'] for t in m['tables'] for x in t['joined_l3_fourccs'])
rebuilt, coverage=ns['build']()
assert m['summary']==rebuilt['summary'], 'recomputed summary differs from ledger'
assert c==coverage, 'coverage does not agree with source recomputation'
print('verify PASS: 67 tables, range bounds valid, source join and regression independently recomputed')
