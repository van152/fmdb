import sys, struct, runpy, collections
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
raw=m['load_payload_mf'](codec,'server',24,cache)
N=len(raw); H=14; F=8
def body_len(b, pre):
    p=pre
    if p+35>N: return None
    c=struct.unpack_from('<H',raw,p+33)[0]
    p=p+35+4*c
    if p+28>N: return None
    p+=28
    for _ in range(2):
        if p+5>N: return None
        l=struct.unpack_from('<I',raw,p)[0]
        if l>400: return None
        if p+4+l+1>N or raw[p+4+l]!=0: return None
        s=raw[p+4:p+4+l]
        if 0 in s: return None
        try: s.decode('utf-8')
        except: return None
        p+=4+l+1
    return p
pos=H; rows=[]
while True:
    cands=[]
    for pre in (0,49):
        e=body_len(raw,pos+pre)
        if e is None: continue
        if e+13>N: continue
        o,u1,u2,sel=struct.unpack_from('<IIIB',raw,e)
        if o==len(rows) and u1==u2: cands.append((pre,e,o,u1,sel))
    if not cands: break
    pre,e,o,u1,sel=cands[0]
    rows.append((pos,pre,e-pos,u1,sel,len(cands)))
    pos=e+13
    if len(rows)>=10: pass
print('rows parsed',len(rows),'pos',pos,'N',N,'closure',pos+F==N, 'tail',N-pos)
for r in rows[:6]: print(r)
print('last', rows[-3:])
print('ambig rows', sum(1 for r in rows if r[5]>1))
