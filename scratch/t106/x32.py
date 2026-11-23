import pathlib,sys,struct,collections
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
b=(D/'payload_server_simple_vars.bin').read_bytes()
N=len(b)
# u32 == FFFFFFFF positions
pos=[i for i in range(len(b)-3) if b[i:i+4]==b'\xff\xff\xff\xff']
gaps=[pos[i+1]-pos[i] for i in range(len(pos)-1)]
print('FFFFFFFF count',len(pos),'gap top',collections.Counter(gaps).most_common(8))
print('first',pos[:8],'last',pos[-3:],'N',N)
# generic parse search
def walk(hdr,kw,lw,le='little',foot=0):
    p=hdr;n=0;end=N-foot
    while p<end:
        if p+kw+lw>end: return None
        key=int.from_bytes(b[p:p+kw],le); L=int.from_bytes(b[p+kw:p+kw+lw],le)
        if L>end-p-kw-lw: return None
        p+=kw+lw+L;n+=1
        if n>100000: return None
    return (n,) if p==end else None
for hdr in range(12,30):
    for kw,lw in ((2,2),(2,3),(2,4),(1,2),(1,3),(4,4),(1,1),(2,1),(4,2)):
        for le in ('little','big'):
            for foot in (0,7,8,9,10):
                r=walk(hdr,kw,lw,le,foot)
                if r: print('PARSE hdr=%d kw=%d lw=%d %s foot=%d recs=%d'%(hdr,kw,lw,le,foot,r[0]))
