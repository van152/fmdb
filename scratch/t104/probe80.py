import re
src=open('scratch/t95/funcs/1411d1730.c',encoding='utf-8',errors='replace').read()
pat=re.compile(r'\(v191,\s*([A-Za-z0-9_&\+\-\*\(\) ]+?),\s*([A-Za-z0-9_]+)\)\)', re.S)
rows=[]
for m in pat.finditer(src):
    tgt=' '.join(m.group(1).split()); size=m.group(2)
    rows.append((src[:m.start()].count('\n')+1, tgt, size))
print(len(rows))
for r in rows: print(r)
