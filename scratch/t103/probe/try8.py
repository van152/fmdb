import sys, struct
sys.path.insert(0, r'D:\tmp2b\fm24\tools\python')
import importlib.util
spec = importlib.util.spec_from_file_location("tr", r"scripts/t95_unicorn_trace.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
emu = m.EditorEmulator()
# map page 0 to survive null derefs (probe only)
try:
    emu.mu.mem_map(0, 0x10000)
    emu.mu.mem_write(0, b"\x00"*0x10000)
    print("mapped page0")
except Exception as e:
    print("map fail", e)
import zstandard as zstd
def dec(p):
    raw=open(p,'rb').read(); i=raw.find(b'\x28\xb5\x2f\xfd')
    out=bytearray(); data=raw[i:]
    while data[:4]==b'\x28\xb5\x2f\xfd':
        o=zstd.ZstdDecompressor().decompressobj(); out+=o.decompress(data)
        if not o.eof: break
        data=o.unused_data
        if not data: break
    return bytes(out)
bp=dec('scratch/data/basic_people_db.dat')
CL={1:83,2:83,3:83,4:34,5:22}
cnt=struct.unpack_from('<I',bp,0)[0]; pos=5; first={}
for i in range(cnt):
    cls=bp[pos+1]; L=CL[cls]
    if cls not in first: first[cls]=(i,pos)
    pos+=L
    if len(first)==5: break
for cls,(i,p0) in sorted(first.items()):
    row=bp[p0:p0+CL[cls]]
    r=emu.trace_read(0x140E4FD70, row[1:]+bp[p0+CL[cls]:p0+CL[cls]+64], version=0x0df1, a7=1)
    print('cls%d row=%d ok=%s consumed=%d err=%s' % (cls, CL[cls], r['ok'], r['bytes_consumed'], r['error']))
    for x in r['reads']:
        print('    pos=%-3d n=%-2d off=%-6s hex=%s' % (x['wire_pos'], x['n'], x.get('obj_off'), x.get('hex')))
    if r['unhandled_calls']: print('   UN', r['unhandled_calls'][:3])
