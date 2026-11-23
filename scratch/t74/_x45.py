import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import struct, collections

raw=load('client',27)
H,F=14,len(raw)-8
p=H; rows=[]
while p<F:
    L=struct.unpack_from('<I',raw,p)[0]
    s=p; e=s+4+L+95+13
    rows.append((s,e,L))
    p=e
print('rows',len(rows),'end',p,F)
for i in range(4):
    s,e,L=rows[i]
    last13=raw[e-13:e]
    o,u1,u2=struct.unpack_from('<III',raw,e-13)
    print(f'row{i} [{s},{e}) len={e-s} L={L} last13={last13.hex()} ord={o} uid={u1}/{u2} mk={last13[12]}')
# verify ord==i and uid pair equal and marker 0 for all
bad=[]
for i,(s,e,L) in enumerate(rows):
    o,u1,u2=struct.unpack_from('<III',raw,e-13)
    if not(o==i and u1==u2 and raw[e-1]==0): bad.append((i,L,o,u1,u2,raw[e-1]))
print('bad',len(bad),bad[:5])
print('L dist', collections.Counter(L for _,_,L in rows).most_common(8))
