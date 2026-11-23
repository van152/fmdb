import json,sys,collections
sys.stdout.reconfigure(encoding='utf-8')
for arch in ('client','server'):
    rows=[json.loads(l) for l in open(f'scratch/t50/out/profiles/table_{arch}_extra_9.rows.jsonl',encoding='utf-8')]
    print('==',arch)
    known={0:('Algeria','Les Fennecs'),55:('China PR','Team Dragon'),61:('Japan','Samurai Blue'),
           120:('United States','Team USA'),139:('England','The Three Lions'),145:('Germany','Die Nationalmannschaft'),
           177:('Australia','The Socceroos'),187:('Argentina','La Albiceleste'),189:('Brazil','Seleção'),
           248:('Yugoslavia','Plavi')}
    for r,exp in sorted(known.items()):
        got=rows[r]['marker']['name_ascii']
        print(f'  row{r:4d} expect={exp[1]!r:26s} got={got!r} {"OK" if got==exp[1] else "MISMATCH"}')
    # post-name dword
    v=collections.Counter()
    for r in rows:
        b=bytes.fromhex(r['raw_hex']); nl=r['marker']['name_len']
        if 12+nl<=len(b): v[int.from_bytes(b[8+nl:12+nl],'little')]+=1
    print(' post-name u32 histogram (top):',v.most_common(12))
