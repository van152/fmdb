import runpy, sys, struct
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw = core['load_payload']('server', 24)
rows = np.load('scratch/t76a/_rows24.npy'); n = len(rows)
starts = rows[:,0].astype(np.int64); lens = rows[:,1].astype(np.int64)
A = np.frombuffer(raw, np.uint8)
def c32(o):
    return (A[starts+o].astype(np.uint64) | (A[starts+o+1].astype(np.uint64)<<8)
            | (A[starts+o+2].astype(np.uint64)<<16) | (A[starts+o+3].astype(np.uint64)<<24))
v24 = c32(24)
u,c = np.unique(v24, return_counts=True)
print('@24: d=', len(u), 'min', int(u.min()), 'max', int(u.max()), 'zero', int((v24==0).sum()), 'ff', int((v24==0xffffffff).sum()))
print('sample', u[:10].tolist())
print('uids24 sample', np.load('scratch/t76a/_uids24.npy')[:5].tolist())
# compare to identity uid
uid = np.load('scratch/t76a/_uids24.npy').astype(np.uint64)
print('@24 == own uid:', int((v24==uid).sum()), '/', n)
print('@24 low bits: all multiple of 256?', bool((v24 % 256 == 0).all()))
print()
# t3 uids correct read: identity is 9 bytes at end (duni,duni,marker)? check
dump = runpy.run_path('scripts/fm24_dump.py', run_name='d2')
codec = dump['_reader']()
t3 = dump['load_payload'](codec, 'client', 3)
r3 = list(dump['walk_club_block'](t3))
for j in (0,1):
    b = r3[j][2]
    print('t3 row', j, 'len', len(b), 'last 12:', b[-12:].hex(' '))
    print('   u32@-9', struct.unpack_from('<I', b, len(b)-9)[0], 'u32@-5', struct.unpack_from('<I', b, len(b)-5)[0])
