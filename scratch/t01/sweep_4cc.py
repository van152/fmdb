"""t01-a: sweep editor.exe for 4CC property-registration blocks.

Pure stdlib byte scan, no disassembler. Run:
  py -V:3.12 -I D:/tmp2b/fm24-db/scratch/t01/sweep_4cc.py
Writes: scratch/t01/t01a_editor_sweep.json (and prints a console digest).
"""
from __future__ import annotations

import hashlib
import json
import re
import struct
import sys
from collections import Counter
from pathlib import Path

EXE = Path(r"D:\tmp2b\fm24\input\editor.exe")
OUT_JSON = Path(r"D:\tmp2b\fm24-db\scratch\t01\t01a_editor_sweep.json")
MASTER = Path(r"D:\tmp2b\fm24-db\evidence\fm24\reports\editor_schema\master.json")

# ---- scan patterns: mov dword ptr <mem>, imm32 with ASCII-4CC imm ----
ALNUM = rb"[0-9A-Za-z]"
PAT_LIST = [
    ("c7_45_disp8", re.compile(rb"\xc7\x45." + ALNUM * 4)),            # c7 45 d8 imm32
    ("c7_44_24_disp8", re.compile(rb"\xc7\x44\x24." + ALNUM * 4)),     # c7 44 24 d8 imm32
    ("c7_85_disp32", re.compile(rb"\xc7\x85.{4}" + ALNUM * 4)),        # c7 85 d32 imm32
    ("c7_84_24_disp32", re.compile(rb"\xc7\x84\x24.{4}" + ALNUM * 4)), # bonus variant
]
# imm32 starts at match.end() - 4 in every pattern above.

CLUSTER_GAP = 4096          # hits closer than this join one cluster (commander spec)
DENSE_GAP = 0x100           # within a cluster: gap <= this => same registration run
MIN_HITS_CLUSTER = 3        # keep clusters with >= 3 4CC hits
KNOWN_HELPERS = (0x83ABF0, 0x83CAF0)  # from commander anchor (file offsets)


def pe_sections(data: bytes):
    e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
    coff = e_lfanew + 4
    _machine, nsec, _ts, _sym, _nsym, opt_size = struct.unpack_from("<HHIIIH", data, coff)
    opt = coff + 20
    magic = struct.unpack_from("<H", data, opt)[0]
    img_base = struct.unpack_from("<Q" if magic == 0x20B else "<I", data, opt + 24)[0]
    secs = []
    st = opt + opt_size
    for i in range(nsec):
        off = st + i * 40
        vsize, vaddr, rsize, rptr = struct.unpack_from("<IIII", data, off + 8)
        secs.append((vaddr, vsize, rptr, rsize))
    return img_base, secs


def make_off2va(img_base: int, secs):
    def off2va(off: int):
        for vaddr, vsize, rptr, rsize in secs:
            if rptr <= off < rptr + rsize:
                return img_base + vaddr + (off - rptr)
        return None
    return off2va


def scan_hits(data: bytes):
    hits = []
    pat_counts = {}
    for name, pat in PAT_LIST:
        n = 0
        for m in pat.finditer(data):
            off = m.start()
            imm = m.end() - 4
            cc = data[imm:imm + 4][::-1].decode("ascii", errors="replace")
            hits.append((off, name, cc))
            n += 1
        pat_counts[name] = n
    hits.sort(key=lambda h: h[0])
    return hits, pat_counts


def hit_len(pattern: str) -> int:
    # total instruction length: opcode+modrm(+sib+disp) + 4-byte imm32
    return {"c7_45_disp8": 7, "c7_44_24_disp8": 8,
            "c7_85_disp32": 10, "c7_84_24_disp32": 11}[pattern]


