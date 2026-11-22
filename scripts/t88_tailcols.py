"""t88-fix6: per-rec_type tail window stats (uid-ref / date / small-int) - data side."""
import sys,json,struct,collections
sys.path.insert(0,'scripts')
from t88_rows import rows,parse
def main():
    import pickle
    clubs=set()
    try:
        cl=json.load(open('scratch/t88/club.json'))
        clubs=set(cl['uids']) if isinstance(cl,dict) else set(cl)
    except Exception as e:
        print('club set load fail',e)
    print('club set',len(clubs))
    acc=collections.defaultdict(list)
    for k,rec in rows():
        club,rt,per,name,tail,ident=parse(rec)
        acc[rt].append(tail)
    out={}
    for rt,ts in sorted(acc.items()):
        n=len(ts); r={'n':n,'u32':{},'u16':{}}
        for off in range(0,23):
            c=collections.Counter()
            for t in ts: c[struct.unpack_from('<I',t,off)[0]]+=1
            ref=sum(v for kk,v in c.items() if kk in clubs)/n if clubs else 0
            r['u32'][off]={'d':len(c),'ff':round(c.get(0xffffffff,0)/n,3),'z':round(c.get(0,0)/n,3),
                           'ref':round(ref,3),'max':max(c)}
        for off in range(0,25):
            c=collections.Counter(struct.unpack_from('<H',t,off)[0] for t in ts)
            good=sum(v for kk,v in c.items() if 1<=(kk&31)<=31 and 1<=((kk>>5)&15)<=12 and 1900<=(kk>>9)+1900<2100)/n
            r['u16'][off]={'d':len(c),'ff':round(c.get(0xffff,0)/n,3),'z':round(c.get(0,0)/n,3),'date':round(good,3),'max':max(c)}
        out[str(rt)]=r
    json.dump(out,open('scratch/t88/out3/tail_cols.json','w'),indent=0)
    for rt in ('25','26','10','13','24','27','28'):
        if rt not in out: continue
        r=out[rt]; print('== rt',rt,'n',r['n'])
        print('  u32 '+' '.join('%d:ref%.2f d%d'%(o,r['u32'][o]['ref'],r['u32'][o]['d']) for o in range(0,14)))
        print('  u16 '+' '.join('%d:dt%.2f d%d'%(o,r['u16'][o]['date'],r['u16'][o]['d']) for o in range(0,14)))
if __name__=='__main__':
    if '--help' in sys.argv: print('usage: t88_tailcols.py'); sys.exit(0)
    main()
