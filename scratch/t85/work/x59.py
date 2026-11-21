import sys
sys.path.insert(0,'scripts'); sys.stdout.reconfigure(encoding='utf-8')
import t85_common as C
codec=C.codec(); p=C.DB/'lang_update_db.dat'
ents=codec['list_tables'](p,'lang_update_db.dat')
print([e['path'] for e in ents if '_10' in e['path']][:20])
print([e['path'] for e in ents if e['path'].endswith('_10.dat')])
