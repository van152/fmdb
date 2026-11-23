import pathlib,sys,struct,collections
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
def get(n): return (D/('payload_summary.bin' if n=='summary' else f'payload_server_{n}.bin')).read_bytes()
def hx(x): return ' '.join(f'{c:02x}' for c in x)

# common_name_links profile
b=get('common_name_links'); cnt=struct.unpack_from('<I',b,8)[0]; S=10
print('cnl cnt',cnt,'close',12+cnt*S==len(b))
for i in range(S):
    vals=[b[12+k*S+i] for k in range(cnt)]
    print(f'  b{i}: distinct={len(set(vals))} top={collections.Counter(vals).most_common(3)}')

# summary 17B body field consistency
s=get('summary')
sep=b'\xff\xff\xff\xff\x03'
offs=[];i=s.find(sep)
while i>=0: offs.append(i); i=s.find(sep,i+1)
bodies=[]
prev=40
for o in offs:
    bodies.append(s[prev:o]); prev=o+5
print('summary bodies',len(bodies),'sizes',collections.Counter(len(x) for x in bodies).most_common(4))
b17=[x for x in bodies if len(x)==17]
print('17B count',len(b17))
for i in range(17):
    vals=[x[i] for x in b17]
    print(f'  b{i}: distinct={len(set(vals))} top={collections.Counter(vals).most_common(2)}')
print('sample 17B rows:',[hx(x) for x in b17[:5]])
print('u32@0 range',min(struct.unpack_from('<I',x,0)[0] for x in b17),max(struct.unpack_from('<I',x,0)[0] for x in b17))
