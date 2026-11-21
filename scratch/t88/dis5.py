import capstone,struct
b=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
# TC_GET2 at fo 0x11f0690 ; VA = fo + 0x400000? check: 0x11f0ca7 -> VA 0x1411f16a7 ; diff = 0x1411f16a7-0x11f0ca7
print(hex(0x1411f16a7-0x11f0ca7))
base_off=0x1411f16a7-0x11f0ca7
fo=0x11f0690; base=fo+base_off
ins=list(md.disasm(b[fo:fo+0x3000],base))
print('first',hex(ins[0].address),ins[0].mnemonic,ins[0].op_str,'n',len(ins))
# find lea with big negative displacement (4CC subtract)
for i in ins[:1400]:
    if i.mnemonic=='lea' and ' - 0x' in i.op_str and 'rip' not in i.op_str:
        print(hex(i.address), i.op_str)
