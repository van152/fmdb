import capstone,re,json,collections
b=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
BO=0x140000a00
lo=0x1415446a0
ins=list(md.disasm(b[lo-BO:lo-BO+0x1000],lo))
lines=[f'{i.address:x} {i.bytes.hex()} {i.mnemonic} {i.op_str}' for i in ins]
open('scratch/t88/record_get.asm','w').write('\n'.join(lines))
pat=re.compile(r'\[(rdi) \+ (0x[0-9a-f]+)\]')
cnt=collections.Counter()
for i in ins:
    if i.mnemonic in ('mov','movsxd','movzx','cmp','lea','movss','movsd'):
        for m in pat.finditer(i.op_str):
            if i.op_str.startswith(m.group(0)) or (', '+m.group(0) in i.op_str) or ('[' in i.op_str and m.start()==i.op_str.find('[')):
                cnt[m.group(2)]+=1
print('rdi offsets touched (as memory operand anywhere):')
for o,k in sorted(cnt.items(), key=lambda x:int(x[0],16)):
    print(' ',o,k)
