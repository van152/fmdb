import json,struct,sys
sys.path.insert(0,'scratch/t102/work'); sys.path.insert(0,'scripts')
import an_body
J=json.load(open('scratch/t102/work/join.json'))
HW={'sub_140DB8980':4}
LSTR={'sub_140814B10'}
T=[0,2,5,6,7,8,18,19,21,22,23,27,35,41,47,56]
for tid in T:
    for side in ('server','client'):
        v=J[str(tid)][side]
        if not v: print(f't{tid} {side}: no reader'); continue
        d=an_body.payload(tid,side); n=struct.unpack_from('<I',d,8)[0]
        body=len(d)-22
        S = body//n if body%n==0 else None
        items=v['items']
        print(f't{tid} {side}: n_items={len(items)} stride={S}')
        cum=0; unknown=False
        for it in items:
            if it['kind']=='direct':
                w=it['w']
            else:
                fn=it['fn']
                if fn in HW: w=HW[fn]
                elif fn in LSTR: w='lstr'
                else: w='?'
            if w=='?': unknown=True
            print(f'    +{cum:4d} {it["kind"]:6s} mem={it["mem"]:3d} w={w} line={it["line"]} {it.get("fn","")}')
            if isinstance(w,int): cum+=w
            else: cum=None if cum is None else cum
        print(f'    tiled_known={cum} target_body={S-13 if S else "var"}')
