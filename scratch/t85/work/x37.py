import sys,struct,re
sys.path.insert(0,'scripts'); sys.stdout.reconfigure(encoding='utf-8')
import t85_common as C
raw=C.payload('client','client_db/table_10.dat',24732)
offs=C.identity_offsets(raw)
print('rows',len(offs),'hdr',raw[:14].hex(' '),'first ident',offs[0])
starts=[14]+[o+13 for o in offs[:-1]]
lens=[o+13-s for o,s in zip(offs,starts)]
print('lens[:8]',lens[:8],'sum',sum(lens),'payload',len(raw))
for i in (0,1,139):
    b=raw[starts[i]:starts[i]+lens[i]]
    print(f'row{i} len={lens[i]}')
    print('  ',b.hex(' '))
    print('  asc', ''.join(chr(c) if 32<=c<127 else '.' for c in b))
