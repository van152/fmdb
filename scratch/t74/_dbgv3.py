import sys; sys.path.insert(0,'scratch/t74/out')
import verify as V
c=V.codec()
for a,t,n in (('client',7,208),('client',47,2488)):
    b=V.load(c,a,t)
    rows=V.rows_id_dp(b,14,8,n,13,8)
    print(a,t,rows is not None, len(rows) if rows else None)
