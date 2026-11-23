"""t81-fix1 probe61 — exact sets + server t6 27B column profile."""
import json
import runpy
import struct
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
core = runpy.run_path(str(REPO / "scripts" / "t73_mapper_core.py"), run_name="p61")
S = json.loads((REPO / "evidence/fm24/reports/editor_schema/master.json").read_text("utf-8"))

raw_c = core["load_payload"]("client", 6)
raw_s = core["load_payload"]("server", 6)
n, Sc, Ss = 115, 16, 40

c0 = {raw_c[14 + j * Sc] for j in range(n)}
c1 = {raw_c[14 + j * Sc + 1] for j in range(n)}
c2 = {raw_c[14 + j * Sc + 2] for j in range(n)}
print("client off0 set:", sorted(c0))
print("client off1 set:", sorted(c1))
print("client off2 set:", sorted(c2))
icla = {int(v["enum"]) for v in S["enums"]["icla"]["values"]}
iscl = {int(v["enum"]) for v in S["enums"]["iscl"]["values"]}
print("icla==off0:", icla == c0, "| icla-{-3}==", icla - {-3} == c0, sorted(icla - c0), sorted(c0 - icla))
print("iscl==off1:", iscl == c1, "| iscl-{-3}==", iscl - {-3} == c1, sorted(iscl - c1), sorted(c1 - iscl))

print("\n--- server t6 27B columns")
for off in range(27):
    b = bytes(raw_s[14 + j * Ss + off] for j in range(n))
    row = {"off": off, "u8d": len(set(b)), "u8": sorted(set(b))[:12]}
    if off + 2 <= 27:
        v = [struct.unpack_from("<H", raw_s, 14 + j * Ss + off)[0] for j in range(n)]
        row["u16"] = {"min": min(v), "max": max(v), "d": len(set(v))}
    if off + 4 <= 27:
        v = [struct.unpack_from("<I", raw_s, 14 + j * Ss + off)[0] for j in range(n)]
        f = [struct.unpack_from("<f", raw_s, 14 + j * Ss + off)[0] for j in range(n)]
        fin = [x for x in f if x == x and abs(x) != float("inf")]
        row["u32"] = {"min": min(v), "max": max(v), "d": len(set(v)),
                      "n_ff": v.count(0xFFFFFFFF), "n0": v.count(0)}
        row["f32"] = {"fin": len(fin), "min": min(fin) if fin else None,
                      "max": max(fin) if fin else None,
                      "plaus": len(fin) == len(f) and all(abs(x) < 1e6 for x in f)}
    print(json.dumps(row, ensure_ascii=False)[:230])
