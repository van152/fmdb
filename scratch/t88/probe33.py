import struct,json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends']); sl=np.array(d['strlen'])
n=len(starts)
a0=np.array([struct.unpack_from('<I',b,s)[0] for s in starts],dtype=np.int64)
print('a0<=84258:',int((a0<=84258).sum()),' >84258:',int((a0>84258).sum()))
print('a0 hist small: unique',len(np.unique(a0[a0<=84258])),'min',a0[a0<=84258].min(),'max',a0[a0<=84258].max())
print('a0 big: unique',len(np.unique(a0[a0>84258])),'min',a0[a0>84258].min(),'max',a0.max())
print('big sample',sorted(np.unique(a0[a0>84258]))[:6])
# For rows with a0<=84258: is a0 == club ordinal of the row's *order*? check dup structure
sub=np.flatnonzero(a0<=84258)
print('\nfirst 30 rows: a0,strlen,rowfirst4')
for i in range(0,30):
    print(i,a0[i],sl[i])
