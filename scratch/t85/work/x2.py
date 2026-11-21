import sys,struct
sys.path.insert(0,'scratch/t85/work'); sys.stdout.reconfigure(encoding='utf-8')
import common as C
# check identity census for name tables: they are 'auxiliary' entries -> run payload anyway
ents,base=C.entries('client')
for e in ents:
    if 'name_table' in e['path']:
        raw=C.payload('client',e['path'],int(e['size']))
        print(e['path'],len(raw))
        for i in range(0,96,16):
            ch=raw[i:i+16]
            print(f'  {i:4d} {ch.hex(" ")}  {"".join(chr(b) if 32<=b<127 else "." for b in ch)}')
        print()
