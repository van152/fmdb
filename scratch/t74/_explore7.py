import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import struct, collections

raw=load('client',7)
n=208; hdr=14; end=len(raw)-8

# find trailer anchors: duni u32 repeated + 0 marker, strictly increasing
# scan candidate positions
anchors=[]
for p in range(hdr, end-9+1):
    a,b=struct.unpack_from('<II',raw,p)
    if a==b and a>0 and raw[p+8]==0:
        anchors.append((p,a))
print('candidates',len(anchors))
# greedy increasing from row start
rows=[]; pos=hdr; cur=0
for i in range(n):
    # next name len prefix
    ln=struct.unpack_from('<I',raw,pos)[0]
    cand=[(p,a) for p,a in anchors if p>=pos+4+ln and a>cur]
    if not cand: print('stuck',i,pos); break
    p,a=cand[0]
    rows.append((pos,p,a))
    cur=a; pos=p+9
print('rows',len(rows),'final pos',pos,'end',end)
lens=[r[0] for r in rows]
print('rowlen distribution sample', [ (rows[i+1][0]-rows[i][0]) if i+1<len(rows) else end-rows[i][0] for i in range(0,5)])
for i in range(3):
    s=rows[i][0]; e=(rows[i+1][0] if i+1<len(rows) else end)
    print(i,'row',s,e,e-s,'duni',rows[i][2],'rel duni',rows[i][1]-s)
print('last', rows[-1], 'rowlen', end-rows[-1][0])
