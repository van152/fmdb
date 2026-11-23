import sys
sys.path.insert(0,'scratch/t85/work'); sys.stdout.reconfigure(encoding='utf-8')
import common as C
raw=C.payload('client','client_db/table_extra_9.dat',83927)
for i in range(0,200,16):
    ch=raw[i:i+16]
    print(f'{i:5d} {ch.hex(" ")}  {"".join(chr(b) if 32<=b<127 else "." for b in ch)}')
