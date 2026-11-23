import importlib.util, json, collections
spec = importlib.util.spec_from_file_location("t109", "scripts/t109_big3_l3_join.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
d = json.load(open("scratch/t109/out/big3_l3_join.json"))
rows = d["rows"]
cross = [c for c in d["accepted_l3_crosscheck"] if c["verdict"].startswith("conflict")]
print("conflicts", len(cross))
for c in cross[:40]:
    r = [x for x in rows if x["entity"] == c["entity"] and x["code"] == c["code"]]
    rr = r[0] if r else None
    print("  %-6s %-5s acc=%-6s engine=%-6s class=%-28s %s" % (
        c["entity"], c["code"], c.get("accepted_off"), c.get("engine_off"),
        rr and rr["new_class"], (rr and rr.get("gap_reason") or "")[:80]))
print()
g = [r for r in rows if r["new_class"] == "gap_off_not_in_read_stream"]
print("gap_off_not_in_read_stream", len(g), collections.Counter(r["entity"] for r in g))
for r in g[:12]:
    print("  %-20s %-5s off=%-6s %-22s %s" % (r["id"], r["code"], r["mem_off"], r["access_kind"], r["getter_cite"]))
