import json, collections, importlib.util, re, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe=pm.default(); raw=pe.raw
md=Cs(CS_ARCH_X86, CS_MODE_64)
spec2 = importlib.util.spec_from_file_location("_b","scratch/t07/out/build.py")
b = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(b)
hits, md = b.decode_cmp_hits(pe); hits.sort()
lo,hi=int(sys.argv[1],16),int(sys.argv[2],16)
sub=[h for h in hits if lo<=h[0]<hi]
print('hits',len(sub),'codes',len({h[1] for h in sub}))
recs=b.find_candidates(pe, sub, md)
print('resolved',len(recs),'codes',len({r['code'] for r in recs}))
for r in sorted(recs,key=lambda r:(r['object_off'],r['code']))[:40]:
    print(f"  {r['code']} {r['object_off']:#5x} {r['size']} {r['kind']} {r['file_off']}")
