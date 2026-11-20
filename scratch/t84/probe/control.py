import sys, struct, random
sys.path.insert(0,'scratch/t84/probe'); sys.path.insert(0,'scripts')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
import t84_join as J
K=lib.K

raw3=lib.K["load_payload"](lib.CODEC,'client','3')
rows=list(K['walk_club_block'](raw3))
starts=[(o,len(b)) for _,o,b in rows]
recs,_,_=J.lang_records(lib.load_member('lang_update','8_3.dat'),6,3)

def row_of(pos):
    lo,hi=0,len(starts)-1
    while lo<=hi:
        m=(lo+hi)//2
        o,l=starts[m]
        if pos<o: hi=m-1
        elif pos>=o+l: lo=m+1
        else: return m,o,l
    return None

def contains_u32(off,ln,v):
    pat=struct.pack('<I',v)
    seg=raw3[off:off+ln]
    return pat in seg

name_hit=uid_in_row=0; wr_uid=0; tot=0
random.seed(84)
allu=[r['uid'] for r in recs]
for r in recs:
    nb=r['fields'][0].encode('utf-8')
    i=raw3.find(struct.pack('<I',len(nb))+nb)
    if i<0: continue
    rr=row_of(i)
    if not rr: continue
    idx,off,ln=rr
    tot+=1
    name_hit+=1
    if contains_u32(off,ln,r['uid']): uid_in_row+=1
    wrong=random.choice(allu)
    if wrong!=r['uid'] and contains_u32(off,ln,wrong): wr_uid+=1
print(f'lang 8_3 names located in a club row: {tot}/3462')
print(f'  true lang uid present as u32 in that row : {uid_in_row}/{tot} ({100*uid_in_row/tot:.1f}%)')
print(f'  WRONG random uid present as u32 in that row: {wr_uid}/{tot} ({100*wr_uid/tot:.1f}%)')
