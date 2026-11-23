import sys, struct
sys.path.insert(0,'scratch/t84/probe'); sys.path.insert(0,'scripts')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
import t84_join as J
K=lib.K
raw3=K['load_payload'](lib.CODEC,'client','3')
rows=list(K['walk_club_block'](raw3))
starts=[(o,len(b)) for _,o,b in rows]
recs,_,_=J.lang_records(lib.load_member('lang_update','8_3.dat'),6,3)
def row_of(pos):
    lo,hi=0,len(starts)-1
    while lo<=hi:
        m=(lo+hi)//2; o,l=starts[m]
        if pos<o: hi=m-1
        elif pos>=o+l: lo=m+1
        else: return m,o,l
# club tail: last 12 bytes = ordinal, uid, uid
tail={}
for idx,o,b in rows:
    if len(b)>=13 and b[-1]==0:
        a,c,d=struct.unpack_from('<III',b,len(b)-12)
        tail[idx]=(a,c,d)
print('rows with tail ordinal|uid|uid:',sum(1 for v in tail.values() if v[0]==v[1]==v[2] or v[1]==v[2]))
same_ou=sum(1 for v in tail.values() if v[1]==v[2])
print('tail uid==uid2:',same_ou,'of',len(tail))
hit=0; tot=0; ex=[]
for r in recs:
    nb=r['fields'][0].encode('utf-8')
    i=raw3.find(struct.pack('<I',len(nb))+nb)
    if i<0: continue
    rr=row_of(i)
    if not rr: continue
    idx,o,l=rr; tot+=1
    t=tail.get(idx)
    if t and t[1]==r['uid']: hit+=1
    elif len(ex)<4: ex.append((r['uid'],t,idx,r['fields'][0][:24]))
print(f'lang 8_3 uid == club row-tail uid: {hit}/{tot} ({100*hit/tot:.1f}%)')
for e in ex: print('   miss',e)
