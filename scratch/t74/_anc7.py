import sys; sys.path.insert(0,'scripts')
import t74_frames_part2 as P, t74_frames_part3 as S
from t74_row_frames9 import payload, codec
import json
c=codec(); out={}
for a,t in [('client',56),('client',0),('client',21)]:
    b=payload(c,a,t); r=P.fixed_rows(b,P.FIXED[(a,t)])
    out[f'{t}_{a}']=S.anchor_report(b,r['rows'],(a,t))
    if t==21: out[f'{t}_{a}geom']=S.geo_report(b,r['rows'],(a,t))
print(json.dumps(out,ensure_ascii=False,indent=1))
