import runpy, sys, struct, re
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
dump = runpy.run_path('scripts/fm24_dump.py', run_name='d4')
codec = dump['_reader']()
raw = core['load_payload']('server', 24)
rows = np.load('scratch/t76a/_rows24.npy'); n=len(rows)
starts = rows[:,0].astype(np.int64); lens = rows[:,1].astype(np.int64)
def name(j):
    b = raw[starts[j]:starts[j]+lens[j]]
    ss = [m.group().decode('utf-8','replace') for m in re.finditer(rb'[\x20-\x7e]{5,}', b)]
    return ss
def u32(j, o): return struct.unpack_from('<I', raw, starts[j]+o)[0]
# t3 rows with names
t3 = dump['load_payload'](codec, 'client', 3)
r3 = list(dump['walk_club_block'](t3))
def n3(j):
    b = r3[j][2]
    return [m.group().decode('utf-8','replace') for m in re.finditer(rb'[\x20-\x7e]{5,}', b)]
print('== team rows with names: @59 value and the t3 row at that ordinal ==')
for j in (74281, 74322, 49928, 75852, 35180):
    v = u32(j, 59)
    print(f'row {j} name={name(j)[:2]} @59={v} -> t3[{v}]={n3(v)[:2] if v < len(r3) else "OOR"}')
print()
print('== @59 domain over ALL rows (fill check) ==')
vals = np.array([u32(j,59) for j in range(n)])
print('min', vals.min(), 'max', vals.max(), 'distinct', len(np.unique(vals)), 'in t3 range', float((vals<len(r3)).mean()))
print('86-byte rows only distinct:', len(np.unique(vals[lens==86])), 'of', int((lens==86).sum()))
