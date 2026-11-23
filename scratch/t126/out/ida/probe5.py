import sys, json
sys.path.insert(0, r"C:\Program Files\IDA Professional 9.4\idalib\python")
ROOT = r"D:\tmp2b\fm24-db"
import idapro
idapro.open_database(ROOT+r"\scratch\t95\editor_work.i64", run_auto_analysis=False)
import idautils, ida_funcs, ida_bytes, struct
target=0x14083B5F0
xs=set()
for x in idautils.XrefsTo(target):
    f=ida_funcs.get_func_start(x.frm)
    xs.add(f)
print('callers of sub_14083B5F0:', len(xs))
cand=[]
for f in sorted(xs):
    fi=ida_funcs.get_func(f)
    sz=fi.end_ea-f
    b=ida_bytes.get_bytes(f, sz)
    hits=0
    for v in range(1346659000,1346665000):
        pass
    cand.append((hex(f), sz))
for c in cand: print(c)
