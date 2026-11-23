import sys, struct, random, collections
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
random.seed(84)
allu=[r['uid'] for r in recs]
tot=inhit=wronghit=0
for r in recs:
    nb=r['fields'][0].encode('utf-8')
    i=raw3.find(struct.pack('<I',len(nb))+nb)
    if i<0: continue
    rr=row_of(i)
    if not rr: continue
    _,o,l=rr; tot+=1
    seg=raw3[o:o+l]
    if struct.pack('<I',r['uid']) in seg: inhit+=1
    w=random.choice(allu)
    if w!=r['uid'] and struct.pack('<I',w) in seg: wronghit+=1
print(f'club lang uid-in-row: {inhit}/{tot} = {100*inhit/tot:.2f}%   wrong-uid: {wronghit}/{tot} = {100*wronghit/tot:.2f}%')

# nation: any name bytes in table_10 at all?
for a in ('client','server'):
    r10=K['load_payload'](lib.CODEC,a,'10')
    pr=sum(1 for b in r10 if 32<=b<127)/len(r10)
    print(f'{a} table_10 printable {100*pr:.1f}%  England={r10.find(b"England")} Brazil={r10.find(b"Brazil")}')
# comp table_25
for a in ('client','server'):
    r25=K['load_payload'](lib.CODEC,a,'25')
    pr=sum(1 for b in r25 if 32<=b<127)/len(r25)
    print(f'{a} table_25 printable {100*pr:.1f}%  Serie={r25.find(b"Serie")} Premier={r25.find(b"Premier")}')
