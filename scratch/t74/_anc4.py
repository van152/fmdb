import sys; sys.path.insert(0,'scripts')
import t74_frames_part2 as P, t74_frames_part3 as S
from t74_row_frames9 import payload, codec, lstr
c=codec()
# t8 suffix rows
b=payload(c,'client',8); F=len(b)-8; p=14; suf=[]
while p<F:
    q,n,_=lstr(b,p,F); suf.append((len(suf), q+17)); p=q+30
print('t8', S.suffix_anchor_report(b,suf,('client',8)))
# t6 对照
b=payload(c,'client',6); n=__import__('struct').unpack_from('<I',b,8)[0]
rows=[(14+i*16,14+(i+1)*16) for i in range(n)]
print('t6', S.anchor_report(b,rows,('client',6)))
# t47
b=payload(c,'client',47); r=P.seq_lcrg(b)
print('t47', S.anchor_report(b,r['rows'],('client',47)))
# t7 rows without rdui: 检查 identity 内部一致
b=payload(c,'client',7); r=P.seq_media7(b)
rep={}
import struct
for nm,off in (('rdui',-13),('duni',-9)):
    hit=sum(1 for i,(s,e) in enumerate(r['rows']) if struct.unpack_from('<I',b,e+off)[0]==(i if nm=='rdui' else struct.unpack_from('<I',b,e-9)[0]))
    rep[nm]={'offset':off,'hit':hit,'total':len(r['rows'])}
print('t7 identity-internal',rep)
