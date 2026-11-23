import capstone,struct,json
b=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
BO=0x140000a00
d=json.load(open('scratch/t88/tcget_switches.json'))
s=[x for x in d if x['sw_base']=='CBWa'][0]
print('CBWa tbl',s['tbl'],'n',s['n'])
def dump(va,n=40):
    for i in md.disasm(b[va-BO:va-BO+n],va):
        print(f'{i.address:x} {i.bytes.hex():18s} {i.mnemonic} {i.op_str}')
for row in s['rows'][:6]:
    print('--- delta',row[0],row[3])
    dump(int(row[3],16),36)
