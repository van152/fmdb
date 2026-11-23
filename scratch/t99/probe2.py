import sys,struct,runpy,time
sys.path.insert(0,r'D:\tmp2b\fm24\tools\python')
k=runpy.run_path(r'scripts/t38_multiframe.py')
MAGIC=bytes.fromhex('03017461642ef10d')
def u32(b,p): return struct.unpack_from('<I',b,p)[0]

def rec_ends(raw,p,uid,L,maxf=8,guard=2048):
    """all (endpos, fields) reachable from p (record start, uid already read)."""
    out=[]
    stack=[(p+4,[],0)]
    seen=set()
    while stack:
        q,strs,d=stack.pop()
        if q>p+guard or (q,tuple(strs)) in seen: continue
        seen.add((q,tuple(strs)))
        if q==L or (q+4<=L and u32(raw,q)>uid):
            out.append((q,strs))
        if d>=maxf: continue
        for fo in (0,1):
            r=q+fo
            if r+4>L: continue
            ln=u32(raw,r)
            if ln>600 or r+4+ln>L: continue
            seg=raw[r+4:r+4+ln]
            try: s=seg.decode('utf-8')
            except UnicodeDecodeError: continue
            if ln and not all(c.isprintable() for c in s): continue
            stack.append((r+4+ln,strs+[s],d+1))
    return out

def parse(raw,maxf=8,maxtr=4):
    L=len(raw)
    if L<12 or raw[:8]!=MAGIC: return {'ok':False,'why':'header'}
    cnt=u32(raw,8)
    if cnt==0: return {'ok':L==12,'cnt':0,'recs':0,'end':12}
    # forward DP: best[nrec][pos]; keep min recs? we want max recs then exact end
    reach={12:0}          # pos -> nrec
    recs={}               # pos -> (startpos, uid, fields)
    order=[12]
    for p in order:
        nrec=reach[p]
        if p+4>L: continue
        uid=u32(raw,p)
        for e,strs in rec_ends(raw,p,uid,L,maxf):
            for tr in range(maxtr+1):
                nxt=e+tr
                if nxt>L: break
                if nxt!=L and not (nxt+4<=L and u32(raw,nxt)>uid): continue
                v=nrec+1
                if reach.get(nxt,-1)<v:
                    reach[nxt]=v; recs[nxt]=(p,uid,strs)
                    if nxt not in order: order.append(nxt)
    if L in reach:
        # walk back for field stats
        seq=[]; q=L
        while q!=12 and q in recs:
            p,uid,strs=recs[q]; seq.append((uid,strs)); q=p
        seq.reverse()
        return {'ok':True,'cnt':cnt,'recs':len(seq),'end':L,'sample':seq[:3],
                'nf':sorted({len(s[1]) for s in seq})}
    fin=max(reach.items(), key=lambda kv:(kv[1],kv[0]))
    return {'ok':False,'why':'partial','cnt':cnt,'recs':fin[1],'end':fin[0],'L':L}

if __name__=='__main__':
    codec=k['_codec'](); cache={}
    info=k['archive_info'](codec,'lang_update',cache)
    names=sorted(x['path'].split('/')[-1] for x in info['entries'])
    ok=0; bad=[]; t=time.time()
    for n in names:
        e=[x for x in info['entries'] if x['path'].split('/')[-1]==n][0]
        raw=k['inspect_entry'](codec,e,info)['data']
        r=parse(raw)
        if r['ok']: ok+=1
        else: bad.append((n,r.get('why'),r.get('recs'),r.get('cnt'),r.get('end'),r.get('L')))
    print(f"closed {ok}/{len(names)} in {time.time()-t:.1f}s")
    for b in bad[:10]: print('  ',b)
