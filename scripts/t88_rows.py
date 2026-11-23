"""t88-fix6: row reader for server table_45 (payload+starts frozen)."""
import sys,json,struct
O='scratch/t88/out2/'
def load():
    p=open(O+'_p_server_45.bin','rb').read()
    st=list(struct.unpack_from('<%dI'%(len(open(O+'_starts.bin','rb').read())//4),open(O+'_starts.bin','rb').read()))
    return p,st
def rows():
    p,st=load()
    n=len(st)
    for k,s in enumerate(st):
        e=st[k+1] if k+1<n else len(p)-8
        yield k,p[s:e]
def parse(rec):
    club=struct.unpack_from('<I',rec,0)[0]
    rt=rec[4]
    per=struct.unpack_from('<I',rec,5)[0]
    nl=struct.unpack_from('<I',rec,37)[0]
    name=rec[41:41+nl]
    tail=rec[41+nl:41+nl+26]
    ident=rec[-13:]
    return club,rt,per,name,tail,ident
if __name__=='__main__':
    p,st=load()
    print('rows',len(st),'payload',len(p))
    import collections
    c=collections.Counter()
    ex={}
    for k,rec in rows():
        club,rt,per,name,tail,ident=parse(rec)
        c[rt]+=1
        if rt not in ex: ex[rt]=(k,club,per,name,tail.hex(),ident.hex())
    print('types',len(c))
    for rt in sorted(c)[:6]:
        print(rt,c[rt],ex[rt])
