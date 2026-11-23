import re, json, collections
def offs(path, var='a1'):
    src=open(path,encoding='utf-8',errors='replace').read()
    s=set()
    for m in re.finditer(r'\*\s*\(\s*[A-Za-z_][\w ]*\*\s*\)\s*\(\s*%s\s*\+\s*(\d+)\s*\)'%var, src): s.add(int(m.group(1)))
    for m in re.finditer(r'%s\s*\+\s*(\d+)\s*\)\s*=\s*'%var, src): s.add(int(m.group(1)))
    for m in re.finditer(r'\(\s*%s\s*\+\s*(\d+)\s*\)'%var, src): s.add(int(m.group(1)))
    return sorted(s)
for f in ('1411d1730','1411d2f80','1411a1280','1411a1640','141053680','143ee6d10','143ee8cc0','1411b01b0','1411b5630'):
    try:
        o=offs('scratch/t95/funcs/%s.c'%f)
    except FileNotFoundError:
        print(f,'MISSING'); continue
    print(f, len(o), o)
