import capstone,struct,json
b=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
BO=0x140000a00
lo,hi=0x1411f1090,0x1411f3a00
ins=list(md.disasm(b[lo-BO:hi-BO],lo))
def cc(v): return struct.pack('>I',v).decode('latin1')
sites=[]
for k,i in enumerate(ins):
    if i.mnemonic=='lea' and i.op_str.startswith('eax, [rsi - 0x'):
        try: base=int(i.op_str.split(' - 0x')[1].rstrip(']'),16)
        except: continue
        n=None; tbl=None
        for j in range(k+1,min(k+14,len(ins))):
            o=ins[j]
            if o.mnemonic=='cmp' and o.op_str.startswith('eax, 0x') and n is None:
                n=int(o.op_str.split(', 0x')[1],16)
            if o.mnemonic=='lea' and 'rcx, [rip' in o.op_str and tbl is None:
                try:
                    d=int(o.op_str.split('rip + ')[1].rstrip(']'),16); tbl=o.address+o.size+d
                except: pass
            if o.mnemonic=='jmp' and tbl and n: break
        sites.append((i.address,base,n,tbl))
print('switch sites',len(sites))
res={}
for a,base,n,tbl in sites:
    if n is None or tbl is None: 
        print('  incomplete',hex(a),cc(base) if base<0x7b7b7b7b else base,n,tbl); continue
    name=cc(base)
    rows=[]
    for idx in range(n+1):
        try: off=struct.unpack_from('<i',b,tbl-BO+4*idx)[0]
        except: break
        va=tbl+off
        dl=None; tag=None; cnt=0
        for i in md.disasm(b[va-BO:va-BO+40],va):
            if i.mnemonic=='mov' and i.op_str.startswith('dl, 0x'): dl=int(i.op_str.split(', ')[1],16)
            if i.mnemonic=='mov' and i.op_str.startswith('r8d, 0x'):
                try:
                    v=int(i.op_str.split(', ')[1],16)
                    if 0x20202020<=v<=0x7a7a7a7a and all(32<=c<127 for c in struct.pack('>I',v)): tag=cc(v)
                except: pass
            if i.mnemonic in ('jmp','ret'): break
            cnt+=1
            if cnt>10: break
        code=cc(base+idx)
        rows.append([code,dl,tag,hex(va)])
    res[name]=dict(site=hex(a),n=n,tbl=hex(tbl),rows=rows)
    print(f'{name} n={n} tbl={hex(tbl)} codes {rows[0][0]}..{rows[-1][0]}')
json.dump(res,open('scratch/t88/f4_all_switches.json','w'),indent=1)
n2=sum(len([r for r in v['rows'] if r[1] is not None]) for v in res.values())
print('handlers with dl:',n2)
