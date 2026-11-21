import json,sys
sys.path.insert(0,'scripts'); sys.stdout.reconfigure(encoding='utf-8')
import t85_common as C
# t47 owner-fixup: container[0xb9] == nation index. Look for a byte self-index in
# any member whose row framing has 251 rows (t9/t10/extra_9) OR per-nation blocks.
cands=[('client','table_9',31956),('server','table_9',307564),
       ('client','table_10',24732),('server','table_10',422345)]
for arch,nm,size in cands:
    raw=C.payload(arch,f'{arch}_db/{nm}.dat',size)
    offs=C.identity_offsets(raw); starts=[14]+[o+13 for o in offs[:-1]]; lens=[o+13-s for o,s in zip(offs,starts)]
    best=[]
    for off in range(0,400):
        ok=tot=0
        for i,(s,l) in enumerate(zip(starts,lens)):
            b=raw[s:s+l]
            if off<len(b):
                tot+=1; ok+= (b[off]==(i&0xff))
        if tot>240: best.append((ok,tot,off))
    best.sort(reverse=True)
    print(f'{arch} {nm}: hdr={raw[:14].hex(" ")} top byte self-index @off: {best[:4]}')
