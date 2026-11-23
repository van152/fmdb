import json,capstone
d=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
base=0x140000000
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
disp=json.load(open('scratch/t88/out3/tcget2_dispatch.json'))
print('n',len(disp),'with entry',sum(1 for v in disp.values() if v.get('entry_va')))
def dis(va,n=12):
    fo=va-base
    return ["%x %s %s"%(i.address-base,i.mnemonic,i.op_str) for i in md.disasm(d[fo:fo+48],va)][:n]
for code in ('Tkg3','TCht','CWLg','TVca','CWLe','PLgn','Cmna','TCmg'):
    v=disp[code]; print('##',code,v.get('entry_va'))
    if v.get('entry_va'): print('  '+' | '.join(dis(int(v['entry_va'],16),8)))
