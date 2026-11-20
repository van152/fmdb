"""t01-e: enumerate entity-definition vtables in editor.exe .debug raw region.

H3 (LEDGER E11): off 0x187d2b0 holds a 44-slot function-pointer table
(43 in-range ptrs + null terminator at slot 43); slot 6 = entity registration fn.
Hypothesis: one homogeneous 44-slot table per entity, slot6 -> its reg fn.

Method:
  1. scan file off 0x1758600..0x1a7d000 for runs of consecutive qwords all in
     [0x140001000, 0x150000000) (8B alignment; 4B offset pass as control).
     NOTE criterion adapted: anchor slot43==0, so primary shape = 43 ptrs + null.
  2. candidate table start = run_end - 43*8 (anchor shape). Also evaluate
     commander's literal 44-in-range windows (for runs len>=44), only kept
     when slot6 externally matches a registration block.
  3. slot6_off = slot6_va - 0x140000000 - 0xA00; match against dense_runs /
     cluster starts of t01a_editor_sweep.json (delta run_start - slot6_off in
     [0x00, 0x40] = registration prologue). .reloc clusters cross-checked with
     VA = off + 0x16B600.
  4. entity naming: dense_run cc_list vs master.json entity_summary codes
     (containment / coverage / jaccard).
  5. spot check: capstone disasm of slot6 targets, expect c7 45 f0 <imm32>.

Outputs: scratch/t01/t01e_vtables.json (+ stdout summary).
"""
from __future__ import annotations

import json
import struct
from pathlib import Path

EXE = Path(r"<OLD_REPO>\input\editor.exe")
SWEEP = Path(r"<WORKSPACE>\scratch\t01\t01a_editor_sweep.json")
MASTER = Path(r"<WORKSPACE>\evidence\fm24\reports\editor_schema\master.json")
OUT = Path(r"<WORKSPACE>\scratch\t01\t01e_vtables.json")

LO, HI = 0x1758600, 0x1A7D000          # .debug raw region (E11)
A0, A1 = 0x140001000, 0x150000000      # VA window for table entries
DELTA_RDATA = 0xA00                    # RVA = off + 0xA00 (rdata + debug raw, E11/E3)
DELTA_RELOC = 0x16B600                 # VA = off + 0x16B600 (E9)
IMAGE_BASE = 0x140000000
SLOT = 6
N_PTR = 43                             # anchor: 43 ptrs + null = 44-slot table
PROLOGUE_TOL = (0x00, 0x80)            # run.start_off - slot6_off range (varies per entity)

# registration-fn prologue variants (byte-verified, file off = block - delta):
#   V1 block-0x20: 55 56 57 48 83 ec 40        (comp/awar/drbr/stad/nati/mdso/inju/weat/pers)
#   V2 block-0x24: 55 56 57 53 48 83 ec 38     (club, nnpl)
#   V3 block-0x29: 55 41 56 56 57 53 48 83 ec 40 (agen/offc/jour)
PRO_V1 = bytes.fromhex("5556574883ec")
PRO_V2 = bytes.fromhex("555657534883ec")
PRO_V3 = bytes.fromhex("5541565657534883ec")
ADD38 = bytes.fromhex("4883c038")


def fn_start_at(off: int) -> bool:
    """true if file off looks like a registration-fn entry (prologue + add rax,0x38)."""
    if not (0 <= off < len(data) - 0x100):
        return False
    head = data[off:off + 9]
    if not (head[:6] == PRO_V1 or head[:7] == PRO_V2 or head[:9] == PRO_V3):
        return False
    return ADD38 in data[off:off + 0x60]

data = EXE.read_bytes()


def inrange(v: int) -> bool:
    return A0 <= v < A1


