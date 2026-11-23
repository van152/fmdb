import re, json, collections
def c4(n):
    b=n.to_bytes(4,'little')
    return ''.join(chr(c) if 32<=c<127 else '.' for c in b)
def blocks(path):
    lines=open(path,encoding='utf-8',errors='replace').read().split('\n')
    idx=[i for i,l in enumerate(lines) if re.match(r'\s*case \d+:',l)]
    out=[]
    for k,i in enumerate(idx):
        n=int(re.match(r'\s*case (\d+):',lines[i]).group(1))
        j=idx[k+1] if k+1<len(idx) else len(lines)
        out.append((n,'\n'.join(lines[i:j])))
    return out
for path in ('scratch/t95/funcs/1411f1090.c','scratch/t95/funcs/1411f4f70.c'):
    bl=blocks(path)
    stats=collections.Counter()
    rows=[]
    for n,txt in bl:
        a1off=re.findall(r'\*\([^)]*?\)a1 \+ (\d+)', txt)
        a1idx=re.findall(r'\ba1\[(\d+)\]', txt)
        hub=re.findall(r'sub_14083D4F0\([^)]*\)\s*\+\s*(\d+)', txt)
        rows.append((c4(n), len(txt), sorted(set(a1off)), sorted(set(a1idx)), sorted(set(hub))))
        stats['has_a1off' if a1off else 'no_a1off']+=1
        stats['has_hub' if hub else 'no_hub']+=1
    print('==',path, stats)
    for r in rows[:8]: print(r)
    print('len dist', collections.Counter(min(r[1]//100,9) for r in rows))
