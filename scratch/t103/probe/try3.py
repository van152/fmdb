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
dt14 = dec('scratch/data/pl_hist_dt.dat')
print('payload[0:48]', dt14[:48].hex(' '))
r = emu.trace_read(0x144354210, dt14[:400], version=0x0df1, a7=1)
print('consumed', r['bytes_consumed'])
for x in r['reads']:
    print('  pos=%-3d n=%-2d off=%-6s hex=%s' % (x['wire_pos'], x['n'], x.get('obj_off'), x.get('hex')))
