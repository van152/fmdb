import sys, struct, runpy, collections, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
d=json.load(open('scratch/t104/path.json'))
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
raw=m['load_payload_mf'](codec,'server',24,cache)
ident=d['ident']; lens=d['lens']; n=len(ident); sel=[x[2] for x in ident]
starts=[14]+[ident[i][0]+13 for i in range(n-1)]
def body(i): return raw[starts[i]:starts[i]+lens[i]]
CONST=bytes.fromhex('01006c0701006c0701006c071a01006c07'+'00'*22+'64000000')[:49]
print('const49 len',len(CONST), CONST.hex())
def parse(b,pre):
    p=pre
    if p+35>len(b): return None
    c=struct.unpack_from('<H',b,p+33)[0]
    if p+35+4*c>len(b): return None
    p=p+35+4*c
    if p+28>len(b): return None
    p+=28
    for _ in range(2):
        if p+5>len(b): return None
        l=struct.unpack_from('<I',b,p)[0]
        if p+4+l+1>len(b) or b[p+4+l]!=0: return None
        s=b[p+4:p+4+l]
        if 0 in s: return None
        try: s.decode('utf-8')
        except: return None
        p+=4+l+1
    return p==len(b)
pre=[i for i in range(n) if body(i)[:49]==CONST]
print('rows with const49 at head', len(pre))
prev_sel=collections.Counter(sel[i-1] if i else 'none' for i in pre)
print('prev selector', prev_sel)
print('own selector', collections.Counter(sel[i] for i in pre))
