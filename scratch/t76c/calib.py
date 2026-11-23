"""t76c scratch: FK encoding calibration — do frozen FK slots hold UIDs or dense ordinals?"""
import runpy, struct, json
from pathlib import Path

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
load = core['load_payload']
D = json.loads(Path('scratch/t76c/domains_client.json').read_text())
CITY = set(D['city']['uid_set'])
STAD = set(D['stadium']['uid_set'])
REG = set(D['region']['uid_set'])
CONT = set(D['continent']['uid_set'])


def col(raw, H, S, n, off, w=4):
    return [int.from_bytes(raw[H + j * S + off:H + j * S + off + w], 'little')
            for j in range(n)]


print('=== CALIBRATION 1: stadium Scti@3 (schema: database_record_unique_id -> city)')
raw21 = load('client', 21)
v = col(raw21, 14, 38, 48413, 3)
print(f'  n={len(v)} distinct={len(set(v))} min={min(v)} max={max(v)}')
print(f'  in CITY uid set: {sum(1 for x in v if x in CITY)}/{len(v)}')
print(f'  < 56293 (city ordinal domain): {sum(1 for x in v if x < 56293)}/{len(v)}')
print(f'  sample {v[:12]}')

print('\n=== CALIBRATION 2: city Cnti@10 (schema -> continent)')
raw2 = load('client', 2)
v = col(raw2, 14, 43, 56293, 10)
print(f'  distinct={len(set(v))} min={min(v)} max={max(v)} values={sorted(set(v))[:12]}')
print(f'  in CONTINENT uid set: {sum(1 for x in v if x in CONT)}/{len(v)}')

print('\n=== CALIBRATION 3: city Clri@25 (t05: region ref)')
v = col(raw2, 14, 43, 56293, 25)
print(f'  distinct={len(set(v))} min={min(v)} max={max(v)}')
print(f'  in REGION uid set: {sum(1 for x in v if x in REG)}/{len(v)}')
print(f'  < 28: {sum(1 for x in v if x < 28)}/{len(v)}')

print('\n=== CALIBRATION 4: stadium Scti vs stadium-set (wrong control)')
v21 = col(raw21, 14, 38, 48413, 3)
print(f'  in STADIUM uid set: {sum(1 for x in v21 if x in STAD)}/{len(v21)}')

print('\n=== DERBY @4/@8 vs city ordinal-domain (dense <56293) for comparison')
print('  reference: stadium Scti<56293 rate would be the "ordinal encoding" signature')
