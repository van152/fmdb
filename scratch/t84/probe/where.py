import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def lp_scan(raw, lo=2, hi=80):
    out=[]
    p=0
    while p<len(raw)-4:
        L=struct.unpack_from('<I',raw,p)[0]
        if lo<=L<=hi and p+4+L<=len(raw):
            try: s=raw[p+4:p+4+L].decode('utf-8')
            except Exception: p+=1; continue
            if s and all(30<ord(c)<0x2100 for c in s) and any(c.isalpha() for c in s):
                out.append((p,L,s)); p+=4+L; continue
        p+=1
    return out

for a,t in (('client','10'),('client','25'),('server','10'),('server','25')):
    raw=K['load_payload'](lib.CODEC,a,t)
    got=lp_scan(raw)
    print(f'== {a} table_{t} len={len(raw)} LP-strings={len(got)}')
    for g in got[:8]: print('   ',g[0],g[1],ascii(g[2]))
