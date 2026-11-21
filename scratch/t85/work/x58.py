import sys,pathlib,collections
sys.path.insert(0,'scripts'); sys.stdout.reconfigure(encoding='utf-8')
import t85_common as C
codec=C.codec()
p=C.DB/'lang_update_db.dat'
ents=codec['list_tables'](p,'lang_update_db.dat')
pref=collections.Counter(e['path'].split('/')[-1].split('_')[0].replace('person_names','PN') for e in ents)
print(pref)
for e in ents:
    if e['path'].endswith('/10_10.dat') or e['path'].endswith('/9_10.dat'):
        print(e['path'],e['size'],e['packed_size'])
