import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
raw=lib.load_member('lang_update','8_3.dat')
print('len',len(raw),'parsed_end 26362, remaining',len(raw)-26362)
for o in range(26362, 26362+96, 16):
    print(f'{o:6d}', raw[o:o+16].hex(' '), ''.join(chr(c) if 32<=c<127 else '.' for c in raw[o:o+16]))
print('...tail...')
for o in range(len(raw)-64, len(raw), 16):
    print(f'{o:6d}', raw[o:o+16].hex(' '))
