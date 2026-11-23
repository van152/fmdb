import re, collections, json
def c4(n): return n.to_bytes(4,'little').decode('latin-1')
def blocks(path):
    lines=open(path,encoding='utf-8',errors='replace').read().split('\n')
    idx=[i for i,l in enumerate(lines) if re.match(r'\s*(case \d+:|if \( \(_DWORD\)a2 (==|!=) \d+\)|\s*if \( \(int\)a2)',l)]
    # use explicit 4cc equality/inequality guards instead
    pat=re.compile(r'(_DWORD\)a2 (?:==|!=) (\d{9,10})|case (\d{9,10}):)')
    marks=[]
    for i,l in enumerate(lines):
        for m in pat.finditer(l):
            n=int(m.group(2) or m.group(3)); marks.append((i,n))
    out=[]
    for k,(i,n) in enumerate(marks):
        j=marks[k+1][0] if k+1<len(marks) else len(lines)
        out.append((n,'\n'.join(lines[i:j])))
    return out
for path in ('scratch/t95/funcs/1411b01b0.c','scratch/t95/funcs/1411b5630.c'):
    bl=blocks(path)
    d={}
    for n,txt in bl:
        offs=[int(x) for x in re.findall(r'a1 \+ (\d+)', txt)]
        if offs: d.setdefault(c4(n),set()).update(offs)
    print(path,'4cc with a1 offsets',len(d))
    print(json.dumps({k:sorted(v) for k,v in list(d.items())[:14]}))
