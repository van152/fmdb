import struct,json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends']); sl=np.array(d['strlen'])
def show(i):
    s=starts[i]; e=ends[i]; r=b[s:e]
    print(f'== row {i} len {e-s} strlen {sl[i]}')
    for o in range(0,len(r),8):
        print(f'  {o:3d} '+' '.join(f'{x:02x}' for x in r[o:o+8]))
show(38968); show(38971)
