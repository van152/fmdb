import struct,sys,collections
sys.path.insert(0,r'D:\tmp2b\fm24\tools\python'); sys.path.insert(0,r'scripts')
import t112_fm24_reader as R, zstandard as z
ar={a:R.Archive(a) for a in ('server','client')}
d=z.ZstdDecompressor()
def body(arch,p):
    a=ar[arch]; e=a.entries[p]; o=d.decompressobj(); return o.decompress(a.data[a.data_base+e['offset']:])

for arch,nm,st in (('server','table_extra_24',82),('server','table_extra_3',None),('server','table_extra_9',None)):
    b=body(arch,f'{arch}_db/{nm}.dat'); n=struct.unpack_from('<I',b,8)[0]
    print('=====',nm,'len',len(b),'n',n,'len-12-n*st',len(b)-12-n*st if st else '')
    if st:
        print(' flags@12+st*i:',collections.Counter(b[12+i*st] for i in range(n)).most_common(8))
        print(' flags@13+st*i:',collections.Counter(b[13+i*st] for i in range(n)).most_common(8))
        print(' tail9',b[-9:].hex())
        print(' row0',' '.join('%02x'%x for x in b[12:12+st]))
        print(' row1',' '.join('%02x'%x for x in b[12+st:12+2*st]))
