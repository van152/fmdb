import capstone,struct,json
b=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
BO=0x140000a00
va0=0x1411f1090
ins=list(md.disasm(b[va0-BO:va0-BO+0x3a00],va0))
addr={i.address:k for k,i in enumerate(ins)}
def cc(v): return struct.pack('<I',v)[::-1].decode('latin1')
out=[]
for k,i in enumerate(ins):
    if i.mnemonic=='lea' and i.op_str.startswith('eax, [rsi - 0x'):
        base=int(i.op_str.split(' - 0x')[1].rstrip(']'),16)
        j=ins[k+1]
        if not (j.mnemonic=='cmp' and j.op_str.startswith('eax, 0x')): continue
        n=int(j.op_str.split(', ')[1],16)
        j2=ins[k+2]
        if j2.mnemonic not in ('jbe','ja'): continue
        j3=ins[k+3]
        if not (j3.mnemonic=='lea' and 'rip' in j3.op_str): continue
        j4=ins[k+4]
        if 'rax*4' not in j4.op_str: continue
        tbl=int(j3.op_str.split('rip + 0x')[1].rstrip(']'),16)+j3.address+j3.size
        # read n+1 s32 entries, relative to tbl
        ents=[struct.unpack_from('<i',b,tbl-BO+q*4)[0]+tbl for q in range(n+1)]
        rows=[]
        for d,va in enumerate(ents):
            kk=addr.get(va)
            if kk is None: rows.append((d,None,None,None)); continue
            rt=tag=None; first=None
            for m in range(4):
                if kk+m>=len(ins): break
                o=ins[kk+m]
                if o.mnemonic=='mov' and o.op_str.startswith('dl, 0x') and rt is None:
                    rt=int(o.op_str.split(', ')[1],16)
                if o.mnemonic=='mov' and o.op_str.startswith('r8d, 0x') and tag is None:
                    tag=int(o.op_str.split(', ')[1],16)
            rows.append((d,rt,cc(tag) if tag and 0x20202020<=tag<=0x7a7a7a7a else None,hex(va)))
        out.append(dict(sw_base=cc(base),base=hex(base),n=n,tbl=hex(tbl),
                        lea=hex(i.address),rows=rows))
print('switches',len(out))
for s in out: print(s['sw_base'],s['base'],'n',s['n'],'tbl',s['tbl'])
json.dump(out,open('scratch/t88/tcget_switches.json','w'),indent=1)
