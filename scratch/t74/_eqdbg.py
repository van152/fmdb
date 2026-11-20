import sys
sys.path.insert(0,'scripts')
import t74_frames_part2 as P
from t74_row_frames9 import payload, codec
c=codec(); b=payload(c,'client',56); n=6
res={}
for W,fo in ((12,9),(13,8),(14,7)):
    cnt,starts,_=P._dp(b,'x',14,len(b)-fo,n,W)
    res[f'{W}/{fo}']=(cnt,starts)
    print(W,fo,'cnt',cnt,'starts',starts)
a=res['12/9'][1]; bb=res['13/8'][1]; cc=res['14/7'][1]
print('12==13',a==bb,'13==14',bb==cc)
