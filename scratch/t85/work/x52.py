import sys,struct
sys.path.insert(0,'scripts'); sys.stdout.reconfigure(encoding='utf-8')
import t85_common as C
raw=C.payload('client','client_db/table_10.dat',24732)
offs=C.identity_offsets(raw); starts=[14]+[o+13 for o in offs[:-1]]; lens=[o+13-s for o,s in zip(offs,starts)]
ok=0; rows=[]
for i,(s,l) in enumerate(zip(starts,lens)):
    b=raw[s:s+l]; body=b[:-13]
    try:
        p=25; a=struct.unpack_from('<b',body,24)[0]; p=25+5*a
        nb=struct.unpack_from('<i',body,p)[0]; p+=4+28*nb
        nc=struct.unpack_from('<i',body,p)[0]; p+=4+28*nc
        nd=struct.unpack_from('<i',body,p)[0]; p+=4+12*nd
        rows.append((a,nb,nc,nd,p,len(body)))
        if p==len(body): ok+=1
    except Exception: rows.append(None)
print('close',ok,'/251')
print('samples',rows[:5])
import collections
for j,nm in enumerate('ABCD'):
    v=[r[j] for r in rows if r]
    print(f'{nm}: min={min(v)} max={max(v)} sum={sum(v)}')
bad=[i for i,r in enumerate(rows) if not r or r[4]!=r[5]]
print('bad rows',bad[:10])
