import pathlib,sys,struct
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
b=(D/'payload_server_club_links.bin').read_bytes()
n=struct.unpack_from('<I',b,8)[0]; st=47
for i in range(4):
    r=b[12+i*st:12+(i+1)*st]
    print('row',i)
    for o in range(0,st,1):
        pass
    for o in range(0,st,8):
        print('   %2d'%o,' '.join('%02x'%x for x in r[o:o+8]))
