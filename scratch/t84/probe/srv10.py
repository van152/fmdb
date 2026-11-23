import sys, struct, re
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
raw=lib.load_member('server','table_10.dat')
print('len',len(raw),'cnt',struct.unpack_from('<I',raw,8)[0])
for o in range(0,120,16):
    print(f'{o:4d}', raw[o:o+16].hex(' '), ''.join(chr(c) if 32<=c<127 else '.' for c in raw[o:o+16]))
# look for utf16
print('utf16 England?', raw.find('England'.encode('utf-16-le')))
print('utf8 England?', raw.find(b'England'))
print('any printable run>=8:', [(m.start(),m.group()[:40]) for m in re.finditer(rb'[ -~]{8,}',raw)][:5])
