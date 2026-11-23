import re, json, collections
def c4(n): return n.to_bytes(4,'little').decode('latin-1')
def cases(path):
    src=open(path,encoding='utf-8',errors='replace').read()
    return src, sorted(set(int(m) for m in re.findall(r'\bcase (\d+):',src)))
s1,c1=cases('scratch/t95/funcs/1411f1090.c')
s2,c2=cases('scratch/t95/funcs/1411f4f70.c')
A,B=set(c1),set(c2)
print('f1090',len(A),'f4f70',len(B),'union',len(A|B),'inter',len(A&B),'only1090',len(A-B),'only4f70',len(B-A))
# hub offsets per 4cc
def hubmap(src):
    lines=src.split('\n')
    idx=[i for i,l in enumerate(lines) if re.match(r'\s*case \d+:',l)]
    out=collections.defaultdict(set)
    for k,i in enumerate(idx):
        n=int(re.match(r'\s*case (\d+):',lines[i]).group(1))
        j=idx[k+1] if k+1<len(idx) else len(lines)
        blk='\n'.join(lines[i:j])
        for off in re.findall(r'sub_14083D4F0\([^;]*?\)\s*\+\s*(\d+)', blk): out[c4(n)].add(int(off))
        for off in re.findall(r'a1\[(\d+)\]', blk): out[c4(n)].add(('idx',int(off)))
    return out
h1=hubmap(s1); h2=hubmap(s2)
allc=sorted(set(h1)|set(h2))
print('4cc total', len(allc))
withoff=[c for c in allc if h1.get(c) or h2.get(c)]
print('with hub off', len(withoff))
print(json.dumps({c: sorted(map(str,h1.get(c,set())|h2.get(c,set()))) for c in withoff[:12]}, indent=0)[:600])
