import importlib.util, json, re, collections
spec = importlib.util.spec_from_file_location("t109", "scripts/t109_big3_l3_join.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
vt = m.load_json("scratch/t95/vtable_index.json")
parser = m.SerializerParser("scratch/t95/funcs")
book = m.SerializerBook(parser, vt)
joined = json.load(open("scratch/t109/out/big3_l3_join.json"))["rows"]
own = m.ENTITY_OWN_TABLES

ALIAS = {}
def touch(va):
    if va in ALIAS: return ALIAS[va]
    p = parser.parse(va)
    lines = parser.read(va)
    out = {}
    if lines is None:
        ALIAS[va] = out; return out
    elem = p["a1_elem"] if p else 1
    # signature line may span; find aliases `vN = (T *)(a1 + K)` and simple `vN = a1`
    aliases = {}
    for i, ln in enumerate(lines, 1):
        for mm in re.finditer(r"(v\d+)\s*=\s*\(?\s*(?:[A-Za-z_][A-Za-z0-9_ ]*\s*\*+\s*\)?\s*)?\(?\s*a1\s*\+\s*(" + m.NUM + r")", ln):
            aliases.setdefault(mm.group(1), set()).add(m.pnum(mm.group(2)) * elem)
    def scan(i, ln):
        for mm in re.finditer(r"(?<![A-Za-z0-9_])a1\s*\+\s*(" + m.NUM + r")", ln):
            out.setdefault(m.pnum(mm.group(1)) * elem, i)
        for name, bases in aliases.items():
            for b in bases:
                for mm in re.finditer(r"(?<![A-Za-z0-9_])" + name + r"\s*\+\s*(" + m.NUM + r")", ln):
                    out.setdefault(b + m.pnum(mm.group(1)), i)
        for name, bases in aliases.items():
            for b in bases:
                if re.search(r"(?<![A-Za-z0-9_])" + name + r"(?![A-Za-z0-9_])", ln):
                    out.setdefault(b, i)
    for i, ln in enumerate(lines, 1):
        scan(i, ln)
    ALIAS[va] = out
    return out

def own_touches(entity):
    s = {}
    for tk in own[entity]:
        slot = book.table_slots.get(tk, {})
        for lane in ("server", "client"):
            v = slot.get(lane)
            if not v: continue
            for node in book.chain(v):
                for off, line in touch(node["va"]).items():
                    s.setdefault(off, ("table_%d/%s" % tk, lane, node["va"], line))
    return s

gap = [r for r in joined if r["new_class"].startswith("gap")]
res = collections.Counter()
hit_samples = collections.defaultdict(list)
for r in gap:
    t = own_touches(r["entity"])
    off = r.get("mem_off")
    if off is None:
        res["no_memoff"] += 1; continue
    if off in t:
        res["would_close:" + r["new_class"]] += 1
        if len(hit_samples[r["new_class"]]) < 5: hit_samples[r["new_class"]].append((r["id"], r["code"], off, t[off]))
    else:
        res["still_open:" + r["new_class"]] += 1
for k, v in res.most_common(): print(v, k)
for k, v in hit_samples.items():
    print("==", k)
    for s in v: print("   ", s)
