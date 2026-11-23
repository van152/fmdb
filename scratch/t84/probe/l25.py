import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
raw=lib.load_member('lang_update','8_25.dat')
print('len',len(raw),'cnt',struct.unpack_from('<I',raw,8)[0])
for o in range(8,220,4):
    chunk=raw[o:o+4]
    print(f'{o:4d}', chunk.hex(' '), ''.join(chr(c) if 32<=c<127 else '.' for c in chunk))
