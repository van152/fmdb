import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct

def rows_of(arch,tid,n):
    raw=load(arch,tid)
    p,b,_,_ = dp_walk(raw,f'{arch}{tid}',14,len(raw)-8,n)
    return raw, [(s,e) for s,e in [(x[0],x[1]) for x in b]]

raw,rows = rows_of('client',7,208)
for i in (0,1,6):
    s,e=rows[i]
    nl=struct.unpack_from('<I',raw,s)[0]
    print(f'=== row{i} [{s},{e}) len={e-s} name_len={nl}')
    body=raw[s:e]
    # 6B prefix then url
    p=s+4+nl
    print('  6B pre',raw[p:p+6].hex())
    ul=struct.unpack_from('<I',raw,p+6)[0]
    print('  url len',ul,'url',raw[p+10:p+10+ul][:50])
    mid=raw[p+10+ul:e-13]
    print('  mid len',len(mid),'mid hex:',mid.hex(' '))
    # parse: u32 seq at 4-aligned? try aligned u32 stream
    u=[struct.unpack_from('<I',mid,k)[0] for k in range(0,len(mid)-3,4)]
    print('  mid u32 stream:',u)
