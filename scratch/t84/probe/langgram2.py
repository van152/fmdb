import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
raw=lib.load_member('lang_update','8_3.dat')
for o in range(330, 460, 8):
    print(f'{o:5d}', raw[o:o+8].hex(' '), ''.join(chr(c) if 32<=c<127 else '.' for c in raw[o:o+8]))
