import runpy, sys, struct
sys.argv=['x']
dump = runpy.run_path('scripts/fm24_dump.py', run_name='notmain')
codec = dump['_reader']()
def show(arch, tid, n=3, stride=None):
    raw = dump['load_payload'](codec, arch, tid)
    print(f"--- {arch} {tid} len={len(raw)} first14={raw[:14].hex()} last8={raw[-8:].hex()}")
    for i in range(n):
        b = 14 + i*stride
        row = raw[b:b+stride]
        print(i, b, row.hex())
        print('   u32s:', [hex(x) for x in struct.unpack_from('<%dI'%(len(row)//4), row, 0)])
        print('   f32@0,1,2:', [struct.unpack_from('<f', row, j)[0] for j in (0,1,2)])
show('client',2,3,43)
show('client',5,3,34)
show('server',5,7,48)
show('client',19,3,45)
show('server',19,2,(1310-14-8)//28)
