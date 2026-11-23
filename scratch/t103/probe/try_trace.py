import sys, struct, json
sys.path.insert(0, r'D:\tmp2b\fm24\tools\python')
sys.path.insert(0, r'scripts')
import importlib.util
spec = importlib.util.spec_from_file_location("tr", r"scripts/t95_unicorn_trace.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
emu = m.EditorEmulator()
print("emu ok")
def dec(path):
    import zstandard as zstd
    raw = open(path,'rb').read()
    i = raw.find(b'\x28\xb5\x2f\xfd')
    out=bytearray(); data=raw[i:]
    while data[:4]==b'\x28\xb5\x2f\xfd':
        o=zstd.ZstdDecompressor().decompressobj(); out+=o.decompress(data)
        if not o.eof: break
        data=o.unused_data
        if not data: break
    return bytes(out)

dt = dec('scratch/data/pl_hist_dt.dat')
print('pl dt len', len(dt))
for va,name in ((0x144354210,'tt14_read_server'),):
    r = emu.trace_read(va, dt[:400], version=0x0df1)
    print(name, r['ok'], r['error'], 'consumed', r['bytes_consumed'], 'reads', r['read_count'])
    for x in r['reads']:
        print('   ', x)
    print('   unhandled', r['unhandled_calls'][:5])
