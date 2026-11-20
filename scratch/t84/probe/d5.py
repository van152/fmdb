import sys
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
raw=lib.load_member('lang_update','8_3.dat')
for o in range(308,400):
    b=raw[o]
    print(f'{o:4d} {b:02x} {chr(b) if 32<=b<127 else "."}')
