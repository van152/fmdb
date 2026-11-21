import capstone,struct,re,json,collections
b=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
BO=0x140000a00
lo,hi=0x1415446a0,0x141545680
ins=list(md.disasm(b[lo-BO:hi-BO],lo))
addr={i.address:k for k,i in enumerate(ins)}
def cc(v): return struct.pack('<I',v)[::-1].decode('latin1')
# find cmp edx,imm ; je target
entries=[]
for k,i in enumerate(ins):
    if i.mnemonic=='cmp' and i.op_str.startswith('edx, 0x'):
        v=int(i.op_str.split(', ')[1],16)
        if not (0x20202020<=v<=0x7a7a7a7a): continue
        nxt=ins[k+1]
        if nxt.mnemonic=='je':
            tgt=int(nxt.op_str,16)
            entries.append((cc(v),v,tgt,nxt.address))
print('je entries',len(entries))
def collect(tgt,limit=400):
    k=addr.get(tgt)
    out=[]
    if k is None: return None
    while k<len(ins) and len(out)<limit:
        i=ins[k]
        if i.mnemonic=='ret': break
        if i.mnemonic=='jmp' and i.op_str.startswith('0x'):
            # follow only if forward within function and not a tail to other
            pass
        m=re.search(r'\[rdi \+ (0x[0-9a-f]+)\]',i.op_str)
        if m and i.mnemonic in ('mov','movsxd','lea','cmp','movzx'):
            out.append((hex(i.address),i.mnemonic,i.op_str))
        if i.mnemonic in ('ret',) or (k>0 and k+1<len(ins) and ins[k+1].address==0 and False): break
        k+=1
        if k<len(ins) and ins[k].address in [e[2] for e in entries] and k>0: break
    return out
res={}
for tag,v,tgt,a in entries:
    r=collect(tgt,60)
    res[tag]=r
    print(tag,hex(tgt),'->', [x[2] for x in (r or [])][:8])
json.dump(res,open('scratch/t88/record_get_handlers.json','w'),ensure_ascii=False)
