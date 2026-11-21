import json,sys
sys.stdout.reconfigure(encoding='utf-8')
rows=[json.loads(l) for l in open('scratch/t50/out/profiles/table_server_extra_9.rows.jsonl',encoding='utf-8')]
t9=[json.loads(l) for l in open('scratch/t50/out/profiles/table_server_9.rows.jsonl',encoding='utf-8')]
d=json.loads(open('reports/t22_nation_capital.json',encoding='utf-8').read())
anchors={}
for grp in ('holdouts','cross_nation'):
    for a in d[grp]: anchors[a['nation_row']]=a['nation_name']
anchors[139]='England(L2)'; anchors[55]='China PR(L2)'
for r in sorted(anchors):
    m=rows[r]['marker']
    print(f'row{r:4d} {anchors[r]:26s} block_nick={m["name_ascii"]!r:32s} t9_row_id={t9[r]["identity"]["row_id"]}')
print()
alln=[(r['marker']['ordinal'],r['marker']['name_ascii']) for r in rows]
print('uniqueness of ordinals:',len(set(o for o,_ in alln))==251)
