import sys,struct
sys.path.insert(0,'scripts'); sys.stdout.reconfigure(encoding='utf-8')
import t85_common as C
for arch in ('client','server'):
    ents,_=C.entries(arch)
    for e in ents:
        if 'name_table' not in e['path'] or 'extra_0' not in e['path']: continue
        raw=C.payload(arch,e['path'],int(e['size']))
        print('==',arch,e['path'],len(raw),'head',raw[:14].hex(' '))
        # name blocks: [u32 ord][u32 len][bytes]
        p=14; n=0; ids=[]
        while p+8<=len(raw):
            o,l=struct.unpack_from('<II',raw,p)
            if not (l<200 and p+8+l<=len(raw)) or not all(32<=b for b in raw[p+8:p+8+l]): break
            ids.append((o,l,raw[p+8:p+8+l][:20]))
            p=p+8+l; n+=1
        print('  blocks',n,'first',ids[:6])
