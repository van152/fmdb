import json,sys,struct
sys.path.insert(0,'scripts'); sys.stdout.reconfigure(encoding='utf-8')
import t85_common as C
def t10_counts(arch,size):
    raw=C.payload(arch,f'{arch}_db/table_10.dat',size)
    offs=C.identity_offsets(raw); starts=[14]+[o+13 for o in offs[:-1]]; lens=[o+13-s for o,s in zip(offs,starts)]
    out=[]
    for s,l in zip(starts,lens):
        b=raw[s:s+l][:-13]
        try:
            a=struct.unpack_from('<b',b,24)[0]; p=25+5*a
            nb=struct.unpack_from('<i',b,p)[0]; p+=4+28*nb
            nc=struct.unpack_from('<i',b,p)[0]; p+=4+28*nc
            nd=struct.unpack_from('<i',b,p)[0]
            out.append((a,nb,nc,nd))
        except Exception: out.append(None)
    return out
for arch,size in (('client',24732),('server',422345)):
    cnt=t10_counts(arch,size)
    rows=[json.loads(l) for l in open(f'scratch/t50/out/profiles/table_{arch}_extra_9.rows.jsonl',encoding='utf-8')]
    nit=[]
    for r in rows:
        b=bytes.fromhex(r['raw_hex']); nl=r['marker']['name_len']; t=b[8+nl:]
        nit.append(t[6] if len(t)>6 else None)
    good=[i for i in range(251) if cnt[i] and nit[i] is not None]
    for j,nm in enumerate('ABCD'):
        same=sum(1 for i in good if cnt[i][j]==nit[i])
        print(f'{arch} extra9.items vs t10.{nm}: {same}/{len(good)}')
    # also vs total
    tot=sum(n for n in nit if n)
    print(f'{arch}: sum(t10.A)={sum(cnt[i][0] for i in good)} sum(extra9.items)={tot}')
