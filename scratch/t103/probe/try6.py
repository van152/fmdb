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
CL={1:83,2:83,3:83,4:34,5:22}
cnt=struct.unpack_from('<I',bp,0)[0]
pos=5; first={}
for i in range(cnt):
    cls=bp[pos+1]; L=CL[cls]
    if cls not in first: first[cls]=(i,pos)
    pos+=L
    if len(first)==5: break
for cls,(i,p0) in sorted(first.items()):
    row=bp[p0:p0+CL[cls]]
    print('== class',cls,'rowlen',len(row),'tag',hex(row[0]),'cls',row[1],'body(no tag,no ident)',CL[cls]-1-12)
    for s in (1,):
        r=emu.trace_read(0x140E4FD70, row[s:], version=0x0df1, a7=1)
        print('  start+%d ok=%s consumed=%d reads=%d err=%s unhandled=%s' % (s,r['ok'],r['bytes_consumed'],r['read_count'],r['error'],r['unhandled_calls'][:2]))
        for x in r['reads']:
            print('    pos=%-3d n=%-2d off=%-6s hex=%s' % (x['wire_pos'],x['n'],x.get('obj_off'),x.get('hex')))
