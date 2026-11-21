import capstone,struct,json,re
b=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
BO=0x140000a00
lo,hi=0x1411f1090,0x1411f3a00
ins=list(md.disasm(b[lo-BO:hi-BO],lo))
addr={i.address:k for k,i in enumerate(ins)}
def cc(v): return struct.pack('<I',v)[::-1].decode('latin1')
def is4cc(v): return 0x20202020<=v<=0x7a7a7a7a
cps=[]
for k,i in enumerate(ins):
    if i.mnemonic=='cmp' and ', 0x' in i.op_str:
        try: v=int(i.op_str.split(', 0x')[1],16)
        except: continue
        if is4cc(v): cps.append((k,i.address,cc(v)))
print('cmp4cc sites',len(cps))
cpset={a for _,a,_ in cps}
out={}
for k,a,tag in cps:
    rt=None; t2=None; j=k+1
    steps=0
    while j<len(ins) and steps<60:
        o=ins[j]
        if o.address in cpset and o.address!=a: break
        if o.mnemonic=='mov' and o.op_str.startswith('dl, 0x') and rt is None:
            try: rt=int(o.op_str.split(', ')[1],16)
            except: rt=None
        if o.mnemonic=='mov' and o.op_str.startswith('r8d, 0x') and t2 is None:
            try:
                vv=int(o.op_str.split(', ')[1],16)
                if is4cc(vv): t2=cc(vv)
            except: pass
        if o.mnemonic=='jmp' and o.op_str.startswith('0x'):
            j=addr.get(int(o.op_str,16),j+1); steps+=1; continue
        j+=1; steps+=1
    out.setdefault(tag,[]).append((hex(a),rt,t2))
json.dump(out,open('scratch/t88/tcget2_cmp_dispatch.json','w'),indent=1)
for t,v in sorted(out.items()): print(f'{t:5s} {v}')
