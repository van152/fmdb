import sys; sys.path.insert(0,'scripts')
import t74_frames_part2 as P
from t74_row_frames9 import payload, codec
c=codec()
for t in (56,0,8,27,18,7,47,21):
    b=payload(c,'client',t)
    print(f't{t:<3} count@8={P.struct_u32(b,8):<7} bytes0..24={b[:24].hex(" ")}')
print()
b=payload(c,'client',47)
for H in (14,25):
    cnt,st,ly=P._dp(b,'h',H,len(b)-8,2488,13)
    print(f't47 H={H} DP路径数={cnt}')
