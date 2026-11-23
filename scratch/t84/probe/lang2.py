import sys, struct, re
sys.path.insert(0,'scratch/t84/probe')
import lib
for nm in ('8_3.dat','8_10.dat','8_25.dat','8_0.dat','8_2.dat'):
    raw=lib.load_member('lang_update',nm)
    runs=[(m.start(),m.group()[:40]) for m in re.finditer(rb'[ -~]{5,}',raw)]
    print(nm,'len',len(raw),'runs',len(runs),runs[:4])
    print('   head',raw[:40].hex(' '))
