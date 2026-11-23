import json,struct,collections
d=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
base=0x140000000
def asc(v):
    b=v.to_bytes(4,'little')
    return ''.join(chr(c) if 32<=c<127 else '.' for c in b)
hits=[]
i=0
pat=b'\x81\xfa'
while True:
    i=d.find(pat,i)
    if i<0: break
    v=struct.unpack_from('<I',d,i+2)[0]
    s=asc(v)
    if all(32<=c<127 for c in v.to_bytes(4,'little')):
        hits.append((i,v,s))
    i+=1
print('cmp edx imm ascii hits',len(hits))
codes=collections.Counter(h[2] for h in hits)
print(len(codes), sorted(codes)[:40])
json.dump([[hex(h[0]),h[2]] for h in hits],open('scratch/t88/out3/_cmpedx.json','w'))
# group by function region
regions=collections.Counter()
for fo,v,s in hits:
    regions[fo>>16]+=1
print(sorted(regions.items())[:20])
