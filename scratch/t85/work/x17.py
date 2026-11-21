import sys
sys.path.insert(0,'scratch/t85/work'); sys.stdout.reconfigure(encoding='utf-8')
import common as C
needles=[b'Algeria',b'ALGERIA',b'Alg\xc3\xa9rie',b'People\'s Democratic']
for arch in ('client','server'):
    ents,_=C.entries(arch)
    for e in ents:
        if 'name_table' not in e['path']: continue
        raw=C.payload(arch,e['path'],int(e['size']))
        h={n.decode('latin-1'):raw.count(n) for n in needles if raw.count(n)}
        print(arch,e['path'],h)
