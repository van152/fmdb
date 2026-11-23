import sys
sys.path.insert(0, r"C:\Program Files\IDA Professional 9.4\idalib\python")
ROOT = r"D:\tmp2b\fm24-db"
import idapro
idapro.open_database(ROOT+r"\scratch\t95\editor_work.i64", run_auto_analysis=False)
import ida_hexrays, ida_funcs, idautils
for va,name in [(0x141467990,'blk_get'),(0x141466c30,'thunk22'),(0x14146f900,'f120')]:
    try:
        cf=ida_hexrays.decompile(va)
        open(ROOT+rf"\scratch\t126\out\ida\{name}_{va:x}.c","w").write(str(cf))
        print(va, len(str(cf).splitlines()))
    except Exception as e:
        print(va,'err',e)
print('xrefs to 0x141467990:', [hex(x.frm) for x in idautils.XrefsTo(0x141467990)][:20])
