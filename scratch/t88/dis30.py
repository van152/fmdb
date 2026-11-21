import capstone,re,struct,json
b=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
BO=0x140000a00
lo,hi=0x1415446a0,0x141545680
ins=list(md.disasm(b[lo-BO:hi-BO],lo))
addr={i.address:k for k,i in enumerate(ins)}
def cc(v): return struct.pack('<I',v)[::-1].decode('latin1')
tags={}
for k,i in enumerate(ins):
    if i.mnemonic=='cmp' and i.op_str.startswith('edx, 0x'):
        v=int(i.op_str.split(', ')[1],16)
        if 0x20202020<=v<=0x7a7a7a7a and ins[k+1].mnemonic=='je':
            tags[int(ins[k+1].op_str,16)]=cc(v)
tstart=sorted(tags)
def block(t):
    k=addr[t]; acc=[]
    while k<len(ins):
        i=ins[k]
        if i.address in tags and i.address!=t: break
        acc.append(i)
        if i.mnemonic=='ret': break
        k+=1
    return acc
res={}
for t in tstart:
    blk=block(t); offs=[]
    for i in blk:
        for m in re.finditer(r'\[rdi \+ (0x[0-9a-f]+)\]',i.op_str):
            offs.append((int(m.group(1),16),i.mnemonic,i.op_str))
    res[tags[t]]=dict(entry=hex(t),n=len(blk),offs=sorted({o for o,_,_ in offs}),
                      detail=[(hex(o),mn,op) for o,mn,op in offs])
    print(f"{tags[t]:5s} entry={t:x} n={len(blk):3d} offs={[hex(o) for o in sorted({o for o,_,_ in offs})]}")
json.dump(res,open('scratch/t88/record_get_tagmap.json','w'),indent=1)
