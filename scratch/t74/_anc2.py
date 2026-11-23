import sys; sys.path.insert(0,'scripts')
import t74_frames_part2 as P, t74_frames_part3 as S
from t74_row_frames9 import payload, codec
import json
c=codec()
out={}
def bnd(r, key='rows'):
    return r.get('rows') if r.get('rows') else None

# t0/t21/t56 fixed -> rows exist
for a,t in [('client',56),('client',0),('client',21)]:
    b=payload(c,a,t); r=P.fixed_rows(b,P.FIXED[(a,t)])
    out[f'{t}_{a}']={'anchors':S.anchor_report(b,r['rows'],(a,t))}
    if t==21: out[f'{t}_{a}']['geom']=S.geo_report(b,r['rows'],(a,t))
# t8: rows need start/end
b=payload(c,'client',8); r=P.seq_lang(b)
rows=[]; p=14
from t74_row_frames9 import lstr
while p<len(b)-8:
    q,n,_=lstr(b,p,len(b)-8); rows.append((p,q+30)); p=q+30
out['8_client']={'anchors':S.anchor_report(b,rows,('client',8)),'anchor_note':'rdui_suffix@17 视为 suffix 内偏移(与 fm24_dump 同口径),此处按行首+rdui_suffix 试算仅作对照'}
# t7
b=payload(c,'client',7); r=P.seq_media7(b)
out['7_client']={'anchors':S.anchor_report(b,r['rows'],('client',7))}
# t47
b=payload(c,'client',47); r=P.seq_lcrg(b)
out['47_client']={'anchors':S.anchor_report(b,r['rows'],('client',47))}
print(json.dumps(out,ensure_ascii=False,indent=1))
