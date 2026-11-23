import struct
d=open('client_db_t10.bin','rb').read()
body=d[14:len(d)-8]
def dump(a,b,label=''):
    print(f'--- {label} [{a}:{b}]')
    for o in range(a,b,16):
        chunk=body[o:min(b,o+16)]
        print(f'{o:6d} 0x{o:04x}  {chunk.hex(" ")}')
dump(0,80,'row0')
