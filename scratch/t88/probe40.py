import struct,json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends']); sl=np.array(d['strlen'])
n=len(starts); ne=starts+41+sl
club=np.array(sorted(json.load(open('scratch/t88/club.json'))['uids']),dtype=np.int64)
c25=open('scratch/t88/t25.bin','rb').read()
print('comp payload',len(c25),'n',struct.unpack_from('<I',c25,8)[0])
# u32 date4 both orders at row-start offsets and name_end offsets
def scan(anchor,label,rng):
    print(f'== {label} ==')
    for o in rng:
        p=anchor+o
        if p.min()<0 or p.max()+4>L: continue
        v=np.array([int.from_bytes(b[int(x):int(x)+4],'little') for x in p],dtype=np.uint64)
        lo=(v&0xffff).astype(np.int64); hi=(v>>16).astype(np.int64)
        f1=float(((lo>=1)&(lo<=366)&(hi>=1850)&(hi<=2120)).mean())
        f2=float(((hi>=1)&(hi<=366)&(lo>=1850)&(lo<=2120)).mean())
        ff=float((v==0xffffffff).mean())
        if max(f1,f2)>0.5 or ff>0.9:
            print(f'  {o:4d} doy_year={f1:.3f} year_doy={f2:.3f} allff={ff:.3f}')
scan(ne,'name_end',range(0,30))
scan(starts,'row_start',range(0,67))
