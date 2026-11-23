import sys, struct
sys.path.insert(0, r"C:\Program Files\IDA Professional 9.4\idalib\python")
ROOT = r"D:\tmp2b\fm24-db"
import idapro
idapro.open_database(ROOT+r"\scratch\t95\editor_work.i64", run_auto_analysis=False)
import idautils, ida_funcs, ida_bytes
target=0x14083B5F0
xs=set(ida_funcs.get_func_start(x.frm) for x in idautils.XrefsTo(target))
keys=[1346659169,1346659181,1346664306]
pats=[struct.pack('<I',k) for k in keys]
found=[]
for f in sorted(xs):
    fi=ida_funcs.get_func(f); sz=fi.end_ea-f
    b=ida_bytes.get_bytes(f, sz)
    n=sum(1 for p in pats if p in b)
    if n>=2:
        found.append((hex(f), sz, n))
print('block reg_prop candidates:', found)
# also check 143bdeaf0-like sanity
for f,sz,n in found:
    try:
        import ida_hexrays
        cf=ida_hexrays.decompile(int(f,16))
        open(ROOT+rf"\scratch\t126\out\ida\regprop_blk_{f[2:]}.c","w").write(str(cf))
        print('decompiled', f, len(str(cf).splitlines()))
    except Exception as e:
        print('err',f,e)
