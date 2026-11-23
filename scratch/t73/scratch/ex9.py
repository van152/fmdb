import runpy, sys, struct
sys.argv=['x']
dump = runpy.run_path('scripts/fm24_dump.py', run_name='notmain')
codec = dump['_reader']()
c=dump['load_payload'](codec,'client',5); s=dump['load_payload'](codec,'server',5)
print('client footer9',c[-9:].hex(),'server footer9',s[-9:].hex())
print('client hdr13',c[:13].hex(),'server hdr13',s[:13].hex())
for i in range(7):
    rc=c[13+i*34:13+(i+1)*34]; rs=s[13+i*48:13+(i+1)*48]
    assert rc[0]==0 and rs[0]==0
    bc,bs=rc[1:],rs[1:]
    print(f'row{i} C body({len(bc)})', bc.hex())
    print(f'     S body({len(bs)})', bs.hex())
    print('     u32C',[hex(x) for x in struct.unpack_from('<5I',bc,0)], 'f32@0',struct.unpack_from('<f',bc,0)[0])
    print('     u32S',[hex(x) for x in struct.unpack_from('<8I',bs,0)])
    print('     bufs', [struct.unpack_from('<H',bc,o)[0] for o in (10,12,14)], 'S', [struct.unpack_from('<H',bs,o)[0] for o in (10,12,14,24,26,28,30,32)])
