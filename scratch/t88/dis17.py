import capstone,re,collections
b=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
BO=0x140000a00
# candidate windows: any occurrence of disp8 0x5e after modrm with mod=01
hits=[]
for m in re.finditer(rb'\x5e', b):
    i=m.start()
    if i<2: continue
    modrm=b[i-1]
    if (modrm>>6)!=1: continue
    op=b[i-2]
    if op in (0x88,0x89,0xc6,0xc7,0x8a,0x8b,0x0f,0x38,0x3a,0x80,0x81):
        rm=modrm&7; reg=(modrm>>3)&7
        hits.append((i,modrm,reg,rm))
print('hits',len(hits))
# group by proximity
groups=[]
for i,modrm,reg,rm in hits:
    if groups and i-groups[-1][-1][0]<0x200: groups[-1].append((i,modrm,reg,rm))
    else: groups.append([(i,modrm,reg,rm)])
print('clusters',len(groups))
cnt=0
for g in groups:
    lo=max(0,g[0][0]-0x120); hi=min(len(b),g[-1][0]+0x180)
    try:
        ins=list(md.disasm(b[lo:hi],lo+BO))
    except: continue
    txt=[f'{i.mnemonic} {i.op_str}' for i in ins]
    has4c=sum(1 for t in txt if '+ 0x4c]' in t)
    has5e=sum(1 for t in txt if '+ 0x5e]' in t)
    if has4c and has5e:
        cnt+=1
        print(f'CLUSTER @fo {lo:#x} va {lo+BO:#x} 4c={has4c} 5e={has5e}')
print('co-occurring clusters',cnt)
