#!/usr/bin/env python3
"""Commander independent spot-check of t26 people census. Re-implements grammars; does NOT import devseek results."""
import os, sys, io, struct, hashlib, collections
from pathlib import Path
sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(r'D:/tmp2b/fm24-db')
DB=ROOT/'scratch/data'
sys.path.insert(0, r'D:/tmp2b/fm24/tools/python')
import zstandard
import numpy as np
checks=[]
def ck(n,c,x=''):
    checks.append((n,bool(c),x)); print(('PASS' if c else 'FAIL'),n,x)
def dec(name, skip=8):
    data=(DB/name).read_bytes()
    with zstandard.ZstdDecompressor().stream_reader(io.BytesIO(data[skip:]), read_across_frames=True) as r:
        return r.read(600*1024*1024)

# 1. people_db payload
pp=dec('people_db.dat')
ck('people_payload_len', len(pp)==400443970, f'len={len(pp)}')
ck('people_sha', hashlib.sha256(pp).hexdigest()=='21686a985e32ebaf8ced73478058e69720be061d08be499be89e4d441f0f2fbd')
total=struct.unpack_from('<I',pp,2)[0]
ck('people_header_count_658011', total==658011, f'u32@2={total}')

# 2. compact walk (independent re-implementation), from pos 6
CL={1:83,2:83,3:83,4:34,5:22}
pos=6; rows=[]; bad=None
while True:
    if pos+33>len(pp): bad=('eof',pos); break
    key,typ=struct.unpack_from('<II',pp,pos)
    ln=struct.unpack_from('<I',pp,pos+9)[0]
    end=pos+13+ln
    if typ!=5 or not(0<=ln<=64) or end+20>len(pp): bad=('header',pos,key,typ,ln); break
    pad=pp[end:end+8]
    k2,d1,d2=struct.unpack_from('<III',pp,end+8)
    if any(pad) or k2!=key or d1!=d2: bad=('trailer',pos); break
    rows.append((key,d1,pos)); pos=end+20
ck('compact_1193_rows', len(rows)==1193, f'n={len(rows)}')
ck('compact_break_55750', bad and bad[1]==55750, f'bad={bad}')
keys=[r[0] for r in rows]
ck('compact_key_range', min(keys)==656818 and max(keys)==658010 and len(set(keys))==1193, f'[{min(keys)},{max(keys)}]')
ck('compact_keys_contiguous_set', sorted(keys)==list(range(656818,658011)))

# 3. basic_people walk (independent)
bp=dec('basic_people_db.dat')
cnt=struct.unpack_from('<I',bp,0)[0]
ck('basic_count_658011', cnt==658011, f'cnt={cnt}')
p=5; cls=collections.Counter(); bduni=[0]*cnt; bbad=None
for i in range(cnt):
    c=bp[p+1]
    if c not in CL: bbad=(i,p,c); break
    cls[c]+=1; ln=CL[c]
    _,dd,_=struct.unpack_from('<III',bp,p+ln-12)
    bduni[i]=dd; p+=ln
ck('basic_walk_end_54060034', p==54060034 and bbad is None, f'end={p} bad={bbad}')
ck('basic_class_dist', dict(cls)=={1:166064,2:476158,3:4757,4:9839,5:1193}, str(dict(cls)))
ck('basic_len_54060043', len(bp)==54060043, f'len={len(bp)}')

# 4. compact duni == basic_people class-5 tail duni (cross-file)
match=sum(1 for (k,d,_) in rows if d==bduni[k])
ck('compact_duni_cross_1193', match==1193, f'{match}/1193')
ck('basic_duni_656818_first', bduni[656818]==2002040996, f'{bduni[656818]}')

# 5. trailer_pos.npy canonical positions
tp=np.load(ROOT/'scratch/t26/trailer_pos.npy')
tk=np.load(ROOT/'scratch/t26/trailer_key.npy')
ck('trailer_pos_658011', len(tp)==658011, f'len={len(tp)}')
ck('trailer_pos_distinct', len(np.unique(tp))==658011, f'distinct={len(np.unique(tp))}')
ck('trailer_key_distinct', len(np.unique(tk))==658011, f'key distinct={len(np.unique(tk))}')
ck('trailer_key_domain', int(tk.min())>=0 and int(tk.max())<=658010, f'[{tk.min()},{tk.max()}]')
# spot-check 40 trailer positions: raw trailer (key2,duni,duni) at pos-12, duni==basic[key2]
import random
idx=random.Random(26).sample(range(len(tp)),40)
ok=0
for j in idx:
    q=int(tp[j]); k=int(tk[j])
    if q<0 or q+12>len(pp): continue
    k2,d1,d2=struct.unpack_from('<III',pp,q)
    if k2==k and d1==d2 and d1==bduni[k]: ok+=1
ck('trailer_spot_40', ok==40, f'{ok}/40')
print('---')
fails=[c for c in checks if not c[1]]
print(f't26 spot: {len(checks)-len(fails)}/{len(checks)} PASS', ('FAILS:'+str([c[0] for c in fails])) if fails else 'ALL GREEN')
sys.exit(1 if fails else 0)