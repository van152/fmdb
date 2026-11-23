import capstone,re,sys
b=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
BO=0x140000a00
def find(va_lo,va_hi,pat):
    ins=list(md.disasm(b[va_lo-BO:va_hi-BO],va_lo))
    return [f'{i.address:x} {i.mnemonic} {i.op_str}' for i in ins if re.search(pat,i.op_str)]
print('=== 0x4c accesses 0x140c5c000..0x140c5e000 ===')
for l in find(0x140c5c000,0x140c5e000,r'\+ 0x4c\]'): print(' ',l)
print('=== 0x5e accesses ===')
for l in find(0x140c5c000,0x140c5e000,r'\+ 0x5e\]'): print(' ',l)
