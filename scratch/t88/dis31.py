import capstone,struct,json,re
b=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
BO=0x140000a00
def cc(v): return struct.pack('<I',v)[::-1].decode('latin1')
def is4cc(v): return 0x20202020<=v<=0x7a7a7a7a and all(32<=c<127 for c in struct.pack('<I',v))
for name,lo,hi in (('TC_GET2',0x1411f1090,0x1411f3a00),('TC_SET2',0x1411f3a00,0x1411f6800)):
    ins=list(md.disasm(b[lo-BO:hi-BO],lo))
    lea=set(); cmpimm=set()
    for i in ins:
        if i.mnemonic=='lea' and ' - 0x' in i.op_str and 'rip' not in i.op_str:
            try: v=int(i.op_str.split(' - 0x')[1].rstrip(']'),16)
            except: continue
            if is4cc(v): lea.add(cc(v))
        if i.mnemonic=='cmp' and i.op_str.split(', 0x')[-1] and ', 0x' in i.op_str:
            try: v=int(i.op_str.split(', 0x')[1],16)
            except: continue
            if is4cc(v): cmpimm.add(cc(v))
    print(name,'insns',len(ins),'lea4cc',len(lea),'cmp4cc',len(cmpimm))
    print('  LEA:',' '.join(sorted(lea)))
    print('  CMP:',' '.join(sorted(cmpimm)))
    json.dump({'lea':sorted(lea),'cmp':sorted(cmpimm)},open(f'scratch/t88/{name}_4cc.json','w'))
