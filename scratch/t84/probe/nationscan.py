import sys, struct, re
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
nats=[b'England',b'Brazil',b'Wales',b'Norway',b'Denmark',b'Iceland',b'Ghana',b'Qatar']
comps=[b'Premier Division',b'Serie A',b'La Liga',b'Bundesliga',b'FA Cup']
for a in ('client','server','lang_update'):
    p=lib.DB/f'{a}_db.dat'
    ents=lib.CODEC['list_tables'](p,f'{a}_db.dat')
    for label,ns in (('NAT',nats),('COMP',comps)):
        found={}
        for e in ents:
            nm=e['path'].split('/')[-1]
            try: raw=lib.load_member(a,nm)
            except Exception: continue
            for n in ns:
                for m in re.finditer(re.escape(n)+rb'(?![A-Za-z])', raw):
                    found.setdefault(n,[]).append(nm)
        if found: print(a,label,{k.decode():sorted(set(v))[:4] for k,v in found.items()})
