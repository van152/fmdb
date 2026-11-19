import json, collections
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import importlib.util
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe = pm.default(); raw = pe.raw
md = Cs(CS_ARCH_X86, CS_MODE_64)
hits = json.loads(Path("scratch/t10/proto/hits.json").read_text())
hits.sort()
print("hits",len(hits))
# gap histogram
gaps = collections.Counter()
for a,b in zip(hits,hits[1:]):
    d=b[0]-a[0]
    gaps[min(d,0x10000)//0x10*0x10]+=1
print(sorted(gaps.items())[:25])
