import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _lib import *

def fit_len_prefixed(raw, count, name_at=4, rest_candidates=range(0,60), hs=14, fs=8):
    """Try: u32 len at row+0, name bytes, then fixed `rest` bytes."""
    res=[]
    for rest in rest_candidates:
        p=hs; ok=0; names=[]; spans=[]
        for i in range(count):
            if p+4>len(raw)-fs: break
            n=int.from_bytes(raw[p:p+4],'little')
            if n>64 or p+4+n>len(raw)-fs: break
            nm=raw[p+4:p+4+n]
            if not all(32<=c<127 for c in nm): break
            names.append(nm)
            spans.append(p)
            ok+=1
            p=p+4+n+rest
        if ok==count and p+0==len(raw)-fs+1 or (ok==count and p==len(raw)-fs):
            res.append((rest,ok,p))
    return res

if __name__=='__main__':
    mod=load_old_decoder()
    for t in (8,41,18):
        s=member(mod,'client_db.dat',t); r=s['_raw']
        print('table',t,'count',s['count'],'len',len(r))
        for rest,ok,p in fit_len_prefixed(r,s['count']):
            print('   FIT rest=',rest,'rows',ok,'end',hex(p),'expected_end',hex(len(r)-8))
