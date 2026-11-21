import sys
sys.path.insert(0,'scratch/t85/work'); sys.stdout.reconfigure(encoding='utf-8')
import common as C
targets=[b'Algeria',b'Les Fennecs',b'ALGERIA',b'England',b'China PR']
for arch in ('client','server'):
    ents,_=C.entries(arch)
    for e in ents:
        raw=C.payload(arch,e['path'],int(e['size']))
        hits={t:raw.count(t) for t in targets if raw.count(t)}
        if hits: print(arch,e['path'],hits)
