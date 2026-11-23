import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
for nm in ('8_0.dat','8_25.dat','8_5.dat','8_2.dat'):
    raw=lib.load_member('lang_update',nm)
    print(f'== {nm} len={len(raw)} cnt={struct.unpack_from("<I",raw,8)[0]}')
    for o in range(12,12+56,4):
        print(f'  {o:4d}', raw[o:o+4].hex(' '), ''.join(chr(c) if 32<=c<127 else '.' for c in raw[o:o+4]))
