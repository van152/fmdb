import sys,struct,json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b); n=84477
starts=json.load(open('scratch/t88/rows.json'))['starts']
print('first10',starts[:10])
ok=sum(1 for i,p in enumerate(starts[:200]) if struct.unpack_from('<I',b,p)[0]==i)
print('ordinal match at starts[:200]',ok)
# maybe starts are identity positions: check p-13
ok2=sum(1 for i,p in enumerate(starts[:200]) if struct.unpack_from('<I',b,p-13)[0]==i)
print('ordinal at starts-13',ok2)
# check gap distribution
g=np.diff(np.array(starts)); print('gap min/max',g.min(),g.max(),'first gaps',g[:15])
