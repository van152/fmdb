import struct,json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends']); sl=np.array(d['strlen'])
club=np.array(sorted(json.load(open('scratch/t88/club.json'))['uids']),dtype=np.int64)
a0=np.array([struct.unpack_from('<I',b,s)[0] for s in starts],dtype=np.int64)
u,c=np.unique(a0,return_counts=True)
print('distinct a0',len(u),'rows',len(a0))
print('first 12 distinct',u[:12].tolist(),c[:12].tolist())
# contiguity: does a0 change into blocks?
chg=np.flatnonzero(np.diff(a0)!=0)
print('contiguous blocks',len(chg)+1)
inn=np.isin(a0,club)
print('rows in club',int(inn.sum()),'not',int((~inn).sum()))
print('not-in-club distinct values',len(np.unique(a0[~inn])),'range',a0[~inn].min(),a0[~inn].max())
print('sample not-in-club',np.unique(a0[~inn])[:15].tolist())
# are they < 84259 ?
print('frac <84259 among not-in-club',float((a0[~inn]<84259).mean()))
# contiguity in club-group terms
print('\nfirst 20 a0:',a0[:20].tolist())
print('rows 38960..38975 a0:',a0[38960:38976].tolist())
