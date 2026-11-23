import capstone,struct,re,json
b=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
BO=0x140000a00
lo=0x141545680; hi=0x141546200
ins=list(md.disasm(b[lo-BO:hi-BO],lo))
addr={i.address:k for k,i in enumerate(ins)}
def cc(v): return struct.pack('<I',v)[::-1].decode('latin1')
tags={}
for k,i in enumerate(ins):
    if i.mnemonic=='cmp' and i.op_str.startswith('ebx, 0x'):
        v=int(i.op_str.split(', ')[1],16)
        if 0x20202020<=v<=0x7a7a7a7a:
            for m in range(k+1,min(k+3,len(ins))):
                if ins[m].mnemonic=='je': tags[int(ins[m].op_str,16)]=cc(v); break
print('tags',len(tags))
starts=sorted(tags)
blocks={}
for t in starts:
    k=addr[t]; acc=[]
    while k<len(ins):
        i=ins[k]
        if i.address in tags and i.address!=t: break
        acc.append(i)
        if i.mnemonic=='ret': break
        k+=1
    blocks[tags[t]]=[f'{i.address:x} {i.mnemonic} {i.op_str}' for i in acc]
for tag,body in blocks.items():
    stores=[l for l in body if re.search(r'\[rsi \+ 0x[0-9a-f]+\], ',l) or 'call' in l]
    print(tag, '|', ' ; '.join(stores[:5]))
json.dump(blocks,open('scratch/t88/record_set_blocks.json','w'),indent=1)
