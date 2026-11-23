import pathlib,sys,struct
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
b=(D/'payload_server_table_for_old_save_25.bin').read_bytes()
n=struct.unpack_from('<I',b,8)[0]
print('len',len(b),'n',n)
for h in range(8,40):
    for s in range(20,260):
        if h+n*s<=len(b) and len(b)-(h+n*s)<=24:
            print('hdr',h,'stride',s,'left',len(b)-(h+n*s))
