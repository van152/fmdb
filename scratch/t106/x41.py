import pathlib,sys,struct
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
def hx(x): return ' '.join(f'{c:02x}' for c in x)
b=(D/'payload_server_table_for_old_save_23.bin').read_bytes()
print('len',len(b),'count@8',struct.unpack_from('<I',b,8)[0])
print('hdr 0..40:',hx(b[:40]))
for i in range(4):
    o=15+14*i; print(f'row{i}@{o}:',hx(b[o:o+14]), struct.unpack_from('<IIIH',b,o))
print('...')
for i in range(275,278):
    o=15+14*i; print(f'row{i}@{o}:',hx(b[o:o+14]) if o+14<=len(b) else 'OOB', struct.unpack_from('<IIIH',b,o) if o+18<=len(b) else '')
print('tail 3880..:',hx(b[3880:]))
