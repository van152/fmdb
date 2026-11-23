import sys, struct
sys.path.insert(0, r"C:\Program Files\IDA Professional 9.4\idalib\python")
ROOT = r"D:\tmp2b\fm24-db"
import idapro
idapro.open_database(ROOT+r"\scratch\t95\editor_work.i64", run_auto_analysis=False)
import idc, ida_bytes, ida_segment, idautils, ida_funcs
keys=[1346659169,1346659171,1346659181,1346664306,1346663014]
pats={k:struct.pack('<I',k) for k in keys}
for seg in idautils.Segments():
    name=idc.get_segm_name(seg); s=idc.get_segm_start(seg); e=idc.get_segm_end(seg)
    b=ida_bytes.get_bytes(s, e-s)
    if not b: continue
    hits={}
    for k,p in pats.items():
        pos=[]; i=b.find(p)
        while i>=0 and len(pos)<6:
            pos.append(hex(s+i)); i=b.find(p,i+1)
        if pos: hits[k]=pos
    if hits: print(name, hex(s), hex(e), hits)
