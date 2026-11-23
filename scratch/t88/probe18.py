import struct,json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=d['starts']; ends=d['ends']; sl=d['strlen']
n=len(starts)
for i in (0,1,2,38968):
    s,e=starts[i],ends[i]; r=b[s:e]
    print(f'--- row {i} len {e-s} strlen {sl[i]} nameend {41+sl[i]} ---')
    for o in range(0,len(r),8):
        tag=''
        print(f'{o:3d} {r[o:o+8].hex(" ")}')
    print('  ident@end-13:',struct.unpack_from('<IIIB',b,e-13))
    print('  name:',r[41:41+sl[i]])
