import pathlib,sys,struct,collections
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
def get(n): return (D/(('payload_summary.bin') if n=='summary' else f'payload_server_{n}.bin')).read_bytes()

b=get('simple_vars')
pos=[];p=32
while True:
    i=b.find(b'\x6c\x07',p)
    if i<0:break
    pos.append(i);p=i+2
print('simple_vars 6c07 count',len(pos),'first',pos[:8],'last',pos[-4:],'len',len(b))
gaps=[pos[i+1]-pos[i] for i in range(len(pos)-1)]
print('gaps top',collections.Counter(gaps).most_common(8))
print('after last 6c07:',len(b)-pos[-1])

print()
print('== old_save_25 rows 0,1')
b2=get('table_for_old_save_25')
mk=b'\x64\xff\xff\xff'
pos2=[];p=12
while True:
    i=b2.find(mk,p)
    if i<0:break
    pos2.append(i);p=i+1
starts=[12]+[p+4 for p in pos2]
for k in range(2):
    s=starts[k]; e=starts[k+1]
    print('row',k,'len',e-s)
    for o in range(s,e,16):
        print('  %6d'%o,' '.join('%02x'%x for x in b2[o:min(o+16,e)]))
print()
print('== fantasy row0')
f=get('fantasy_draft_future_regens')
mk2=b'\x01\x00\x6c\x07'
pos3=[];p=12
while True:
    i=f.find(mk2,p)
    if i<0:break
    pos3.append(i);p=i+1
ss=[12]+[p+4 for p in pos3]
for k in range(2):
    s=ss[k]; e=ss[k+1]
    print('row',k,'len',e-s)
    for o in range(s,e,16):
        print('  %6d'%o,' '.join('%02x'%x for x in f[o:min(o+16,e)]))
