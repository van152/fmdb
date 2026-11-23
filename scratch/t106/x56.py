import pathlib,sys,struct,collections
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
def get(n): return (D/f'payload_server_{n}.bin').read_bytes()

# club_links column profile
b=get('club_links'); cnt=struct.unpack_from('<I',b,8)[0]; stride=47
print('club_links cnt',cnt,'len',len(b),'close',12+cnt*stride==len(b))
for i in range(stride):
    vals=[b[12+k*stride+i] for k in range(cnt)]
    d=len(set(vals)); top=collections.Counter(vals).most_common(3)
    print(f'  b{i:2d} distinct={d:4d} top={top}')
