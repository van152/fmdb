import runpy, sys, struct
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
dump = runpy.run_path('scripts/fm24_dump.py', run_name='t76a_dump')
codec = dump['_reader']()
t3 = dump['load_payload'](codec, 'client', 3)
specs = dump['fixed_specs']()
print('t3 len', len(t3))
rows = list(dump['walk_club_block'](t3))
print('t3 rows', len(rows), 'first', rows[0][1], rows[0][2].hex(' ')[:60])
u3 = np.array([struct.unpack_from('<I', r[2], len(r[2])-9)[0] for r in rows])
print('t3 uids', len(set(u3.tolist())), u3[:5], u3.max())
np.save('scratch/t76a/_uids3.npy', u3)
# t25 comp server 13+1533950+9 ; count 7047
t25 = core['load_payload']('server', 25)
print('t25 len', len(t25), 'count hdr', struct.unpack_from('<I', t25, 8)[0])
