import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
raw=lib.load_member('lang_update','8_3.dat')
print('count',struct.unpack_from('<I',raw,8)[0])
print('bytes 12..112:')
for o in range(12,112):
    print(f'{o:4d} {raw[o]:02x} {chr(raw[o]) if 32<=raw[o]<127 else "."}')