# ---------- 1. pointer-run scan (8B alignment) ----------
def scan_runs(step_off: int) -> list[tuple[int, int, int | None]]:
    """maximal runs of consecutive in-range qwords at qwords starting LO+step_off."""
    runs = []
    n = (HI - LO - step_off) // 8
    base = LO + step_off
    vals = struct.unpack_from(f"<{n}Q", data, base)
    i = 0
    while i < n:
        if inrange(vals[i]):
            j = i
            while j < n and inrange(vals[j]):
                j += 1
            if j - i >= N_PTR:
                runs.append((base + i * 8, j - i, vals[j] if j < n else None))
            i = j
        else:
            i += 1
    return runs


runs8 = scan_runs(0)
runs4 = scan_runs(4)  # control pass: 4B-misaligned tables

# ---------- 2. candidates ----------
candidates = []  # dicts: off, shape, run_len, term
for off, ln, term in runs8:
    if ln == N_PTR and term == 0:
        candidates.append({"off": off, "shape": "43ptr+null", "run_len": ln,
                           "term": term, "primary": True})
    elif ln > N_PTR and term == 0:
        # window ending at the null: last 43 ptrs + null (anchor shape)
        candidates.append({"off": off + (ln - N_PTR) * 8, "shape": "tail43+null",
                           "run_len": ln, "term": term, "primary": False})
        # commander literal 44-in-range windows inside the run
        for k in range(0, ln - 43):
            candidates.append({"off": off + k * 8, "shape": "44inrange",
                               "run_len": ln, "term": term, "primary": False})
    elif ln >= N_PTR:  # term != 0 (run continues/ends on other data)
        for k in range(0, ln - 43):
            candidates.append({"off": off + k * 8, "shape": "44inrange_noterm",
                               "run_len": ln, "term": term, "primary": False})

anchor_off = 0x187D2B0
assert any(c["off"] == anchor_off for c in candidates), "anchor window missing"

# ---------- 3. load sweep + master, build match index ----------
sweep = json.loads(SWEEP.read_text())
master = json.loads(MASTER.read_text())

dense = []      # (start_off, end_off, cc_list, cluster_id, region)
clusters = []   # cluster dicts as-is
for c in sweep["clusters"]:
    clusters.append(c)
    for dr in c["dense_runs"]:
        dense.append((int(dr["start_off"], 16), int(dr["end_off"], 16),
                      dr["cc_list"], c["cluster_id"], c["region"]))
dense.sort()
dense_starts = [d[0] for d in dense]
cluster_starts = sorted(int(c["start_off"], 16) for c in clusters)

import bisect


def near_dense(off: int, tol: int):
    """dense runs whose start_off within ±tol of off."""
    i = bisect.bisect_left(dense_starts, off - tol)
    out = []
    while i < len(dense) and dense_starts[i] <= off + tol:
        out.append(dense[i])
        i += 1
    return out


def near_cluster_start(off: int, tol: int):
    i = bisect.bisect_left(cluster_starts, off - tol)
    return [s for s in cluster_starts[i:] if s <= off + tol]


# entity code sets
ent_codes = {}
for key, es in master["entity_summary"].items():
    ent_codes[key.split("#")[1]] = set(es["codes"])


def best_entity(codes: list[str]) -> dict:
    cs = set(codes)
    best = None
    for name, ec in ent_codes.items():
        inter = cs & ec
        cont = len(inter) / len(cs) if cs else 0.0
        cov = len(inter) / len(ec)
        jac = len(inter) / len(cs | ec)
        cand = (cont, cov, jac, name, len(inter))
        if best is None or (cand[0], cand[1], cand[4]) > (best[0], best[1], best[4]):
            best = cand
    cont, cov, jac, name, n = best
    return {"entity": name, "containment": round(cont, 4), "coverage": round(cov, 4),
            "jaccard": round(jac, 4), "inter_n": n}


HELPER_PAIRS = {("0x83abf0", "0x83caf0"): "A(rdata)",
                ("0x6cfff0", "0x6d1ef0"): "B(reloc)"}


def helper_pair_of(dr_idx: int) -> str:
    # helpers recorded on cluster call_targets
    pass


