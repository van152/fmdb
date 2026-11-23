import capstone,re
b=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
BO=0x140000a00
# find all store-to-[reg+0x4c] imm/reg and store-to-[reg+0x5e], then check same function has both
ins_all={}
for va in (0x140c5d2c3,0x140c5d604):
    lo=va-0x600
    ins=list(md.disasm(b[lo-BO:lo-BO+0xc00],lo))
    print('window',hex(lo),'n',len(ins))
    for i in ins:
        if re.search(r'\+(0x4c|0x5e)\]',i.op_str) or ('rsi + 0x3' in i.op_str and i.mnemonic=='mov' and ', ' in i.op_str):
            print(' ',hex(i.address),i.mnemonic,i.op_str)
    print()
