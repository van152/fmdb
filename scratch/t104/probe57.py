import re, struct, json, collections
src=open('scratch/t95/funcs/1411f1090.c',encoding='utf-8',errors='replace').read()
lines=src.split('\n')
def c4(n):
    b=n.to_bytes(4,'little')
    try: return b.decode('latin-1')
    except: return None
idx=[i for i,l in enumerate(lines) if re.match(r'\s*case \d+:',l)]
print('cases',len(idx))
out=[]
for k,i in enumerate(idx):
    m=re.match(r'\s*case (\d+):',lines[i]); n=int(m.group(1))
    end=idx[k+1] if k+1<len(idx) else len(lines)
    blk='\n'.join(lines[i:end])
    offs=re.findall(r'a1 \+ (\d+)', blk)
    casts=re.findall(r'\*\(\((\w[\w ]*?) \*\)a1', blk)
    out.append((n, c4(n), offs[:3], casts[:2]))
for o in out[:25]: print(o)
print('...')
print('no-offset cases', sum(1 for o in out if not o[2]))
