import json, collections, re
d=json.load(open('scratch/t97/out/fourcc_mem_map.json'))
W_TEAM=[(176,1),(171,1),(168,2),(80,4),(96,4),(88,4),(120,4),(128,4),(152,4),(175,1),(104,4),
        (136,4),(144,4),(170,1),(172,1),(173,1),(174,1),(177,1),(112,4),(178,1)]
W_NAT=[(184,4),(188,4),(220,4),(224,1),(192,4),(204,4),(208,4),(212,4),(216,4),(196,4),(200,4),
       (225,1),(226,1),(228,1),(229,1),(230,1),(231,1),(227,1)]
def wiremap(order):
    m={}; off=0
    for mo,w in order:
        m[mo]=(off,w); off+=w
    return m, off
tm,tlen=wiremap(W_TEAM); nm,nlen=wiremap(W_NAT)
print('TEAM wire total',tlen,'NAT prefix total',nlen)
for tt,order in ((24,tm),):
    pass
def join(cls, wm):
    t=[x for x in d['tables'] if x['class']==cls][0]
    hit=[]; miss=[]
    for fc,v in t['fourccs'].items():
        po=v.get('primary_off_int')
        if po is None: miss.append(fc); continue
        if po in wm: hit.append((fc,po,wm[po][0],wm[po][1]))
        else: miss.append((fc,po))
    return t,hit,miss
t,hit,miss=join('TEAM',tm)
print('TEAM fourcc',len(t['fourccs']),'joined',len(hit),'unjoined',len(miss))
print(hit[:10])
t2,hit2,miss2=join('NATIONAL_TEAM',nm)
print('NAT fourcc',len(t2['fourccs']),'joined',len(hit2),'unjoined',len(miss2))
print(hit2[:10])
print('NAT unjoined sample',[x for x in miss2 if isinstance(x,tuple)][:8])
