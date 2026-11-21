import sys,struct
sys.path.insert(0,'scripts'); sys.stdout.reconfigure(encoding='utf-8')
import t85_common as C
raw=C.payload('server','server_db/table_66.dat',18094)
print('head',raw[:14].hex(' '))
offs=C.identity_offsets(raw)
print('rows',len(offs))
starts=[14]+[o+13 for o in offs[:-1]]
lens=[o+13-s for o,s in zip(offs,starts)]
print('lens',lens[:12],'set',sorted(set(lens))[:10])
for i in (0,1,2,3,4,5):
    b=raw[starts[i]:starts[i]+lens[i]]
    print(f'row{i} len={lens[i]} {b.hex(" ")}')
