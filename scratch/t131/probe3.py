import struct,sys,collections
sys.path.insert(0,r'D:\tmp2b\fm24\tools\python'); sys.path.insert(0,r'scripts')
import t112_fm24_reader as R, zstandard as z
ar={a:R.Archive(a) for a in ('server','client')}
d=z.ZstdDecompressor()
def body(arch,nm):
    a=ar[arch]; p=f'{arch}_db/{nm}.dat'; e=a.entries[p]; o=d.decompressobj(); return o.decompress(a.data[a.data_base+e['offset']:])

# identity check: name_table rows = [u16][u32 uid][u16][u16][u16] ?
for i in (0,1,2):
    b=body('server',f'name_table_{i}'); n=struct.unpack_from('<I',b,8)[0]
    ok=all(struct.unpack_from('<I',b,12+r*12+2)[0]==r for r in range(n))
    print(f'name_table_{i} n={n} uid==row for all: {ok}')
    f0=[struct.unpack_from('<H',b,12+r*12)[0] for r in range(n)]
    print('   f0 sentinel count',f0.count(65535),'distinct non-sent',len(set(f0)-{65535}),'top',collections.Counter(f0).most_common(4))

# table_extra_24 u32@0 == i ?
b=body('server','table_extra_24'); n=struct.unpack_from('<I',b,8)[0]; st=82
print('extra24 n',n,'u32@0==i',all(struct.unpack_from('<I',b,12+r*st)[0]==r for r in range(n)))
print('extra24 row0:',[hex(x) for x in struct.unpack_from('<41H',b,12)])
print('extra24 row1:',[hex(x) for x in struct.unpack_from('<41H',b,12+st)])
# distinct per u16 col
for k in range(0,41):
    v=[struct.unpack_from('<H',b,12+r*st+k*2)[0] for r in range(n)]
    print('  u16[%2d] distinct=%5d min=%5d max=%5d top=%s'%(k,len(set(v)),min(v),max(v),collections.Counter(v).most_common(3)))
