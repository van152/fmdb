import pathlib,sys,struct,collections
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
def get(n): return (D/('payload_summary.bin' if n=='summary' else f'payload_server_{n}.bin')).read_bytes()
def hx(x): return ' '.join(f'{c:02x}' for c in x)

# summary framing
s=get('summary'); sep=b'\xff\xff\xff\xff\x03'
offs=[];i=s.find(sep)
while i>=0: offs.append(i); i=s.find(sep,i+1)
bodies=[];prev=40
for o in offs:
    bodies.append(s[prev:o]); prev=o+5
tail=s[prev:]
print('hdr40 + sum(body+5) =',40+sum(len(x)+5 for x in bodies),'len',len(s),'tail',len(tail))
print('closure with tail', 40+sum(len(x)+5 for x in bodies)+len(tail)==len(s))
# tail structure: 17B? then?
print('tail head',hx(tail[:40]))
# does tail start with a 17B body + sep?
print('tail 17:',hx(tail[:17]),'next5:',hx(tail[17:22]))
# variable bodies
for L in (28,41,1019):
    ex=[x for x in bodies if len(x)==L][:2]
    for e in ex: print(L,hx(e))
# count u32@8=7 header ids
print('hdr',hx(s[:40]))
# tail: last (u32,f32) pairs
p=len(s)
print('last 9',hx(s[-9:]))
# find start of float-pair list: scan backwards pairs of (u32,f32) ending with ffffffff
idx=len(s)-4
print('term',hx(s[idx:]))
