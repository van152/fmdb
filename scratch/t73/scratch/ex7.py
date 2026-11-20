import runpy, sys, struct
sys.argv=['x']
dump = runpy.run_path('scripts/fm24_dump.py', run_name='notmain')
codec = dump['_reader']()
raw=dump['load_payload'](codec,'client',2)
n=struct.unpack_from('<I',raw,8)[0]; S=43
for h in (13,14):
    oki=okd=0; tails={}
    for i in range(n):
        body=raw[h+i*S:h+(i+1)*S]
        r=struct.unpack_from('<I',body,30)[0]
        u1=struct.unpack_from('<I',body,34)[0]; u2=struct.unpack_from('<I',body,38)[0]
        oki+= (r==i); okd += (u1==u2 and u1!=0)
        tails[body[-1]]=tails.get(body[-1],0)+1
    print(f'h={h}: rdui@30==row {oki}/{n}; duni@34==@38 nonzero {okd}/{n}; last-byte hist {tails}')
    print('   row0 body', raw[h:h+S].hex())
