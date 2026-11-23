import sys, struct, runpy, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
d=json.load(open('scratch/t104/path.json'))
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
raw=m['load_payload_mf'](codec,'server',24,cache)
ident=d['ident']
print('len',len(raw))
for off in range(0,64,16):
    print(off, raw[off:off+16].hex())
print('--- boundary row0 end 136 ---')
for off in range(120,176,8):
    print(off, raw[off:off+8].hex())
print('--- tail ---')
print(len(raw), raw[-32:].hex())
