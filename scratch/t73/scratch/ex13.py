import runpy, sys, struct
sys.argv=['x']
dump = runpy.run_path('scripts/fm24_dump.py', run_name='notmain')
codec = dump['_reader']()
c=dump['load_payload'](codec,'client',5); s=dump['load_payload'](codec,'server',5)
print('client abs dump first 60:', c[:60].hex())
print('server abs dump first 76:', s[:76].hex())
def show(raw,n,S,h,label):
    print('---',label,'h',h,'S',S)
    for i in range(n):
        b=h+i*S; print(f'  row{i} abs{b}', ' '.join(f'{j:02d}:{x:02x}' for j,x in enumerate(raw[b:b+S])))
show(c,7,34,14,'cont client')
show(s,7,48,14,'cont server')
# f32 at each offset for cont client
for o in range(0,14):
    vals=[struct.unpack_from('<f',c,14+i*34+o)[0] for i in range(7)]
    if all(0.0<v<2.0 for v in vals): print('client f32 plausible at row offset',o,vals)
for o in range(0,14):
    vals=[struct.unpack_from('<f',s,14+i*48+o)[0] for i in range(7)]
    if all(0.0<v<2.0 for v in vals): print('server f32 plausible at row offset',o,vals)
