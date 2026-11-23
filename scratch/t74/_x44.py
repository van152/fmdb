import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct

for arch in ('client','server'):
    raw=load(arch,27)
    H,F=14,len(raw)-8
    print('===',arch,'payload',len(raw))
    print('bytes 120..150:',raw[120:150].hex(' '))
    p=H; i=0; lens=[]
    while p<F:
        L=struct.unpack_from('<I',raw,p)[0]
        if not (0<L<200): print('  STOP at',p,'L',L); break
        p+=4+L+95+13; lens.append(4+L+95+13); i+=1
    print('sequential rows',i,'end',p,'F',F,'match',p==F,'len range',min(lens),max(lens))
