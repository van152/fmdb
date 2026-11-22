"""t88-fix6: data-side anchor scan - tail/prefix slot membership vs entity uid sets."""
import sys,json,struct,collections
sys.path.insert(0,'scripts')
from t88_rows import rows,parse
def main():
    cl=json.load(open('scratch/t88/club.json'))['uids']
    clubs=set(cl)
    recs=[]
    persons=set()
    for k,rec in rows():
        club,rt,per,name,tail,ident=parse(rec)
        persons.add(per)
        recs.append((club,rt,per,tail))
    print('rows',len(recs),'persons',len(persons),'clubs',len(clubs))
    out={}
    by=collections.defaultdict(list)
    for club,rt,per,tail in recs: by[rt].append((club,per,tail))
    for rt,rs in sorted(by.items()):
        n=len(rs); r={}
        for off in range(0,23):
            cu=sum(1 for c,p,t in rs if struct.unpack_from('<I',t,off)[0] in clubs)
            pu=sum(1 for c,p,t in rs if struct.unpack_from('<I',t,off)[0] in persons)
            r[off]=(round(cu/n,3),round(pu/n,3))
        out[str(rt)]={'n':n,'clubref':{str(k):v[0] for k,v in r.items()},'perref':{str(k):v[1] for k,v in r.items()}}
    json.dump(out,open('scratch/t88/out3/tail_ref.json','w'),indent=0)
    for rt in sorted(by,key=lambda x:x)[:14]:
        r=out[str(rt)]
        cr=[(k,v) for k,v in r['clubref'].items() if v>=0.3]
        pr=[(k,v) for k,v in r['perref'].items() if v>=0.3]
        print('rt',rt,'n',r['n'],'clubref',cr,'perref',pr)
if __name__=='__main__':
    if '--help' in sys.argv: print('usage: t88_anchor.py'); sys.exit(0)
    main()
