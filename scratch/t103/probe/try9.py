import sys, struct
sys.path.insert(0, r'D:\tmp2b\fm24\tools\python')
import importlib.util
spec = importlib.util.spec_from_file_location("tr", r"scripts/t95_unicorn_trace.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
emu = m.EditorEmulator()
emu.mu.mem_map(0, 0x10000); emu.mu.mem_write(0, b"\x00"*0x10000)
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
row=bp[5:5+83]
for a7 in (0,1):
    r=emu.trace_read(0x140E4FD70, row[1:], version=0x0df1, a7=a7)
    print('a7=%d ok=%s consumed=%d reads=%d err=%s'%(a7,r['ok'],r['bytes_consumed'],r['read_count'],r['error']))
    for x in r['reads']:
        print('   pos=%-3d n=%-2d off=%-6s hex=%s'%(x['wire_pos'],x['n'],x.get('obj_off'),x.get('hex')))
    print('   un',r['unhandled_calls'][:3])
# also dump obj memory after
mem=bytes(emu.mu.mem_read(m.THIS_BASE, 0x80))
print('obj dump', mem.hex(' '))
