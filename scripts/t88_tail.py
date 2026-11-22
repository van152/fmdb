"""t88-fix6: per-rec_type tail byte profile + u16/u32 slot census (data side)."""
import sys,json,struct,collections
sys.path.insert(0,'scripts')
from t88_rows import rows,parse
def main():
    prof=collections.defaultdict(lambda: {'n':0,'b':[collections.Counter() for _ in range(26)]})
    for k,rec in rows():
        club,rt,per,name,tail,ident=parse(rec)
        p=prof[rt]; p['n']+=1
        for i in range(26): p['b'][i][tail[i]]+=1
    out={}
    for rt,p in sorted(prof.items()):
        n=p['n']
        row=[]
        for i in range(26):
            c=p['b'][i]; top=c.most_common(2)
            row.append({'o':i,'d':len(c),'ff':round(c.get(255,0)/n,3),'z':round(c.get(0,0)/n,3),
                        'top':[[v,round(k2/n,3)] for v,k2 in top]})
        out[str(rt)]={'n':n,'bytes':row}
    json.dump(out,open('scratch/t88/out3/tail_prof.json','w'),indent=0)
    for rt in sorted(prof)[:6]:
        n=prof[rt]['n']
        print('== rt',rt,'n',n)
        print('   '+' '.join('%02x'%prof[rt]['b'][i].most_common(1)[0][0] for i in range(26)))
        print('   d: '+' '.join('%2d'%len(prof[rt]['b'][i]) for i in range(26)))
if __name__=='__main__':
    if '--help' in sys.argv: print('usage: t88_tail.py'); sys.exit(0)
    main()
