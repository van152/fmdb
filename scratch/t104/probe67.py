import sys, struct, runpy, collections, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
d=json.load(open('scratch/t104/path.json'))
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
raw=m['load_payload_mf'](codec,'server',24,cache)
ident=d['ident']; lens=d['lens']; n=len(ident); sel=[x[2] for x in ident]
print('lens[48:53]',lens[48:53])
print('ident gaps 48..53',[ident[i+1][0]-ident[i][0] for i in range(48,53)])
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
    if p!=len(b): return None
    return b[p-28-10:p-28]
# model T (trailer): body ends at ident[i][0]
# model H (header): body = [ident[i][0]+13, +lens[i])
def try_model(mode):
    okT=0; okH=0; mism=0
    for i in range(n):
        if mode=='T':
            s=14 if i==0 else ident[i-1][0]+13
            b=raw[s:ident[i][0]]
        else:
            b=raw[ident[i][0]+13:ident[i][0]+13+lens[i]]
        r=parse(b,0) or parse(b,49)
        if r is None: return ('FAIL',i,mode)
        blk=r
        u=struct.unpack_from('<I',blk,6)[0] if len(blk)==10 else None
        if u==ident[i][1]: okT+=1
        else: mism+=1
    return (okT,mism)
for mode in ('T','H'):
    print(mode, try_model(mode))
