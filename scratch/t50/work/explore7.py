import os,pathlib,runpy,struct,sys
from collections import Counter
ROOT=pathlib.Path(r'D:\tmp2b\fm24-db'); sys.path.append(r'D:\tmp2b\fm24\tools\python')
import zstandard as z
codec=runpy.run_path(r'D:\tmp2b\fm24\scripts\modding_read_dbdat.py')
DB=pathlib.Path(os.environ.get('FM24_DB_DIR') or ROOT/'scratch/data')
P={}
for side in ('client','server'):
    db=(DB/f'{side}_db.dat').read_bytes(); lay=codec['_archive_layout'](db); base=lay['data_base']
    es={(x['path'].split('/')[-1]):x for x in lay['entries']}
    for name in ('table_9.dat','table_extra_9.dat'):
        e=es[name]; P[side,name]=z.ZstdDecompressor().decompressobj().decompress(db[base+e['offset']:base+e['offset']+e['packed_size']])
def cands(b,i,lo=13,exclude0=True):
    out=[]; needle=struct.pack('<I',i); p=b.find(needle,lo)
    while p>=0:
        if p+13<=len(b):
            c,d=struct.unpack_from('<II',b,p+4)
            if c==d and b[p+12]==0 and (c!=0 or not exclude0): out.append((p,c))
        p=b.find(needle,p+1)
    return out
R={}
for side in ('client','server'):
    b=P[side,'table_9.dat']; n=struct.unpack_from('<I',b,8)[0]; end=len(b)-8; pos=13; rows=[]
    for i in range(n):
        cl=[x for x in cands(b,i,pos) if x[0]+13<=end]
        r=cl[0]; rows.append(dict(ord=i,tail=r[0],id=r[1],span=r[0]+13-pos,amb=len(cl))); pos=r[0]+13
    R[side]=rows
c,s=R['client'],R['server']
for i in range(251):
    if c[i]['id']!=s[i]['id']:
        print('first id diff at row',i,'client',c[i]['id'],'server',s[i]['id']); break
diffs=[(i,c[i]['id'],s[i]['id']) for i in range(251) if c[i]['id']!=s[i]['id']]
print('id diffs count',len(diffs),diffs[:5])
print('client span hist head',Counter(r['span'] for r in c).most_common(6))
print('server span hist head',Counter(r['span'] for r in s).most_common(6))
print('sum spans client',sum(r['span'] for r in c),'server',sum(r['span'] for r in s))
# ambiguity stats
print('client amb>1 rows',[(r['ord'],r['amb'],r['span']) for r in c if r['amb']>1][:10])
print('server amb>1 rows count',sum(1 for r in s if r['amb']>1),[ (r['ord'],r['amb'],r['span']) for r in s if r['amb']>1][:10])
# raw hex of client rows 0..2 and server rows 0..2
for side,rows in (('client',c),('server',s)):
    b=P[side,'table_9.dat']
    for k in (0,1,250):
        r=rows[k]; start=13+sum(x['span'] for x in rows[:k])
        print(side,'row',k,'start',start,'span',r['span'],'hex',b[start:start+r['span']].hex()[:400])
