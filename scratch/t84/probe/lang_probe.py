import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
p=lib.DB/'lang_update_db.dat'
ents=lib.CODEC['list_tables'](p,'lang_update_db.dat')
print('entries',len(ents))
hits=[]
for e in ents:
    name=e['path'].split('/')[-1]
    try:
        raw=lib.load_member('lang_update',name)
    except Exception as ex:
        print('ERR',name,ex); continue
    for nd in (b'Liverpool',b'England',b'Albpetrol'):
        if nd in raw: hits.append((name,nd,raw.find(nd),len(raw)))
for h in hits: print(h)
