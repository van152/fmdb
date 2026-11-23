import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def names_in(body):
    """scan length-prefixed utf8 runs, return list of (rel, text)."""
    out=[]; p=0
    while p<len(body)-4:
        L=struct.unpack_from('<I',body,p)[0]
        if 1<=L<=120 and p+4+L<=len(body):
            try: s=body[p+4:p+4+L].decode('utf-8')
            except Exception: p+=1; continue
            if s and all(31<ord(c)<0x2100 for c in s) and any(c.isalpha() for c in s):
                out.append((p,s)); p+=4+L; continue
        p+=1
    return out

raw3=K['load_payload'](lib.CODEC,'client','3')
rows=list(K['walk_club_block'](raw3))
two=one=zero=0
for i,off,b in rows:
    ns=names_in(b)
    if len(ns)>=2: two+=1
    elif len(ns)==1: one+=1
    else: zero+=1
print(f'CLUB rows={len(rows)}: >=2 inline names {two}, 1 {one}, 0 {zero}')

# comp: client 127B rows
c25=K['load_payload'](lib.CODEC,'client','25')
tot=struct.unpack_from('<I',c25,9)[0]
c_two=sum(1 for i in range(tot) if len(names_in(c25[13+i*127:13+(i+1)*127]))>=2)
print(f'COMP rows={tot}: >=2 inline names {c_two}')
