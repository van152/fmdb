import sys, struct
sys.path.insert(0, r'D:\tmp2b\fm24\tools\python')
import importlib.util
spec = importlib.util.spec_from_file_location("tr", r"scripts/t95_unicorn_trace.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
emu = m.EditorEmulator()
import zstandard as zstd
def dec(path):
    raw = open(path,'rb').read(); i = raw.find(b'\x28\xb5\x2f\xfd')
    out=bytearray(); data=raw[i:]
    while data[:4]==b'\x28\xb5\x2f\xfd':
        o=zstd.ZstdDecompressor().decompressobj(); out+=o.decompress(data)
        if not o.eof: break
        data=o.unused_data
        if not data: break
    return bytes(out)

bp = dec('scratch/data/basic_people_db.dat')
print('bp len', len(bp), 'count', struct.unpack_from('<I',bp,0)[0], 'hdr5', bp[4])
CL={1:83,2:83,3:83,4:34,5:22}
def rows(bp, limit=None):
    cnt=struct.unpack_from('<I',bp,0)[0]; pos=5; i=0
    while i<cnt and (limit is None or i<limit):
        tag=bp[pos]; cls=bp[pos+1]; L=CL[cls]
        yield i, pos, cls, bp[pos:pos+L]
        pos+=L; i+=1
for i,pos,cls,row in rows(bp, 1200):
    if i in (0,89,972,1155,656818):
        print('row',i,'pos',pos,'cls',cls,'len',len(row),row.hex(' ')[:80])
# emulation per class
samples={}
for i,pos,cls,row in rows(bp, 700000):
    if cls not in samples: samples[cls]=(i,pos,row)
    if len(samples)==5: break
print({k:(v[0],v[1]) for k,v in samples.items()})
for cls,(i,pos,row) in sorted(samples.items()):
    r = emu.trace_read(0x140E4FD70, row, version=0x0df1, a7=1)
    print(f'== tt1 class {cls} row {i} ok={r["ok"]} err={r["error"]} consumed={r["bytes_consumed"]} reads={r["read_count"]}')
    for x in r['reads']:
        print('   pos=%-3d n=%-2d off=%-6s hex=%s u=%s' % (x['wire_pos'], x['n'], x.get('obj_off'), x.get('hex'), x.get('u_val')))
    if r['unhandled_calls']: print('   UN', r['unhandled_calls'][:3])
