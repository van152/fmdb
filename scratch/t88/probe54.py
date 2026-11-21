import json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends']); sl=np.array(d['strlen'])
n=len(starts); ne=starts+41+sl
refs=json.load(open('scratch/t88/refsets.json'))
S={k:set(v) for k,v in refs.items()}
b4=np.array([b[int(s)+4] for s in starts])
def u32(o):
    return np.array([int.from_bytes(b[int(x)+o:int(x)+o+4],'little') for x in ne],dtype=np.int64)
A,B,C=u32(12),u32(16),u32(20)
def frac(v,st,m):
    sub=v[m]; ok=[x in S[st] for x in sub.tolist()]
    return float(np.mean(ok))
print('rt   n     A:comp club  B:comp club  C:comp club  D(u8)')
for rt in (10,24,25,27,28,26,13,19):
    m=b4==rt
    if m.sum()<20: continue
    print(f'{rt:3d} {int(m.sum()):5d}  '+'  '.join(f'{frac(v,"t25",m):.3f}' for v in (A,B,C))+'  | '+
          '  '.join(f'{frac(v,"t3",m):.3f}' for v in (A,B,C)))
