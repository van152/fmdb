import runpy, sys, struct
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw = core['load_payload']('server', 24)
n = struct.unpack_from('<I', raw, 8)[0]
pos = 14; rows=[]
for j in range(n):
    for ln in range(86, 667):
        e = pos + ln
        if e > len(raw)-8: break
        if struct.unpack_from('<I', raw, e-13)[0] == j:
            a,b = struct.unpack_from('<II', raw, e-9)
            if a==b!=0:
                rows.append((pos,ln)); pos = e; break
    else:
        print('stuck', j); break
np.save('scratch/t76a/_rows24.npy', np.array(rows))
print('rows', len(rows), 'end', pos, 'footer', len(raw)-pos)
lens = np.array([l for _,l in rows])
print('modal len count 86:', int((lens==86).sum()), 'of', len(lens))
# print a few 86-byte rows
for j in [0,1,2,3,4]:
    p,l = rows[j]
    print(j, l, raw[p:p+min(l,120)].hex(' '))
