import importlib.util, json, struct, hashlib
from pathlib import Path
spec=importlib.util.spec_from_file_location("m","D:/tmp2b/fm24/scripts/modding_read_dbdat.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
DB=Path("Z:/SteamLibrary/steamapps/common/Football Manager 2024/data/database/db/2430/2430_fm")
OUT=Path("D:/tmp2b/fm24-db/scratch/t02/inbox/fw8/framework.json")
def get(a):
    p,pk,l=m._entries(db_path=DB, archive=a)
    e=m._resolve_table(8,l["entries"],p.name)
    return m._decompress_entry(pk,l["data_base"],e), e["path"]
def side(a):
    raw,name=get(a); n=len(raw); cnt=struct.unpack_from("<I",raw,8)[0]
    pos=14; lens=[]; trailers=[]
    for i in range(cnt):
        ln=struct.unpack_from("<I",raw,pos)[0]
        assert ln<=64 and pos+34+ln<=n
        trailers.append(raw[pos+4+ln:pos+34+ln].hex(" "))
        lens.append(4+ln+30)
        pos+=34+ln
    ok = pos+8==n
    return {"member":name,"count":cnt,"stride":None,"variable":True,
            "rows_offset":"0xe","payload_len":n,
            "header":raw[:14].hex(" "),"footer":raw[-8:].hex(" "),
            "payload_sha256":hashlib.sha256(raw).hexdigest(),
            "row_len_formula":"row_len = 4 + len(utf8_name) + 30  (u32 name_len + name bytes + 30B trailer)",
            "row_len_min":min(lens),"row_len_max":max(lens),"row_len_distinct":len(set(lens)),
            "row_len_sample_first10":lens[:10],
            "trailer_len":30,"trailer_sample_first3":trailers[:3],
            "rows_end":"0x%x"%pos,"footer_len":n-pos,
            "closure":f"14 + sum(row_len_i) + 8 == {n} (sum={pos-14}, count={cnt})",
            "closure_ok":ok,"_raw":raw}
c=side("client_db.dat"); s=side("server_db.dat")
cr,oo=c.pop("_raw"),s.pop("_raw")
k=0
while k<min(len(cr),len(oo)) and cr[k]==oo[k]: k+=1
res={"type_id":8,"status":"complete" if (c["closure_ok"] and s["closure_ok"]) else "in_progress",
     "client":c,"server":s,
     "relation":f"payloads byte-identical={cr==oo}; common prefix {k} of {len(cr)}/{len(oo)} bytes",
     "payload_identical":cr==oo}
OUT.write_text(json.dumps(res,indent=1)+"\n")
print(json.dumps({kk:res[kk] for kk in ("type_id","status","relation")},indent=1))
print("client stride",c["stride"],"closure",c["closure_ok"],"server closure",s["closure_ok"])
