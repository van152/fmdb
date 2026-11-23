import sys, struct, runpy, collections, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
d=json.load(open('scratch/t104/path.json'))
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
raw=m['load_payload_mf'](codec,'server',24,cache)
ident=d['ident']; lens=d['lens']; n=len(ident); sel=[x[2] for x in ident]
starts=[14]+[ident[i][0]+13 for i in range(n-1)]
def body(i): return raw[starts[i]:starts[i]+lens[i]]
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
rows=[]
for i in range(n):
    b=body(i); a=parse(b,0); c=parse(b,49)
    v = 49 if (c and not a) else (0 if (a and not c) else ('ambig' if a and c else None))
    rows.append((i, ident[i][1], ident[i][2], v, len(b)))
mis=[r for r in rows if r[3] not in (0,49) or (r[2]==11)!=(r[3]==49)]
print('anomalies',len(mis))
print('ambig/fail', [r for r in rows if r[3] not in (0,49)][:5])
for r in mis[:20]: print(r)
print('uid ranges: sel11 pre49', min(r[1] for r in rows if r[2]==11 and r[3]==49), max(r[1] for r in rows if r[2]==11 and r[3]==49))
print('sel10 pre49 count', sum(1 for r in rows if r[2]==10 and r[3]==49))
print('sel11 pre0 count', sum(1 for r in rows if r[2]==11 and r[3]==0))
print('sel11 pre49 count', sum(1 for r in rows if r[2]==11 and r[3]==49))
