import sys, struct
sys.path.insert(0, r"C:\Program Files\IDA Professional 9.4\idalib\python")
ROOT = r"D:\tmp2b\fm24-db"
import idapro
idapro.open_database(ROOT+r"\scratch\t95\editor_work.i64", run_auto_analysis=False)
import ida_hexrays, ida_funcs, idautils
for va in [0x141465590, 0x1414622c0]:
    try:
        cf=ida_hexrays.decompile(va)
        txt=str(cf)
        p=ROOT+rf"\scratch\t126\out\ida\d_{va:x}.c"
        open(p,"w",encoding="utf-8").write(txt)
        print(hex(va), len(txt.splitlines()), p, flush=True)
        print('  xrefs:', [hex(x.frm) for x in idautils.XrefsTo(va)][:8], flush=True)
    except Exception as e:
        print(hex(va),'err',e, flush=True)
