import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
raw=lib.load_member('client','table_3.dat')
for nm in (b'Atl\xc3\xa9tico Petr\xc3\xb3leos de Luanda', b'Liverpool', b'Arsenal'):
    i=raw.find(nm)
    print('==',nm,'at',i)
    print('   prev32', raw[max(0,i-32):i].hex(' '))
    print('   prev24u32', [struct.unpack_from('<I',raw,i-4*k)[0] for k in range(1,7)])
