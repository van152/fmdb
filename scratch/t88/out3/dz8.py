import json,capstone
d=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
base=0x140000000
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
disp=json.load(open('scratch/t88/out3/tcget2_dispatch.json'))
ents=[int(v['entry_va'],16) for v in disp.values() if v.get('entry_va')]
print('entries',len(ents),hex(min(ents)),hex(max(ents)))
def dis(va,n=14):
    fo=va-base
    return ["%x %s %s"%(i.address-base,i.mnemonic,i.op_str) for i in md.disasm(d[fo:fo+56],va)][:n]
for t in (0x1411f1cf6,0x1411f1d06,0x1411f2a60,0x1411f2a95,0x1411f2a5a):
    print('##',hex(t)); print('  '+'\n  '.join(dis(t,10)))
print('--- 0x13d90a0 bytes', d[0x13d90a0:0x13d90b0].hex())
print('--- 0x13d90a0 as ptr', hex(int.from_bytes(d[0x13d90a0:0x13d90a8],'little')))