def slot6_va_at(off: int) -> int:
    return struct.unpack_from("<Q", data, off + SLOT * 8)[0]


# ---------- match candidates ----------
results = []
matched_dense_keys = set()   # (dense_start_off) matched by some slot6
matched_cluster_ids = set()

for cand in candidates:
    off = cand["off"]
    va = slot6_va_at(off)
    rva = va - IMAGE_BASE
    s6off = rva - DELTA_RDATA                      # candidate reg-fn file off (.rdata map)
    rec = {"table_off": f"{off:#x}", "shape": cand["shape"], "run_len": cand["run_len"],
           "primary": cand["primary"], "slot6_va": f"{va:#x}", "slot6_rva": f"{rva:#x}",
           "slot6_off_rdata": f"{s6off:#x}"}
    m = None
    if 0 <= s6off < len(data):
        hits = near_dense(s6off, PROLOGUE_TOL[1])
        # keep runs with start_off - slot6_off in [0, 0x40]
        hits = [h for h in hits if 0 <= h[0] - s6off <= PROLOGUE_TOL[1]]
        if hits:
            hits.sort(key=lambda h: h[0] - s6off)
            d_start, d_end, cc, cid, region = hits[0]
            delta = d_start - s6off
            be = best_entity(cc)
            rec["matched"] = {"dense_run_off": f"{d_start:#x}", "delta": delta,
                              "cluster_id": cid, "region": region,
                              "n_codes": len(cc), **be}
            m = (d_start, cid)
    rec["matched_cluster_off"] = rec["matched"]["dense_run_off"] if m else None
    rec["entity"] = rec["matched"]["entity"] if m else None
    rec["containment"] = rec["matched"]["containment"] if m else None
    results.append(rec)
    if m:
        matched_dense_keys.add(m[0])
        matched_cluster_ids.add(m[1])

# ---------- 4b. reverse lookup: reg-fn VA -> pointer references ----------
# For every registration function (dense run / cluster start), search the whole
# file for its VA as an 8-byte pointer; characterize the table window around
# each reference (T = P - 0x30 = presumed slot6 position).
rev_targets = {}  # va -> {kind, off, region, cluster_id, cc_list}
# VA mapping is region-consistent (a block's VA is fixed by its section):
# .rdata -> off+0xA00, .reloc -> off+0x16B600 (E3/E9/E11)
def region_map(region: str) -> int:
    return DELTA_RELOC if region == ".reloc" else DELTA_RDATA


for c in sweep["clusters"]:
    cstart = int(c["start_off"], 16)
    region = c["region"]
    va = IMAGE_BASE + cstart + region_map(region)
    key = f"{va:#x}"
    if key not in rev_targets:
        rev_targets[key] = {"va": va, "kind": "cluster", "off": cstart,
                            "region": region, "map": region_map(region),
                            "cluster_id": c["cluster_id"], "cc_list": c["cc_list"]}
for (d_start, d_end, cc, cid, region) in dense:
    va = IMAGE_BASE + d_start + region_map(region)
    key = f"{va:#x}"
    if key not in rev_targets:
        rev_targets[key] = {"va": va, "kind": "dense_run", "off": d_start,
                            "region": region, "map": region_map(region),
                            "cluster_id": cid, "cc_list": cc}
    else:
        rev_targets[key]["kind"] = "dense_run"
        rev_targets[key]["cc_list"] = cc

# maximal in-range run lookup over the whole file (8-aligned), cached
run_index = None


def build_run_index():
    global run_index
    n = len(data) // 8
    vals = struct.unpack_from(f"<{n}Q", data, 0)
    run_index = []
    i = 0
    while i < n:
        if inrange(vals[i]):
            j = i
            while j < n and inrange(vals[j]):
                j += 1
            run_index.append((i * 8, (j - i) * 8, vals[j] if j < n else None))  # off, n_bytes, term
            i = j
        else:
            i += 1


