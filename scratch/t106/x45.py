import pathlib,sys,struct
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
def hx(x): return ' '.join(f'{c:02x}' for c in x)
b=(D/'payload_server_table_for_old_save_25.bin').read_bytes()
for off in range(0,200,16):
    print(f'{off:6d}',hx(b[off:off+16]),''.join(chr(c) if 32<=c<127 else '.' for c in b[off:off+16]))
print('--- row0 identity candidates')
for p in range(12,200):
    v=struct.unpack_from('<I',b,p)[0]
    if v<3 and struct.unpack_from('<I',b,p+4)[0]==struct.unpack_from('<I',b,p+8)[0]:
        print(p,v,struct.unpack_from('<I',b,p+4)[0])
print('--- last row region 1464400')
for off in range(1464400,1464951,16):
    print(f'{off:8d}',hx(b[off:off+16]),''.join(chr(c) if 32<=c<127 else '.' for c in b[off:off+16]))
