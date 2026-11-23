import pathlib,sys,struct
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
s=(D/'payload_summary.bin').read_bytes()
T=1637009+5
print('tail start',T,'len',len(s)-T)
for off in range(T,len(s),16):
    print(f'{off:8d}',s[off:off+16].hex(' '),''.join(chr(c) if 32<=c<127 else '.' for c in s[off:off+16]))
