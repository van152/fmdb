import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def pool(n):
    raw=lib.load_member('client',f'name_table_extra_{n}.dat')
    cnt=struct.unpack_from('<I',raw,8)[0]; pos=12; out=[]
    while pos+8<=len(raw):
        i,l=struct.unpack_from('<II',raw,pos); out.append(raw[pos+8:pos+8+l].decode('utf-8','replace')); pos+=8+l
    return out
P={n:pool(n) for n in (0,1,2)}
SETS={n:set(v) for n,v in P.items()}

raw3=K['load_payload'](lib.CODEC,'client','3')
rows=list(K['walk_club_block'](raw3))

# collect club inline full names (length-prefixed, min len 5)
clubs=[]
p=14
while p<len(raw3)-8:
    L=struct.unpack_from('<I',raw3,p)[0]
    if 3<=L<=90 and p+4+L<=len(raw3):
        try: s=raw3[p+4:p+4+L].decode('utf-8')
        except Exception: p+=1; continue
        if s and all(31<ord(c)<0x2100 for c in s) and any(c.isalpha() for c in s) and ' ' in s:
            clubs.append((p,s)); p+=4+L; continue
    p+=1
print('inline candidate club names:',len(clubs))

# H1: does any u32 in the 40 bytes preceding a club name index into a pool to give that exact name?
def idblock_before(pos):
    for back in range(26,40):
        if pos-back<0: return None
        a,b,c,d=struct.unpack_from('<IIII',raw3,pos-back)
        if b==0xFFFFFFFF and a==c==d: return (a,pos-back)
    return None

hit=0; tot=0; samples=[]
for pos,s in clubs[:3000]:
    ib=idblock_before(pos)
    if not ib: continue
    tot+=1
    row_start=ib[1]
    win=raw3[max(0,row_start-60):pos]
    found=False
    for k in range(0,len(win)-3,1):
        v=struct.unpack_from('<I',win,k)[0]
        for n in (0,1,2):
            if v < len(P[n]) and P[n][v]==s: found=True; break
        if found: break
    if found: hit+=1; samples.append(s)
print(f'H1 pool-index->same club name: {hit}/{tot} ({(100*hit/tot if tot else 0):.2f}%)')
print('samples',samples[:5])
