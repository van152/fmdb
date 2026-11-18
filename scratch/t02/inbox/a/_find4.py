import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _lib import *

def find_imm(pe, imm, start=0, end=None):
    """Find cmp/other places where imm32 appears as immediate."""
    d=pe.data; end=end or len(d)
    b=imm.to_bytes(4,'little')
    out=[]
    p=d.find(b,start,end)
    while p!=-1:
        out.append(p); p=d.find(b,p+1,end)
    return out

if __name__=='__main__':
    pe=PE(EDITOR.read_bytes())
    for code in sys.argv[1:]:
        imm=int.from_bytes(code.encode(),'big')
        hits=find_imm(pe,imm)
        # keep only those where the preceding bytes look like cmp reg,imm (81 f8..ff / 41 81 / 3d)
        good=[]
        for p in hits:
            for back,nm in ((p-2,'81'),(p-3,'4181'),(p-1,'3d')):
                if back>=0:
                    i=pe.ins(back)
                    if i is not None and i.mnemonic=='cmp' and back+i.size==p+4:
                        good.append((back,(i.mnemonic+' '+i.op_str)))
                        break
        print(code, 'total', len(hits), 'cmp-sites', len(good))
        for g in good[:40]:
            print('   ', hex(g[0]), g[1])
