import struct,collections,json
d=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
base=0x140000000
def a4(v):
    b=v.to_bytes(4,'little')
    return ''.join(chr(c) if 32<=c<127 else '.' for c in b) if all(32<=c<127 for c in b) else None
hits=[]
i=0
while True:
    i=d.find(b'\x81\xfe',i)
    if i<0: break
    v=struct.unpack_from('<I',d,i+2)[0]; s=a4(v)
    if s: hits.append((i,s))
    i+=1
print('cmp esi ascii',len(hits),'distinct codes',len(set(h[1] for h in hits)))
reg=collections.Counter(h[0] for h in hits)
print('fo range', hex(min(reg)), hex(max(reg)))
# cluster
cl=collections.Counter(h[0]>>12 for h in hits)
print(sorted(cl.items()))
json.dump([[hex(f),s] for f,s in hits],open('scratch/t88/out3/_cmpesi.json','w'))
