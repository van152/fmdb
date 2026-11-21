import sys,struct
sys.path.insert(0,'scratch/t85/work'); sys.stdout.reconfigure(encoding='utf-8')
import common as C
raw=C.payload('server','server_db/table_66.dat',18094)
print('len',len(raw),'head',raw[:20].hex(' '))
# walk identity rows
p=14; rows=[]
while p+13<=len(raw):
    a,b,c=struct.unpack_from('<III',raw,p)
    rows.append((p,a,b,c,raw[p+12]))
    p+=1
    if len(rows)>5: break
# proper: find identity offsets
offs=[]
for i in range(0,len(raw)-13):
    a,b,c=struct.unpack_from('<III',raw,i)
    if b==c and raw[i+12]==0 and a==len(offs): offs.append(i)
print('ident rows',len(offs),'first',offs[:6],'last',offs[-2:])
print('deltas',[offs[i+1]-offs[i] for i in range(8)])
