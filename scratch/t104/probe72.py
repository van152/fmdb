import re, collections
def c4(n):
    b=n.to_bytes(4,'little'); return ''.join(chr(c) if 32<=c<127 else '.' for c in b)
for path in ('scratch/t95/funcs/1411f1090.c','scratch/t95/funcs/1411f4f70.c'):
    lines=open(path,encoding='utf-8',errors='replace').read().split('\n')
    idx=[i for i,l in enumerate(lines) if re.match(r'\s*case \d+:',l)]
    print('==',path,'cases',len(idx))
    grp=collections.Counter(); rows=[]
    for k,i in enumerate(idx):
        n=int(re.match(r'\s*case (\d+):',lines[i]).group(1))
        j=idx[k+1] if k+1<len(idx) else len(lines)
        body='\n'.join(lines[i+1:j])
        first=[l.strip() for l in body.split('\n') if l.strip()][:1]
        gotos=re.findall(r'goto (LABEL_\d+)', body)
        rows.append((c4(n), n, first[0][:60] if first else '', gotos[:2]))
    for r in rows[:12]: print(r)
    for r in rows:
        grp[(r[2][:40], tuple(r[3]))]+=1
    for k,v in grp.most_common(10): print(v,k)
