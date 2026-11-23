import runpy, sys, struct
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw = core['load_payload']('server', 24)
rows = np.load('scratch/t76a/_rows24.npy')
n = len(rows)
starts = rows[:,0]; lens = rows[:,1]
print('rows', n, 'end', starts[-1]+lens[-1], 'footer', len(raw)-(starts[-1]+lens[-1]))
# identity check
ordok = all(struct.unpack_from('<I', raw, int(s+l-13))[0]==j for j,(s,l) in enumerate(rows))
print('ordinal ok', ordok)
sel = np.array([raw[int(s+l-1)] for s,l in rows])
print('selector hist', dict(zip(*[x.tolist() for x in np.unique(sel, return_counts=True)])))
uid = np.array([struct.unpack_from('<I', raw, int(s+l-9))[0] for s,l in rows])
print('uid uniq', len(np.unique(uid)), 'min', uid.min(), 'max', uid.max())
np.save('scratch/t76a/_uids24.npy', uid)
# reference tables: get UID sets
def uidset(arch, tid, stride, idoff, cnt=None):
    r = core['load_payload'](arch, tid)
    c = cnt or struct.unpack_from('<I', r, 8)[0]
    return np.array([struct.unpack_from('<I', r, 14 + j*stride + idoff)[0] for j in range(c)])
refs = {}
refs['t21'] = uidset('client', 21, 38, 29)
refs['t2']  = uidset('client', 2, 43, 34)
refs['t23'] = uidset('server', 23, 14, 5)
print({k:(len(v), int(v.min()), int(v.max())) for k,v in refs.items()})
np.save('scratch/t76a/_uids21.npy', refs['t21']); np.save('scratch/t76a/_uids2.npy', refs['t2'])
