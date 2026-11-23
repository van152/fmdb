import sys, struct, collections
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

# 1. lang_update member set: is there ANY nation (type 10) member?
p=lib.DB/'lang_update_db.dat'
ents=lib.CODEC['list_tables'](p,'lang_update_db.dat')
types=collections.Counter()
for e in ents:
    stem=e['path'].split('/')[-1][:-4]
    if stem.endswith('person_names'): types['person_names']+=1; continue
    l,t=stem.split('_'); types[t]+=1
print('lang_update table types present:', dict(sorted(types.items(), key=lambda kv:(len(kv[0]),kv[0]))))
print('has type 10 (nation)?', '10' in types)

# 2. how many clubs carry an inline length-prefixed name (Cnam) at body+25/29 pattern
raw3=K['load_payload'](lib.CODEC,'client','3')
rows=list(K['walk_club_block'](raw3))
ok=0; bad=[]
for i,off,body in rows[:3000]:
    L=struct.unpack_from('<I',body,25)[0]
    if 1<=L<=120 and 25+4+L<=len(body):
        try:
            s=body[29:29+L].decode('utf-8')
            if any(c.isalpha() for c in s): ok+=1; continue
        except Exception: pass
    bad.append((i,body[:40].hex(' ')))
print(f'club inline Cnam decode at body+29: {ok}/3000 ok; first bad {bad[:2]}')
