import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
raw=lib.load_member('lang_update','8_3.dat')
print('len',len(raw),'u32@8',struct.unpack_from('<I',raw,8)[0])
# find offsets where u32 id plausible and next u32 len plausible and utf8 valid
hits=[]
for p in range(9,len(raw)-12):
    a,b=struct.unpack_from('<II',raw,p)
    if 1<=a<=300000 and 1<=b<=200 and p+8+b<=len(raw):
        try: s=raw[p+8:p+8+b].decode('utf-8')
        except Exception: continue
        if all(31<ord(c)<0x2200 for c in s) and any(c.isalpha() for c in s):
            hits.append((p,a,b,s))
print('candidate row starts',len(hits))
for h in hits[:12]: print(h[:3],ascii(h[3]))
