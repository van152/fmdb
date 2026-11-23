import sys; sys.path.insert(0,'scratch/t74/out')
import verify as V
c=V.codec()
for a,t,n in (('client',7,208),('client',47,2488)):
    b=V.load(c,a,t); hi=len(b)-8
    cand=V.scan(b,14,hi,n,13)
    print(a,t,'ords',len(cand),'missing',[i for i in range(n) if i not in cand][:5])
    pos=V.solo_path(b,14,hi,n,13)
    print('  solo',bool(pos))
