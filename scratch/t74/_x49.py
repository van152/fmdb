import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
raw=load('server',24)
for j in range(0,384,16):
    print(f'{j:5d} {raw[j:j+16].hex(" ")}  {raw[j:j+16]!r}')
print('...tail')
n=len(raw)
for j in range(n-160,n,16):
    print(f'{j:5d} {raw[j:j+16].hex(" ")}  {raw[j:j+16]!r}')
