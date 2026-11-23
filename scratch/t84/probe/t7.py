import sys, struct, re
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
for a in ('client','server'):
    raw=K['load_payload'](lib.CODEC,a,'7')
    print(f'== {a} table_7 len={len(raw)} cnt@8={struct.unpack_from("<I",raw,8)[0]}')
    print('  head', raw[:52].hex(' '))
    runs=[(m.start(),m.group()[:40]) for m in re.finditer(rb'[ -~]{4,}',raw)]
    print('  runs',len(runs),runs[:6])
print()
for a in ('client','server'):
    raw=K['load_payload'](lib.CODEC,a,'18')
    print(f'== {a} table_18 len={len(raw)} cnt@8={struct.unpack_from("<I",raw,8)[0]} runs={len(re.findall(rb"[ -~]{5,}",raw))}')
