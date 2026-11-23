import pathlib,sys,struct
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
s=(D/'payload_summary.bin').read_bytes()
T=1637014
off=T+12  # skip fa 000000 | ec7ae404 | 00000000
print('at',off,s[off:off+16].hex(' '))
# hypothesis: u32 n then n u32 ids
p=off
while p+4<=len(s):
    n=struct.unpack_from('<I',s,p)[0]
    if n>0x100000 or p+4+4*n>len(s): print('stop at',p,'n',n); break
    ids=struct.unpack_from('<%dI'%n,s,p+4)
    asc=all(b>=a for a,b in zip(ids,ids[1:]))
    print(f'block@ {p} n={n} asc={asc} first={ids[:3]} last={ids[-2:]}')
    p=p+4+4*n
print('end p',p,'len',len(s),'rem',len(s)-p)
print('rem bytes',s[p:].hex(' '))
