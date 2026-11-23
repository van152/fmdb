import sys; sys.path.insert(0,'scripts')
import t74_frames_part2 as P
from t74_row_frames9 import payload, codec
import struct
c=codec(); b=payload(c,'client',47)
print('payload',len(b))
print('bytes 0..40',b[:40].hex(' '))
for H in (14,25):
    rows=[];p=H;F=len(b)-8;ok=True
    while p<F:
        L=None
        for cand in range(41,77,5):
            if p+cand<=F and P._ident_at(b,p+cand-13,len(rows)):
                L=cand;break
        if L is None: ok=False;break
        rows.append((p,p+L));p+=L
    print('H',H,'rows',len(rows),'closed',p==F and ok, 'allmod5', all((e-s-41)%5==0 for s,e in rows))
