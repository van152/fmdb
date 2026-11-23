import pathlib,sys,struct,collections
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
b=(D/'payload_server_simple_vars.bin').read_bytes()[34:]
N=len(b)
# non-zero density per 1024 block
dens=[(i, sum(1 for c in b[i:i+1024] if c)) for i in range(0,N,1024)]
print('blocks with density<5:',[(i,d) for i,d in dens if d<5][:20])
print('blocks density>200:',[(i,d) for i,d in dens if d>200][:20])
print('n blocks',len(dens))
# stride autocorrelation on nonzero bytes
best=[]
for s in range(2,600):
    hit=sum(1 for i in range(0,N-s) if b[i] and b[i]==b[i+s])
    tot=sum(1 for i in range(0,N-s) if b[i])
    best.append((hit/max(tot,1),hit,s))
best.sort(reverse=True)
print('top strides',best[:10])
# run-length of zeros
runs=[];cur=0
for c in b:
    if c==0: cur+=1
    else:
        if cur: runs.append(cur)
        cur=0
if cur: runs.append(cur)
print('zero runs',len(runs),'max',max(runs),'top',collections.Counter(runs).most_common(8))
