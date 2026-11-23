import sys, json, struct
sys.path.insert(0, r"C:\Program Files\IDA Professional 9.4\idalib\python")
ROOT = r"D:\tmp2b\fm24-db"
import idapro
idapro.open_database(ROOT+r"\scratch\t95\editor_work.i64", run_auto_analysis=False)
import ida_bytes, ida_segment, ida_funcs, ida_hexrays, ida_name, idautils, idc

def find_ptrs(target):
    res=[]
    for seg in idautils.Segments():
        s=idc.get_segm_name(seg)
        if 'rdata' not in s.lower() and 'data' not in s.lower(): continue
        ea=idc.get_segm_start(seg); end=idc.get_segm_end(seg)
        cur=ea
        while cur<end:
            v=ida_bytes.get_qword(cur)
            if v==target:
                res.append(cur)
            cur+=8
    return res

for t in [0x141467B70, 0x1414679F0, 0x141467A00, 0x141467A80]:
    print(hex(t), [hex(x) for x in find_ptrs(t)][:10], flush=True)
