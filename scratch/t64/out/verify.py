#!/usr/bin/env python3
"""Independent t64 verifier: frozen ledger checks plus a fresh table_25 replay."""
from __future__ import annotations
import argparse
from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path
import runpy
import struct as S
import sys

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "scratch" / "t64" / "out"
EXE = ROOT.parent / "fm24" / "input" / "editor.exe"
EXEH = "b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4"
HEAD = bytes.fromhex("03017461642ef10d")
FOOT = bytes.fromhex("00000000014ec43a77")
SIDES = ("client", "server")
N = 7047

class Check(Exception): pass

def ck(ok, detail):
    if not ok: raise Check(detail)

def H(b): return sha256(b).hexdigest()
def verify_instruction(record, binary):
    off=record["file_offset"]; raw=bytes.fromhex(record["bytes"])
    ck(bool(raw) and binary[off:off+len(raw)] == raw, ("instruction bytes", hex(off)))
def U(b, at=0): return S.unpack_from("<I", b, at)[0]

def load_table25():
    depot = Path(os.environ.get("FM24_DB_DIR", str(ROOT / "scratch" / "data")))
    ck(depot.drive.upper() != "Z:", "Z: access is forbidden")
    old = ROOT.parent / "fm24"
    sys.path.append(str(old / "tools" / "python"))
    import zstandard as zstd
    entries = runpy.run_path(str(old / "scripts" / "modding_read_dbdat.py"))["_entries"]
    raw = {}
    for side in SIDES:
        _, blob, directory = entries(depot / f"{side}_db.dat")
        base = directory["data_base"]
        index = {x["path"]: x for x in directory["entries"]}
        entry = index[f"{side}_db/table_25.dat"]
        start = base + entry["offset"]
        finish = start + entry["packed_size"]
        bound = min((base + x["offset"] for x in index.values() if x["offset"] > entry["offset"]), default=directory["toc_offset"])
        candidates = []
        p = start
        while p < finish:
            ck(blob[p:p+4] == b"\x28\xb5\x2f\xfd", (side, "zstd magic", p))
            dec = zstd.ZstdDecompressor().decompressobj()
            payload = dec.decompress(blob[p:finish])
            q = finish - len(dec.unused_data)
            ck(dec.eof and q > p and q <= bound, (side, "zstd frame", p))
            if len(payload) == entry["size"]: candidates.append(payload)
            p = q
        ck(len(candidates) == 1, (side, "declared-size selector"))
        raw[side] = candidates[0]
        ck(raw[side][:8] == HEAD and U(raw[side], 8) == N, (side, "header"))
    return raw

