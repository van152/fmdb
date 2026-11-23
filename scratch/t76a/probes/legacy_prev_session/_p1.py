import runpy, sys, struct, json
from pathlib import Path
sys.path.insert(0, 'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_c = core['load_payload']('client', 21)
raw_s = core['load_payload']('server', 21)
print('len', len(raw_c), len(raw_s))
H, Sc, n = 14, 38, 48413
print('client row0', raw_c[H:H+Sc].hex(' '))
print('client row1', raw_c[H+Sc:H+2*Sc].hex(' '))
Hs, Ss = 14, 181
print('server row0 first 60', raw_s[Hs:Hs+60].hex(' '))
print('server row0 tail ', raw_s[Hs+150:Hs+181].hex(' '))
# identity checks
ok = all(struct.unpack_from('<I', raw_c, H+j*Sc+25)[0]==j for j in range(n))
print('client ord ok', ok)
oks = all(struct.unpack_from('<I', raw_s, Hs+j*Ss+168)[0]==j for j in range(n))
print('server ord ok', oks)
