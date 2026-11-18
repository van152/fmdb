import struct
d=open('client_db_t10.bin','rb').read()
body=d[14:len(d)-8]
def dump(a,b,label=''):
    print(f'--- {label} [{a}:{b}] len={b-a}')
    for o in range(a,b,16):
        print(f'{o:6d} 0x{o:04x}  {body[o:min(b,o+16)].hex(" ")}')
dump(56,215,'rows 0-2 region')
