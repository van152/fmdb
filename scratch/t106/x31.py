import pathlib,sys,struct
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
b=(D/'payload_summary.bin').read_bytes()
sep=b'\xff\xff\xff\xff\x03'
pos=[];p=0
while True:
    i=b.find(sep,p)
    if i<0:break
    pos.append(i);p=i+5
print('seps',len(pos),'first',pos[:3],'last',pos[-2:])
lens=[pos[i+1]-(pos[i]+5) for i in range(len(pos)-1)]
import collections
print('body len hist top',collections.Counter(lens).most_common(6))
print('17B count',lens.count(17))
print('tail start',pos[-1]+5,'len',len(b))
t=b[pos[-1]+5:]
print('tail bytes',len(t))
for o in range(0,64,16):
    print('%5d'%o,' '.join('%02x'%x for x in t[o:o+16]))
