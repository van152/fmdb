"""t01-a analysis pass: unify hits, per-entity code->offset index, residual raw search.

Reuses scanners from sweep_4cc.py. Run:
  py -V:3.12 -I D:/tmp2b/fm24-db/scratch/t01/analyze_4cc.py
Rewrites scratch/t01/t01a_editor_sweep.json (final artifact) with:
  meta / clusters (per commander spec + dense_runs) / hits / entity_index.
"""
from __future__ import annotations

import hashlib
import json
import re
import struct
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, r"D:\tmp2b\fm24-db\scratch\t01")
import sweep_4cc as sw

ALNUM = rb"[0-9A-Za-z]"
AUX_PATTERNS = [  # auxiliary imm32 idioms beyond the commander's c7 mov-imm forms
    ("push_imm32", re.compile(rb"\x68" + ALNUM * 4), 1),          # 68 <imm32>
    ("mov_r32_imm32", re.compile(rb"[\xb8-\xbf]" + ALNUM * 4), 1),  # b8..bf <imm32>
    ("mov_r32_imm32_rex", re.compile(rb"\x41[\xb8-\xbf]" + ALNUM * 4), 2),
    ("cmp_r32_imm32", re.compile(rb"\x81[\xf8-\xff]" + ALNUM * 4), 2),   # 81 f8..ff <imm32> (per-field switch)
    ("cmp_eax_imm32", re.compile(rb"\x3d" + ALNUM * 4), 1),              # 3d <imm32>
]
SWITCH_GAP = 0x800      # cmp-4CC hits closer than this join one dispatch-switch cluster
MIN_HITS_SWITCH = 5
CLUSTER_GAP = sw.CLUSTER_GAP
DENSE_GAP = sw.DENSE_GAP


def pe_sections_named(data: bytes):
    e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
    coff = e_lfanew + 4
    _m, nsec, _ts, _sym, _nsym, opt_size = struct.unpack_from("<HHIIIH", data, coff)
    opt = coff + 20
    magic = struct.unpack_from("<H", data, opt)[0]
    img_base = struct.unpack_from("<Q" if magic == 0x20B else "<I", data, opt + 24)[0]
    secs = []
    st = opt + opt_size
    for i in range(nsec):
        off = st + i * 40
        name = data[off:off + 8].rstrip(b"\0").decode(errors="replace") or f"sec{i}"
        vsize, vaddr, rsize, rptr = struct.unpack_from("<IIII", data, off + 8)
        secs.append({"name": name, "vaddr": vaddr, "vsize": vsize, "rptr": rptr, "rsize": rsize})
    return img_base, secs


def region_of(secs, off: int) -> str:
    for s in secs:
        if s["rptr"] <= off < s["rptr"] + s["rsize"]:
            return s["name"]
    return "unmapped"


def shape_of(data: bytes, imm_off: int) -> str:
    """Classify the instruction shape carrying the imm32 at imm_off."""
    p1 = data[imm_off - 1]
    p2 = data[imm_off - 2:imm_off]
    p3 = data[imm_off - 3:imm_off]
    p4 = data[imm_off - 4:imm_off]
    if p2 == b"\xc7\x45":
        return "c7_45_disp8"
    if p2 == b"\xc7\x85":
        return "c7_85_disp32"
    if p3 == b"\xc7\x44\x24":
        return "c7_44_24_disp8"
    if p4 == b"\xc7\x84\x24":
        return "c7_84_24_disp32"
    if p2 == b"\x41" and 0xB8 <= p1 <= 0xBF:
        return "mov_r32_imm32_rex"
    if 0xB8 <= p1 <= 0xBF:
        return "mov_r32_imm32"
    if p1 == 0x68:
        return "push_imm32"
    if p1 == 0xC7:
        return "c7_other_modrm"
    return f"other({data[imm_off-4:imm_off].hex(' ')})"


