import struct, json, pathlib, runpy, collections
ROOT=pathlib.Path(r"D:\tmp2b\fm24-db")
NY=runpy.run_path(str(ROOT/"scripts/fm24_dump.py")); codec=NY["_reader"]()
master={x['table_type']:x for x in json.load(open(ROOT/'scratch/t110/out/master_67tables_l3.json'))['tables']}
fixed=json.load(open(ROOT/'scratch/t112/discover.json'))

def grid(tid, archive, rowlen_free):
    x=master.get(tid)
    if not x: return None
    ents=[e for e in x['joined_l3_fourccs'] if e.get('archive')==archive]
    cand=[]
    for e in ents:
        off=e['wire_off_row0']+(e.get('in_slot_off') or 0)
        wl=e['wire_len'] or 1
        w=wl-(e.get('in_slot_off') or 0)
        if w<=0: continue
        cand.append((off,w,e['fourcc'],e.get('access_kind')))
    cand.sort(key=lambda r:(r[0], -r[1]))
    taken=[]; aliases=[]
    for off,w,fc,ak in cand:
        if off<0 or off+w>rowlen_free: aliases.append((fc,off,w,'out_of_row')); continue
        if any(not(off+w<=a or off>=a+b) for a,b,_ in taken): aliases.append((fc,off,w,'overlap')); continue
        taken.append((off,w,fc))
    taken.sort()
    return taken, aliases

for key,v in fixed.items():
    if v.get('model')!='fixed': continue
    a,t=key.split('/'); t=int(t)
    r=grid(t,a,v['stride']-13)
    if r is None: print(key,'NO_MASTER'); continue
    taken,al=r
    print(f"{key:12s} st={v['stride']:<4d} named={len(taken):2d} aliases={len(al):2d} cov={sum(w for _,w,_ in taken)}/{v['stride']-13}")
