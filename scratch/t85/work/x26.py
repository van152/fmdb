import sys
sys.path.insert(0,'scratch/t85/work'); sys.stdout.reconfigure(encoding='utf-8')
import common as C
for arch in ('client',):
    ents,_=C.entries(arch)
    for e in ents:
        raw=C.payload(arch,e['path'],int(e['size']))
        for n in (b'E\x00n\x00g\x00l\x00a\x00n\x00d\x00', b'England'):
            if raw.count(n): print(arch,e['path'],n[:8],raw.count(n))
