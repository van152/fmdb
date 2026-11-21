import capstone,struct,json,re
b=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
BO=0x140000a00
lo,hi=0x1411f1090,0x1411f3a00
ins=list(md.disasm(b[lo-BO:hi-BO],lo))
addr={i.address:k for k,i in enumerate(ins)}
def cc(v): return struct.pack('<I',v)[::-1].decode('latin1')
def is4cc(v): return 0x20202020<=v<=0x7a7a7a7a
REG=re.compile(r'^(e?[a-z]{2,3})$')
def val(op,st):
    op=op.strip()
    m=re.fullmatch(r'(rsi|esi)',op)
    if m: return st.get('rsi')
    if re.fullmatch(r'0x[0-9a-f]+',op): return int(op,16)
    m2=re.fullmatch(r'eax',op)
    if m2: return st.get('eax')
    if re.fullmatch(r'-\s*0x[0-9a-f]+',op): return None
    return None
def walk(target):
    k=addr[lo]; st={'rsi':target}; flags=None; steps=0
    while k<len(ins) and steps<3000:
        i=ins[k]; steps+=1
        op=i.op_str; mn=i.mnemonic
        if mn=='lea' and op.startswith('eax, [rsi - 0x'):
            base=int(op.split(' - 0x')[1].rstrip(']'),16); st['eax']=target-base
        elif mn=='lea' and op.startswith('eax, [rsi + 0x'):
            base=int(op.split(' + 0x')[1].rstrip(']'),16); st['eax']=target+base
        elif mn=='cmp' and ', ' in op:
            a,bb=op.split(', ',1); va,vb=val(a,st),val(bb,st)
            flags=(va-vb) if (va is not None and vb is not None) else None
        elif mn in ('je','jne','jg','jle','ja','jbe','jge','jl','js','jns','jb','jae'):
            tgt=int(op,16) if op.startswith('0x') else None
            take=None
            if flags is not None:
                take={'je':flags==0,'jne':flags!=0,'jg':flags>0,'jle':flags<=0,'ja':flags>0,
                      'jbe':flags<=0,'jge':flags>=0,'jl':flags<0,'jb':flags<0,'jae':flags>=0,
                      'js':flags<0,'jns':flags>=0}[mn]
            if take is None: return None
            if take and tgt is not None:
                k=addr.get(tgt)
                if k is None: return None
                flags=None; continue
        elif mn=='jmp' and op.startswith('0x'):
            k=addr.get(int(op,16)); 
            if k is None: return None
            continue
        elif mn=='mov' and op.startswith('dl, 0x'):
            st['dl']=int(op.split(', ')[1],16)
        elif mn=='mov' and op.startswith('r8d, 0x'):
            vv=int(op.split(', ')[1],16)
            if is4cc(vv): st['r8d']=cc(vv)
        elif mn=='ret':
            return st
        k+=1
        if k is None: return None
    return st
# gather 117 cmp 4CCs
cps={}
for k,i in enumerate(ins):
    if i.mnemonic=='cmp' and ', 0x' in i.op_str:
        try: v=int(i.op_str.split(', 0x')[1],16)
        except: continue
        if is4cc(v): cps[cc(v)]=v
print('4CC count',len(cps))
res={}
for tag,v in sorted(cps.items()):
    s=walk(v)
    res[tag]=dict(rt=s.get('dl'),tag=s.get('r8d')) if s else None
json.dump(res,open('scratch/t88/f4_dispatch.json','w'),indent=1)
ok=[t for t in res if res[t] and res[t]['tag']]
print('resolved',len(ok),'/',len(res))
for t in sorted(res): print(f'{t:5s} {res[t]}')
