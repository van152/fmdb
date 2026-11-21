import sys,struct,json
sys.path.insert(0,'scripts'); sys.stdout.reconfigure(encoding='utf-8')
import t85_common as C
raw=C.payload('client','client_db/table_10.dat',24732)
offs=C.identity_offsets(raw); starts=[14]+[o+13 for o in offs[:-1]]; lens=[o+13-s for o,s in zip(offs,starts)]
cnt={k:[] for k in 'ABCD'}; bad=[]
for i,(s,l) in enumerate(zip(starts,lens)):
    b=raw[s:s+l][:-13]
    try:
        a=struct.unpack_from('<b',b,24)[0]; p=25+5*a
        nb=struct.unpack_from('<i',b,p)[0]; p+=4+28*nb
        nc=struct.unpack_from('<i',b,p)[0]; p+=4+28*nc
        nd=struct.unpack_from('<i',b,p)[0]
        for k,v in zip('ABCD',(a,nb,nc,nd)): cnt[k].append(v)
    except Exception as ex:
        bad.append((i,l,str(ex))); 
        for k in 'ABCD': cnt[k].append(None)
print('bad rows',bad[:6],'n',len(bad))
rows=[json.loads(l) for l in open('scratch/t50/out/profiles/table_client_extra_9.rows.jsonl',encoding='utf-8')]
pat=bytes.fromhex('ffffffffffffffff'); nff=[]
for r in rows:
    b=bytes.fromhex(r['raw_hex']); nl=r['marker']['name_len']; t=b[8+nl:]
    c=0;p=t.find(pat)
    while p>=0: c+=1;p=t.find(pat,p+1)
    nff.append(c)
for k in 'ABCD':
    same=sum(1 for i in range(251) if cnt[k][i]==nff[i])
    print(f'  extra9-items vs t10.{k}: {same}/251')
print('sums',{k:sum(v for v in cnt[k] if v) for k in 'ABCD'},'extra9',sum(nff))
