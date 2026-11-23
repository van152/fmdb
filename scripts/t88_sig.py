"""t88-fix6: per-rec_type tail signature (distinct vector, sentinel/date/person slots)."""
import sys,json,struct,collections
sys.path.insert(0,'scripts')
from t88_rows import rows,parse
def main():
    persons=set(); acc=collections.defaultdict(list)
    allrows=[]
    for k,rec in rows():
        club,rt,per,name,tail,ident=parse(rec)
        persons.add(per); allrows.append((rt,per,tail))
    out={}
    for rt,per,tail in allrows: acc[rt].append((per,tail))
    for rt,rs in acc.items():
        n=len(rs)
        dv=[len(set(t[o] for p,t in rs)) for o in range(26)]
        d2=[len(set(struct.unpack_from('<H',t,o)[0] for p,t in rs)) for o in range(25)]
        # person uid slot
        pu=[o for o in range(23) if sum(1 for p,t in rs if struct.unpack_from('<I',t,o)[0] in persons)/n>0.5]
        ff=[o for o in range(26) if sum(1 for p,t in rs if t[o]==255)/n>0.5]
        small=[o for o in range(25) if d2[o]>3 and max(struct.unpack_from('<H',t,o)[0] for p,t in rs)<=120]
        out[str(rt)]={'n':n,'dv':dv,'d2':d2,'person_slots':pu,'ff_bytes':ff,'small_u16':small}
    json.dump(out,open('scratch/t88/out3/tail_sig.json','w'),indent=0)
    print('rt  n     dv[0:26]')
    for rt in sorted(out,key=int):
        v=out[rt]
        print('%-4s %-6d %s'%(rt,v['n'],' '.join('%d'%min(d,9) for d in v['dv'])))
    print('--- person_slots / small_u16 / ff_bytes')
    for rt in sorted(out,key=int):
        v=out[rt]
        print('%-4s p=%-18s s=%-14s ff=%s'%(rt,v['person_slots'],v['small_u16'],v['ff_bytes']))
if __name__=='__main__':
    if '--help' in sys.argv: print('usage: t88_sig.py'); sys.exit(0)
    main()
