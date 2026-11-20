import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

# --- comp: uid 130026 present in table_25? ---
for a in ('client','server'):
    raw=K['load_payload'](lib.CODEC,a,'25')
    pat=struct.pack('<I',130026)
    idx=[i for i in range(len(raw)-3) if raw[i:i+4]==pat]
    print(f'{a} table_25: uid 130026 occurrences', idx[:5], 'len',len(raw))

# --- club inline offsets: exact position of full & short name ---
raw3=K['load_payload'](lib.CODEC,'client','3')
rows=list(K['walk_club_block'](raw3))
import collections
off=collections.Counter(); off2=collections.Counter()
for i,o,b in rows[:20000]:
    p=0; got=[]
    while p<len(b)-4 and len(got)<2:
        L=struct.unpack_from('<I',b,p)[0]
        if 1<=L<=120 and p+4+L<=len(b):
            try: s=b[p+4:p+4+L].decode('utf-8')
            except Exception: p+=1; continue
            if s and any(c.isalpha() for c in s): got.append((p,L)); p+=4+L; continue
        p+=1
    if got: off[got[0][0]]+=1
    if len(got)>1: off2[got[1][0]-got[0][0]]+=1
print('full-name rel offset top', off.most_common(5))
print('short-minus-full offset top', off2.most_common(5))
