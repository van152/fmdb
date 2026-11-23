import pathlib,sys,struct,collections
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
def hx(x): return ' '.join(f'{c:02x}' for c in x)
b=(D/'payload_server_simple_vars.bin').read_bytes()
body=b[34:]
print('body len',len(body))
print('hist',collections.Counter(body).most_common(12))
print('zeros',body.count(0), 'frac',body.count(0)/len(body))
for off in (0,60,3680,4200,24180,25000,len(body)-120):
    print(f'@{off}:',hx(body[off:off+48]))
print('u16 seq @0:',[struct.unpack_from('<H',body,2*i)[0] for i in range(16)])
print('around 3731:',hx(body[3731-16:3731+24]))
print('around 24256:',hx(body[24256-16:24256+24]))
# look for repeating tail pattern 00 00 00 00 00 00 01 02 00 00 00 00 00 00 01 02
pat=b'\x00\x00\x00\x00\x00\x00\x01\x02\x00\x00\x00\x00\x00\x00\x01\x02'
print('pat count',body.count(pat),'first',body.find(pat))
