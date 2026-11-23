import sys,struct,runpy,json,time
sys.path.insert(0,r'D:\tmp2b\fm24\tools\python')
k=runpy.run_path(r'scripts/t38_multiframe.py')
DAT=bytes.fromhex('03017461642ef1 0d'.replace(' ',''))
def u32(b,p): return struct.unpack_from('<I',b,p)[0]

def parse_member(raw, maxfields=80, maxgap=3):
    L=len(raw)
    if L<12 or raw[:8]!=DAT: return {'ok':False,'why':'bad header'}
    cnt=u32(raw,8)
    if cnt==0: return {'ok':L==12,'cnt':0,'recs':[]}
    def valid_str(p):
        if p+4>L: return None
        ln=u32(raw,p)
        if ln<1 or ln>512 or p+4+ln>L: return None
        try: s=raw[p+4:p+4+ln].decode('utf-8')
        except UnicodeDecodeError: return None
        if not s.isprintable(): return None
        return ln,s
    memo={}
    def solve(i,p):
        key=(i,p)
        if key in memo: return memo[key]
        memo[key]=None
        if i==cnt: 
            r=([] if p==L else None); memo[key]=r; return r
        if p+4>L: memo[key]=None; return None
        uid=u32(raw,p)
        # enumerate candidate (end,strs)
        cands=[]
        def dfs(q, strs, gap):
            if len(strs)>=maxfields or gap>12: return
            if q==L or (q+4<=L and i+1<cnt and u32(raw,q)>uid):
                cands.append((q,list(strs)))
            for g in range(0,maxgap+1):
                v=valid_str(q+g)
                if v:
                    ln,s=v
                    strs.append(s); dfs(q+g+4+ln,strs,gap+g); strs.pop()
        dfs(p+4,[],0)
        for end,strs in cands:
            sub=solve(i+1,end)
            if sub is not None:
                r=[(uid,strs)]+sub
                memo[key]=r; return r
        memo[key]=None; return None
    t=time.time()
    res=solve(0,12)
    return {'ok':res is not None,'cnt':cnt,'recs':res or [],'sec':time.time()-t,'states':len(memo)}

if __name__=='__main__':
    codec=k['_codec'](); cache={}
    info=k['archive_info'](codec,'lang_update',cache)
    names=sorted(x['path'].split('/')[-1] for x in info['entries'])
    okc=0; bad=[]
    tot=time.time()
    for n in names:
        e=[x for x in info['entries'] if x['path'].split('/')[-1]==n][0]
        raw=k['inspect_entry'](codec,e,info)['data']
        r=parse_member(raw)
        if r['ok']: okc+=1
        else: bad.append((n,r.get('why') or f"cnt={r.get('cnt')}"))
    print(f"closed {okc}/{len(names)} in {time.time()-tot:.1f}s")
    print('unclosed:',bad)
