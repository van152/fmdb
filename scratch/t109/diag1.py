import importlib.util, json, sys, collections
spec = importlib.util.spec_from_file_location("t109", "scripts/t109_big3_l3_join.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
rows_all = m.load_json("reports/xml_denominator_coverage.json")["rows"]
memmap = m.load_json("scratch/t108/out2/fourcc_mem_map_v2.json")
vt = m.load_json("scratch/t95/vtable_index.json")
parser = m.SerializerParser("scratch/t95/funcs")
book = m.SerializerBook(parser, vt)
joined = json.load(open("scratch/t109/out/big3_l3_join.json"))["rows"]
own = m.ENTITY_OWN_TABLES
def stream_offsets(tk):
    s = set()
    for lane in ("server","client"):
        for op in book.stream(tk, lane)[0]:
            if op.get("off_int") is not None:
                s.add((op["off_int"], op.get("lane"), op.get("line"), op["file"]))
    return s
cache={}
gap=[r for r in joined if r["new_class"]=="gap_off_not_in_read_stream"]
print("rows", len(gap))
cnt=collections.Counter()
samples=collections.defaultdict(list)
for r in gap:
    ent=r["entity"]
    offs=set()
    for tk in own[ent]:
        if tk not in cache: cache[tk]=stream_offsets(tk)
        for o in cache[tk]: offs.add(o[0])
    memoff=r["mem_off"]
    # is memoff multiple of 8 of an offset present? is memoff*8 present? memoff//8 present?
    key = None
    if memoff in offs: key="exact_present_but_missed"
    elif memoff*8 in offs: key="x8_present(scaled)"
    elif memoff//8 in offs and memoff%8==0: key="div8_present"
    else:
        near=[o for o in offs if abs(o-memoff)<=8]
        key="near%r"%sorted(near)[:3] if near else "absent"
    cnt[key]+=1
    if len(samples[key])<4: samples[key].append((r["id"],r["code"],memoff,r.get("getter_cite"),r.get("access_kind")))
for k,v in cnt.most_common(20):
    print(v,k)
    for s in samples[k]: print("     ",s)