build_run_index()
run_starts = [r[0] for r in run_index]


def window_shape(T: int) -> dict:
    """characterize presumed table at T (slot6 at T+0x30)."""
    if T < 0:
        return {"plausible": False}
    i = bisect.bisect_right(run_starts, T) - 1
    if i < 0:
        return {"plausible": False}
    r0, rn, term = run_index[i]
    if T < r0 or T + 44 * 8 > r0 + rn + 8:
        return {"plausible": False}
    arity_to_null = (r0 + rn - T) // 8 if term == 0 else None
    pre_ok = all(inrange(struct.unpack_from("<Q", data, T + k * 8)[0]) for k in range(6))
    slot43_null = term == 0 and T + 44 * 8 == r0 + rn + 8
    return {"plausible": True, "run_start": r0, "run_len": rn // 8,
            "run_term": term, "arity_to_null": arity_to_null,
            "pre6_ok": pre_ok, "slot43_null": slot43_null}


rev_hits = []
# sorted index of ALL in-range qwords in the whole file: (va, off)
n_all = len(data) // 8
_all_vals = struct.unpack_from(f"<{n_all}Q", data, 0)
pairs = sorted((v, i * 8) for i, v in enumerate(_all_vals) if inrange(v))
ptr_vs = [p[0] for p in pairs]
del _all_vals

for key, tgt in sorted(rev_targets.items()):
    block_va = tgt["va"]  # VA of first mov-imm block
    lo = block_va - PROLOGUE_TOL[1] - 0x08
    hi = block_va + 0x08
    i = bisect.bisect_left(ptr_vs, lo)
    j = bisect.bisect_right(ptr_vs, hi)
    seen = set()
    for k in range(i, j):
        P = pairs[k][1]
        if P % 8:
            continue  # vtable slots are 8-aligned
        slot_va = pairs[k][0]
        delta = block_va - slot_va  # reg block start VA - slot6 target VA
        T = P - SLOT * 8
        sh = window_shape(T)
        be = best_entity(tgt["cc_list"]) if tgt["cc_list"] else {}
        rec = {"reg_block_off": f"{tgt['off']:#x}", "reg_kind": tgt["kind"],
               "reg_region": tgt["region"], "reg_map": tgt["map"],
               "slot6_va": f"{slot_va:#x}", "slot6_rva": f"{slot_va - IMAGE_BASE:#x}",
               "block_delta": delta, "cluster_id": tgt["cluster_id"],
               "ref_off": f"{P:#x}", "presumed_table_off": f"{T:#x}", **sh}
        if be and be["inter_n"] > 0:
            rec.update({"entity": be["entity"], "containment": be["containment"],
                        "coverage": be["coverage"], "jaccard": be["jaccard"],
                        "inter_n": be["inter_n"], "n_codes": len(tgt["cc_list"])})
        else:
            rec.update({"entity": None, "containment": be["containment"] if be else None,
                        "coverage": be["coverage"] if be else None,
                        "jaccard": be["jaccard"] if be else None,
                        "inter_n": be["inter_n"] if be else 0,
                        "n_codes": len(tgt["cc_list"]) if tgt["cc_list"] else 0})
        sig = (P, slot_va)
        if sig in seen:
            continue
        seen.add(sig)
        rev_hits.append(rec)

# keep table-like references: slot6 window plausible AND ref target byte-verifies
# as a registration-fn start (prologue V1/V2/V3 + add rax,0x38)
for h in rev_hits:
    h["fn_start_ref"] = fn_start_at(int(h["slot6_rva"], 16) - DELTA_RDATA)
rev_table_like = [h for h in rev_hits
                  if h.get("plausible") and h.get("pre6_ok") and h["fn_start_ref"]
                  and h["run_start"] + h["run_len"] * 8 >= int(h["presumed_table_off"], 16) + 43 * 8]

