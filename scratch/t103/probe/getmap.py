import re, sys, json
def fourcc(v):
    return v.to_bytes(4,'little').decode('latin1')
def parse(path):
    txt=open(path, encoding='utf-8', errors='replace').read()
    lines=txt.splitlines()
    # find case labels with numeric constants and their blocks
    out=[]
    idxs=[i for i,l in enumerate(lines) if re.match(r'\s*(case \d+:|if \( a2 == \d+ \))', l)]
    for n,i in enumerate(idxs):
        l=lines[i]
        m=re.search(r'(case |a2 == )(\d+)', l)
        val=int(m.group(2))
        end = idxs[n+1] if n+1<len(idxs) else len(lines)
        block='\n'.join(lines[i:end])
        offs=[int(x) for x in re.findall(r'a1 \+ (\d+)', block)]
        offs2=[int(x,16) for x in re.findall(r'a1 \+ 0x([0-9a-fA-F]+)', block)]
        out.append(dict(line=i+1, val=val, cc=fourcc(val) if 32<=val<0x80000000 else None,
                        offs=sorted(set(offs+offs2)), block=block))
    return out
for p in ('scratch/t95/funcs/141439760.c','scratch/t95/funcs/14143a1a0.c','scratch/t95/funcs/14437ef40.c','scratch/t95/funcs/14437f2a0.c'):
    print('#####',p)
    for e in parse(p):
        print('  line %4d  %-10s offs=%s'%(e['line'], repr(e['cc']), [hex(x) for x in e['offs']]))
