import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _lib import *

def cmp_sites(pe):
    d=pe.data; regs={0xF8:'eax',0xF9:'ecx',0xFA:'edx',0xFB:'ebx',0xFC:'esp',0xFD:'ebp',0xFE:'esi',0xFF:'edi'}
    out=[]
    for p in range(len(d)-8):
        b=d[p]
        if b==0x81 and d[p+1] in regs:
            out.append((p, int.from_bytes(d[p+2:p+6],'little'), '81',regs[d[p+1]],6))
        elif b==0x3D:
            out.append((p,int.from_bytes(d[p+1:p+5],'little'),'3d','eax',5))
        elif b==0x41 and d[p+1]==0x81 and d[p+2] in regs:
            out.append((p,int.from_bytes(d[p+3:p+7],'little'),'4181',regs[d[p+2]],7))
    return out

if __name__=='__main__':
    pe=PE(EDITOR.read_bytes())
    sites=cmp_sites(pe)
    print('total imm-cmp sites', len(sites), file=sys.stderr)
    MASTER=json.loads(MASTER.read_text(encoding='utf-8'))
    ent2codes={}
    for k,v in MASTER['entities'].items():
        for e in v: ent2codes[e['id']]=[f['field'] for f in e['fields']]
    for ent in sys.argv[1:]:
        codes=ent2codes[ent]
        want={int.from_bytes(c.encode(),'big'):c for c in codes}
        hits=[(p,imm) for p,imm,_,_,_ in sites if imm in want]
        hits.sort()
        clusters=[]
        for p,imm in hits:
            if clusters and p-clusters[-1][-1][0] < 0x1800:
                clusters[-1].append((p,imm))
            else:
                clusters.append([(p,imm)])
        clusters.sort(key=lambda c: -len({i for _,i in c}))
        print(f"=== {ent} codes={codes}")
        for c in clusters[:6]:
            uniq=sorted({want[i] for _,i in c})
            print(f"   cluster @{c[0][0]:#x}..{c[-1][0]:#x}  distinct={len(uniq)} {uniq}")
