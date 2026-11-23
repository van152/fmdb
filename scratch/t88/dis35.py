import capstone,struct,json
b=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
BO=0x140000a00
d=json.load(open('scratch/t88/tcget_switches.json'))
s=[x for x in d if x['sw_base']=='CHSa'][0]
def cc(v): return struct.pack('<I',v)[::-1].decode('latin1')
for row in s['rows']:
    va=int(row[3],16)
    print(f'--- idx {row[0]} {cc(0x43485361+row[0])} -> {hex(va)}')
    n=0
    for i in md.disasm(b[va-BO:va-BO+64],va):
        print(f'   {i.address:x} {i.mnemonic} {i.op_str}'); n+=1
        if n>=5: break
