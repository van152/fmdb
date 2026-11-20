import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
raw=lib.load_member('lang_update','8_3.dat')
seg=raw[316:392]
print('record4 bytes 316..391 len',len(seg))
for o in range(0,len(seg),4):
    print(f'{316+o:4d}', seg[o:o+4].hex(' '), ''.join(chr(c) if 32<=c<127 else '.' for c in seg[o:o+4]))
