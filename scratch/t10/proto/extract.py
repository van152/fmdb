import json, sys, importlib.util
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe=pm.default()
spec2 = importlib.util.spec_from_file_location("_b","scratch/t07/out/build.py")
b = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(b)
hits, md = b.decode_cmp_hits(pe)
print("hits", len(hits))
lo,hi = int(sys.argv[1],16), int(sys.argv[2],16)
sub=[h for h in hits if lo<=h[0]<hi]
print("chain hits", len(sub), "distinct codes", len({h[1] for h in sub}))
recs = b.find_candidates(pe, sub, md)
print("records", len(recs), "codes with record", len({r['code'] for r in recs}))
codes={h[1] for h in sub}
got={r['code'] for r in recs}
print("codes with narrow access", len(got), f"{len(got)/len(codes):.1%}")
import collections
print(collections.Counter(r['kind'] for r in recs))
# print some
seen=set()
for r in sorted(recs,key=lambda r:(r['object_off'],r['code']))[:40]:
    print(f"  {r['code']} off={r['object_off']:#x} size={r['size']} {r['kind']} {r['file_off']}")
