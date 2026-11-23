import pathlib,sys,struct
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
f=(D/'payload_server_fantasy_draft_future_regens.bin').read_bytes()
def hx(x): return ' '.join(f'{c:02x}' for c in x)
marks=[];i=f.find(b'\x01\x00\x6c\x07')
while i>=0: marks.append(i); i=f.find(b'\x01\x00\x6c\x07',i+1)
starts=[12]+[m+4 for m in marks[:-1]]
for k in range(3):
    s=starts[k]; e=marks[k]
    print(f'--- row{k} start={s} bodylen={e-s}')
    print(hx(f[s:e]))
    print('tail16 of body:',hx(f[e-16:e]))
print('tail region',hx(f[5626:]))
# scan whole file for u32 pairs equal
for p in range(12,len(f)-8):
    a=struct.unpack_from('<I',f,p)[0]; b2=struct.unpack_from('<I',f,p+4)[0]
    if a==b2 and a>1000: print('pair eq @',p,a)
