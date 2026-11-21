import capstone,struct,json
b=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
BO=0x140000a00
lo,hi=0x1411f1090,0x1411f3600
ins=list(md.disasm(b[lo-BO:hi-BO],lo))
def cc(v):
    return struct.pack('<I',v)[::-1].decode('latin1')
pairs=[]
for k,i in enumerate(ins):
    if i.mnemonic=='mov' and i.op_str.startswith('dl, '):
        try: rt=int(i.op_str.split(', ')[1],16)
        except: continue
        # look ahead up to 3 for mov r8d, imm
        for j in range(k+1,min(k+4,len(ins))):
            o=ins[j]
            if o.mnemonic=='mov' and o.op_str.startswith('r8d, 0x'):
                tag=int(o.op_str.split(', ')[1],16)
                if 0x20202020<=tag<=0x7a7a7a7a:
                    pairs.append((i.address,cc(tag),rt,o.address))
                break
print('pairs',len(pairs))
seen={}
for a,tag,rt,b2 in pairs:
    seen.setdefault((tag,rt),[]).append(a)
print('distinct (tag,rectype)',len(seen))
tags=sorted({t for t,_ in seen})
print('tags',len(tags),' '.join(tags))
import collections
c=collections.Counter(rt for _,rt in seen)
print('rec_type hist',sorted(c.items()))
json.dump([[a,t,r,b] for a,t,r,b in pairs],open('scratch/t88/tcget_pairs.json','w'))
