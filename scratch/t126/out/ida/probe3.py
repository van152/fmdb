import sys
sys.path.insert(0, r"C:\Program Files\IDA Professional 9.4\idalib\python")
ROOT = r"D:\tmp2b\fm24-db"
import idapro
idapro.open_database(ROOT+r"\scratch\t95\editor_work.i64", run_auto_analysis=False)
import idc, ida_funcs, ida_bytes, struct
for ea in range(0x141465000, 0x141468000, 1):
    pass
# enumerate functions via funcs list
import idautils
out=[]
for ea in idautils.Functions(0x141460000, 0x141470000):
    f=ida_funcs.get_func(ea)
    out.append((hex(ea), f.end_ea-ea))
print(len(out))
for a,b in out:
    print(a,b)
