import sys; sys.path.insert(0,'scripts')
from t74_row_frames9 import payload, codec, lstr
import t74_frames_part3 as S
c=codec(); b=payload(c,'client',8); F=len(b)-8
p=14; suf=[]
while p<F:
    q,n,_=lstr(b,p,F); suf.append((len(suf), q)); p=q+30
print('t8 suffix anchor (suffix start + 17 == ordinal):', S.suffix_anchor_report(b,suf,('client',8)))
