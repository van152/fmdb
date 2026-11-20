import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_c = core['load_payload']('client', 21)
H, n, Sc = 14, 48413, 38
mc = np.frombuffer(raw_c, dtype=np.uint8, count=H+n*Sc)[H:].reshape(n, Sc)
for j in range(6):
    r = mc[j].tobytes()
    print(j, r.hex(' '), 'lat=%.4f lon=%.4f' % (np.frombuffer(r[17:21],'<f4')[0], np.frombuffer(r[21:25],'<f4')[0]))
print()
# Scti lane: u16@3 join to t2 ordinal domain (0..56292)
v16 = mc[:,3:5].copy().view('<u2').ravel()
v32 = mc[:,3:7].copy().view('<u4').ravel()
print('u16@3 max', v16.max(), 'u32@3 max', v32.max(), 'equal?', bool((v16==v32).all()))
print('n out of t2 ordinal range:', int((v32>56292).sum()), 'n zero', int((v32==0).sum()))
print('distinct', len(np.unique(v32)))
# city UID set from t2
raw2 = core['load_payload']('client', 2)
m2 = np.frombuffer(raw2, dtype=np.uint8, count=14+56293*43)[14:].reshape(56293,43)
uid2 = m2[:,34:38].copy().view('<u4').ravel()
print('city UID sample', uid2[:6], 'min', uid2.min(), 'max', uid2.max())
uid2s = set(uid2.tolist())
print('Scti u32@3 hit city UID rate:', sum(1 for v in v32.tolist() if v in uid2s)/len(v32))
print('Scti as ordinal -> city row exists:', float((v32 < 56293).mean()))
# wrong-UID control: join stadium u32@3 against other tables' UID sets
for tid in (10,25,3,23,47):
    try:
        rr = core['load_payload']('client', tid)
    except Exception as e:
        print(tid, 'ERR', e); continue
    fr = core['resolve_frame'](rr)
    c = fr['frame']
    print('t',tid,'resolved',fr['resolved'], c and (c['stride'],c['count'],c['identity_offset']))