# ---------- table (b): clusters not pointed by any slot6 ----------
# match tracking = forward slot6->dense-run matches + reverse table-like refs
rev_block_offs = {int(h["reg_block_off"], 16) for h in rev_table_like}
rev_cluster_ids = {h["cluster_id"] for h in rev_table_like}
unmatched_clusters = []
for c in sweep["clusters"]:
    cs = int(c["start_off"], 16)
    dr_starts = [int(dr["start_off"], 16) for dr in c["dense_runs"]]
    hit_fwd = any(ds in matched_dense_keys for ds in dr_starts) or cs in matched_dense_keys
    hit_rev = (cs in rev_block_offs
               or any(ds in rev_block_offs for ds in dr_starts)
               or c["cluster_id"] in rev_cluster_ids)
    rec = {"cluster_id": c["cluster_id"], "start_off": c["start_off"],
           "region": c["region"], "n_hits": c["n_hits"],
           "n_unique_cc": c["n_unique_cc"], "confidence": c["confidence"],
           "entity_top3": c.get("entity_top3", []),
           "matched_by_slot6": hit_fwd or hit_rev,
           "via": ("forward" if hit_fwd else "") + ("+reverse" if hit_rev and hit_fwd else "")
                  + ("reverse" if hit_rev and not hit_fwd else "")}
    unmatched_clusters.append(rec)

# ---------- table (c): slot6 not matching any cluster ----------
slot6_unmatched = []
for rec in results:
    if rec["matched_cluster_off"] is None:
        rva = int(rec["slot6_rva"], 16)
        roff = rva - DELTA_RELOC                    # .reloc alternative mapping
        near = near_cluster_start(roff, PROLOGUE_TOL[1]) if roff >= 0 else []
        rec2 = dict(rec)
        rec2["reloc_xcheck_off"] = f"{roff:#x}" if roff >= 0 else None
        rec2["reloc_cluster_near"] = [f"{s:#x}" for s in near]
        slot6_unmatched.append(rec2)

# ---------- 5. spot check: disasm slot6 targets (signature based) ----------
# registration-fn signature (E2/E11 + club variant): prologue 55 56 57 [53];
# sub rsp; lea rbp; mov [rbp+x],-1; mov rsi,rdx; call helper; add rax,0x38;
# then repeating c7 45 <d8> <imm32> 4CC blocks (disp8 varies: f0/f8/00...)
try:
    import capstone
    HAVE_CAPSTONE = True
except ImportError:
    HAVE_CAPSTONE = False

STUB_RVAS = set()
spot_checks = []
if HAVE_CAPSTONE:
    rev_ok = [h for h in rev_table_like
              if h.get("entity") and 0 <= h["block_delta"] <= 0x40
              and h.get("containment", 0) >= 0.3]
    seen_tables = set()
    picks = []
    for h in rev_ok:
        if h["presumed_table_off"] not in seen_tables:
            seen_tables.add(h["presumed_table_off"])
            picks.append(h)
    # spread picks across distinct prologue deltas for variant coverage
    bydelta = {}
    for h in picks:
        bydelta.setdefault(h["block_delta"], h)
    picks = [bydelta[d] for d in sorted(bydelta)][:3]
    picks.append(next(h for h in rev_hits
                      if h["presumed_table_off"] == f"{anchor_off:#x}"))
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

    def sig_verify(slot6_off: int) -> dict:
        blob = data[slot6_off:slot6_off + 0xA0]
        txt = []
        for ins in md.disasm(blob, slot6_off + DELTA_RDATA):
            txt.append(f"{ins.address:#x} {ins.bytes.hex():<22} {ins.mnemonic} {ins.op_str}")
        full = " ".join(txt)
        first4 = blob[:4]
        prologue = (first4[:3] == b"\x55\x56\x57"          # V1/V2
                    or first4[:2] == b"\x55\x41")          # V3: 55 41 56 56 57 53
        add38 = "add rax, 0x38" in full
        blocks = []
        ccs = []
        for t in txt:
            parts = t.split(None, 3)
            if len(parts) == 4 and parts[2] == "mov" and parts[3].startswith("dword ptr [rbp"):
                blocks.append(parts[3])
                if "0x" in parts[3]:
                    try:
                        imm = int(parts[3].split(", 0x")[1], 16)
                        if 0x20202020 <= imm <= 0x7f7f7f7f:
                            ccs.append(struct.pack("<I", imm).decode("latin1")[::-1])
                    except (IndexError, ValueError):
                        pass
        return {"prologue_555657": prologue, "add_rax_38": add38,
                "reg_blocks": blocks[:3], "first_4ccs": ccs[:6],
                "reg_sig_ok": prologue and add38 and bool(blocks)}

    for h in picks:
        tgt_off = int(h["slot6_rva"], 16) - DELTA_RDATA
        sv = sig_verify(tgt_off)
        spot_checks.append({"table_off": h["presumed_table_off"], "entity": h.get("entity"),
                            "slot6_off": f"{tgt_off:#x}", "block_delta": h["block_delta"],
                            **sv})