def collect_hits(data: bytes):
    """Primary c7 patterns for clustering; aux idioms recorded separately.
    Primary hits: (pat_start, imm_off, pattern, cc). Aux hits: (imm_off, pattern, cc)."""
    prim, pat_counts = sw.scan_hits(data)
    hits = []
    for off, pat, cc in prim:
        imm_off = off + sw.hit_len(pat) - 4
        hits.append((off, imm_off, pat, cc))
    aux = []
    for name, pat, delta in AUX_PATTERNS:
        n = 0
        for m in pat.finditer(data):
            imm_off = m.start() + delta
            cc = data[imm_off:imm_off + 4][::-1].decode("ascii", errors="replace")
            aux.append((imm_off, name, cc))
            n += 1
        pat_counts[name] = n
    return hits, aux, pat_counts


def dense_runs_of(group):
    runs, run = [], [group[0]]
    for h in group[1:]:
        if h[0] - run[-1][0] <= DENSE_GAP:
            run.append(h)
        else:
            if len(run) >= 3:
                runs.append(run)
            run = [h]
    if len(run) >= 3:
        runs.append(run)
    return runs


def main() -> int:
    t0 = time.time()
    data = sw.EXE.read_bytes()
    img_base, secs_tuple = sw.pe_sections(data)
    _, secs = pe_sections_named(data)
    off2va = sw.make_off2va(img_base, secs_tuple)
    ents = sw.load_entities()
    ent_codes = {c for codes in ents.values() for c in codes}
    print(f"loaded {len(data):,} bytes, {len(ents)} entities  t={time.time()-t0:.1f}s", flush=True)

    hits, aux, pat_counts = collect_hits(data)
    aux_entity = [a for a in aux if a[2] in ent_codes]
    print(f"primary hits: {len(hits)}  aux: {len(aux)} (entity-code matches: {len(aux_entity)})"
          f"  {pat_counts}  t={time.time()-t0:.1f}s", flush=True)

    # ---- clusters (spans in instruction-start space = pat_start) ----
    clusters = []
    cur = [hits[0]]
    for h in hits[1:]:
        if h[0] - cur[-1][0] < CLUSTER_GAP:
            cur.append(h)
        else:
            clusters.append(cur)
            cur = [h]
    clusters.append(cur)
    clusters = [g for g in clusters if len(g) >= sw.MIN_HITS_CLUSTER]

    cc_index = defaultdict(list)   # cc -> [(imm_off, shape)]
    for _ps, imm_off, pat, cc in hits:
        cc_index[cc].append((imm_off, pat))
    for imm_off, pat, cc in aux_entity:
        cc_index[cc].append((imm_off, pat))
    for v in cc_index.values():
        v.sort(key=lambda t: t[0])

    out_clusters = []
    run_registry = []  # (cluster_id, run_idx, lo, hi, [(cc, off)])
    for ci, group in enumerate(clusters):
        lo = group[0][0]
        hi_ex = group[-1][1] + 4  # end of last imm32
        cc_list = [g[3] for g in group]
        cc_set = set(cc_list)
        strides = Counter(group[i + 1][0] - group[i][0] for i in range(len(group) - 1))
        pats = Counter(g[2] for g in group)

        runs = dense_runs_of(group)
        dense_runs = []
        for ri, run in enumerate(runs):
            rlo = run[0][0]
            rhi = run[-1][1] + 4
            r_cc = [g[3] for g in run]
            r_set = set(r_cc)
            r_str = Counter(run[i + 1][0] - run[i][0] for i in range(len(run) - 1))
            r_tgts = sw.cluster_call_targets(data, rlo, rhi, off2va)
            r_scored = sw.match_entities(r_set, ents)
            helpers = [t for t, n in r_tgts if n >= max(2, len(run) // 2)]
            run_registry.append((ci, ri, rlo, rhi, [(g[3], g[1]) for g in run], helpers))
            dense_runs.append({
                "start_off": hex(rlo), "end_off": hex(rhi),
                "start_va": hex(v) if (v := off2va(rlo)) else "unmapped",
                "end_va": hex(v) if (v := off2va(rhi)) else "unmapped",
                "region": region_of(secs, rlo),
                "n_hits": len(run),
                "cc_list": r_cc,
                "strides": {hex(k): v for k, v in sorted(r_str.items())},
                "call_targets": [
                    {"target_off": hex(t),
                     "target_va": hex(v) if (v := off2va(t)) else None,
                     "count": n, "known_helper": t in sw.KNOWN_HELPERS}
                    for t, n in r_tgts],
                "helper_targets_off": [hex(t) for t in helpers],
                "entity_top3": [{"entity": s[0], "containment": s[1],
                                 "entity_coverage": s[2], "jaccard": s[3]} for s in r_scored],
                "confidence": sw.confidence_of(r_scored),
            })

        tgts = sw.cluster_call_targets(data, lo, hi_ex, off2va)
        scored = sw.match_entities(cc_set, ents)
        out_clusters.append({
            "cluster_id": ci,
            "start_off": hex(lo), "end_off": hex(hi_ex),
            "start_va": hex(v) if (v := off2va(lo)) else "unmapped",
            "end_va": hex(v) if (v := off2va(hi_ex)) else "unmapped",
            "region": region_of(secs, lo),
            "n_hits": len(group), "n_unique_cc": len(cc_set),
            "patterns_seen": {k: v for k, v in sorted(pats.items())},
            "cc_list": cc_list,
            "strides": {hex(k): v for k, v in sorted(strides.items())},
            "call_targets": [
                {"target_off": hex(t), "target_va": hex(v) if (v := off2va(t)) else None,
                 "count": n, "known_helper": t in sw.KNOWN_HELPERS}
                for t, n in tgts],
            "entity_top3": [{"entity": s[0], "containment": s[1],
                             "entity_coverage": s[2], "jaccard": s[3]} for s in scored],
            "confidence": sw.confidence_of(scored),
            "dense_runs": dense_runs,
        })

    # ---- dispatch-switch clusters from cmp-imm32 hits (entity-code 4CCs) ----
    # span space: opcode start (imm-2 for 81 xx /r, imm-1 for 3d)
    cmp_hits = sorted(((o - (2 if p == "cmp_r32_imm32" else 1), o, c)
                       for o, p, c in aux_entity if p.startswith("cmp_")))
    switch_clusters = []
    if cmp_hits:
        cur = [cmp_hits[0]]
        for h in cmp_hits[1:]:
            if h[0] - cur[-1][0] < SWITCH_GAP:
                cur.append(h)
            else:
                if len(cur) >= MIN_HITS_SWITCH:
                    switch_clusters.append(cur)
                cur = [h]
        if len(cur) >= MIN_HITS_SWITCH:
            switch_clusters.append(cur)
    out_switches = []
    for g in switch_clusters:
        lo, hi_ex = g[0][0], g[-1][1] + 4
        ccs = [c for _, _, c in g]
        ent_counts = Counter()
        for c in ccs:
            for name, codes in ents.items():
                if c in codes:
                    ent_counts[name] += 1
                    break
        strides = Counter(g[i + 1][0] - g[i][0] for i in range(len(g) - 1))  # opcode-start deltas
        out_switches.append({
            "start_off": hex(lo), "end_off": hex(hi_ex),
            "start_va": hex(v) if (v := off2va(lo)) else "unmapped",
            "end_va": hex(v) if (v := off2va(hi_ex)) else "unmapped",
            "region": region_of(secs, lo),
            "n_cmp_hits": len(g), "n_unique_cc": len(set(ccs)),
            "strides": {hex(k): v for k, v in sorted(strides.items())},
            "entity_hits": dict(ent_counts.most_common(6)),
            "sample_cc": ccs[:12],
        })
    print(f"dispatch-switch clusters: {len(out_switches)}  t={time.time()-t0:.1f}s", flush=True)

    # ---- per-entity index: code -> offsets(shapes) mapped to function sites ----
    residual = {}  # entity -> codes not present in any unified hit
    entity_index = {}
    for name, codes in ents.items():
        found, miss = {}, []
        for code in dict.fromkeys(codes):  # unique, keep order
            offs = cc_index.get(code, [])
            if offs:
                found[code] = offs
            else:
                miss.append(code)
        residual[name] = miss
        # map found codes to sites (dense runs)
        sites = defaultdict(list)
        for code, offs in found.items():
            for imm_off, pat in offs:
                for ci, ri, rlo, rhi, _, _h in run_registry:
                    if rlo <= imm_off < rhi:
                        sites[(ci, ri)].append((code, imm_off, pat))
                        break
        site_list = []
        for (ci, ri), items in sorted(sites.items(), key=lambda kv: kv[1][0][1]):
            reg = next(c["region"] for c in out_clusters if c["cluster_id"] == ci)
            shapes = Counter(p for _, _, p in items)
            site_list.append({
                "cluster_id": ci, "run_idx": ri,
                "n_codes_here": len({c for c, _, _ in items}),
                "shapes": {k: v for k, v in sorted(shapes.items())},
            })
        found_sample = [
            {"code": c, "first_off": hex(offs[0][0]), "shape": offs[0][1], "n_occurrences": len(offs)}
            for c, offs in list(found.items())[:8]
        ]
        # entity's dispatch-switch presence
        sw_sites = [s for s in out_switches if name in s["entity_hits"]]
        entity_index[name] = {
            "n_codes_unique": len(dict.fromkeys(codes)),
            "n_codes_found_in_imm_context": len(found),
            "coverage": round(len(found) / max(1, len(dict.fromkeys(codes))), 4),
            "sites": site_list,
            "switch_sites": [{"start_off": s["start_off"], "end_off": s["end_off"],
                              "region": s["region"], "n_cmp_hits": s["n_cmp_hits"],
                              "entity_hits": s["entity_hits"].get(name, 0)}
                             for s in sw_sites],
            "found_codes_sample": found_sample,
            "residual_codes": miss,
        }

    # ---- residual raw byte search (reversed + direct forms) ----
    print("residual raw search ...", flush=True)
    residual_hits = {}
    for name, miss in residual.items():
        for code in miss:
            for tag, needle in (("rev", code[::-1].encode("ascii", "replace")),
                                ("fwd", code.encode("ascii", "replace"))):
                offs = []
                i = data.find(needle)
                while i != -1 and len(offs) < 24:
                    offs.append(i)
                    i = data.find(needle, i + 1)
                if offs:
                    residual_hits.setdefault(code, []).append(
                        {"entity": name, "form": tag, "n": len(offs), "truncated": len(offs) >= 24,
                         "offsets": [hex(o) for o in offs],
                         "shapes": [shape_of(data, o + (0 if tag == 'fwd' else 0)) for o in offs[:8]]})
    # dedupe: same code may appear for several entities; keep first entity per code
    seen_code = set()
    resid_clean = {}
    for code, recs in sorted(residual_hits.items()):
        if code in seen_code:
            continue
        seen_code.add(code)
        resid_clean[code] = recs[:1]
    n_res_codes = len(resid_clean)
    print(f"residual codes located anywhere in file: {n_res_codes}  t={time.time()-t0:.1f}s", flush=True)

    result = {
        "meta": {
            "exe": str(sw.EXE).replace("\\", "/"),
            "exe_size": len(data),
            "sha256_first1k": hashlib.sha256(data[:1024]).hexdigest(),
            "image_base": hex(img_base),
            "scanned_bytes": len(data),
            "primary_patterns": sw_meta(sw),
            "aux_patterns": {
                "push_imm32": "68 <imm32>",
                "mov_r32_imm32": "b8..bf <imm32>",
                "mov_r32_imm32_rex": "41 b8..bf <imm32>",
                "cmp_r32_imm32": "81 f8..ff <imm32> (per-field dispatch switch, cf. H2)",
                "cmp_eax_imm32": "3d <imm32>",
            },
            "switch_gap": SWITCH_GAP,
            "min_hits_switch": MIN_HITS_SWITCH,
            "raw_hit_counts": pat_counts,
            "primary_hits_count": len(hits),
            "aux_entity_hits_count": len(aux_entity),
            "cluster_gap": CLUSTER_GAP,
            "dense_gap": DENSE_GAP,
            "min_hits_cluster": sw.MIN_HITS_CLUSTER,
            "va_rule": "VA = image_base + vaddr + (fileoff - rptr); .rdata: VA=fileoff+0xA00; .reloc: VA=fileoff+0x16B600",
            "sections": [{"name": s["name"], "rptr": hex(s["rptr"]), "rsize": hex(s["rsize"]),
                          "vaddr": hex(s["vaddr"])} for s in secs],
            "confidence_rule": ("high = exactly one entity explains >=60% of cluster 4CCs "
                                "(containment>=0.6, runner-up<0.6); medium = >=0.3 or ambiguous top; low otherwise"),
            "entity_source": str(sw.MASTER).replace("\\", "/"),
            "known_helpers_off": [hex(h) for h in sw.KNOWN_HELPERS],
            "notes": [
                "4CC = imm32 bytes reversed (little-endian); e.g. bytes 6d 61 6e 63 = 'cnam'",
                "clusters[] built from PRIMARY c7 mov-imm patterns only (commander spec); spans use instruction-start offsets (c7 45 f0 ...)",
                "aux idioms (push/mov-r32/cmp) used only to locate entity codes; filtered to entity-code 4CCs",
                "dispatch_switches spans use opcode-start offsets (81 xx imm32 => opcode at imm-2)",
                "hits[] has every primary raw hit (instruction start + imm offset + shape + 4CC) for byte-level verification",
            ],
        },
        "clusters": out_clusters,
        "dispatch_switches": out_switches,
        "entity_index": entity_index,
        "residual_code_hits": resid_clean,
        "hits": [{"off": hex(ps), "imm_off": hex(io), "shape": p, "cc": c} for ps, io, p, c in hits],
        "aux_hits": [{"imm_off": hex(o), "shape": p, "cc": c} for o, p, c in aux_entity],
    }
    sw.OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {sw.OUT_JSON}  t={time.time()-t0:.1f}s", flush=True)

    # console digest: per-entity coverage
    print("\nentity coverage (codes found in any imm context) and sites:")
    for name, rec in sorted(entity_index.items(), key=lambda kv: -kv[1]["coverage"]):
        site_s = "; ".join(f"c{ s['cluster_id']}r{s['run_idx']}:{s['n_codes_here']}@{next(c['start_off'] for c in out_clusters if c['cluster_id']==s['cluster_id'])}" for s in rec["sites"][:6])
        sw_s = "; ".join(f"{s['start_off']}:{s['entity_hits']}" for s in rec["switch_sites"][:3])
        print(f"  {rec['coverage']:6.2%} {name:32s} found={rec['n_codes_found_in_imm_context']}/{rec['n_codes_unique']} resid={len(rec['residual_codes'])} sites=[{site_s}] sw=[{sw_s}]")
    print("\ntop dispatch switches:")
    for s in out_switches[:12]:
        print(f"  {s['start_off']}..{s['end_off']} {s['region']:6s} cmp={s['n_cmp_hits']:4d} uniq={s['n_unique_cc']:4d} strides={dict(list(s['strides'].items())[:4])} ents={dict(list(s['entity_hits'].items())[:3])}")
    return 0


def sw_meta(sw) -> dict:
    return {
        "c7_45_disp8": "c7 45 <d8> <imm32>; 4CC = imm32 bytes reversed",
        "c7_44_24_disp8": "c7 44 24 <d8> <imm32>",
        "c7_85_disp32": "c7 85 <d32> <imm32>",
        "c7_84_24_disp32": "c7 84 24 <d32> <imm32> (bonus variant)",
    }


if __name__ == "__main__":
    sys.exit(main())
