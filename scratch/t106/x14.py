import pathlib,sys,struct,collections
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
b=(D/'payload_server_table_for_old_save_25.bin').read_bytes()
n=struct.unpack_from('<I',b,8)[0]
pos=[]
p=12
while True:
    i=b.find(b'\xff\x64\xff\xff',p)
    if i<0: break
    pos.append(i); p=i+1
print('hits',len(pos),'first',pos[:6],'last',pos[-3:])
gaps=[pos[i+1]-pos[i] for i in range(len(pos)-1)]
print('gap hist',collections.Counter(gaps).most_common(12))
print('last gap to end',len(b)-pos[-1])
# check each row starts right after previous marker+4? rows might end with ff64ffff?
print('context of first 3 markers:')
for i in pos[:3]:
    print('  ',i,' '.join('%02x'%x for x in b[i-16:i+8]))
