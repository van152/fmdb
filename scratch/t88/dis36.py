import capstone,struct,json
b=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
BO=0x140000a00
d=json.load(open('scratch/t88/tcget_switches.json'))
def cc(v): return struct.pack('>I',v).decode('latin1')
def rd(va,n): return b[va-BO:va-BO+n]
out={}
for s in d:
    base=struct.unpack('>I',s['sw_base'].encode())[0]
    tbl=int(s['tbl'],16)
    rows=[]
    for k in range(len(s['rows'])):
        va=struct.unpack_from('<Q',rd(tbl+8*k,8))[0]
        if not (0x140000000<va<0x141000000+0x200000): break
        dl=None; tag=None; j=0
        for i in md.disasm(rd(va,48),va):
            if i.mnemonic=='mov' and i.op_str.startswith('dl, 0x'): dl=int(i.op_str.split(', ')[1],16)
            if i.mnemonic=='mov' and i.op_str.startswith('r8d, 0x'):
                try:
                    v=int(i.op_str.split(', ')[1],16)
                    if 0x20202020<=v<=0x7a7a7a7a and all(32<=c<127 for c in struct.pack('>I',v)): tag=cc(v)
                except: pass
            if i.mnemonic=='jmp' or i.mnemonic=='ret': break
            j+=1
            if j>8: break
        rows.append([cc(base+k) if base+k<0x7b7b7b7b else None,dl,tag,hex(va)])
    out[s['sw_base']]=dict(base=s['sw_base'],n=len(rows),rows=rows)
json.dump(out,open('scratch/t88/f4_full.json','w'),indent=1)
tot=0
for k,v in out.items():
    good=[r for r in v['rows'] if r[1] is not None]
    print(f"{k} n={v['n']} handlers={len(good)} range={v['rows'][0][0]}..{v['rows'][-1][0]}")
    tot+=len(good)
print('total handlers',tot)
