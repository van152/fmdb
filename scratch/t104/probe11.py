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
# rows: 82,217 rows with base 12 => c=0 rows
ex=[]
for i in range(n):
    if sel[i]!=10: continue
    b=body(i)
    c=struct.unpack_from('<H',b,33)[0]
    if c!=0: continue
    tail=b[53:]
    if len(tail)>=12 and struct.unpack_from('<I',tail,12-12+0)[0] <= 64:
        pass
    ex.append((i,b))
print('c=0 TEAM rows', len(ex))
for i,b in ex[:6]:
    print(i,len(b),'c',struct.unpack_from('<H',b,33)[0])
    print('   body',b.hex())
    print('   tail12',b[53:65].hex(),'len tail',len(b)-53)