# ---------- 6. primary-table family classification ----------
def slot6_class(r: dict) -> str:
    va = int(r["slot6_va"], 16)
    rva = va - IMAGE_BASE
    off = rva - DELTA_RDATA
    if 0x1000 <= rva < 0x2000:
        return "stub"
    if 0 <= off < len(data):
        if fn_start_at(off):
            return "regfn_unlisted"      # reg-fn shaped but not in t01a clusters
        b = data[off:off + 8]
        if b[:1] == b"\x55" and bytes.fromhex("4883ec") in data[off:off + 8] \
                and ADD38 in data[off:off + 0x60]:
            return "regfn_variant"       # 4th prologue shape
        return "other_code"
    if rva - DELTA_RELOC >= 0:
        return "reloc_zone"
    return "unknown"

n_primary = sum(1 for r in results if r["primary"])
rev_by_table = {}
for h in rev_table_like:
    rev_by_table.setdefault(h["presumed_table_off"], h)
for r in results:
    rv = rev_by_table.get(r["table_off"])
    r["reverse_hit"] = rv is not None
    if rv and r["matched_cluster_off"] is None:
        r["matched_cluster_off"] = rv["reg_block_off"]
        r["entity"] = rv.get("entity")
        r["containment"] = rv.get("containment")
        r["match_via"] = "reverse"
    elif r["matched_cluster_off"] is not None:
        r["match_via"] = "forward"
    if r["primary"] and r["matched_cluster_off"] is None:
        r["slot6_class"] = slot6_class(r)
prim_matched = [r for r in results if r["primary"] and r["matched_cluster_off"]]
prim_unmatched = [r for r in results if r["primary"] and not r["matched_cluster_off"]]
sec_matched = [r for r in results if not r["primary"] and r["matched_cluster_off"]]

from collections import Counter
fam_dist = Counter(r.get("slot6_class", "entity_matched") for r in prim_unmatched)

# ---------- final vtables table (confirmed entity mapping rows) ----------
vtable_rows = []
seen_t = set()
for h in rev_table_like:
    T = h["presumed_table_off"]
    if T in seen_t:
        continue
    seen_t.add(T)
    vtable_rows.append({
        "table_off": T,
        "run_start": f"{h['run_start']:#x}", "run_len": h["run_len"],
        "run_term": h["run_term"], "arity_to_null": h["arity_to_null"],
        "slot6_rva": h["slot6_rva"], "slot6_va": h["slot6_va"],
        "reg_block_off": h["reg_block_off"], "block_delta": h["block_delta"],
        "cluster_id": h["cluster_id"],
        "matched_cluster_off": h["reg_block_off"],
        "entity": h.get("entity"), "containment": h.get("containment"),
        "coverage": h.get("coverage"), "inter_n": h.get("inter_n"),
        "n_codes": h.get("n_codes"),
        "note": "arity>43: run continues past slot43, table boundary ambiguous"
                if (h["arity_to_null"] or 44) != 43 or not h["slot43_null"] else
                "44-slot table: 43 ptrs + null (anchor shape)" if h["slot43_null"] else "",
    })

