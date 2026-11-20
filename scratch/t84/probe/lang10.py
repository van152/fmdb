import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
raw=lib.load_member('lang_update','8_10.dat')
print('8_10 len',len(raw),'count',struct.unpack_from('<I',raw,8)[0])
for o in range(0,160,16):
    print(f'{o:4d}', raw[o:o+16].hex(' '), ''.join(chr(c) if 32<=c<127 else '.' for c in raw[o:o+16]))
