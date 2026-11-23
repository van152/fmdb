import json,sys,struct
sys.stdout.reconfigure(encoding='utf-8')
# per-row collection widths from t72 fingerprints vs extra_9 item counts
fp=json.loads(open('scratch/t72/out/fingerprints.json',encoding='utf-8').read())
slots=[s for s in fp['tables']['nation']['slots'] if s['slot_type']=='collection']
# rebuild per-row widths by re-walking t10 directly
sys.path.insert(0,'scripts'); import t85_common as C
raw=C.payload('client','client_db/table_10.dat',24732)
offs=C.identity_offsets(raw); starts=[14]+[o+13 for o in offs[:-1]]; lens=[o+13-s for o,s in zip(offs,starts)]
# t25 grammar: prefix 25, A: i8 at row+24, 5B each; B/C: i32 28B; D: i32 12B
w={}
for i,(s,l) in enumerate(zip(starts,lens)):
    b=raw[s:s+l]; p=25; a=struct.unpack_from('<b',b,24)[0]
    w.setdefault('A',[]).append(a); p=25+5*a
    nb=struct.unpack_from('<i',b,p)[0]; w.setdefault('B',[]).append(nb); p+=4+28*nb
    nc=struct.unpack_from('<i',b,p)[0]; w.setdefault('C',[]).append(nc); p+=4+28*nc
    nd=struct.unpack_from('<i',b,p)[0]; w.setdefault('D',[]).append(nd)
    exp=50+5*a+28*nb+28*nc+12*nd
    w.setdefault('ok',[]).append(exp==l)
print('t10 row grammar closes:',sum(w['ok']),'/251 (13B identity incl.)')
for k in 'ABCD':
    print(f'  {k}: min={min(w[k])} max={max(w[k])} sum={sum(w[k])} distinct={len(set(w[k]))}')
# extra_9 counts
rows=[json.loads(l) for l in open('scratch/t50/out/profiles/table_client_extra_9.rows.jsonl',encoding='utf-8')]
pat=bytes.fromhex('ffffffffffffffff'); nff=[]
for r in rows:
    b=bytes.fromhex(r['raw_hex']); nl=r['marker']['name_len']; t=b[8+nl:]
    c=0;p=t.find(pat)
    while p>=0: c+=1;p=t.find(pat,p+1)
    nff.append(c)
print('extra_9 ff8-count sum',sum(nff),'distinct',len(set(nff)))
for k in 'ABCD':
    same=sum(1 for i in range(251) if w[k][i]==nff[i])
    print(f'  extra9 vs {k}: exact match {same}/251')
