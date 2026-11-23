import sys; sys.path.insert(0,'scripts')
import t74_frames_part2 as P
from t74_row_frames9 import payload, codec
c=codec(); b=payload(c,'client',7)
for pair in (True,False):
    for strict in (True,False):
        tot,bounds,nl=P._dp(b,'7',14,len(b)-8,208,13,strict_uid=strict,pair=pair)
        print('pair',pair,'strict',strict,'paths',tot,'bounds',bool(bounds))
