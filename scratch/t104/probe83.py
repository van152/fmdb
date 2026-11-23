import sys, struct, importlib.util, collections
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
spec=importlib.util.spec_from_file_location('t82','scripts/t82_extra3_remaining.py')
m82=importlib.util.module_from_spec(spec); spec.loader.exec_module(m82)
from pathlib import Path
buf={}
for arch in ('server','client'):
    ent,raw=m82.open_fmf(Path('scratch/data/%s_db.dat'%arch))
    buf[arch]=m82.extract_fmf_member(raw,ent,'%s_db/table_extra_9.dat'%arch)
a,b=buf['server'],buf['client']
print(len(a),len(b))
d=next(i for i in range(min(len(a),len(b))) if a[i]!=b[i])
print('first divergence at',d)
# tail common?
k=0
while k<min(len(a),len(b)) and a[-1-k]==b[-1-k]: k+=1
print('common tail',k)
# find record starts: u32 == k in increasing order, from 12
pos=12; starts=[]
for k in range(251):
    needle=struct.pack('<I',k)
    j=a.find(needle,pos,pos+2000)
    if j<0: print('miss',k,'at',pos); break
    starts.append(j); pos=j+1
print('found',len(starts),'starts; first 6',starts[:6])
lens=[starts[i+1]-starts[i] for i in range(len(starts)-1)]
print('lens',lens[:12],'min',min(lens),'max',max(lens))
print('after last start',len(a)-starts[-1])
