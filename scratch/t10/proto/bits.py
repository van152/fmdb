import json, collections, importlib.util, re
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe=pm.default(); raw=pe.raw
md=Cs(CS_ARCH_X86, CS_MODE_64)
spec2 = importlib.util.spec_from_file_location("_b","scratch/t07/out/build.py")
b = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(b)
hits, md = b.decode_cmp_hits(pe); hits.sort()
si=json.load(open('scratch/t05/schema_inventory.json',encoding='utf-8'))
clubs={f['code'] for f in si['entities']['club']['fields'] if f['parent'] is None}
A=[h for h in hits if 0xe82afc<=h[0]<0xe846ac]
B=[h for h in hits if 0xe89a34<=h[0]<0xe8cded]
def bitscan(sub,label):
    out=[]
    for off,code,va,_ in sub:
        ins=list(md.disasm(raw[off:off+0x18],va))
        br=next((x for x in ins[1:4] if x.mnemonic in ('je','jz')),None)
        if not br: continue
        t=int(br.op_str,0); tf=pe.va2f(t)
        body=list(md.disasm(raw[tf:tf+0xc0],t))[:30]
        disp=None; bit=None; width=None
        for y in body:
            m=re.search(r"\[(r12|r13|rdi|rsi|rbx|r14|r15)\s*\+\s*(0x[0-9a-f]+)\]", y.op_str)
            if m and y.mnemonic in ('mov','movzx','movsx','test') and disp is None:
                disp=int(m.group(2),16)
                if 'byte' in y.op_str: width=1
                elif 'word' in y.op_str: width=2
                elif 'dword' in y.op_str: width=4
            if y.mnemonic=='shr' and re.match(r'[a-z0-9]+, 0x[0-9a-f]+$', y.op_str):
                bit=int(y.op_str.split(',')[1],16)
            if y.mnemonic=='and' and re.match(r'[a-z0-9]+, 0x[0-9a-f]+$', y.op_str):
                v=int(y.op_str.split(',')[1],16)
                if v and (v&(v+1))==0: bit=v.bit_length()-1
            if y.mnemonic=='bt' and re.match(r'[a-z0-9]+, 0x[0-9a-f]+$', y.op_str):
                bit=int(y.op_str.split(',')[1],16)
            if y.mnemonic=='ret': break
        if disp is not None:
            out.append((code,disp,bit,width))
    c=collections.Counter((d) for _,d,_,_ in out)
    bb=collections.Counter((d,bit) for _,d,bit,_ in out if bit is not None)
    print(f'[{label}] resolved {len(out)}/{len(sub)}; top disp: {[(hex(k),v) for k,v in c.most_common(6)]}')
    print(f'   disp+bit pairs: {len(bb)}; top: {[(hex(d),b,n) for (d,b),n in bb.most_common(12)]}')
    return out
a=bitscan(A,'A'); b2=bitscan(B,'B')
