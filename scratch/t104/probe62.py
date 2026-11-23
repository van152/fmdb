import re, json, collections
def c4(n):
    return n.to_bytes(4,'little').decode('latin-1')
src=open('scratch/t95/funcs/1411f1090.c',encoding='utf-8',errors='replace').read()
nums=sorted(set(int(m) for m in re.findall(r'\bcase (\d+):',src)))
print('distinct case consts',len(nums))
four=[n for n in nums if 0x20202020<n<0x7f7f7f7f]
print('printable-4CC count',len(four))
print([c4(n) for n in four][:40])
# count distinct 4CC-looking literals anywhere
lit=sorted(set(int(m) for m in re.findall(r'(?<![\w.])(1[0-9]{9})(?![\w.])',src)))
print('10-digit literals',len(lit))
print([c4(n) for n in lit][:20])
