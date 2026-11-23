import struct,json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
starts=np.array(json.load(open('scratch/t88/rows.json'))['starts'],dtype=np.int64)
ends=np.append(starts[1:],L-8)
lens=ends-starts
print('len hist:',{int(k):int(v) for k,v in zip(*np.unique(lens,return_counts=True))})
i=int(np.argmin(lens))
for idx in [i, i+1]:
    s,e=starts[idx],ends[idx]
    print(f'\n--- row {idx} len {e-s} ---')
    r=b[s:e]
    for o in range(0,len(r),16):
        print(f'{o:3d} {r[o:o+16].hex(" ")}')
