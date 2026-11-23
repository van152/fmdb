import struct,sys,collections
sys.path.insert(0,r'D:\tmp2b\fm24\tools\python'); sys.path.insert(0,r'scripts')
import t112_fm24_reader as R, zstandard as z
ar={a:R.Archive(a) for a in ('server','client')}
d=z.ZstdDecompressor()
def body(arch,nm):
    a=ar[arch]; p=f'{arch}_db/{nm}.dat'; e=a.entries[p]; o=d.decompressobj(); return o.decompress(a.data[a.data_base+e['offset']:])

cl=body('server','club_links'); n=struct.unpack_from('<I',cl,8)[0]; st=47
print('club_links n',n,'12+n*47',12+n*47,'len',len(cl))
print(' u32@0==i:',all(struct.unpack_from('<I',cl,12+i*st)[0]==i for i in range(n)))
print(' u32@9==i:',all(struct.unpack_from('<I',cl,12+i*st+9)[0]==i for i in range(n)))
for off in (0,9,43):
    v=[struct.unpack_from('<I',cl,12+i*st+off)[0] for i in range(n)]
    print('  u32@%2d min %d max %d uniq %d sample %s'%(off,min(v),max(v),len(set(v)),v[:6]))
print(' row0',' '.join('%02x'%x for x in cl[12:12+47]))
print(' row1',' '.join('%02x'%x for x in cl[12+47:12+94]))
print(' row2',' '.join('%02x'%x for x in cl[12+94:12+141]))

cn=body('server','common_name_links'); m=struct.unpack_from('<I',cn,8)[0]
print()
print('common_name_links n',m,'12+n*10',12+m*10,'len',len(cn))
print(' u32@0==i:',all(struct.unpack_from('<I',cn,12+i*10)[0]==i for i in range(m)))
for i in range(6): print('  row%d'%i,' '.join('%02x'%x for x in cn[12+i*10:12+i*10+10]))
print(' byte8 dist',collections.Counter(cn[12+i*10+8] for i in range(m)).most_common(5))
print(' byte9 dist',collections.Counter(cn[12+i*10+9] for i in range(m)).most_common(5))

print()
o23=body('server','table_for_old_save_23'); t23=body('server','table_23')
print('old23 == table_23 bytes:',o23==t23,'len',len(o23),len(t23))
o23c=body('client','table_for_old_save_23'); t23c=body('client','table_23')
print('client old23 == client table_23:',o23c==t23c)
o25=body('client','table_for_old_save_25'); t25=body('client','table_25')
print('client old25 len',len(o25),'n',struct.unpack_from('<I',o25,8)[0],'(13+n*123+9)=',13+7047*123+9)
print('client old25 == client table_25:',o25==t25)
print('client old25 flags',collections.Counter(o25[13+i*123] for i in range(7047)).most_common(6))
print('client table25 flags',collections.Counter(t25[13+i*127] for i in range(7047)).most_common(6))
print('client old25 row0',' '.join('%02x'%x for x in o25[13:13+123]))
print('client old25 tail9',o25[-9:].hex())
s25=body('server','table_for_old_save_25'); t25s=body('server','table_25')
print()
print('server old25 len',len(s25),'n',struct.unpack_from('<I',s25,8)[0],'tail9',s25[-9:].hex())
print('server old25 == server table_25:',s25==t25s)
print('s25 count ff64ffff',s25.count(b'\xff\x64\xff\xff'))
print('s25 count 01006c07',s25.count(b'\x01\x00\x6c\x07'))
