import pathlib,sys,struct
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
b=(D/'payload_server_simple_vars.bin').read_bytes()
def hx(x): return ' '.join(f'{c:02x}' for c in x)
print('len',len(b))
for off in range(0,320,16):
    print(f'{off:5d}',hx(b[off:off+16]),''.join(chr(c) if 32<=c<127 else '.' for c in b[off:off+16]))
print('--- u32 seq from 12')
print([struct.unpack_from('<I',b,12+4*i)[0] for i in range(20)])
print('--- ascii runs')
import re
runs=[(m.start(),m.group().decode()) for m in re.finditer(rb'[ -~]{4,}',b)]
print(len(runs)); print(runs[:40])