def block_confirm(data: bytes, off: int, pattern: str) -> int:
    """If bytes after the imm look like the anchor block, return call-target
    file offset of the first plausible e8 within the window, else -1."""
    imm_end = off + hit_len(pattern)
    win = data[imm_end:imm_end + 0x30]
    if b"\x48\x8d" not in win[:0x10] and b"\x48\x89" not in win[:0x10]:
        return -1  # no mov/lea continuation -> data-ish
    for k in range(len(win) - 4):
        if win[k] == 0xE8:
            rel = struct.unpack_from("<i", win, k + 1)[0]
            tgt = imm_end + k + 5 + rel
            if 0 <= tgt < len(data):
                return tgt
    return -1


def cluster_call_targets(data: bytes, lo: int, hi: int, off2va):
    """Decode every e8 in range; keep targets that recur >= 3 times and map
    into the image (mid-instruction e8 garbage almost never recurs/maps)."""
    counter = Counter()
    for i in range(lo, hi - 4):
        if data[i] == 0xE8:
            rel = struct.unpack_from("<i", data, i + 1)[0]
            tgt = i + 5 + rel
            if 0 <= tgt < len(data) and off2va(tgt) is not None:
                counter[tgt] += 1
    return [(tgt, n) for tgt, n in counter.most_common(8) if n >= 3]


def load_entities():
    d = json.loads(MASTER.read_text(encoding="utf-8"))
    ents = {}
    for name, rec in d["entity_summary"].items():
        ents[name] = set(rec["codes"])
    return ents


def match_entities(cc_set: set, ents: dict):
    scored = []
    for name, codes in ents.items():
        inter = cc_set & codes
        if not inter:
            continue
        cont = len(inter) / len(cc_set)                # how much of cluster is entity
        cov = len(inter) / len(codes)                  # how much of entity is in cluster
        jac = len(inter) / len(cc_set | codes)
        scored.append((name, round(cont, 4), round(cov, 4), round(jac, 4)))
    scored.sort(key=lambda t: (-t[1], -t[3], -t[2]))
    return scored[:3]


def confidence_of(scored) -> str:
    best = scored[0][1] if scored else 0.0
    second = scored[1][1] if len(scored) > 1 else 0.0
    if best >= 0.6 and second < 0.6:
        return "high"      # single entity explains >=60% of cluster 4CCs
    if best >= 0.6:
        return "medium"    # >=60% but ambiguous across entities
    if best >= 0.3:
        return "medium"
    return "low"


def hexc(c: Counter) -> dict:
    return {hex(k): v for k, v in sorted(c.items())}


