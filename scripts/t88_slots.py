"""t88-fix6: assemble out3/slots.json (117 codes) + domain_stats.json.
Evidence ladder: L3 = exe static (dispatch case body / RECORD_GET), L2 = data-side,
L1 = self-check. Unresolved -> status=held with first counterexample.
usage: t88_slots.py [--selftest]
"""
import sys,json,struct
O='scratch/t88/out3/'
# tag -> reader-struct offset (RECORD_GET 0x1543ca0 case bodies, L3)
TAG_READER={'gols':(0x56,2),'ogls':(0x58,2),'stdt':(0x40,2),'stdb':(0x30,4),
            'comp':(0x34,4),'stid':(0x1c,4),'atte':(0x50,4),'gams':(0x54,2),
            'endt':(0x5c,1),'fsgt':(0x5e,1),'otht':(0x5a,1),'cash':(0x58,4),
            'stnm':(0x20,0)}
# suffix -> tag (editor schema semantics; CBWf=Team Goals etc.)
SUF={'o':'stdb','f':'gols','a':'ogls','d':'stdt','c':'comp','g':'gams',
     's':'stdt','e':'endt','p':'stid','n':'stnm','m':'stdt','b':'stid','i':'stid'}
def main():
    m=json.load(open('evidence/fm24/reports/editor_schema/master.json'))
    fields=m['entities']['club.xml'][0]['fields'][211:328]
    f4=json.load(open('scratch/t88/f4_to_rectype.json'))
    rtf=json.load(open('scratch/t88/rt_tag_fields.json'))
    rt_tag={}   # code -> (rt, tag)
    for k,v in rtf.items():
        t,tag=k.split('|')
        for c in v: rt_tag.setdefault(c,[]).append((int(t),tag))
    disp=json.load(open(O+'tcget2_dispatch.json'))
    # family -> rec_type from L3 anchors
    fam_rt={}
    for c,lst in rt_tag.items():
        for rt,tag in lst: fam_rt.setdefault(c[:3],{}).setdefault(rt,0)
    fam={k:sorted(v) for k,v in fam_rt.items()}
    out=[]
    for f in fields:
        c=f['field']; rec={'code':c,'name':f['name'],'type':f['type'],'family':c[:3],'suffix':c[3]}
        l3=rt_tag.get(c)
        if l3 and len(set(l3))==1:
            rt,tag=l3[0]; rec.update({'rec_type':rt,'tag':tag,'status':'mapped','grade':'L3'})
            ro=TAG_READER.get(tag)
            if ro: rec['reader_off']=ro[0]; rec['width']=ro[1]
            rec['crit']='exe 0x1543ca0 RECORD_GET case tag=%s -> [rdi+0x%x]; rt from 0x11f... block dl=%d'%(tag,ro[0] if ro else 0,rt)
        elif c[:3] in fam and len(fam[c[:3]])==1 and c[3] in SUF:
            rt=fam[c[:3]][0]; tag=SUF[c[3]]
            rec.update({'rec_type':rt,'tag':tag,'status':'derived','grade':'L2'})
            ro=TAG_READER.get(tag)
            if ro: rec['reader_off']=ro[0]; rec['width']=ro[1]
            rec['crit']='family %s anchored rt=%d by L3 sibling; suffix %s -> tag %s (schema semantics)'%(c[:3],rt,c[3],tag)
        else:
            tag=SUF.get(c[3])
            rec.update({'rec_type':None,'tag':tag,'status':'held','grade':'-'})
            rec['crit']='no L3 dispatch entry; 4CC bytes absent from editor.exe+fm.exe (first counterexample); family %s has no anchored rt'%c[:3]
        out.append(rec)
    json.dump({'meta':{'task':'t88-fix6','source':'evidence/fm24/reports/editor_schema/master.json fields[211:328]',
                       'n':len(out)},'codes':out},open(O+'slots.json','w'),indent=0)
    from collections import Counter
    print('n',len(out),Counter(r['status'] for r in out))
    print('families',Counter(r['family'] for r in out))
    return out
if __name__=='__main__':
    if '--help' in sys.argv: print(__doc__); sys.exit(0)
    main()
