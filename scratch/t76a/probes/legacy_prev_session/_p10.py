import runpy, sys, re
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_c = core['load_payload']('client', 21); raw_s = core['load_payload']('server', 21)
print('client header', raw_c[:14].hex(' '), 'footer', raw_c[-8:].hex(' '))
print('server header', raw_s[:14].hex(' '), 'footer', raw_s[-8:].hex(' '))
for name, raw in (('c',raw_c),('s',raw_s)):
    runs = [m.group() for m in re.finditer(rb'[\x20-\x7e]{5,}', raw)]
    print(name, 'printable runs', len(runs), runs[:8])
