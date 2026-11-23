import runpy, sys, struct
sys.argv=['x']
dump = runpy.run_path('scripts/fm24_dump.py', run_name='notmain')
codec = dump['_reader']()
raw = dump['load_payload'](codec,'client',41)
print('len',len(raw),'head',raw[:16].hex())
p=14
for i in range(3):
    rec=[]
    for k in range(4):
        n=struct.unpack_from('<I',raw,p)[0]; s=raw[p+4:p+4+n]; p+=4+n; rec.append((n,s.decode('utf-8','replace')))
    f=struct.unpack_from('<f',raw,p)[0]; p+=4
    cnt=struct.unpack_from('<I',raw,p)[0]; p+=4
    print(i,'strings',rec,'rate',f,'hist',cnt)
    print('  next 32B',raw[p:p+32].hex())
    p2=p+7*cnt
    print('  after 7*N:',raw[p2:p2+40].hex())
    # guess trailer 13
    j,u,v,m=struct.unpack_from('<IIIB',raw,p2)
    print('  trailer u32s',j,u,v,m,'rowlen',p2+13-14)
    p=p2+13
print('pos',p,'len',len(raw),'footer',raw[-8:].hex(), 'remaining',len(raw)-p)
