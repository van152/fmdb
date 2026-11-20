"""Build normalized regression fixtures for field_mapper from 14 verified entities.
Read-only on all source artifacts; writes only scratch/t02/field_mapper/fixtures.json.
Run: py -V:3.12 -I -B scripts/build_fixtures.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'scratch/t02/field_mapper/fixtures.json'


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding='utf-8'))


def first_offset(v):
    """Extract a row offset from the many field-record shapes in artifacts."""
    for k in ('row_offset', 'row_off', 'client_row_offset', 'server_row_offset'):
        if k in v and isinstance(v[k], int):
            return v[k]
    # weather: row_offset_formula "row_start + 7 + name_byte_length + 0 + 0"
    if 'row_offset_formula' in v:
        f = v['row_offset_formula']
        import re
        nums = [int(x) for x in re.findall(r'\+ (\d+)', str(f))]
        if nums:
            return sum(nums)
    # person: offsets_by_class {"1/2/3": {row_offset: 1}, "4": {...}}
    obc = v.get('offsets_by_class')
    if isinstance(obc, dict):
        for sub in obc.values():
            if isinstance(sub, dict) and isinstance(sub.get('row_offset'), int):
                return sub['row_offset']
    return None


def norm(entries):
    """Normalize a row_offset_map (dict or list) to {code: row_offset}."""
    out = {}
    if isinstance(entries, dict):
        for code, v in entries.items():
            if isinstance(v, dict):
                ro = first_offset(v)
                if ro is not None:
                    out[code] = ro
    elif isinstance(entries, list):
        for v in entries:
            if isinstance(v, dict):
                code = v.get('code') or v.get('field') or v.get('4cc')
                ro = first_offset(v)
                if code is not None and ro is not None:
                    out[code] = ro
    return out


census = load('scratch/t01/inbox/t01h/output.json')['census']
reader = {}
for it in census:
    s = (it.get('reader', {}).get('slot19_readers') or [{}])[0]
    if s.get('entry_file_offset'):
        reader[it['type_id']] = {
            'entry': s['entry_file_offset'],
            'unwrapped': s.get('unwrapped_file_offset'),
            'mode': it.get('reader', {}).get('mode'),
        }

sources = [
    ('t01f', 25, 'scratch/t01/inbox/t01f/output.json', 'row_offset_map'),
    ('t01l', 27, 'scratch/t01/inbox/t01l/output.json', 'row_offset_map'),
    ('t01m', 21, 'scratch/t01/inbox/t01m/output.json', 'row_offset_map'),
    ('t01g', 10, 'scratch/t01/inbox/t01g/output.json', 'row_offset_map'),
    ('t02p', 1, 'scratch/t02/inbox/pw/output.json', 'row_offset_map'),
    ('t02g2', 10, 'scratch/t02/inbox/nati/OUTBOX/framework.json', 'field_offsets'),
    ('t02c', 3, 'scratch/t02/inbox/club_v2/output.json', 'row_offset_map'),
]

fixtures = []
for tag, tid, rel, key in sources:
    d = load(rel)
    fields = norm(d.get(key))
    if not fields:
        continue
    fixtures.append({
        'source': tag, 'type_id': tid, 'entity': d.get('entity', ''),
        'field_count': len(fields), 'fields': fields,
        'reader': reader.get(tid),
    })

# t02 reference tables (9) with count-only semantics
for rel in sorted((ROOT / 'scratch/t02').glob('*_reference.json')):
    d = json.loads(rel.read_text(encoding='utf-8'))
    fields = norm(d.get('row_offset_map'))
    if not fields:
        continue
    fixtures.append({
        'source': rel.stem.replace('_reference', ''), 'type_id': d.get('type_id'),
        'entity': d.get('entity', ''), 'field_count': len(fields), 'fields': fields,
        'reader': reader.get(d.get('type_id')),
    })

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(fixtures, ensure_ascii=False, indent=1), encoding='utf-8')
print('wrote', OUT, 'fixtures', len(fixtures), 'total_fields', sum(f['field_count'] for f in fixtures))
for f in fixtures:
    print(' ', f['source'], 'type', f['type_id'], f['field_count'], 'fields', 'reader', f['reader'])
