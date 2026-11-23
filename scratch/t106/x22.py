import pathlib,sys,struct,collections,math
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
b=(D/'payload_server_club_links.bin').read_bytes()
n=struct.unpack_from('<I',b,8)[0]; st=47
rows=[b[12+i*st:12+(i+1)*st] for i in range(n)]
print('rows',n,'len',len(b),'12+n*47',12+n*47)
for off in range(st):
    col=[r[off] for r in rows]
    h=collections.Counter(col); ent=-sum(v/n*math.log2(v/n) for v in h.values())
    top=h.most_common(3)
    print('%2d ent=%.2f top=%s'%(off,ent,top))
