import sys, struct
sys.path.insert(0, r'D:\tmp2b\fm24\tools\python')
import zstandard as zstd
def dec(path):
    raw=open(path,'rb').read(); i=raw.find(b'\x28\xb5\x2f\xfd')
    out=bytearray(); data=raw[i:]
    while data[:4]==b'\x28\xb5\x2f\xfd':
        o=zstd.ZstdDecompressor().decompressobj(); out+=o.decompress(data)
        if not o.eof: break
        data=o.unused_data
        if not data: break
    return bytes(out)
pl=dec('scratch/data/pl_hist_dt.dat'); npl=dec('scratch/data/non_pl_hist_dt.dat')
print('pl head 0..300:', pl[:300].hex(' '))
print()
for off in (748, 792, 1496, 1540):
    print('pl @%d'%off, pl[off:off+44].hex(' '))
print()
for off in (0, 24, 48):
    print('npl @%d'%off, npl[off:off+24].hex(' '))
print()
print('pl tail', pl[-64:].hex(' '))
print('npl tail', npl[-64:].hex(' '))
print('pl first 16 as u32', struct.unpack_from('<16I', pl, 0))
