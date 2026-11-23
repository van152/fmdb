import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
p=lib.DB/'lang_update_db.dat'
ents=lib.CODEC['list_tables'](p,'lang_update_db.dat')
by={e['path'].split('/')[-1]:e['size'] for e in ents}
for k in sorted(by):
    if k.startswith('8_') or k.startswith('8person'):
        print(k, by[k])
