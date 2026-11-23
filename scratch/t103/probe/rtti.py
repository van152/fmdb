import sys, struct, re
sys.path.insert(0, r'D:\tmp2b\tools\python')
raw=open(r'D:\tmp2b\fm24\input\editor.exe','rb').read()
import pefile
pe=pefile.PE(r'D:\tmp2b\fm24\input\editor.exe', fast_load=True)
base=pe.OPTIONAL_HEADER.ImageBase
secs=[(s.VirtualAddress, s.Misc_VirtualSize, s.PointerToRawData, s.SizeOfRawData, s.Name.rstrip(b'\x00').decode()) for s in pe.sections]
for s in secs: print(s)
def rva2fo(rva):
    for va,vs,fo,rs,n in secs:
        if va<=rva<va+max(vs,rs): return fo+(rva-va)
    return None
def fo2rva(fo):
    for va,vs,rf,rs,n in secs:
        if rf<=fo<rf+rs: return va+(fo-rf)
    return None
# scan for type descriptors: .?AVNAME@@ preceded by vtable etc. Simply find b'.?AV' occurrences
names={}
for m in re.finditer(rb'\.\?AV[A-Za-z0-9_@?$<>]{2,120}@@', raw):
    fo=m.start(); nm=raw[fo:m.end()].decode('ascii','replace')
    names.setdefault(nm, fo)
print('TD names', len(names))
pat=re.compile(r'(PLAYER|NON_PLAYER|OFFICIAL|PERSON|STAFF|HUMAN|PEOPLE|PERSON_)', re.I)
hits={k:v for k,v in names.items() if pat.search(k)}
print('person-ish', len(hits))
for k in sorted(hits)[:200]:
    print('  ', k, hex(hits[k]))
