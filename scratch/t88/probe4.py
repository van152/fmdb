import struct, numpy as np
b=open('D:/tmp2b/fm24-db/scratch/t88/t45.bin','rb').read()
L=len(b); n=struct.unpack_from('<I',b,8)[0]
print('L',L,'n',n,'L-14-8',L-22,(L-22)/n)
# candidate positions per phase where u32 == small ordinal
for phase in (0,1,2,3):
    v=np.frombuffer(b,'<u4',(L-phase)//4,phase)
    for lim,label in ((n,'lt_n'),(90000,'lt_90k')):
        ix=np.flatnonzero(v<lim)
        print(f'phase{phase} {label}: {len(ix)}')
