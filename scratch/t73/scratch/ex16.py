import runpy, sys, struct, collections
import numpy as np
sys.argv=['x']
dump = runpy.run_path('scripts/fm24_dump.py', run_name='notmain')
codec = dump['_reader']()

def getrows(arch,tid,n,S,H):
    raw=dump['load_payload'](codec,arch,tid)
    return raw, np.frombuffer(raw,dtype=np.uint8,count=n*S,offset=H).reshape(n,S)

# region: locate identity, then test 4-byte grids at different relative origins
for arch,n,S in (('client',28,45),('server',28,46)):
    raw=dump['load_payload'](codec,arch,19)
    H=len(raw)-n*S-8
    M=np.frombuffer(raw,dtype=np.uint8,count=n*S,offset=H).reshape(n,S)
    print('=====',arch,'H',H,'S',S,'footer',raw[-9:].hex())
    for d in range(0,4):
        cols=[]
        for o in range(d,S-12-3,4):
            v=M[:,o:o+4].copy().view('<u4').ravel()
            cols.append((o, int(v.max()), len(np.unique(v))))
        print('  grid@',d,cols)
