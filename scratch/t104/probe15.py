import sys, struct, runpy, collections, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
d=json.load(open('scratch/t104/path.json'))
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
raw=m['load_payload_mf'](codec,'server',24,cache)
H=14; T=13; ident=d['ident']; n=len(ident); lens=d['lens']
def body(i):
    s=H if i==0 else ident[i-1][0]+T
    return raw[s:ident[i][0]]
sel=[x[2] for x in ident]
cols=collections.defaultdict(collections.Counter)
cnt=0
for i in range(n):
    b=body(i); pref=49 if sel[i]==11 else 0
    if len(b)<pref+53+12: continue
    c=struct.unpack_from('<H',b,pref+33)[0]
    base=pref+53+4*c
    if len(b)<base+12: continue
    blk=b[base:base+12]
    rest=b[base+12:]
    if len(rest)<8: continue
    l1=struct.unpack_from('<I',rest,0)[0]
    if l1>80 or 4+l1+4>len(rest): continue
    l2=struct.unpack_from('<I',rest,4+l1)[0]
    if l2>80 or 4+l1+4+l2!=len(rest): continue
    cnt+=1
    for o in range(12): cols[o][blk[o]]+=1
print('rows',cnt)
for o in range(12):
    c=cols[o]; print(o, len(c), sorted(c.items(), key=lambda kv:-kv[1])[:6])
