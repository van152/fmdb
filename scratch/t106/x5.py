import pathlib,sys,struct,collections
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
b=(D/'payload_server_table_for_old_save_25.bin').read_bytes()
print('len',len(b),'hdr count',struct.unpack_from('<I',b,8)[0])
print('head40',' '.join('%02x'%x for x in b[:48]))
print('tail32',' '.join('%02x'%x for x in b[-32:]))
n=struct.unpack_from('<I',b,8)[0]
for s in range(8,30):
    for k in range(4,40):
        if s+n*k>len(b): continue
        ok=sum(1 for i in range(30) if struct.unpack_from('<I',b,s+i*k)[0]==i)
        if ok>=30: print('start',s,'stride',k,'tail',len(b)-(s+n*k))