class Cursor:
    def __init__(self, b, side): self.b=b; self.side=side; self.p=13; self.end=len(b)-9; self.row=-1
    def take(self, n, label):
        ck(n >= 0 and self.p+n <= self.end, (self.side,self.row,label,self.p,n))
        x=self.b[self.p:self.p+n]; self.p += n; return x
    def u(self,n,label): return int.from_bytes(self.take(n,label),"little")
    def s(self,n,label): return int.from_bytes(self.take(n,label),"little",signed=True)
    def count(self,n,unit,label,signed=False):
        x=self.s(n,label) if signed else self.u(n,label)
        ck(0 <= x <= (self.end-self.p)//unit, (self.side,self.row,label,x)); return x

def replay(b, side):
    c=Cursor(b,side); events={}; values={}; rows=[]
    def rec(k,a,z,v=None):
        events.setdefault(k,[]).append((c.row,a,z-a))
        if v is not None: values.setdefault(k,[]).append((c.row,v))
    def take(k,n):
        a=c.p; v=c.u(n,k); rec(k,a,c.p,v); return v
    def raw(k,n):
        a=c.p; c.take(n,k); rec(k,a,c.p)
    for i in range(N):
        c.row=i; start=c.p
        vals=[take("selector",1),take("m15c",1),take("m15d",1),take("colour_tag",1)]
        for k in ("m120","m124","m128","m12c","m130"): take(k,2)
        take("m134",1); tag=take("m1a0",1)
        for k in ("m1a2","m1a3","m1a4","m1a5"): take(k,1)
        vals += [take("stat_a_tag",1)]
        for k in ("m198","m199","m19a","m19b","m19c","m19d","m19e"): take(k,1)
        vals += [take("stat_b_tag",1)]
        raw("m189_197",15); take("mf6",1)
        for k in ("m138","m13c","m58","m60","m70","m68"): take(k,4)
        take("m150",2)
        ck(tuple(vals) == (0,0,0,1,2,3), (side,i,"fixed tags")); ck(tag != 4, (side,i,"tag4"))
        if side == "server":
            for k,n in (("m180",2),("mb8",4),("m188",1),("m184",2),("m186",2),("m182",2),("m160",8),("m168",8),("m170",8),("m178",8)): take(k,n)
            a=c.p; n=c.count(4,2,"vec30-count"); c.take(2*n,"vec30-body"); rec("vec30",a,c.p)
            p=take("a8_present",1)
            if p:
                a=c.p; v=c.u(1,"a8-version"); c.take(32+4*(v>=2)+9+(2 if v>=3 else 1)+8,"obj_a8-body"); rec("obj_a8",a,c.p)
            for k,n in (("mf0",4),("m1a1",1),("m1a8",1),("mf4",1),("mf5",1)): take(k,n)
            p=take("e0_present",1); ck(p == 0, (side,i,"nonzero e0 outside verifier scope"))
            a=c.p; n=c.count(4,8,"vec18-count",True)
            for j in range(n):
                v=c.s(1,"vec18-version"); c.take(7+(v>=2),"vec18-body")
            rec("vec18",a,c.p)
            p=take("e8_present",1)
            if p:
                a=c.p; c.take(4,"e8-header"); n=c.count(4,8,"e8-count")
                for j in range(n):
                    v=c.s(2,"e8-version"); c.take(6+(2 if v>=2 else 1)+1+(v>=3),"e8-body")
                rec("obj_e8",a,c.p)
            p=take("c0_present",1)
            if p:
                a=c.p; c.take(1,"c0-header"); n=c.count(4,6,"c0-count")
                for j in range(n): c.take(2,"c0-item"); c.take(12*c.count(4,12,"c0-subcount"),"c0-body")
                rec("obj_c0",a,c.p)
            p=take("c8_present",1)
            if p: raw("obj_c8",25)
            take("m1a7",1); p=take("d0_present",1)
            if p: raw("obj_d0",15)
            p=take("d8_present",1)
            if p: raw("obj_d8",15)
            a=c.p; n=c.s(2,"vec100-count"); ck(n >= 0 and n <= (c.end-c.p)//5,(side,i,"vec100")); c.take(5*n,"vec100-body"); rec("vec100",a,c.p)
        for k,n in (("m148",4),("m152",2),("m154",2),("m156",2),("m158",2),("m15a",2),("m80",4),("m88",4),("m90",4),("m98",4)): take(k,n)
        p=take("wbcl_present",1)
        if p: raw("m14c",2)
        for k,n in (("m140",4),("m144",4),("mf7",1),("mf8",1),("mf9",1)): take(k,n)
        a=c.p; row,uid,repeat=S.unpack_from("<III",b,a); c.take(12,"identity"); rec("identity",a,c.p)
        ck((row,uid,repeat)==(i,uid,uid) and uid > (rows[-1][2] if rows else 0),(side,i,"identity")); rows.append((start,c.p,uid))
    ck(b[c.p:] == FOOT,(side,"footer")); return rows,events,values

def check_static():
    helpers=json.loads((OUT/"helpers.json").read_text())
    binary=EXE.read_bytes()
    ck(H(binary) == EXEH == helpers["provenance"]["editor_sha256"], "editor.exe sha256")
    main=helpers["main_reader"]["direct_stream_call_accounting"]
    ck(main["direct_call_count"] == 55 and main["outer_observed_call_count"] == 52 and main["alternate_call_count"] == 3, "stream call accounting")
    ck(len(main["calls"]) == 55, "stream call ledger completeness")
    sites={x["site"] for x in main["calls"]}
    ck({0xEB7218,0xEB72F8,0xEB7332,0xEB7C8F} <= sites, "alternate and extra marker sites")
    wbcl=next(x for x in main["calls"] if x["site"] == 0xEB7C8F)
    ck(wbcl["slot"] == "wbcl_present", "additional marker reconciliation")
    for item in main["calls"]:
        verify_instruction(item["call_instruction"], binary)
    helper_calls=helpers["main_reader"]["direct_helper_call_accounting"]
    ck(len(helper_calls["calls"]) == helper_calls["direct_non_stream_call_count"] == 43, "helper call ledger completeness")
    ck(all(isinstance(item.get("field_mapping_status"), str) and item["field_mapping_status"] for item in helper_calls["calls"]), "helper mapping-status completeness")
    for item in helper_calls["calls"]:
        verify_instruction(item["call_instruction"], binary)
        ck(item["call_instruction"].get("direct_target_file_offset") == item["target_file_offset"], ("helper target", hex(item["site"])))
    payloads=helpers["main_reader"]["payload_entry_conditions"]
    ck(payloads["a8"]["member_offset"] == 0xA8 and payloads["e0"]["member_offset"] == 0xE0, "payload offsets")
    ck(payloads["a8"]["presence_test"]["file_offset"] == 0xEB753F and payloads["e0"]["presence_test"]["file_offset"] == 0xEB76CD, "payload tests")
    for payload in payloads.values():
        for key in ("presence_read","presence_test","skip_target","allocator","reader"):
            verify_instruction(payload[key], binary)
        for key in ("member_store","constructor"):
            if key in payload: verify_instruction(payload[key], binary)
    routes=helpers["bounded_getter_routes"]
    for code, member in (("cnam",0x40),("csnm",0x48),("c3ln",0x50)):
        item=routes["string_getter_paths"][code]
        ck(item["member_offset"] == member, (code,"member offset"))
        verify_instruction(item["compare"], binary)
        verify_instruction(item["member_add"], binary)
    chain=routes["rules_context_chain"]
    for code in ("VARt","HKEt"):
        item=chain[code]
        ck(item["same_comp_scalar_wire_binding_proved"] is False, (code,"wire closure"))
        for key in ("row_object_load","field_code_compare","code_mismatch_branch","object_null_test","object_nonnull_branch"):
            verify_instruction(item[key], binary)
        for record in item["context_dispatch_sequence"]:
            verify_instruction(record, binary)
    separate=chain["separate_nested_rules_dispatch"]
    for record in separate["shared_entry"]:
        verify_instruction(record, binary)
    verify_instruction(separate["nested_helper_entry"], binary)
    for family in separate["jump_table_families"].values():
        base_va=None
        for case in family["cases"]:
            entry=case["entry_file_offset"]
            ck(entry == family["table_file_offset"] + 4*case["index"], "rules table entry offset")
            rel=S.unpack_from("<i", binary, entry)[0]
            ck(rel == case["relative_value"], "rules table relative value")
            target_va=int(case["handler"]["va"],16)
            this_base=target_va-rel
            if base_va is None: base_va=this_base
            ck(this_base == base_va, "rules table target base")
            verify_instruction(case["handler"], binary)

def check():
    base_path=ROOT/"scratch"/"t59"/"out"/"field_map.json"
    base_bytes=base_path.read_bytes()
    base=json.loads(base_bytes)
    r2=json.loads((OUT/"field_map_r2.json").read_text())
    ex=json.loads((OUT/"exclusions.json").read_text())
    helpers=json.loads((OUT/"helpers.json").read_text())
    base_sha=H(base_bytes)
    ck(base["summary"] == {"L3":49,"held":10,"unmapped":196}, "t59 baseline summary")
    ck(base_sha == r2["baseline"]["sha256"] == ex["baseline_field_map_sha256"] == helpers["provenance"]["baseline_field_map_sha256"], "t59 baseline hash")
    ck(r2["summary"]["reviewed_unmapped_occurrences"] == 196 and r2["summary"]["new_L3"] == 0, "r2 summary")
    ck(len(r2["fields"]) == len(ex["fields"]) == 196, "field ledger count")
    expected=[(x["xml_index"],x["code"]) for x in base["fields"] if x["status"] == "unmapped"]
    observed=[(x["xml_index"],x["code"]) for x in r2["fields"]]
    ck(observed == expected, "unmapped occurrence identity/order")
    ck(all(x["baseline_status"] == "unmapped" and x["wire_binding"] is None for x in r2["fields"]), "baseline or wire mutation")
    ck(r2["baseline"]["inversion_count"] == len(base["inversions"]) == 818, "inversion freeze")
    ck(r2["summary"]["baseline_L3_unchanged"] and r2["summary"]["baseline_held_unchanged"] and r2["summary"]["baseline_inversions_unchanged"], "frozen t59 closure")
    check_static()
    raw=load_table25()
    runs={side:replay(raw[side],side) for side in SIDES}
    for side in SIDES:
        rows,events,values=runs[side]
        ck(len(rows) == N, (side,"row count"))
        for key in ("a8_present","e0_present","d0_present","d8_present"):
            if side == "client": ck(not events.get(key), (side,key,"unexpected client event"))
            else: ck(len(events.get(key,[])) == N, (side,key,"event count"))
        if side == "server":
            ck(sum(v != 0 for _,v in values["a8_present"]) == 0 and sum(v != 0 for _,v in values["e0_present"]) == 0, (side,"zero payload presence"))
            ck(len(events.get("obj_a8",[])) == len(events.get("obj_e0",[])) == 0, (side,"payload objects"))
            ck(sum(v != 0 for _,v in values["d0_present"]) == 121 and sum(v != 0 for _,v in values["d8_present"]) == 51, (side,"rules presence"))
    print("t64 verify: PASS; 196 unmapped occurrences reviewed, t59 baseline frozen, a8/e0 presence zero")

def main(argv=None):
    ap=argparse.ArgumentParser(description="independently verify t64 outputs")
    ap.add_argument("--selftest",action="store_true",help="run the verifier")
    ap.parse_args(argv)
    try: check()
    except (Check, OSError, ValueError, ImportError) as exc:
        print(f"t64 verify: FAIL: {exc}", file=sys.stderr); return 1
    return 0

if __name__ == "__main__": raise SystemExit(main())
