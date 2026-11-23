import sys,struct
sys.path.insert(0,'scratch/t85/work'); sys.stdout.reconfigure(encoding='utf-8')
import common as C
raw=C.payload('client','client_db/table_extra_9.dat',83927)
seg=raw[12:12+120]
for i in range(0,len(seg),2):
    print(f'{(12+i):4d} {seg[i:i+2].hex():>6}  {struct.unpack_from("<H",seg,i)[0]:6d}')
