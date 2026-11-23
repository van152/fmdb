import importlib.util, re, collections
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe=pm.default(); raw=pe.raw
md=Cs(CS_ARCH_X86, CS_MODE_64)
start=0xe57de0
va=pe.f2va(start)
ins=list(md.disasm(raw[start:start+0x4000], va))
print('insn',len(ins))
acc=collections.Counter()
mem=re.compile(r"\[(r[a-z0-9]+)(?:\s*\+\s*(0x[0-9a-f]+))?\]")
for i in ins:
    m=mem.search(i.op_str)
    if m and i.mnemonic.startswith('mov'):
        acc[(m.group(1), m.group(2))]+=1
for k,v in acc.most_common(25): print(k,v)
print('calls', sum(1 for i in ins if i.mnemonic=='call'))
print('tail jmps', collections.Counter(i.op_str for i in ins if i.mnemonic=='jmp').most_common(5))
