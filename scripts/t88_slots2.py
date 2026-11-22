"""t88-fix6 step2: 117 codes -> (rec_type, tag, wire_off, width)."""
import sys,json
O='scratch/t88/out3/'
TAGOFF={'gols':[0x56,2],'ogls':[0x58,2],'stdt':[0x40,2],'stdb':[0x30,4],
        'comp':[0x34,4],'stid':[0x1c,4],'stnm':[0x20,0],'atte':[0x50,4],
        'gams':[0x54,2],'endt':[0x5c,1],'fsgt':[0x5e,1],'otht':[0x5a,1],
        'cash':[0x58,4],'infn':[0x28,4],'stic':[0x24,4]}
def main():
    bl=json.load(open(O+'_blocks.json')); dp=json.load(open(O+'_dispatch2.json'))
    m=json.load(open('evidence/fm24/reports/editor_schema/master.json'))
    fields=m['entities']['club.xml'][0]['fields'][211:328]
    ent=sorted(bl,key=lambda b:b['entry'])
    def res(tfo):
        for b in ent:
            if b['entry']<=tfo<b['entry']+24: return b
        return None
    out=[]
    for f in fields:
        c=f['field']; cand=[]
        for a,tg in dp.get(c,[]):
            for mn,t in tg:
                b=res(int(t,16))
                if b: cand.append({'cmp':a,'mn':mn,'tgt':t,'rt':b['rec_type'],'tag':b['tag'],'entry':b['entry']})
        rec={'code':c,'name':f['name'],'type':f['type'],'cand':cand}
        if len(cand)==1:
            rec['rec_type']=cand[0]['rt']; rec['tag']=cand[0]['tag']
            to=TAGOFF.get(cand[0]['tag'])
            if to: rec['wire_off']=to[0]; rec['width']=to[1]
        out.append(rec)
    json.dump(out,open(O+'_codecand.json','w'),indent=0)
    ok=[r for r in out if r.get('rec_type') is not None]
    print('codes',len(out),'resolved',len(ok))
    from collections import Counter
    print(Counter((r.get('rec_type'),r.get('tag')) for r in ok))
    miss=[r['code'] for r in out if r.get('rec_type') is None]
    print('miss',len(miss),miss[:50])
    amb=[(r['code'],len(r['cand'])) for r in out if r.get('rec_type') is None and r['cand']]
    print('amb',amb[:20])
if __name__=='__main__':
    if '--help' in sys.argv: print('usage: t88_slots2.py'); sys.exit(0)
    main()
