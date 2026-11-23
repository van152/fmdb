import struct,sys,collections
sys.path.insert(0,r'D:\tmp2b\fm24\tools\python'); sys.path.insert(0,r'scripts')
import t112_fm24_reader as R, zstandard as z
ar={a:R.Archive(a) for a in ('server','client')}
d=z.ZstdDecompressor()
def body(arch,p):
    a=ar[arch]; e=a.entries[p]; o=d.decompressobj(); return o.decompress(a.data[a.data_base+e['offset']:])
b=body('server','server_db/simple_vars.dat')
print('len',len(b),'count of f1 0d:',b.count(b'\xf1\x0d'))
# u16 view of first 120
print('u16:',[hex(x) for x in struct.unpack_from('<%dH'%(40),b,0)])
# print printable runs
import re
for m in re.finditer(rb'[\x20-\x7e]{3,}',b[:2000]):
    print(m.start(),m.group())
