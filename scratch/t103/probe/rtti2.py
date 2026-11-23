import sys, struct, re, json
sys.path.insert(0, r'D:\tmp2b\tools\python')
import pefile
pe=pefile.PE(r'D:\tmp2b\fm24\input\editor.exe', fast_load=True)
raw=open(r'D:\tmp2b\fm24\input\editor.exe','rb').read()
base=pe.OPTIONAL_HEADER.ImageBase
secs=[(s.VirtualAddress, s.Misc_VirtualSize, s.PointerToRawData, s.SizeOfRawData) for s in pe.sections]
def rva2fo(rva):
    for va,vs,fo,rs in secs:
        if va<=rva<va+max(vs,rs):
            d=rva-va
            if d<rs: return fo+d
    return None
def fo2rva(fo):
    for va,vs,rf,rs in secs:
        if rf<=fo<rf+rs: return va+(fo-rf)
    return None
# TDs
tds={}  # rva -> name
for m in re.finditer(rb'\.\?AV[A-Za-z0-9_@?$<>]{2,120}@@', raw):
    fo=m.start(); rva=fo2rva(fo-16)
    if rva is None: continue
    tds[rva]=raw[fo:m.end()].decode('ascii','replace')
print('TD count', len(tds))
tdset=set(tds)
# COLs: sig=1,offset,cd,td_rva
cols={}
for va,vs,fo,rs in secs:
    # scan only likely rdata
    pass
for fo in range(0, len(raw)-16, 4):
    sig,off,cd,td=struct.unpack_from('<IIII',raw,fo)
    if sig==1 and td in tdset and off<0x10000 and cd<0x10000000:
        rva=fo2rva(fo)
        if rva is not None: cols[rva]=(td,off,cd)
print('COL count', len(cols))
colrva=set(cols)
# vtables: 8-byte pointer to col_va
vt={}  # vtable_va -> class
for va,vs,fo,rs in secs:
    for o in range(0, rs-8, 8):
        v=struct.unpack_from('<Q',raw,fo+o)[0]
        if not (base<=v<base+pe.OPTIONAL_HEADER.SizeOfImage): continue
        r=v-base
        if r in colrva:
            vtrva=fo2rva(fo+o+8)
            if vtrva: vt[base+vtrva]=list(cols[r])
print('vtable count', len(vt))
fams={}
pat=re.compile(r'\.\?AV(PERSON|PLAYER|OFFICIAL|NON_PLAYER|STAFF|HUMAN|PERSON_)', re.I)
out={}
for vva,(td,off,cd) in vt.items():
    nm=tds[td]
    if nm.endswith('@db@@') and pat.search(nm):
        out[hex(vva)]=nm
for k in sorted(out, key=lambda x:int(x,16)): print(k, out[k])
json.dump({k:v for k,v in out.items()}, open('scratch/t103/probe/person_vtables.json','w'), indent=1)
print(len(out))
