import pathlib,sys,struct,collections
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
b=(D/'payload_server_simple_vars.bin').read_bytes()[34:]
N=len(b)
import math
def fac(n):
    f=[];d=2
    while d*d<=n:
        while n%d==0: f.append(d);n//=d
        d+=1
    if n>1: f.append(n)
    return f
print('N',N,'factors',fac(N))
for off in range(4):
    m=(N-off)//4
    vals=struct.unpack_from('<%dI'%m,b,off)
    small=sum(1 for v in vals if v<100); tiny=sum(1 for v in vals if v<65536)
    print(f'u32@off{off}: n={m} <100={small/m:.3f} <65536={tiny/m:.3f} top={collections.Counter(vals).most_common(6)}')
for off in range(2):
    m=(N-off)//2
    vals=struct.unpack_from('<%dH'%m,b,off)
    tiny=sum(1 for v in vals if v<300)
    print(f'u16@off{off}: n={m} <300={tiny/m:.3f} top={collections.Counter(vals).most_common(6)}')
