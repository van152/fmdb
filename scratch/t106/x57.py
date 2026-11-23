import pathlib,sys,struct
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
b=(D/'payload_server_club_links.bin').read_bytes()
cnt=struct.unpack_from('<I',b,8)[0]; S=47
def hx(x): return ' '.join(f'{c:02x}' for c in x)
for k in range(6):
    r=b[12+k*S:12+(k+1)*S]
    print(k,hx(r))
print('u32 grid per row (offset:value) for row0')
r=b[12:12+S]
for o in range(0,44):
    print(o, hex(struct.unpack_from('<I',r,o)[0]))
