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
for r in recs[:3]:
    nb=r['fields'][0].encode('utf-8')
    i=raw3.find(struct.pack('<I',len(nb))+nb)
    idx,o,l=row_of(i)
    seg=raw3[o:o+l]
    k=seg.find(struct.pack('<I',r['uid']))
    print(f"uid={r['uid']} row={idx} len={l} uid@row+{k} name@row+{i-o}")
    print('   ', seg.hex(' '))
    print('   tail_u32s', [struct.unpack_from('<I',seg,p)[0] for p in range(max(0,l-24),l-3,4)])
