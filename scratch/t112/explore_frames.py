import sys, struct, json, pathlib, runpy, collections
ROOT=pathlib.Path(r"D:\tmp2b\fm24-db")
NY=runpy.run_path(str(ROOT/"scripts/fm24_dump.py"))
codec=NY["_reader"]()
load=lambda a,t: NY["load_payload"](codec,a,t)
ents={a:codec["list_tables"](NY["DB_DIR"]/f"{a}_db.dat", f"{a}_db.dat") for a in ("client","server")}
for a in ents:
    ids=sorted(e["table_id"] for e in ents[a] if e.get("table_id") is not None)
    print(a, len(ids), ids)
