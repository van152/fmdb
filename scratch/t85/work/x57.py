import sys,pathlib,collections
sys.path.insert(0,'scripts'); sys.stdout.reconfigure(encoding='utf-8')
import t85_common as C
codec=C.codec()
p=C.DB/'lang_update_db.dat'
ents=codec['list_tables'](p,'lang_update_db.dat')
paths=[e['path'] for e in ents]
print('sample',paths[:6])
ids=collections.Counter()
for pa in paths:
    b=pa.split('/')[-1]
    if b.endswith('.dat') and '_' in b:
        t=b[:-4].split('_')
        ids[t[0]]+=1
print('nametable-ish ids:',ids.most_common(12))
lang=[pa for pa in paths if pa.split('/')[-1].split('_')[0] not in ('8','9','10')]
print('non 8/9/10:',lang[:20], len(lang))
