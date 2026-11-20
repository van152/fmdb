import pickle, json, struct
from hashlib import sha256
raw=pickle.load(open('scratch/t72/work/raw.pkl','rb'))
fsP=json.load(open('scratch/t59/out/field_slots.json'))
U=lambda b,p=0: struct.unpack_from('<I',b,p)[0]
H=lambda x: sha256(x).hexdigest()
FOOT=bytes.fromhex('00000000014ec43a77')
class Bad(Exception): pass

FIXED='selector m15c m15d colour_tag m120 m124 m128 m12c m130 m134 m1a0 m1a2 m1a3 m1a4 m1a5 stat_a_tag m198 m199 m19a m19b m19c m19d m19e stat_b_tag m189_197 mf6 m138 m13c m58 m60 m70 m68 m150'.split()
W=[1,1,1,1]+[2]*5+[1]*15+[15,1]+[4]*6+[2]  # 1+3+5+15+2+6+1 = 33 slots
EXT='m180 mb8 m188 m184 m186 m182 m160 m168 m170 m178'.split()
SUF='m148 m152 m154 m156 m158 m15a m80 m88 m90 m98 wbcl_present'.split()

def comp(b,server):
    n=U(b,8); cols={}; q=13; rr=[]
    for i in range(n):
        start=q
        def rec(k,s,e):
            if not (s<=e<=len(b)-9): raise Bad((k,i,s,e))
            cols.setdefault(k,[]).append((i,s,e-s))
        def tr(k,w):
            nonlocal q
            p=q; q+=w; rec(k,p,q); return int.from_bytes(b[p:q],'little')
        def block(keys,ws): return [tr(k,w) for k,w in zip(keys,ws,strict=True)]
        vals=block(FIXED,W)
        if not (vals[0]==0 and vals[3]==1 and vals[10]!=4 and vals[15]==2 and vals[23]==3): raise Bad((i,'tags',vals))
        if server:
            block(EXT,[2,4,1,2,2,2,8,8,8,8])
            p=q; q+=4+2*U(b,p); rec('vec30',p,q)
            if tr('a8_present',1):
                ver=b[q]; tr('obj_a8',1+32+4*(ver>=2)+9+(2 if ver>=3 else 1)+8)
            block(['mf0','m1a1','m1a8','mf4','mf5'],[4,1,1,1,1])
            if tr('e0_present',1):
                if tr('obj_e0',4)!=0: raise Bad((i,'e0'))
            p=q; m=struct.unpack_from('<i',b,p)[0]
            if not (0<=m<(len(b)-p)//7): raise Bad((i,'vec18',m))
            q+=4
            for _ in range(m): q+=8+(struct.unpack_from('<b',b,q)[0]>=2)
            rec('vec18',p,q)
            if tr('e8_present',1):
                p=q; m=U(b,p+4)
                if not m<(len(b)-p)//8: raise Bad((i,'e8',m))
                q+=8
                for _ in range(m):
                    v=struct.unpack_from('<h',b,q)[0]; q+=10+(v>=2)+(v>=3)
                rec('obj_e8',p,q)
            if tr('c0_present',1):
                p=q; m=U(b,p+1)
                if not m<(len(b)-p)//6: raise Bad((i,'c0',m))
                q+=5
                for _ in range(m): q+=6+12*U(b,q+2)
                rec('obj_c0',p,q)
            if tr('c8_present',1): tr('obj_c8',25)
            tr('m1a7',1)
            if tr('d0_present',1): tr('obj_d0',15)
            if tr('d8_present',1): tr('obj_d8',15)
            m=struct.unpack_from('<h',b,q)[0]
            if m<0: raise Bad((i,'vec100'))
            tr('vec100',2+5*m)
        if block(SUF,[4,2,2,2,2,2,4,4,4,4,1])[-1]: tr('m14c',2)
        block(['m140','m144','mf7','mf8','mf9'],[4,4,1,1,1])
        at=q; j,uid,rep=struct.unpack_from('<III',b,at); tr('identity',12)
        if not (j==i and uid==rep and uid>(rr[-1][2] if rr else 0)): raise Bad((i,at,'id'))
        rr.append((start,q,uid))
    if b[q:]!=FOOT: raise Bad(('footer',q))
    return cols,rr

for side,srv in (('client',False),('server',True)):
    try:
        cols,rr=comp(raw[side,25],srv)
    except Bad as e:
        print(side,'FAIL',e); continue
    print(side,'rows',len(rr))
    ok=0; bad=[]
    for s in fsP['slots']:
        prof=s['profiles'][side]; cells=cols.get(s['key'],[])
        if not cells:
            if prof.get('events')==0: ok+=1
            else: bad.append((s['key'],'empty vs',prof.get('events')))
            continue
        dg=H(b''.join(struct.pack('<III',i,a,w) for i,a,w in cells))
        if dg==prof['coordinate_sha256']: ok+=1
        else: bad.append((s['key'],dg[:10],prof['coordinate_sha256'][:10]))
    print('  slot digest ok',ok,'/',len(fsP['slots']),'bad',bad)