unmatched_cluster_list = [u for u in unmatched_clusters if not u["matched_by_slot6"]]

out = {
    "meta": {
        "exe": str(EXE), "task": "t01-e vtable enum (H3, LEDGER E11)",
        "scan_region": [f"{LO:#x}", f"{HI:#x}"],
        "criterion": "forward: runs of consecutive in-range qwords [0x140001000,0x150000000) "
                     "in debug region; anchor shape = 43 ptrs + null (anchor slot43==0, "
                     "literal 44-in-range would MISS the anchor); "
                     "reverse: whole-file ptr index queried at block_va-0x80..block_va+8; "
                     "ref kept only if target byte-verifies as reg-fn start "
                     "(prologue V1 55 56 57 48 83 ec / V2 55 56 57 53 48 83 ec / "
                     "V3 55 41 56 56 57 53 48 83 ec + add rax,0x38)",
        "va_maps": {"rdata_and_debug_raw": "RVA=off+0xA00",
                    "reloc": "VA=off+0x16B600"},
        "slot": 6, "anchor": {"table_off": f"{anchor_off:#x}",
                              "slot6_va": "0x140ebfa40"},
        "prologue_tol": list(PROLOGUE_TOL),
        "runs8_ge43": len(runs8), "runs4_ge43_control": len(runs4),
        "candidates_total": len(results),
        "primary_candidates": n_primary,
        "primary_entity_matched": len(prim_matched),
        "primary_unmatched": len(prim_unmatched),
        "primary_unmatched_families": dict(fam_dist),
        "secondary_matched_windows": len(sec_matched),
        "reverse_targets": len(rev_targets),
        "reverse_ptr_refs": len(rev_hits),
        "reverse_table_like": len(rev_table_like),
        "confirmed_entities": sorted({h.get("entity") for h in rev_table_like if h.get("entity")}),
        "confirmed_entity_count": len({h.get("entity") for h in rev_table_like if h.get("entity")}),
        "clusters_total": len(unmatched_clusters),
        "clusters_matched_by_slot6": sum(1 for u in unmatched_clusters if u["matched_by_slot6"]),
        "clusters_unmatched": len(unmatched_cluster_list),
        "spot_check_capstone": HAVE_CAPSTONE,
    },
    "vtables": vtable_rows,
    "forward_scan": results,
    "reverse_refs": rev_hits,
    "reverse_table_like": rev_table_like,
    "unmatched_clusters": unmatched_cluster_list,
    "all_clusters_status": unmatched_clusters,
    "slot6_unmatched": [r for r in results if r["primary"] and r["matched_cluster_off"] is None],
    "spot_checks": spot_checks,
}
OUT.write_text(json.dumps(out, indent=1))

print(f"runs8>=43: {len(runs8)}  runs4 control: {len(runs4)}")
print(f"candidates: {len(results)}  primary(43+null): {n_primary}")
print(f"primary entity-matched: {len(prim_matched)}  unmatched: {len(prim_unmatched)}  families: {dict(fam_dist)}")
print(f"reverse: targets={len(rev_targets)} refs={len(rev_hits)} table_like={len(rev_table_like)}")
print("confirmed entities:", out["meta"]["confirmed_entities"])
print(f"clusters matched by slot6: {out['meta']['clusters_matched_by_slot6']}/{len(unmatched_clusters)}")
for sc in spot_checks:
    print(f"spot {sc['table_off']} entity={sc['entity']} sig_ok={sc['reg_sig_ok']} "
          f"pro={sc['prologue_555657']} add38={sc['add_rax_38']} 4ccs={sc['first_4ccs']}")
