import sys; sys.path.insert(0,'scripts')
import t74_frames_part2 as P
from t74_row_frames9 import payload, codec
c=codec(); b=payload(c,'client',47)
for H in (14,25):
    cnt,starts,_=P._dp(b,'h',H,len(b)-8,2488,13)
    hi=len(b)-8
    rows=list(zip(starts,starts[1:]+[hi])) if starts else []
    ordok=sum(1 for i,(s,e) in enumerate(rows) if P.struct_u32(b,e-13)==i)
    print(f'H={H} DP={cnt} rows={len(rows)} ord==idx {ordok}/{len(rows)} '
          f'lenset={sorted({e-s for s,e in rows})} first3={rows[:3]}')
