import runpy, struct, math, collections, json, io
m = runpy.run_path('scripts/t73_mapper_core.py', run_name='x')
u32 = lambda b,o: struct.unpack_from('<I', b, o)[0]
f32 = lambda b,o: struct.unpack_from('<f', b, o)[0]

rc=m['load_payload']('client',2); H,S,n=14,43,56293
lat=[f32(rc,H+j*S+1) for j in range(n)]
lon=[f32(rc,H+j*S+5) for j in range(n)]
cwea=[u32(rc,H+j*S+14) for j in range(n)]
cnti=[u32(rc,H+j*S+10) for j in range(n)]
clri=[u32(rc,H+j*S+25) for j in range(n)]
clgi=[u32(rc,H+j*S+21) for j in range(n)]

def spread(groups, vals_a, vals_b):
    """mean within-group great-circle-ish spread (deg) vs global spread"""
    num=0.0; den=0
    for g,idx in groups.items():
        if len(idx)<2: continue
        la=[vals_a[i] for i in idx]; lo=[vals_b[i] for i in idx]
        ml=sum(la)/len(la); mo=sum(lo)/len(lo)
        for i in idx:
            num+=math.hypot(vals_a[i]-ml, vals_b[i]-mo); den+=1
    return num/max(1,den)

def groupof(col, maxg=4000):
    g=collections.defaultdict(list)
    for j,v in enumerate(col):
        if v!=0xFFFFFFFF and v<maxg: g[v].append(j)
    return g

print('=== Cwea -> weather: geographic coherence')
gc=groupof(cwea,400)
print(' groups',len(gc),'sizes',sorted((len(v) for v in gc.values()))[-5:])
print(' within-weather spread(deg)', round(spread(gc,lat,lon),3), ' global spread', round(spread({0:list(range(n))},lat,lon),3))
print('=== Clri -> local_region')
gl=groupof(clri,3000)
print(' groups',len(gl))
print(' within-lcrg spread(deg)', round(spread(gl,lat,lon),3))
print('=== Cnti -> nation')
gn=groupof(cnti,300)
print(' groups',len(gn))
print(' within-nation spread(deg)', round(spread(gn,lat,lon),3))
print('=== Clgi -> language')
gg=groupof(clgi,300)
print(' groups',len(gg))
print(' within-language spread(deg)', round(spread(gg,lat,lon),3))
# control: shuffled assignment
import random
random.seed(7)
shuf=cwea[:]; random.shuffle(shuf)
print(' CONTROL shuffled Cwea spread', round(spread(groupof(shuf,400),lat,lon),3))
