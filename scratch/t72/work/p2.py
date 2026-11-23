import pickle, json, struct
from hashlib import sha256
raw=pickle.load(open('scratch/t72/work/raw.pkl','rb'))
fsC=json.load(open('scratch/t57/out/field_slots.json'))
fsP=json.load(open('scratch/t59/out/field_slots.json'))
fsN=json.load(open('scratch/t55/out/field_slots.json'))
U=lambda b,p=0: struct.unpack_from('<I',b,p)[0]
H=lambda x: sha256(x).hexdigest()

COrder='selector derived_170 derived_178 ref_d8 ref_e0 ref_e8 ref_f0 ref_f8 flags160 name_len name_bytes short_len short_bytes raw16a raw166 person148 raw16c vec110 obj150_tag obj150 vec130 vec138 raw168 stad140 base_ba base_b8 base18 base30 base60 base78 base90 base48 basea8 identity'.split()
CG={17:(1,4),20:(1,24),21:(1,12),26:(1,4),27:(1,4),28:(1,4),29:(1,4),30:(1,4),31:(1,16),32:(2,28)}
class Bad(Exception): pass
def club(b,server):
    n=U(b,8); foot=len(b)-9; q=13; cols=[[] for _ in COrder]; ids=[]; rr=[]
    for o in range(n):
        p=q; start=q
        def span(k,w):
            nonlocal p
            if w<=0 or p+w>foot: raise Bad((o,p,k,w))
            cols[k].append((o,p,w)); p+=w
        sel=b[q]; span(0,1)
        if sel: span(1,4); span(2,1)
        for k in range(3,8): span(k,4)
        span(8,6)
        for k in (9,11):
            at=p; span(k,4); L=U(b,at)
            if L: span(k+1,L)
        def group(k):
            w,s=CG[k]; rawv=int.from_bytes(b[p:p+w],'little')
            if k in (17,20,21,28,29,32) and rawv>=1<<(8*w-1): raise Bad((o,p,'cnt',k,rawv))
            span(k,w+rawv*s)
        if server:
            for k,w in zip((13,14,15,16),(1,2,4,1)): span(k,w)
            group(17); tag=b[p]; span(18,1)
            if tag==0: span(19,45)
            elif tag!=2: raise Bad((o,p,'tag',tag))
            group(20); group(21); span(22,2); span(23,4)
        span(24,1); span(25,2)
        if server:
            for k in range(26,33): group(k)
        at=p; span(33,12); got,a,c=struct.unpack_from('<III',b,at); q=p
        if not (got==o and a==c and a>(ids[-1] if ids else 0)): raise Bad((o,at,'id'))
        ids.append(a); rr.append((start,q,a,sel))
    if q!=foot or b[q:]!=bytes.fromhex('0000000001e3c03a77'): raise Bad('footer')
    return cols,rr

for side,srv in (('client',False),('server',True)):
    cols,rr=club(raw[side,3],srv)
    print(side,'rows',len(rr))
    ok=0; bad=[]
    for k,s in enumerate(fsC['slots']):
        prof=s['profiles'][side]
        cells=cols[k]
        if not cells:
            if prof.get('rows')==0 or prof.get('status')=='bypassed': ok+=1
            else: bad.append((s['key'],'empty vs',prof.get('rows')))
            continue
        dg=H(b''.join(struct.pack('<III',i,a,w) for i,a,w in cells))
        if dg==prof['coordinate_sha256']: ok+=1
        else: bad.append((s['key'],dg[:12],prof['coordinate_sha256'][:12]))
    print('  slot digest ok',ok,'bad',bad[:5])
