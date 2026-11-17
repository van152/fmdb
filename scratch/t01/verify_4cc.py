"""t01-a verification: re-check every recorded hit/cluster/switch claim against raw exe bytes.

Run: py -V:3.12 -I D:/tmp2b/fm24-db/scratch/t01/verify_4cc.py
"""
from __future__ import annotations

import json
import re
import struct
import sys
from pathlib import Path

sys.path.insert(0, r"D:\tmp2b\fm24-db\scratch\t01")
import sweep_4cc as sw

ALNUM = re.compile(rb"[0-9A-Za-z]{4}")
CMP_RE = re.compile(rb"\x81[\xf8-\xff]")

SHAPE_PREFIX = {  # shape -> (opcode bytes at instruction start, len from op start to imm)
    "c7_45_disp8": (b"\xc7\x45", 3),
    "c7_44_24_disp8": (b"\xc7\x44\x24", 4),
    "c7_85_disp32": (b"\xc7\x85", 6),
    "c7_84_24_disp32": (b"\xc7\x84\x24", 7),
}


def main() -> int:
    data = sw.EXE.read_bytes()
    j = json.loads(Path(r"D:\tmp2b\fm24-db\scratch\t01\t01a_editor_sweep.json").read_text(encoding="utf-8"))
    errs = []

    # 1. every primary hit: opcode prefix + imm bytes reversed == cc
    n_ok = 0
    for h in j["hits"]:
        off = int(h["off"], 16)
        io = int(h["imm_off"], 16)
        if h["shape"] not in SHAPE_PREFIX:
            errs.append(f"hit {h['off']} unknown shape {h['shape']}")
            continue
        op, d = SHAPE_PREFIX[h["shape"]]
        if data[off:off + len(op)] != op or off + d != io:
            errs.append(f"hit {h['off']} prefix mismatch shape={h['shape']}")
            continue
        got = data[io:io + 4][::-1].decode("ascii", "replace")
        if got != h["cc"] or not ALNUM.fullmatch(data[io:io + 4]):
            errs.append(f"hit {h['off']} cc mismatch json={h['cc']} bytes={got}")
            continue
        n_ok += 1
    print(f"primary hits verified: {n_ok}/{len(j['hits'])}")

    # 2. every cluster: cc_list equals hits inside [start,end); counts consistent
    for c in j["clusters"]:
        lo, hi = int(c["start_off"], 16), int(c["end_off"], 16)
        cc_in = [h["cc"] for h in j["hits"] if lo <= int(h["off"], 16) < hi]
        if cc_in != c["cc_list"]:
            errs.append(f"cluster {c['start_off']} cc_list mismatch ({len(cc_in)} vs {c['n_hits']})")
        if len(cc_in) != c["n_hits"] or len(set(cc_in)) != c["n_unique_cc"]:
            errs.append(f"cluster {c['start_off']} counts mismatch")
    print(f"clusters checked: {len(j['clusters'])}")

    # 3. dense runs: n_hits + call targets decodable from inside run range
    t_ok = t_all = 0
    for c in j["clusters"]:
        for r in c["dense_runs"]:
            rlo, rhi = int(r["start_off"], 16), int(r["end_off"], 16)
            offs = sorted(int(h["off"], 16) for h in j["hits"] if rlo <= int(h["off"], 16) < rhi)
            if len(offs) != r["n_hits"]:
                errs.append(f"run {r['start_off']} n_hits mismatch")
            for t in r["call_targets"]:
                toff = int(t["target_off"], 16)
                found = any(
                    data[i] == 0xE8 and i + 5 + struct.unpack_from("<i", data, i + 1)[0] == toff
                    for i in range(rlo, rhi - 4))
                t_all += 1
                if found:
                    t_ok += 1
                else:
                    errs.append(f"run {r['start_off']} target {t['target_off']} not decodable in range")
    print(f"run call targets decodable: {t_ok}/{t_all}")

    # 4. dispatch switches: sample_cc byte-verified as cmp-imm inside span
    s_ok = 0
    for s in j["dispatch_switches"]:
        lo, hi = int(s["start_off"], 16), int(s["end_off"], 16)
        checked = 0
        i = lo
        while i < hi - 8 and checked < 4:
            m = CMP_RE.match(data, i)
            if m:
                imm = m.end()
                if ALNUM.fullmatch(data[imm:imm + 4]):
                    if data[imm:imm + 4][::-1].decode("ascii", "replace") in s["sample_cc"]:
                        s_ok += 1
                    checked += 1
                    i = imm + 4
                    continue
            i += 1
    print(f"switch sample 4CCs byte-verified: {s_ok}")

    # 5. anchor cluster deep-check
    c = next(x for x in j["clusters"] if x["start_off"] == "0xebf060")
    print("anchor cluster:", c["start_off"], c["end_off"], "n_hits", c["n_hits"],
          "top:", c["entity_top3"][0])
    blk = data[0xebf060:0xebf090]
    sig15 = b"\x48\x89\x45\xe8\x48\x8d\x7d\xe8\x48\x89\xf1\x48\x89\xfa\xe8"
    sig = blk[:7] == b"\xc7\x45\xf0\x6e\x67\x4c\x50" and blk[7:7 + len(sig15)] == sig15
    rel = struct.unpack_from("<i", blk, 0x16)[0]
    tgt = 0xebf075 + 5 + rel
    print(f"anchor block signature ok={sig} helperA target off={hex(tgt)} (expect 0x83abf0)")
    if c["cc_list"][:3] != ["PLgn", "cnam", "csnm"]:
        errs.append(f"anchor cc_list head unexpected: {c['cc_list'][:3]}")

    if errs:
        print(f"\nERRORS ({len(errs)}):")
        for e in errs[:20]:
            print(" ", e)
        return 1
    print("\nALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
