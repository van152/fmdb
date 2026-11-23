import pathlib,sys,struct,itertools
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
b=(D/'payload_server_table_for_old_save_23.bin').read_bytes()
n=278
# search: start offset s, stride k, such that first u32 == row index for first 20 rows
for s in range(8,30):
    for k in range(8,30):
        if s+k*n>len(b): continue
        ok=sum(1 for i in range(20) if struct.unpack_from('<I',b,s+i*k)[0]==i)
        if ok>=20:
            print('start',s,'stride',k,'tail',len(b)-(s+k*n),'ok20')
for s in range(8,30):
    for k in range(8,30):
        if s+k*n>len(b): continue
        ok=sum(1 for i in range(20) if struct.unpack_from('>I',b,s+i*k)[0]==i)
        if ok>=20:
            print('BE start',s,'stride',k,'tail',len(b)-(s+k*n))
