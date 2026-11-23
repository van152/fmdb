import sys, struct, collections
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
    return None
offs=collections.Counter(); nameoff=collections.Counter()
for r in recs:
    nb=r['fields'][0].encode('utf-8')
    i=raw3.find(struct.pack('<I',len(nb))+nb)
    if i<0: continue
    rr=row_of(i)
    if not rr: continue
    idx,o,l=rr
    seg=raw3[o:o+l]
    pat=struct.pack('<I',r['uid'])
    k=seg.find(pat)
    if k>=0: offs[k]+=1
    nameoff[i-o]+=1
print('uid u32 offset within club row (top):', offs.most_common(8))
print('full-name rel offset within club row (top):', nameoff.most_common(6))
