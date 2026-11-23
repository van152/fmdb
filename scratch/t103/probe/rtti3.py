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
def fo2rva(fo):
    for va,vs,rf,rs in secs:
        if rf<=fo<rf+rs: return va+(fo-rf)
tds={}
for m in re.finditer(rb'\.\?AV[A-Za-z0-9_@?$<>]{2,120}@@', raw):
    tds[fo2rva(m.start()-16)]=raw[m.start():m.end()].decode('ascii','replace')
tdset=set(tds)
def td_name(rva): return tds.get(rva)
def chd(td_rva):
    # TD: vftable_ptr, spare, CHD rva at +0xC
    fo=rva2fo(td_rva)+0xC
    c=struct.unpack_from('<I',raw,fo)[0]
    if not c: return None
    cfo=rva2fo(c)
    if cfo is None: return None
    attr,nbase=struct.unpack_from('<II',raw,cfo)
    arr=struct.unpack_from('<%dI'%nbase, raw, cfo+8)
    return [td_name(x) for x in arr if td_name(x)]
cols={}
for fo in range(0,len(raw)-16,4):
    sig,off,cd,td=struct.unpack_from('<IIII',raw,fo)
    if sig==1 and td in tdset and off<0x10000:
        cols[fo2rva(fo)]=(td,off)
vt={}
for va,vs,fo,rs in secs:
    for o in range(0,rs-8,8):
        v=struct.unpack_from('<Q',raw,fo+o)[0]
        if not (base<=v<base+pe.OPTIONAL_HEADER.SizeOfImage): continue
        r=v-base
        if r in cols:
            vtrva=fo2rva(fo+o+8)
            if vtrva: vt[base+vtrva]=cols[r][0]
want={0x14187bd28:'BASIC_PERSON',0x14187a428:'PLAYER',0x14187a8f8:'PLAYER2',0x141889da8:'PERSON',0x141888098:'HUMAN_NON_PLAYER1',0x1418880b8:'HUMAN_NON_PLAYER2',0x141888108:'HUMAN_NON_PLAYER3',0x1418c0628:'OFFICIAL1',0x1418c0658:'OFFICIAL2'}
res={}
for vva,label in want.items():
    td=vt.get(vva)
    nm=td_name(td) if td else None
    fo=rva2fo(vva-base)
    slots=[struct.unpack_from('<Q',raw,fo+8*i)[0] for i in range(32)]
    res[label]={'vtable_va':hex(vva),'class':nm,'bases':chd(td) if td else None,'slot19':hex(slots[19]),'slot2':hex(slots[2]),'slot3':hex(slots[3]),'slot20':hex(slots[20]),'slot21':hex(slots[21]),'slots_nonzero':sum(1 for s in slots if s)}
    print(label, json.dumps({k:v for k,v in res[label].items() if k!='slots'}, indent=1))
json.dump(res, open('scratch/t103/probe/person_vtable_detail.json','w'), indent=1)
# also enumerate all db classes with PERSON ancestry
print('\n--- classes whose CHD mentions PERSON/BASIC_PERSON')
for vva,td in vt.items():
    nm=td_name(td)
    if not nm or not nm.endswith('@db@@'): continue
    b=chd(td) or []
    if any('PERSON' in (x or '') for x in b) or 'PERSON' in nm:
        print(hex(vva), nm, b)
