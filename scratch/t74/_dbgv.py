import sys; sys.path.insert(0,'scratch/t74/out')
import verify as V
c=V.codec()
for a,t,n in (('client',7,208),('client',24,84507)):
    b=V.load(c,a,t); F=8
    cand=V.scan(b,14,len(b)-F,n,13)
    missing=[i for i in range(n) if i not in cand]
    print(a,t,'cand ords',len(cand),'missing',len(missing),missing[:5])
    pos=V.solo_path(b,14,len(b)-F,n,13)
    print('  solo_path',bool(pos), 'last',pos[-1] if pos else None,'need',len(b)-F-13)
