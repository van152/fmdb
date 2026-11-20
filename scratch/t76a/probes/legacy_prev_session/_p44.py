import runpy, sys, struct, re
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
dump = runpy.run_path('scripts/fm24_dump.py', run_name='d3')
codec = dump['_reader']()
t3 = dump['load_payload'](codec, 'client', 3)
r3 = list(dump['walk_club_block'](t3))
def names(j):
    b = r3[j][2]
    return [m.group().decode('utf-8','replace') for m in re.finditer(rb'[\x20-\x7e]{4,}', b)]
raw_s = core['load_payload']('server', 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
own = np.ascontiguousarray(ms[:,16:20]).view('<u4').ravel().astype(np.int64)
print('t3 rows', len(r3))
for name, row in (('Old Trafford', 71), ('Anfield', 67), ('Emirates', 7718), ('Villa Park', 3),
                  ('Stamford Bridge', 27), ('Etihad', 7716), ('Camp Nou', 414), ('Bernabeu', 430),
                  ('Allianz Arena', 12048), ('Signal Iduna', 642), ('San Siro', 563), ('Celtic Park', 1191)):
    o = int(own[row])
    if o == 0xffffffff:
        print(f'{name:16s} row {row:6d} owner=null'); continue
    print(f'{name:16s} row {row:6d} owner ordinal {o:6d} -> t3 row names {names(o)[:3]}')
