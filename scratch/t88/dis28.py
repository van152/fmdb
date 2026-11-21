import capstone,re,collections
b=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
BO=0x140000a00
# collect all unique insn addresses that reference +0x4c or +0x5e with base r?x
pat4=re.compile(r'\[(r\w+) \+ 0x4c\]'); pat5=re.compile(r'\[(r\w+) \+ 0x5e\]')
hits4=[];hits5=[]
# linear sweep whole .text is expensive; instead sweep windows around all occurrences of 0x4c/0x5e bytes after modrm
import json
cands=set()
for m in re.finditer(rb'\x4c',b):
    i=m.start()
    if i<3: continue
    if (b[i-1]>>6)!=1: continue
    if b[i-2] in (0x88,0x89,0x8a,0x8b,0xc6,0xc7,0x80,0x81,0x0f): cands.add(i)
print('disp4c cands',len(cands))
# For each, disassemble from i-8 to see the instruction
seen=collections.Counter()
for i in sorted(cands):
    lo=i-10
    try: ins=list(md.disasm(b[lo:i+4],lo+BO))
    except: continue
    for x in ins:
        if x.address<=i+BO<x.address+x.size and pat4.search(x.op_str):
            seen[(x.address,x.mnemonic,x.op_str)]+=1
print('instrs with [reg+0x4c]:',len(seen))
for (a,mn,op),c in seen.most_common(24):
    print(f'  {a:x} {mn} {op}')
json.dump([[a,mn,op,c] for (a,mn,op),c in seen.items()],open('scratch/t88/disp4c_sites.json','w'))
