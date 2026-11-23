import pickle, json, struct
from hashlib import sha256
raw=pickle.load(open('scratch/t72/work/raw.pkl','rb'))
fsN=json.load(open('scratch/t55/out/field_slots.json'))
U=lambda b,p=0: struct.unpack_from('<I',b,p)[0]
H=lambda x: sha256(x).hexdigest()
HEAD=bytes.fromhex('03017461642ef10d'); TAIL=bytes.fromhex('0000000001ec7ae404')
WIDTHS=[1,4,2,4,2,4,4,4,4,4,4,4,4,4,1,4,4,4,4,1,1,4,1,1,4,4,4,4,4,4,4,4,4,4,4,4,4,2,1,12]
VEC={2:('h',4),3:('i',4),4:('h',37),11:('i',23),12:('I',12),13:('I',14),23:('b',5),24:('i',28),25:('i',28),26:('i',12)}
class Bad(Exception): pass

def nat(b,server):
    n=U(b,8); pos=13; rows=[]
    for r in range(n):
        start=pos; row={}
        order=range(40) if server else (0,*range(14,27),39)
        for k in order:
            a=pos; w=WIDTHS[k]
            if a+w>len(b)-9: raise Bad((r,k,a,'short'))
            pos+=w
            if k in VEC:
                code,iw=VEC[k]; cnt=struct.unpack_from('<'+code,b,a)[0]
                if not (0<=cnt<=(len(b)-9-pos)//iw): raise Bad((r,a,'cnt',k,cnt))
                if k==4:
                    for _ in range(cnt):
                        pos+=1
                        for _f in range(4):
                            if pos+4>len(b)-9: raise Bad((r,pos,'nftb'))
                            L=U(b,pos); pos+=4+L
                            if pos>len(b)-9: raise Bad((r,pos,'nftb b'))
                        pos+=20
                elif k==11:
                    for _ in range(cnt):
                        if pos>=len(b)-9: raise Bad((r,pos,'ntxr'))
                        tag=b[pos]; pos+= 25 if tag>=2 else 23
                else:
                    pos+=cnt*iw
            if pos>len(b)-9: raise Bad((r,k,'bound'))
            row[k]=(a,pos-a,cnt if k in VEC else None)
        ia=row[39][0]; i,uid,rep=struct.unpack_from('<III',b,ia)
        if not (b[start]==0 and i==r and uid==rep and uid): raise Bad((r,ia,'ident',i,uid,rep))
        rows.append((start,pos,row))
    if b[pos:]!=TAIL: raise Bad(('tail',pos,len(b)))
    return rows

for side,srv in (('client',False),('server',True)):
    try: rows=nat(raw[side,10],srv)
    except Bad as e: print(side,'FAIL',e); continue
    n=len(rows); print(side,'rows',n,'end',rows[-1][1],'len',len(raw[side,10]))
    ids=H(b''.join(raw[side,10][r[2][39][0]:r[2][39][0]+12] for r in rows))
    d=fsN['targets'][side]['10']
    print('  identity', ids[:16], d['identity_sha256'][:16], ids==d['identity_sha256'])
    bad=[]
    for s in fsN['slots']:
        k=s['position']; exp=s['coordinates'][side]
        got=[[r[2][k][0], r[2][k][1]] for r in rows if k in r[2]]
        if got!=exp: bad.append((k,s['type'],len(got),len(exp)))
    print('  coord match bad=',bad)
    print('  envelope', (13,rows[-1][1]-13,rows[-1][1]) )
