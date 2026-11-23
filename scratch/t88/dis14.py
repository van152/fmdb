import capstone,struct,re,json
b=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
BO=0x140000a00
lo,hi=0x1415446a0,0x141545680
ins=list(md.disasm(b[lo-BO:hi-BO],lo))
addr={i.address:k for k,i in enumerate(ins)}
tagaddrs={}
for k,i in enumerate(ins):
    if i.mnemonic=='cmp' and i.op_str.startswith('edx, 0x'):
        v=int(i.op_str.split(', ')[1],16)
        if 0x20202020<=v<=0x7a7a7a7a and ins[k+1].mnemonic=='je':
            tagaddrs[int(ins[k+1].op_str,16)]=struct.pack('<I',v)[::-1].decode('latin1')
starts=sorted(tagaddrs)
def block(start):
    """walk until ret or next tag entry or backward jmp out."""
    k=addr[start]; out=[]
    while k<len(ins):
        i=ins[k]
        if i.address in tagaddrs and i.address!=start: break
        out.append(i)
        if i.mnemonic=='ret': break
        k+=1
        if k>=len(ins): break
    return out
res={}
for s in starts:
    tag=tagaddrs[s]; blk=block(s)
    touches=[]
    for i in blk:
        for m in re.finditer(r'\[(rdi|rcx|rbx|rsi|rdx) \+ (0x[0-9a-f]+)\]',i.op_str):
            if m.group(1)=='rdi': touches.append((m.group(2),i.mnemonic,i.op_str))
    res[tag]=dict(entry=hex(s),n=len(blk),touches=touches[:12],
                  text=[f'{i.address:x} {i.mnemonic} {i.op_str}' for i in blk][:18])
    print(tag,hex(s),len(blk),'offs',sorted({t[0] for t in touches}))
json.dump(res,open('scratch/t88/record_get_handlers.json','w'),ensure_ascii=False,indent=1)
