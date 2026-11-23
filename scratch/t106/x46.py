import pathlib,sys,struct
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
def get(n): return (D/f'payload_server_{n}.bin').read_bytes()
def hx(x): return ' '.join(f'{c:02x}' for c in x)

b=get('table_for_old_save_25'); cnt=struct.unpack_from('<I',b,8)[0]
pat=b'\x01\xe0\x7f\x01\x00\x6c\x07\x01\x00\x6c\x07\x00\x00\xff'
pos=[];i=b.find(pat)
while i>=0: pos.append(i); i=b.find(pat,i+1)
print('old25 pat count',len(pos),'cnt',cnt,'first',pos[:3],'last',pos[-2:])
ok=all(struct.unpack_from('<I',b,p+14)[0]==k for k,p in enumerate(pos))
print('ordinal seq ok',ok,'first start',12,'closure',12+ (pos[-1]+26-12) +9, len(b))
print('row0 span',pos[0]+26-12,'row1 span',pos[1]-pos[0])
uids=[struct.unpack_from('<II',b,p+18) for p in pos]
print('uid pairs equal',sum(1 for a,c in uids if a==c),'sentinel',sum(1 for a,c in uids if a==0xffffffff))

# fantasy
f=get('fantasy_draft_future_regens'); fc=struct.unpack_from('<I',f,8)[0]
print()
print('fantasy len',len(f),'count',fc,'header',hx(f[:16]))
mp=[];i=f.find(b'\x01\x00\x6c\x07')
while i>=0: mp.append(i); i=f.find(b'\x01\x00\x6c\x07',i+1)
print('markers',len(mp),mp[:5],mp[-3:])
for k in range(len(mp)-1):
    if k<3 or k>len(mp)-3:
        print(' row',k,'marker@',mp[k],'span',(mp[k+1]-mp[k]))
print('tail after last marker',len(f)-mp[-1],hx(f[mp[-1]:]))
print('row0 head',hx(f[12:80]))
