import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
targets=[b'England',b'Norway',b'Denmark',b'Iceland',b'Brazil',b'Wales',b'Serie A',b'La Liga',b'Premier Division',b'Liverpool']
for a in ('client','server','lang_update'):
    p=lib.DB/f'{a}_db.dat'
    ents=lib.CODEC['list_tables'](p,f'{a}_db.dat')
    print('=====',a)
    for e in ents:
        mn=e['path'].split('/')[-1]
        try: raw=lib.load_member(a,mn)
        except Exception: continue
        h={}
        for t in targets:
            if raw.count(struct.pack('<I',len(t))+t): h[t.decode('utf-8','replace')]=1
        if h: print(f'  {mn:24s} LP {sorted(h)}')
