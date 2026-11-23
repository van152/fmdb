import sys, struct, json
sys.path.insert(0, r'D:\tmp2b\fm24\tools\python')
import importlib.util
spec = importlib.util.spec_from_file_location("tr", r"scripts/t95_unicorn_trace.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
emu = m.EditorEmulator()

def dec(path):
    import zstandard as zstd
    raw = open(path,'rb').read(); i = raw.find(b'\x28\xb5\x2f\xfd')
    out=bytearray(); data=raw[i:]
    while data[:4]==b'\x28\xb5\x2f\xfd':
        o=zstd.ZstdDecompressor().decompressobj(); out+=o.decompress(data)
        if not o.eof: break
        data=o.unused_data
        if not data: break
    return bytes(out)

def show(tag, va, payload, a7=1, a5=0, a6=0, ver=0x0df1):
    r = emu.trace_read(va, payload, version=ver, a5=a5, a6=a6, a7=a7)
    print(f'-- {tag} ok={r["ok"]} err={r["error"]} consumed={r["bytes_consumed"]} reads={r["read_count"]}')
    for x in r['reads']:
        print('    pos=%-3d n=%-2d off=%-6s kind=%-6s hex=%s u=%s' % (x['wire_pos'], x['n'], x.get('obj_off'), x.get('dst_kind'), x.get('hex'), x.get('u_val')))
    if r['unhandled_calls']: print('    UNHANDLED', r['unhandled_calls'][:4])
    return r

dt14 = dec('scratch/data/pl_hist_dt.dat')
dt44 = dec('scratch/data/non_pl_hist_dt.dat')
show('tt14 slot19 a7=1', 0x144354210, dt14[:400])
show('tt14 slot21 write', 0x144354740, dt14[:400])
show('tt44 slot19 a7=1', 0x14437E8D0, dt44[:400])
show('tt44 slot21 write', 0x14437EAE0, dt44[:400])
