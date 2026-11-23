import pathlib,sys,struct,collections
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
b=(D/'payload_server_table_for_old_save_25.bin').read_bytes()
n=struct.unpack_from('<I',b,8)[0]
print('len',len(b),'n',n)
# find "duni" tails: u32 pair equal, followed by u16 0
hits=[]
for p in range(12,len(b)-10):
    if b[p:p+4]==b[p+4:p+8] and b[p+8:p+10]==b'\x00\x00':
        hits.append(p)
print('pair+u16zero hits',len(hits))
d=collections.Counter(hits[i+1]-hits[i] for i in range(len(hits)-1))
print('gap top',d.most_common(10))
print('first hits',hits[:10],'last',hits[-3:])
