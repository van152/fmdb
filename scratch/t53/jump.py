from probe import *
def cell(base,i): return F(V(base)+struct.unpack_from('<i',B,base+4*i)[0])
for name in ('PUnI','PUnT','PUnP','PUnJ'):
 n=int.from_bytes(name.encode(),'big')-0x50556e49; print(name,n,hex(cell(0x155a728,n)))
for j in [9,0x1f]:
 t=cell(0x14d0184,j); print(j,hex(t));dump(t,t+0x32)
PY=0
