import runpy, struct
m = runpy.run_path('scripts/t73_mapper_core.py', run_name='x')
u32 = lambda b,o: struct.unpack_from('<I', b, o)[0]
rc = m['load_payload']('client',6); rs = m['load_payload']('server',6)
print('client body triples:')
trip = [rc[14+j*16:14+j*16+3] for j in range(115)]
for j in range(0,115):
    pass
print(' '.join(t.hex() for t in trip[:30]))
print('server rows 0..8:')
for j in range(9):
    print(' ', j, rs[14+j*40:14+j*40+27].hex())
c=set(trip)
print('client 3B distinct combos',len(c))
# does client body equal server first 3 bytes?
same = sum(1 for j in range(115) if rc[14+j*16:14+j*16+3]==rs[14+j*40:14+j*40+3])
print('client body == server body[:3]:',same,'/115')
