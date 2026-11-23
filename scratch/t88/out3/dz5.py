import json,capstone
d=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
base=0x140000000
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
disp=json.load(open('scratch/t88/tcget2_cmp_dispatch.json'))
for code in ('CBWo','CBWf','CHSo','CHSf','CYPp','CHRa','CHRf','CMAp','CGMg','CBDo'):
    v=disp.get(code)
    print('##',code,v)
    if not v: continue
    for ent in v[:2]:
        va=int(ent[0],16); fo=va-base
        for i in md.disasm(d[fo:fo+40],va):
            print('   %x %s %s'%(i.address-base,i.mnemonic,i.op_str))
        print('   ---')
