import sys, struct, collections
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
p=lib.DB/'lang_update_db.dat'
ents=lib.CODEC['list_tables'](p,'lang_update_db.dat')
names=[e['path'].split('/')[-1] for e in ents]
langs=collections.defaultdict(dict)
for nm in names:
    stem=nm[:-4]
    if stem.endswith('person_names'):
        langs[stem[:-12]][ 'person_names']=nm; continue
    l,t=stem.split('_')
    langs[l][t]=nm
print('languages',len(langs))
for l in sorted(langs, key=lambda x:int(x)):
    print(f'  lang {l:>9s}: {len(langs[l])} members')
print('\nfirst lang keys', list(langs)[:5])
print('table types', sorted(langs['8']))
