import sys, struct, json
sys.path.insert(0,r'D:\tmp2b\fm24-db\scripts'); sys.dont_write_bytecode=True
import t133_fm24_reader_v2 as t133, t112_fm24_reader as base, numpy as np
exec(open('scratch/t142/out/proto2.py').read().split('for tid in')[0])
nat_o,nat_u=ids(('server',10))
cl = base.Archive('server').payload(3)
s=specs[('server',3)]
r=base.TableReader(s,l3); 
# decode CLUB rows fully using sample_walk to get named fields
fasts={k:t133.compile_walk(v) for k,v in t133.SELECTORS[('server',3)].items()}
names=None
p=base.HEADER_END; n=struct.unpack_from('<I',cl,8)[0]
vals={}
for i in range(n):
    f=cl[p]; body=p+1; q=fasts[f](cl,body,len(cl)-9)
    fields,_=t133.sample_walk(t133.SELECTORS[('server',3)][f],cl,body,q)
    if names is None:
        names,_ls = t133.bind_sample(fields, t133.load(t133.TRACE)['tables'][ [t['archive']+str(t['table_id']) for t in []] ] if False else [x for x in t133.load(t133.TRACE)['tables'] if x['archive']=='server' and x['table_id']==3][0], l3, ('server',3))
    for path,off,w,kind,val in fields:
        nm=names.get(path,'?')
        if kind=='u' and w in (1,2,4):
            vals.setdefault(nm,[]).append(val)
    p=q
for nm,arr in vals.items():
    a=np.array(arr,dtype=np.int64)
    if a.size!=n: 
        print(nm,'partial',a.size); continue
    u=np.unique(a)
    ho=np.isin(a,nat_o).mean(); hu=np.isin(a,nat_u).mean()
    print(f'{nm:12} min={a.min():>12} max={a.max():>12} distinct={len(u):>6} hit_nation_ord={ho:.3f} hit_nation_uid={hu:.3f}')
