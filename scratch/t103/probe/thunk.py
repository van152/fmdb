import sys, struct
sys.path.insert(0, r'D:\tmp2b\tools\python')
import pefile
pe=pefile.PE(r'D:\tmp2b\fm24\input\editor.exe', fast_load=True)
raw=open(r'D:\tmp2b\fm24\input\editor.exe','rb').read()
base=pe.OPTIONAL_HEADER.ImageBase
secs=[(s.VirtualAddress, s.Misc_VirtualSize, s.PointerToRawData, s.SizeOfRawData) for s in pe.sections]
def va2fo(va):
    rva=va-base
    for v,vs,fo,rs in secs:
        if v<=rva<v+max(vs,rs):
            d=rva-v
            if d<rs: return fo+d
for va in (0x141438db0,0x141438f70,0x141438fd0,0x141454370,0x1414544e0,0x141454800,0x141454c20,0x144354210,0x14437e8d0,0x140e50170,0x140e53ba0):
    fo=va2fo(va)
    b=raw[fo:fo+8]
    tgt=None
    if b[0]==0xe9:
        rel=struct.unpack_from('<i',b,1)[0]; tgt=va+5+rel
    print(hex(va), b.hex(' '), '->', hex(tgt) if tgt else '')
