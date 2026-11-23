import sys, json, time
sys.path.insert(0, r"C:\Program Files\IDA Professional 9.4\idalib\python")
ROOT = r"D:\tmp2b\fm24-db"
t0=time.time()
import idapro
idapro.open_database(ROOT+r"\scratch\t95\editor_work.i64", run_auto_analysis=False)
print("opened", time.time()-t0, flush=True)
import ida_funcs, ida_bytes, ida_hexrays, ida_name
for va in [0x141467B70]:
    f = ida_funcs.get_func(va)
    print(hex(va), f.start_ea if f else None, f.end_ea if f else None, flush=True)
    try:
        cf = ida_hexrays.decompile(va)
        print("lines", cf.__len__() if hasattr(cf,'__len__') else '?', flush=True)
        open(ROOT+r"\scratch\t126\out\ida\test_141467b70.c","w").write(str(cf))
    except Exception as e:
        print("err", e, flush=True)
# find xrefs
import idautils
print("xrefs:", [hex(x.frm) for x in idautils.XrefsTo(0x141467B70)][:20], flush=True)
idapro.close_database(False)
