import sys, struct, json, pathlib, runpy
ROOT=pathlib.Path(r"D:\tmp2b\fm24-db")
NY=runpy.run_path(str(ROOT/"scripts/fm24_dump.py"))
codec=NY["_reader"]()
load=lambda a,t: NY["load_payload"](codec,a,t)
print(f"{'arch':7s}{'tid':>4s}{'len':>11s}{'hdr_hex':>30s}{'cnt':>9s} stride ok_ident")
for a in ("client","server"):
    ents=codec["list_tables"](NY["DB_DIR"]/f"{a}_db.dat", f"{a}_db.dat")
    for e in sorted(ents, key=lambda x: x["table_id"]):
        t=e["table_id"]
        try: raw=load(a,t)
        except Exception as ex:
            print(f"{a:7s}{t:4d} LOADFAIL {ex}"); continue
        cnt=struct.unpack_from("<I",raw,8)[0]
        body=len(raw)-14-8
        ok=[]
        if cnt and body % cnt==0:
            st=body//cnt
            # verify identity for up to 3 rows and last
            good=0; test=0
            for i in ([0,1,2,cnt-1] if cnt>3 else list(range(cnt))):
                b=14+i*st
                o,d,u=struct.unpack_from("<III",raw,b+st-12)
                test+=1
                if o==i and raw[b+st-1]==0: good+=1
            ok.append(f"{'ok' if good==test else 'bad'}:{good}/{test}")
        print(f"{a:7s}{t:4d}{len(raw):11d}  {raw[:14].hex():>28s}{cnt:9d} {st if cnt and body%cnt==0 else -1:6d} {' '.join(ok)}")
