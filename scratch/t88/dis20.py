import capstone,re,collections
b=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
BO=0x140000a00
# candidate store sites to +0x5e
cands=[m.start() for m in re.finditer(rb'\x5e',b)]
found=[]
for i in cands:
    lo=max(0,i-24)
    try: ins=list(md.disasm(b[lo:i+12],lo+BO))
    except: continue
    for k,x in enumerate(ins):
        if x.address+x.size<=i+BO<x.address+x.size+1: continue
        if x.mnemonic=='mov' and re.match(r'(byte|dword) ptr \[r\w+ \+ 0x5e\]', x.op_str):
            found.append((x.address,x.op_str))
            break
print('store-to-0x5e sites',len(found))
for a,o in found: print(hex(a),o)
