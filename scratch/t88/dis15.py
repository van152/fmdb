import capstone,struct,re,json
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
        if 0x20202020<=v<=0x7a7a7a7a: tags[cc(v)]=v
entry=lo
def run(tag):
    v=tags[tag]; k=addr[entry]; path=[]; offs=set(); seq=[]
    for _ in range(400):
        if k>=len(ins): break
        i=ins[k]; seq.append(i)
        if i.mnemonic=='ret': break
        nxt=None
        if i.mnemonic=='cmp' and i.op_str.startswith('edx, 0x'):
            c=int(i.op_str.split(', ')[1],16); nxt=(v<c and -1) or (v>c and 1) or 0
        elif i.mnemonic=='cmp' and i.op_str.startswith('edx, '):
            nxt=None
        m=re.search(r'\[rdi \+ (0x[0-9a-f]+)\]',i.op_str)
        if m: offs.add(m.group(1))
        j=i.mnemonic
        if j.startswith('j'):
            t=i.op_str
            if j=='jmp' and t.startswith('0x'):
                k=addr.get(int(t,16),k+1); continue
            if nxt is not None and t.startswith('0x'):
                take = {'je':nxt==0,'jne':nxt!=0,'jg':nxt>0,'jle':nxt<=0,'ja':nxt>0,'jbe':nxt<=0,
                        'jge':nxt>=0,'jl':nxt<0,'jb':nxt<0,'jae':nxt>=0}.get(j)
                if take is not None:
                    k=addr.get(int(t,16),k+1) if take else k+1; continue
            if j in ('je','jne') and t.startswith('0x'): pass
        k+=1
    return offs,seq
out={}
for tag in sorted(tags):
    offs,seq=run(tag)
    out[tag]=dict(offsets=sorted(offs),n=len(seq),
                  tail=[f'{i.address:x} {i.mnemonic} {i.op_str}' for i in seq[-6:]])
    print(tag,sorted(offs))
json.dump(out,open('scratch/t88/tag_offsets.json','w'),indent=1)
