import capstone,struct,json
b=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
BO=0x140000a00
va0=0x1411f1090
ins=list(md.disasm(b[va0-BO:va0-BO+0x3a00],va0))
addr={i.address:k for k,i in enumerate(ins)}
def cc(v): return struct.pack('<I',v)[::-1].decode('latin1')
sw=[]
for k,i in enumerate(ins):
    if i.mnemonic=='lea' and i.op_str.startswith('eax, [rsi - 0x'):
        base=int(i.op_str.split(' - 0x')[1].rstrip(']'),16)
        j,j2,j3,j4=ins[k+1],ins[k+2],ins[k+3],ins[k+4]
        if not(j.mnemonic=='cmp' and j.op_str.startswith('eax, 0x')): continue
        if j2.mnemonic not in('jbe','ja') or 'rax*4' not in j4.op_str: continue
        n=int(j.op_str.split(', ')[1],16)
        tbl=int(j3.op_str.split('rip + 0x')[1].rstrip(']'),16)+j3.address+j3.size
        ents=[struct.unpack_from('<i',b,tbl-BO+q*4)[0]+tbl for q in range(n+1)]
        rows=[]
        for d,va in enumerate(ents):
            kk=addr.get(va); rt=tag=None
            if kk is not None:
                for m in range(0,10):
                    if kk+m>=len(ins): break
                    o=ins[kk+m]
                    if rt is None and o.mnemonic=='mov' and o.op_str.startswith('dl, 0x'): rt=int(o.op_str.split(', ')[1],16)
                    if tag is None and o.mnemonic=='mov' and o.op_str.startswith('r8d, 0x'):
                        v=int(o.op_str.split(', ')[1],16)
                        if 0x20202020<=v<=0x7a7a7a7a: tag=cc(v)
                    if rt is not None and tag is not None: break
            rows.append((cc(base+d),rt,tag))
        sw.append((cc(base),rows))
print('switches',len(sw))
m={}
for base,rows in sw:
    for f4,rt,tag in rows:
        m.setdefault(f4,[]).append((rt,tag))
json.dump({k:v for k,v in m.items()},open('scratch/t88/f4_to_rectype.json','w'),indent=1)
print('distinct 4CC mapped',len(m))
for base,rows in sw: print(base,[(f,rt,tg) for f,rt,tg in rows])
