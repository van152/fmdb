import sys, struct, re
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
for nm in ('8_10.dat','8_25.dat','8_3.dat','8_5.dat','8_0.dat'):
    raw=lib.load_member('lang_update',nm)
    cnt=struct.unpack_from('<I',raw,8)[0]
    print(f'== {nm} len={len(raw)} hdr_cnt={cnt} u32@12={struct.unpack_from("<I",raw,12)[0]}')
    print('   head', raw[:60].hex(' '))
    for nd in (b'England',b'Premier',b'Serie A',b'Liverpool',b'China'):
        print('    ',nd, raw.find(nd))
