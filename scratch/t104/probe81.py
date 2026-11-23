import re
src=open('scratch/t95/funcs/1411d1730.c',encoding='utf-8',errors='replace').read()
lines=src.split('\n')
out=[]
for i,l in enumerate(lines):
    if '40LL))(' in l or '40LL))(' in ''.join(lines[i:i+3]):
        blk='\n'.join(lines[i:i+4])
        out.append((i+1,' '.join(blk.split())[:170]))
print(len(out))
for o in out[:25]: print(o)
