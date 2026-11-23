import json,sys,struct
sys.path.insert(0,'scratch/t102/work'); sys.path.insert(0,'scripts')
import an_body
J=json.load(open('scratch/t102/work/join.json'))
FIX={0:77,2:43,5:None,6:40,19:46,21:181,22:79,23:14,35:15,56:13}
for tid in (0,2,6,19,21,22,23,35,56):
    for arch in ('server','client'):
        d=an_body.payload(tid,arch); n=struct.unpack_from('<I',d,8)[0]
        body=len(d)-22
        S=body//n
        print(f't{tid} {arch} stride={S} body={S-13}')
        # identity check at S-13
        ok=all(struct.unpack_from('<I',d,13+r*S+S-13)[0]==r for r in range(0,n,7))
        uok=all(struct.unpack_from('<I',d,13+r*S+S-9)[0]==struct.unpack_from('<I',d,13+r*S+S-5)[0] for r in range(0,n,7))
        print('   ord_ok',ok,'uid_eq',uok,'sel_set',sorted({d[13+r*S] for r in range(0,n,5)}))