def main() -> int:
    data = EXE.read_bytes()
    n_bytes = len(data)
    sha_first1k = hashlib.sha256(data[:1024]).hexdigest()
    img_base, secs = pe_sections(data)
    off2va = make_off2va(img_base, secs)

    print(f"scanning {n_bytes:,} bytes ...", flush=True)
    hits, pat_counts = scan_hits(data)
    print(f"raw hits: {len(hits)}  by pattern: {pat_counts}", flush=True)

    ents = load_entities()

    # ---- cluster (commander spec: gap < 4096 joins) ----
    clusters = []
    cur = [hits[0]]
    for h in hits[1:]:
        if h[0] - cur[-1][0] < CLUSTER_GAP:
            cur.append(h)
        else:
            clusters.append(cur)
            cur = [h]
    clusters.append(cur)

    out_clusters = []
    for ci, group in enumerate(clusters):
        if len(group) < MIN_HITS_CLUSTER:
            continue
        lo = group[0][0]
        hi_ex = group[-1][0] + hit_len(group[-1][1])
        cc_list = [g[2] for g in group]
        cc_set = set(cc_list)
        strides = Counter(group[i + 1][0] - group[i][0] for i in range(len(group) - 1))

        # dense registration runs inside the cluster
        runs = []
        run = [group[0]]
        for h in group[1:]:
            if h[0] - run[-1][0] <= DENSE_GAP:
                run.append(h)
            else:
                if len(run) >= 3:
                    runs.append(run)
                run = [h]
        if len(run) >= 3:
            runs.append(run)

        dense_runs = []
        for run in runs:
            rlo = run[0][0]
            rhi = run[-1][0] + hit_len(run[-1][1])
            r_cc = [g[2] for g in run]
            r_set = set(r_cc)
            r_str = Counter(run[i + 1][0] - run[i][0] for i in range(len(run) - 1))
            r_targets = cluster_call_targets(data, rlo, rhi, off2va)
            r_scored = match_entities(r_set, ents)
            dense_runs.append({
                "start_off": hex(rlo), "end_off": hex(rhi),
                "start_va": hex(off2va(rlo)) if off2va(rlo) is not None else "unmapped",
                "end_va": hex(off2va(rhi)) if off2va(rhi) is not None else "unmapped",
                "n_hits": len(run), "cc_list": r_cc,
                "strides": hexc(r_str),
                "call_targets": [
                    {"target_off": hex(t), "target_va": hex(off2va(t)) if off2va(t) else None,
                     "count": n,
                     "known_helper": t in KNOWN_HELPERS}
                    for t, n in r_targets],
                "entity_top3": [{"entity": s[0], "containment": s[1],
                                 "entity_coverage": s[2], "jaccard": s[3]} for s in r_scored],
                "confidence": confidence_of(r_scored),
            })

        targets = cluster_call_targets(data, lo, hi_ex, off2va)
        scored = match_entities(cc_set, ents)
        out_clusters.append({
            "cluster_id": ci,
            "start_off": hex(lo), "end_off": hex(hi_ex),
            "start_va": hex(off2va(lo)) if off2va(lo) is not None else "unmapped",
            "end_va": hex(off2va(hi_ex)) if off2va(hi_ex) is not None else "unmapped",
            "n_hits": len(group), "n_unique_cc": len(cc_set),
            "cc_list": cc_list,
            "strides": hexc(strides),
            "call_targets": [
                {"target_off": hex(t), "target_va": hex(off2va(t)) if off2va(t) else None,
                 "count": n, "known_helper": t in KNOWN_HELPERS}
                for t, n in targets],
            "entity_top3": [{"entity": s[0], "containment": s[1],
                             "entity_coverage": s[2], "jaccard": s[3]} for s in scored],
            "confidence": confidence_of(scored),
            "dense_runs": dense_runs,
        })

    result = {
        "meta": {
            "exe": str(EXE).replace("\\", "/"),
            "exe_size": n_bytes,
            "sha256_first1k": sha_first1k,
            "image_base": hex(img_base),
            "scanned_bytes": n_bytes,
            "patterns": {
                "c7_45_disp8": "c7 45 <d8> <imm32>; 4CC = imm32 bytes reversed",
                "c7_44_24_disp8": "c7 44 24 <d8> <imm32>",
                "c7_85_disp32": "c7 85 <d32> <imm32>",
                "c7_84_24_disp32": "c7 84 24 <d32> <imm32> (bonus variant)",
            },
            "raw_hit_counts": pat_counts,
            "cluster_gap": CLUSTER_GAP,
            "dense_gap": DENSE_GAP,
            "min_hits_cluster": MIN_HITS_CLUSTER,
            "va_rule": "VA = image_base + vaddr + (fileoff - rptr); inside .rdata VA = fileoff + 0xA00",
            "confidence_rule": ("high = exactly one entity explains >=60% of cluster 4CCs "
                                "(containment>=0.6, runner-up <0.6); medium = >=0.3 or ambiguous; low otherwise"),
            "entity_source": str(MASTER).replace("\\", "/"),
            "known_helpers_off": [hex(h) for h in KNOWN_HELPERS],
        },
        "clusters": out_clusters,
    }
    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {OUT_JSON}  clusters={len(out_clusters)}", flush=True)

    # console digest
    for c in out_clusters:
        t3 = c["entity_top3"]
        t3s = "; ".join(f"{t['entity']} cont={t['containment']} cov={t['entity_coverage']} j={t['jaccard']}" for t in t3) or "-"
        print(f"[{c['confidence']:6}] {c['start_off']}..{c['end_off']} hits={c['n_hits']} uniq={c['n_unique_cc']} "
              f"runs={len(c['dense_runs'])} :: {t3s}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
