import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
raw=lib.load_member('lang_update','8_3.dat')
seg=raw[12:109]
print('record1 len',len(seg))
for o in range(0,len(seg)):
    b=seg[o]
    print(f'{o:3d} {b:02x} {chr(b) if 32<=b<127 else "."}')
