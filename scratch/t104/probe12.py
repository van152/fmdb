import sys, struct, runpy, collections, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
d=json.load(open('scratch/t104/path.json'))
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
raw=m['load_payload_mf'](codec,'server',24,cache)
H=14; T=13; ident=d['ident']; n=len(ident); lens=d['lens']
def body(i):
    s=H if i==0 else ident[i-1][0]+T
    return raw[s:ident[i][0]]
sel=[x[2] for x in ident]
TEAM=[('+0xb0',176,1),('+0xab',171,1),('+0xa8',168,2),('+0x50',80,4),('+0x60',96,4),('+0x58',88,4),
      ('+0x78',120,4),('+0x80',128,4),('+0x98',152,4),('+0xaf',175,1),('+0x68',104,4),
      ('vec',None,2),('+0x88',136,4),('+0x90',144,4),('+0xaa',170,1),('+0xac',172,1),
      ('+0xad',173,1),('+0xae',174,1),('+0xb1',177,1),('+0x70',112,4),('+0xb2',178,1)]
for i in [56,60,89,50]:
    b=body(i); print('row',i,'len',len(b))
    p=0
    for name,off,w in TEAM:
        v=int.from_bytes(b[p:p+w],'little'); p+=w
        print('   ',name,w,v)
    c=struct.unpack_from('<H',b,33)[0]
    print('   remaining',len(b)-p, b[p:].hex())
