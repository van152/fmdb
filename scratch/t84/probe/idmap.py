import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
raw3=K['load_payload'](lib.CODEC,'client','3')

def idblock_before(pos):
    for back in range(26, 34):
        if pos-back<0: return None
        a,b,c,d=struct.unpack_from('<IIII',raw3,pos-back)
        if b==0xFFFFFFFF and a==c==d and 0<a<2*10**6: return (a,pos-back)
    return None

# build name -> db_id for all clubs using inline len-prefixed names
names={}
pos=14
import re
p=0
found=0
while p<len(raw3)-8 and found<2000:
    L=struct.unpack_from('<I',raw3,p)[0]
    if 2<=L<=90 and p+4+L<=len(raw3):
        seg=raw3[p+4:p+4+L]
        try: s=seg.decode('utf-8')
        except Exception: p+=1; continue
        if s and all(31<ord(c)<0x2100 for c in s) and any(c.isalpha() for c in s):
            ib=idblock_before(p)
            if ib: names.setdefault(ib[0],[]).append(s); found+=1
            p+=4+L; continue
    p+=1
print('db_id -> name pairs:',len(names))
for d in (74,75,76,102,103,126,128,139,149,150,151):
    print(f'  db_id {d}: {names.get(d)}')
