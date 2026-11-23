import re
def c4(n):
    b=n.to_bytes(4,'little')
    return ''.join(chr(c) if 32<=c<127 else '.' for c in b)
for f in ('1411f4f70','1411f1090','1411d1730','1411d2f80','1411b01b0','1411b5630'):
    src=open('scratch/t95/funcs/%s.c'%f,encoding='utf-8',errors='replace').read()
    cases=sorted(set(int(m) for m in re.findall(r'\bcase (\d+):',src)))
    four=[n for n in cases if 0x20202020<n<0x7f7f7f7f]
    print(f, 'cases',len(cases),'4cc',len(four), [c4(n) for n in four][:12])
