import sys, struct, runpy, collections, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
d=json.load(open('scratch/t104/path.json'))
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
raw=m['load_payload_mf'](codec,'server',24,cache)
H=14; T=13; ident=d['ident']; n=len(ident)
def body(i):
    s=H if i==0 else ident[i-1][0]+T
    return raw[s:ident[i][0]]
sel=[x[2] for x in ident]
TEAM=[('+0xb0',1),('+0xab',1),('+0xa8',2),('+0x50',4),('+0x60',4),('+0x58',4),('+0x78',4),('+0x80',4),
      ('+0x98',4),('+0xaf',1),('+0x68',4)]
NATP=[('+0xb8',4),('+0xbc',4),('+0xdc',4),('+0xe0',1),('+0xc0',4),('+0xcc',4),('+0xd0',4),('+0xd4',4),
      ('+0xd8',4),('+0xc4',4),('+0xc8',4),('+0xe1',1),('+0xe2',1),('+0xe4',1),('+0xe5',1),('+0xe6',1),('+0xe7',1),('+0xe3',1)]
def dump(b, layout):
    p=0; out=[]
    for name,w in layout:
        v=int.from_bytes(b[p:p+w],'little'); out.append((name,w,v)); p+=w
    return out,p
i=0
b=body(i)
print('row0 len',len(b))
o,p=dump(b,TEAM); print('as TEAM prefix:',o,'p',p)
print(' count@33', struct.unpack_from('<H',b,33)[0])
o2,p2=dump(b,NATP); print('as NAT prefix:',o2,'p',p2,'cnt byte',b[48])
# try nat-first then team
o3,p3=dump(b[49:], TEAM); print('nat->team:',o3,'p',p3,'count',struct.unpack_from('<H',b,49+33)[0])
# row 1162
i=1162; b=body(i); print('\nrow1162 len',len(b))
o,p=dump(b,TEAM); print('as TEAM:',o)
print(' count@33',struct.unpack_from('<H',b,33)[0])
o2,p2=dump(b,NATP); print('as NAT:',o2,'cnt',b[48])
