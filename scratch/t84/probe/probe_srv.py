import sys, struct, re
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K
for a,t in [('server','10'),('server','25'),('server','3'),('client','10')]:
    raw=K['load_payload'](lib.CODEC,a,t)
    runs=[(m.start(), m.group()[:40]) for m in re.finditer(rb'[ -~]{5,}', raw)]
    print(a,t,'len',len(raw),'runs',len(runs),'first',runs[:5])
