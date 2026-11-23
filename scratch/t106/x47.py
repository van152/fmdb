import pathlib,sys,struct
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
b=(D/'payload_server_table_for_old_save_25.bin').read_bytes()
cnt=struct.unpack_from('<I',b,8)[0]
# DP: row k ends with 12B identity at p (u32@p==k, u32@p+4==u32@p+8)
cand={}
for p in range(12,len(b)-11):
    v=struct.unpack_from('<I',b,p)[0]
    if v<cnt and struct.unpack_from('<I',b,p+4)[0]==struct.unpack_from('<I',b,p+8)[0]:
        cand.setdefault(v,[]).append(p)
print('cand sizes',{k:len(v) for k,v in list(cand.items())[:5]}, 'missing',[k for k in range(cnt) if k not in cand][:10])
# greedy forward
pos=[]; prev=12
ok=True
for k in range(cnt):
    c=[q for q in cand.get(k,[]) if q>=prev]
    if not c: ok=False; print('fail at',k,'prev',prev); break
    pos.append(c[0]); prev=c[0]+12
print('greedy ok',ok,'last end',prev,'len',len(b),'footer',len(b)-prev)
if ok:
    starts=[12]+[p+12 for p in pos[:-1]]
    lens=[pos[i]+12-starts[i] for i in range(cnt)]
    print('min/max row len',min(lens),max(lens))
    import collections
    print('len hist top',collections.Counter(lens).most_common(10))
    print('rows with len<12',sum(1 for l in lens if l<12))
    print('first 6 rows starts/lens',list(zip(starts[:6],lens[:6])))
    print('uids row0',struct.unpack_from('<II',b,pos[0]+4))
    print('footer bytes',b[prev:].hex(' '))
