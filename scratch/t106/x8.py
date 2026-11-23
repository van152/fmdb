import pathlib,sys,struct
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
b=(D/'payload_server_table_for_old_save_25.bin').read_bytes()
n=struct.unpack_from('<I',b,8)[0]
print('len',len(b),'n',n)
# find positions of u32 == 0,1,2,3 ... for first 40 rows and measure gaps
pos=[]
for i in range(0,40):
    pat=struct.pack('<I',i)
    # search within window
    start=12 if i==0 else pos[-1]+1
    idx=b.find(pat,start,start+400)
    pos.append(idx)
print('pos',pos[:20])
print('gaps',[pos[i+1]-pos[i] for i in range(min(19,len(pos)-1))])
