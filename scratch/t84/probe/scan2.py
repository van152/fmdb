import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
needles=[b'Serie A',b'La Liga',b'Bundesliga',b'Premier League',b'Premier Division',
         b'England',b'China PR',b'UEFA Champions League',b'FA Cup',b'Liverpool',b'Everton']
wide={nb: nb.decode().encode('utf-16-le') for nb in needles}
for a in ('client','server','lang_update'):
    p=lib.DB/f'{a}_db.dat'
    ents=lib.CODEC['list_tables'](p,f'{a}_db.dat')
    print('=====',a,len(ents))
    for e in ents:
        nm=e['path'].split('/')[-1]
        try: raw=lib.load_member(a,nm)
        except Exception as ex: continue
        u8={k:raw.count(k) for k in needles if raw.count(k)}
        u16={k:raw.count(v) for k,v in wide.items() if raw.count(v)}
        if u8 or u16: print(f'  {nm:26s} len={len(raw):9d} u8={u8} u16={u16}')
