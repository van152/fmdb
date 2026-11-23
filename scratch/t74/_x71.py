import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import numpy as np, struct, collections

raw=load('server',24); n=len(raw); N=struct.unpack_from('<I',raw,8)[0]
W=np.lib.stride_tricks.sliding_window_view(np.frombuffer(raw,dtype=np.uint8),4).view('<u4').ravel()[:n-3]
for p in range(126,160):
    print(p, W[p], W[p+1], W[p+2], 'mk', raw[p+12])
print()
for j in range(120,200,16):
    print(f'{j:6d} {raw[j:j+16].hex(" ")}  {raw[j:j+16]!r}')
