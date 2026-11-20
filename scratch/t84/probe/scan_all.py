import sys, struct, re, collections
sys.path.insert(0,'scratch/t84/probe')
import lib
needles={b'Premier Division':'comp:EnglandPremier', b'Albpetrol Patos':'club:Albpetrol',
         b'Liverpool':'club:Liverpool', b'Klubi i Futbollit':'club:prefix'}
for a in ('client','server'):
    p=lib.DB/f'{a}_db.dat'
    ents=lib.CODEC['list_tables'](p,f'{a}_db.dat')
    print('=====',a,len(ents))
    for e in ents:
        name=e['path'].split('/')[-1]
        try: raw=lib.load_member(a,name)
        except Exception as ex:
            print('  ERR',name,ex); continue
        got={k:raw.count(k) for k in needles if raw.count(k)}
        if got: print(f'  {name:32s} len={len(raw):9d} {got}')
