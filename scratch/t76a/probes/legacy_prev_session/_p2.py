import runpy, sys, json
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
for tid in (2,5,10,21,25,3,47,23):
    try:
        raw = core['load_payload']('server', tid)
    except Exception as e:
        print(tid,'ERR',type(e).__name__,e); continue
    fr = core['resolve_frame'](raw)
    c = fr['frame']
    print(f"t{tid} len={len(raw)} arith={fr['arith_candidates']} closed={fr['closed_candidates']} resolved={fr['resolved']} amb={fr['ambiguous']}",
          {k:c[k] for k in ('header','footer','stride','count','identity_offset','mode')} if c else None)
    for r in fr['runners_up'][:3]: print('   ru',r)
