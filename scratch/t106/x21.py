import pathlib,sys,struct,collections
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
b=(D/'payload_server_table_for_old_save_25.bin').read_bytes()
print('tail region from 1464829:')
for o in range(1464829,len(b),16):
    print('%7d'%o,' '.join('%02x'%x for x in b[o:o+16]))
print()
f=(D/'payload_server_fantasy_draft_future_regens.bin').read_bytes()
pos=[];p=0
while True:
    i=f.find(b'\x01\x00\x6c\x07',p)
    if i<0:break
    pos.append(i);p=i+1
print('fantasy markers',len(pos),pos[:5],pos[-3:])
ends=[i+4 for i in pos]
starts=[12]+ends[:-1]
lens=[ends[i]-starts[i] for i in range(len(ends))]
print('lens',lens)
print('sum',sum(lens),'+12=',sum(lens)+12,'len',len(f),'tail after last',len(f)-ends[-1])
for o in range(ends[-1],len(f),16):
    print('%6d'%o,' '.join('%02x'%x for x in f[o:o+16]))
