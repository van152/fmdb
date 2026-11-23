import struct,json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends']); sl=np.array(d['strlen'])
club=np.array(sorted(json.load(open('scratch/t88/club.json'))['uids']),dtype=np.int64)
a0=np.array([struct.unpack_from('<I',b,s)[0] for s in starts],dtype=np.int64)
print('monotone nondecreasing?',bool((np.diff(a0)>=0).all()))
inn=np.isin(a0,club)
print('in club',inn.mean(),'bad',(~inn).sum())
bad=a0[~inn]
print('bad sample',sorted(set(bad.tolist()))[:12],'max small',bad[bad<10**6].max() if (bad<10**6).any() else None)
print('\nrows 0..5 bytes 0..20:')
for i in range(6):
    s=starts[i]
    print(i,'club?',a0[i],'strlen',sl[i],'bytes',b[s:s+21].hex(' '))
print('\nrows with bad club id: first 5')
for i in np.flatnonzero(~inn)[:5]:
    s=starts[i]
    print(i,a0[i],sl[i],b[s:s+21].hex(' '),'end',b[ends[i]-13:ends[i]].hex(' '))
