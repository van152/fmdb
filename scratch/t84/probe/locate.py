import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
needles=[b'China PR',b'Faroe Islands',b'Trinidad',b'Northern Ireland',b'South Korea',
         b'Albpetrol Patos',b'Premier Division',b'Champions League']
for a in ('client','server','lang_update'):
    p=lib.DB/f'{a}_db.dat'
    ents=lib.CODEC['list_tables'](p,f'{a}_db.dat')
    hits={}
    for e in ents:
        nm=e['path'].split('/')[-1]
        try: raw=lib.load_member(a,nm)
        except Exception: continue
        c={k:raw.count(k) for k in needles if raw.count(k)}
        if c: hits[nm]=c
    print('=====',a,'members with hits',len(hits))
    agg={}
    for nm,c in hits.items():
        for k,v in c.items(): agg.setdefault(k,[]).append((nm,v))
    for k in needles:
        if k in agg: print(' ',k,agg[k][:6])
