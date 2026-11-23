import sys, struct, runpy, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
d=json.load(open('scratch/t104/path.json'))
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
raw=m['load_payload_mf'](codec,'server',24,cache)
ident=d['ident']; lens=d['lens']; n=len(ident); sel=[x[2] for x in ident]
for i in (48,49,50,51,52,91,92,93,94,95):
    st=ident[i][0]
    print(i, 'ident@',st, raw[st:st+13].hex(), '->', struct.unpack_from('<III',raw,st), raw[st+12])
print()
starts=[14]+[ident[i][0]+13 for i in range(n-1)]
b=raw[starts[50]:starts[50]+lens[50]]
print('row50 body len',len(b))
for o in range(0,49):
    print(o, '%02x'%b[o], end='  |  ')
    if o%8==7: print()
print()
