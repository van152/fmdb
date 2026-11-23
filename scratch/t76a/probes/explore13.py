import runpy, sys, json
import numpy as np
sys.path.insert(0, 'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
rawC = core["load_payload"]("client", 21)
rawS = core["load_payload"]("server", 21)
H, n = 14, 48413
mc = np.frombuffer(rawC, np.uint8, H + n * 38)[H:].reshape(n, 38)
ms = np.frombuffer(rawS, np.uint8, H + n * 181)[H:].reshape(n, 181)
SV = ms[:, :143]
NROWS = {"city": 56293, "club": 84259, "nation": 251, "region": 28, "comp": 7047,
         "stadium": 48413, "team": 84507, "continent": 7, "language": 126,
         "weather": 334, "local_region": 2488}
NULL = 0xFFFFFFFF


def U(m, o, w):
    return np.ascontiguousarray(m[:, o:o + w]).view(f"<u{w}").ravel().astype(np.int64)


def ordcheck(v, N, name):
    keep = v != NULL
    vv = v[keep]
    if vv.size == 0:
        return None
    return {"what": name, "null": int((~keep).sum()), "nonnull": int(keep.sum()),
            "min": int(vv.min()), "max": int(vv.max()), "distinct": int(np.unique(vv).size),
            "in_domain": round(float((vv < N).mean()), 6),
            "max_over_N": round(float(vv.max() / N), 4),
            "null0_present": int((vv == 0).sum())}


print("=== CLIENT FK candidates ===")
for o, w, tg in ((3, 4, "city"), (7, 4, "stadium")):
    v = U(mc, o, w)
    print(json.dumps(ordcheck(v, NROWS[tg], f"client@{o}->{tg}"), ensure_ascii=False))

print("\n=== CLIENT @3 wrong-UID control: city UIDs vs city ordinal ===")
try:
    city = core["reference_uids"]("client", 2)
    print("city ref ok:", city["ok"], "domain:", len(city["uids"]) if city["ok"] else city["why"])
    if city["ok"]:
        s = set(city["uids"])
        v = U(mc, 3, 4)
        print("  Scti@3 in city UID set:", int(sum(1 for x in v.tolist() if x in s)), "/", n,
              "=", round(sum(1 for x in v.tolist() if x in s) / n, 6))
except Exception as e:
    print("city ref FAILED:", type(e).__name__, e)

print("\n=== config: are client @3 values dense ordinals covering city rows? ===")
v3 = U(mc, 3, 4)
print("  distinct", np.unique(v3).size, "of", NROWS["city"], "-> coverage",
      round(np.unique(v3).size / NROWS["city"], 4))
v7 = U(mc, 7, 4)
nn7 = v7[v7 != NULL]
print("  Snbs@7 distinct", np.unique(nn7).size, "nonnull", nn7.size)

print("\n=== SERVER @16 club ordinal + UID control ===")
v16 = U(SV, 16, 4)
print(json.dumps(ordcheck(v16, NROWS["club"], "server@16->club"), ensure_ascii=False))
try:
    cl = core["reference_uids"]("client", 3)
    print("club ref ok:", cl["ok"], "domain:", len(cl["uids"]) if cl["ok"] else cl["why"])
    if cl["ok"]:
        s = set(cl["uids"])
        nn = v16[v16 != NULL]
        hits = int(sum(1 for x in nn.tolist() if x in s))
        print("  server@16 in club UID set:", hits, "/", nn.size, "=", round(hits / nn.size, 6))
except Exception as e:
    print("club ref FAILED:", type(e).__name__, e)
