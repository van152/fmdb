import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
raw=lib.load_member('lang_update','8_3.dat')
print('len',len(raw))
for o in range(0,200,16):
    print(f'{o:4d}', raw[o:o+16].hex(' '), ''.join(chr(c) if 32<=c<127 else '.' for c in raw[o:o+16]))
print('tail', raw[-32:].hex(' '))
