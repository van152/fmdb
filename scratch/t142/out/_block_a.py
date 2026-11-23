# ---------------------------------------------------------------- domains
# Scoring constants (documented in REPORT.md; `classify` holds the decision
# tree).  A column is only promoted when no plausible coincidence explains it.
ENUM_DISTINCT_MAX = 24          # <= this many distinct values looks like an enum
UID_UNIFORM_MAX = 1e-4         # accidental hit chance of a random u32 draw
UID_LARGE_SHARE_MIN = 0.5      # share of target uids >= 1e6 (non-sequential)
SAMPLE_PROBE = 4096            # values used by the cheap pre-filter


def domain_stats(arr) -> dict:
    a = np.unique(np.asarray(arr, dtype=np.uint64))
    n = int(a.size)
    if n == 0:
        return dict(count=0, min=None, max=None, dense_ratio=0.0, digest=digest_set(a))
    lo, hi = int(a[0]), int(a[-1])
    span = hi - lo + 1
    return dict(count=n, min=lo, max=hi, span=span,
                dense_ratio=round(n / span, 12), digest=digest_set(a),
                uniform_chance=round(n / float(1 << 32), 12),
                large_share=round(float(np.count_nonzero(a >= 1_000_000)) / n, 6),
                unique=n == int(np.asarray(arr).size))


def build_domains(write=True):
    """Identity-domain registry for every entity table (stage 2)."""
    CACHE.mkdir(parents=True, exist_ok=True)
    registry, domain_sets = {}, {}
    names = [table_key(*k) for k in all_table_keys()] + list(SPECIALS)
    for name in names:
        cols, meta = load_columns(name)
        ords = [c["values"] for c in cols.values() if c["kind"] == "ord"]
        uids = [c["values"] for c in cols.values() if c["kind"] == "uid"]
        ord_arr = np.unique(np.concatenate(ords)) if ords else np.zeros(0, np.uint64)
        uid_arr = np.unique(np.concatenate(uids)) if uids else np.zeros(0, np.uint64)
        anomalies = []
        dense = False
        if ords:
            raw_ord = np.concatenate(ords)
            dup = int(raw_ord.size - ord_arr.size)
            if dup:
                anomalies.append(f"duplicate ordinal values: {dup}")
            if ord_arr.size and int(ord_arr.min()) == 0 and ord_arr.size == raw_ord.size and \
                    bool((ord_arr == np.arange(ord_arr.size, dtype=np.uint64)).all()):
                dense = True
                anomalies.append("ordinal == row index (dense 0..N-1)")
        if uids:
            raw_uid = np.concatenate(uids)
            dup = int(raw_uid.size - uid_arr.size)
            if dup:
                anomalies.append(f"duplicate uid values: {dup}")
            for sent in (0xFFFFFFFF, 0xFFFFFFFE):
                if bool((uid_arr == sent).any()):
                    anomalies.append(f"uid domain contains sentinel 0x{sent:X}")
        ent = dict(table=name, klass=meta["klass"], table_id=meta["table_id"],
                   archive=meta["archive"], rows=meta["rows"], columns=meta["columns"],
                   ordinal=domain_stats(ord_arr),
                   uid=domain_stats(uid_arr) if uid_arr.size else None,
                   anomalies=anomalies)
        ent["ordinal"]["form"] = "dense 0..N-1" if dense else ("sparse" if ord_arr.size else "absent")
        registry[name] = ent
        domain_sets[(name, "ordinal")] = ord_arr
        if uid_arr.size:
            domain_sets[(name, "uid")] = uid_arr

    classes = {}
    for name, ent in registry.items():
        slot = classes.setdefault(ent["klass"], {"tables": [], "ordinal": None, "uid": None})
        slot["tables"].append(name)
        for key in ("ordinal", "uid"):
            if (name, key) in domain_sets and (slot[key] is None or ent["archive"] == "server"):
                slot[key] = domain_sets[(name, key)]
                slot[f"{key}_source"] = name
    classes["basic_person"] = dict(tables=["basic_people"],
                                   ordinal=domain_sets[("basic_people", "ordinal")],
                                   uid=domain_sets[("basic_people", "uid")],
                                   ordinal_source="basic_people", uid_source="basic_people")

    digs, shared = {}, []
    for klass, slot in classes.items():
        for key in ("ordinal", "uid"):
            arr = slot.get(key)
            if arr is None or arr.size == 0:
                continue
            digs.setdefault(digest_set(arr), []).append(f"{klass}.{key}")
    for d, members in digs.items():
        if len(members) > 1:
            klass, key = members[0].split(".")
            shared.append(dict(digest=d, members=sorted(members),
                               count=int(classes[klass][key].size)))
    out = dict(schema_id="fm24.t142.stage2_domains", schema_version=1,
               registry=registry,
               classes={k: dict(tables=v["tables"],
                                ordinal_source=v.get("ordinal_source"),
                                uid_source=v.get("uid_source"),
                                ordinal_count=int(v["ordinal"].size) if v["ordinal"] is not None else 0,
                                uid_count=int(v["uid"].size) if v["uid"] is not None else 0,
                                ordinal_stats=domain_stats(v["ordinal"]) if v["ordinal"] is not None else None,
                                uid_stats=domain_stats(v["uid"]) if v["uid"] is not None else None)
                        for k, v in classes.items()},
               shared_namespaces=shared)
    if write:
        dump_json(STAGE2, out)
    return registry, domain_sets, classes


# ---------------------------------------------------------------- FK scoring
class Domain:
    """A target key domain plus the statistics used to judge an edge."""

    __slots__ = ("klass", "key", "arr", "count", "min", "max", "large_share",
                 "uniform_chance", "digest")

    def __init__(self, klass, key, arr):
        self.klass, self.key = klass, key
        self.arr = np.ascontiguousarray(arr, dtype=np.uint64)
        self.count = int(self.arr.size)
        self.min = int(self.arr[0])
        self.max = int(self.arr[-1])
        self.large_share = float(np.count_nonzero(self.arr >= 1_000_000)) / self.count
        self.uniform_chance = self.count / float(1 << 32)
        self.digest = digest_set(self.arr)


def build_domain_list(classes):
    out = []
    for klass, slot in sorted(classes.items()):
        for key in ("ordinal", "uid"):
            arr = slot.get(key)
            if arr is None or arr.size == 0:
                continue
            out.append(Domain(klass, key, arr))
    return out


def domain_hits(arr, dom_arr):
    """Count values of ``arr`` present in the sorted unique ``dom_arr``."""
    if dom_arr.size == 0 or arr.size == 0:
        return 0
    idx = np.searchsorted(dom_arr, arr)
    idx[idx == dom_arr.size] = dom_arr.size - 1
    return int(np.count_nonzero(dom_arr[idx] == arr))


def in_domain(arr, dom_arr):
    if dom_arr.size == 0 or arr.size == 0:
        return np.zeros(arr.size, dtype=bool)
    idx = np.searchsorted(dom_arr, arr)
    idx[idx == dom_arr.size] = dom_arr.size - 1
    return dom_arr[idx] == arr


def sentinel_mask(values, width, kind="u"):
    """Rows carrying a real value (all-ones sentinels removed)."""
    s = SENTINEL_BY_WIDTH.get(width)
    if s is None:
        return np.ones(values.size, dtype=bool)
    return values != np.uint64(s)


def column_profile(values, width, kind="u"):
    keep = sentinel_mask(values, width, kind)
    live = values[keep]
    sent = [f"0x{int(x):X}" for x in np.unique(values[~keep])[:4]]
    return dict(rows=int(values.size), non_sentinel_rows=int(live.size),
                sentinel_rows=int(values.size - live.size), sentinel_values=sent,
                distinct=int(np.unique(live).size) if live.size else 0,
                min=int(live.min()) if live.size else None,
                max=int(live.max()) if live.size else None,
                width=width, live=live)


def corroboration(src_name, target, pair_kind=None):
    """4CC/L3 field-name token or reference-pair layout corroboration."""
    ev = []
    low = (src_name or "").lower()
    for tok in NAME_TOKENS.get(target.upper(), ()):
        if tok in low:
            ev.append("name_token:" + tok)
    if pair_kind:
        ev.append("layout:" + pair_kind)
    return ev


def classify(cand, prof, src_name):
    """Promotion decision for one (column, target-domain) candidate."""
    if prof["non_sentinel_rows"] < MIN_ROWS:
        return "rejected", ["too_few_rows"]
    if prof["distinct"] < MIN_DISTINCT:
        return "rejected", ["constant_column"]
    if cand["hit_rate"] < HIT_RATE_MIN:
        return "rejected", ["hit_rate_below_floor"]
    corr = corroboration(src_name, cand["target"], cand.get("pair_kind"))
    enum_like = (cand["distinct"] <= ENUM_DISTINCT_MAX
                 and cand["target_domain_count"] <= SMALL_DOMAIN_GUARD)
    if corr:
        return "verified", ["corroborated:" + ",".join(corr)]
    if (cand["target_key"] == "uid" and cand["uniform_chance"] <= UID_UNIFORM_MAX
            and cand["target_large_share"] >= UID_LARGE_SHARE_MIN):
        return "verified", ["statistical_uid_sparse:%.2e" % cand["uniform_chance"]]
    if enum_like:
        return "ambiguous", ["enum_like_small_domain"]
    if cand["target_key"] == "ordinal":
        return "ambiguous", ["dense_ordinal_domain_not_provable"]
    return "ambiguous", ["low_specificity"]


def evaluate_column(vals, width, src_name, src_table, domains, own):
    """Test one column against every target key domain."""
    prof = column_profile(vals, width)
    live = prof["live"]
    out = []
    if live.size < MIN_ROWS or prof["distinct"] < MIN_DISTINCT:
        return out, prof
    vmin, vmax = prof["min"], prof["max"]
    probe = live[::max(1, live.size // SAMPLE_PROBE)]
    for d in domains:
        if (d.klass, d.key) in own:
            continue
        if vmax > d.max or vmin < d.min:
            continue
        if domain_hits(probe, d.arr) < 0.90 * probe.size:
            continue
        h = domain_hits(live, d.arr)
        rate = h / live.size
        if rate < 0.90:
            continue
        out.append(dict(target=d.klass, target_key=d.key, target_domain_count=d.count,
                        target_large_share=round(d.large_share, 6),
                        uniform_chance=d.uniform_chance,
                        hits=h, rows=int(live.size), hit_rate=round(rate, 6)))
    out.sort(key=lambda r: (-r["hit_rate"], r["uniform_chance"], -r["target_domain_count"]))
    return out, prof


def orphan_detail(vals, width, dom_arr, limit=SAMPLE_ORPHANS):
    prof = column_profile(vals, width)
    miss = prof["live"][~in_domain(prof["live"], dom_arr)]
    if miss.size == 0:
        return 0, 0, []
    uniq, counts = np.unique(miss, return_counts=True)
    samples = [dict(value=int(v), rows=int(c)) for v, c in zip(uniq[:limit], counts[:limit])]
    return int(miss.size), int(uniq.size), samples


def scan_edges(classes, verbose=True):
    """Stage 3: audit every integer scalar column and every reference pair."""
    domains = build_domain_list(classes)
    dmap = {(d.klass, d.key): d for d in domains}
    edges, ambiguous, pair_edges = [], [], []
    scanned = tests = 0
    t0 = time.perf_counter()
    names = [table_key(*k) for k in all_table_keys()] + list(SPECIALS)
    for name in names:
        cols, meta = load_columns(name)
        klass = meta["klass"]
        own = {(klass, "ordinal"), (klass, "uid")}
        test_cols = []
        for cid, c in cols.items():
            k, w = c["kind"], c["width"]
            if k in ("gate", "ord", "uid", "dbid", "uwide"):
                continue
            mask = c.get("present")
            if k == "u" and w in (1, 2, 4):
                test_cols.append((cid, c["name"], w, c["values"], mask, c["off"]))
            elif k in ("pair_ord", "pair_uid"):
                test_cols.append((cid, c["name"], 4, c["values"], mask, c["off"]))
            elif k == "u" and w == 8:
                v = c["values"]
                test_cols.append((cid + "#lo32", c["name"] + ".lo32", 4,
                                  v & np.uint64(0xFFFFFFFF), mask, c["off"]))
                test_cols.append((cid + "#hi32", c["name"] + ".hi32", 4,
                                  v >> np.uint64(32), mask, c["off"]))
        for cid, cname, width, vals, mask, off in test_cols:
            if mask is not None:
                vals = vals[mask]
            if vals.size < MIN_ROWS:
                continue
            scanned += 1
            cands, prof = evaluate_column(vals, width, cname, name, domains, own)
            if not cands:
                continue
            tests += len(cands)
            best = None
            for cand in cands:
                tier, notes = classify(cand, prof, cname)
                if tier == "rejected":
                    continue
                rec = dict(src_table=name, src_class=klass, src_column=cname,
                           src_col_id=cid, src_width=width, src_offset=off,
                           rows=prof["rows"], non_sentinel_rows=prof["non_sentinel_rows"],
                           sentinel_rows=prof["sentinel_rows"],
                           sentinel_values=prof["sentinel_values"],
                           distinct=prof["distinct"], min=prof["min"], max=prof["max"],
                           target=cand["target"], target_key=cand["target_key"],
                           target_domain_count=cand["target_domain_count"],
                           target_large_share=cand["target_large_share"],
                           uniform_chance=round(cand["uniform_chance"], 12),
                           valid_hits=cand["hits"], hit_rate=cand["hit_rate"],
                           tier=tier, evidence=notes)
                if tier == "verified":
                    d = dmap[(cand["target"], cand["target_key"])]
                    orph, orph_uniq, samples = orphan_detail(vals, width, d.arr)
                    rec.update(orphan_rows=orph, orphan_values=orph_uniq,
                               orphan_samples=samples)
                    if best is None:
                        best = rec
                        edges.append(rec)
                    else:
                        rec["tier"] = "superseded"
                        rec["evidence"] = notes + ["superseded_by:" +
                                                   best["target"] + "." + best["target_key"]]
                        ambiguous.append(rec)
                else:
                    ambiguous.append(rec)
        # ---- reference pairs: adjacent u32 columns and u64 halves
        pair_cands = []
        by_off = {}
        for cid, c in cols.items():
            if c["kind"] == "u" and c["width"] == 4 and "present" not in c:
                by_off.setdefault(c["off"], []).append(c)
        for off in sorted(by_off):
            for c1 in by_off[off]:
                for c2 in by_off.get(off + 4, []):
                    if c2 is not c1:
                        pair_cands.append((c1["name"], c2["name"], c1["values"],
                                           c2["values"], "adjacent_u32"))
        for cid, c in cols.items():
            if c["kind"] == "u" and c["width"] == 8 and "present" not in c:
                v = c["values"]
                pair_cands.append((c["name"] + ".lo32", c["name"] + ".hi32",
                                   v & np.uint64(0xFFFFFFFF), v >> np.uint64(32),
                                   "u64_halves"))
        if name == "basic_people":
            for base in ("nation", "club"):
                a, b = cols.get("basic|%s_ord" % base), cols.get("basic|%s_uid" % base)
                if a is None or b is None:
                    continue
                m = a["present"] & b["present"]
                pair_cands.append((base + "_ref.ordinal", base + "_ref.uid",
                                   a["values"][m], b["values"][m], "declared_pair"))
        for n1, n2, v1, v2, layout in pair_cands:
            pair_edges.extend(test_reference_pair(name, klass, n1, n2, v1, v2,
                                                 layout, domains))
        if verbose:
            print("  %-26s cols=%5d edges=%5d pairs=%3d (%.1fs)" %
                  (name, scanned, len(edges), len(pair_edges), time.perf_counter() - t0))
    return dict(edges=edges, ambiguous=ambiguous, pair_edges=pair_edges,
                columns_scanned=scanned, candidate_tests=tests,
                elapsed_ms=round(1000 * (time.perf_counter() - t0), 1))


def test_reference_pair(src_table, src_class, n1, n2, v1, v2, layout, domains):
    """``(ordinal u32, uid u32)`` pair proof: both halves must land at >= 99 %."""
    if v1.size < MIN_ROWS or v2.size != v1.size:
        return []
    keep = sentinel_mask(v1, 4) & sentinel_mask(v2, 4)
    if int(keep.sum()) < MIN_ROWS:
        return []
    a, b = v1[keep], v2[keep]
    probe = slice(None, None, max(1, a.size // SAMPLE_PROBE))
    out = []
    for d_ord in domains:
        if d_ord.key != "ordinal" or d_ord.klass == src_class:
            continue
        d_uid = None
        for d in domains:
            if d.klass == d_ord.klass and d.key == "uid":
                d_uid = d
                break
        if d_uid is None:
            continue
        if int(a.max()) > d_ord.max or int(b.max()) > d_uid.max:
            continue
        if domain_hits(a[probe], d_ord.arr) < 0.90 * a[probe].size:
            continue
        h_ord, h_uid = in_domain(a, d_ord.arr), in_domain(b, d_uid.arr)
        joint = int(np.count_nonzero(h_ord & h_uid))
        res = dict(src_table=src_table, src_class=src_class, layout=layout,
                   ordinal_column=n1, uid_column=n2, target=d_ord.klass,
                   rows=int(a.size),
                   ordinal_hit_rate=round(int(np.count_nonzero(h_ord)) / a.size, 6),
                   uid_hit_rate=round(int(np.count_nonzero(h_uid)) / a.size, 6),
                   joint_hits=joint, joint_rate=round(joint / a.size, 6))
        if res["joint_rate"] >= PAIR_RATE_MIN:
            bad = a[(~h_ord) | (~h_uid)]
            res["orphan_rows"] = int(a.size - joint)
            res["orphan_samples"] = [int(x) for x in np.unique(bad)[:SAMPLE_ORPHANS]]
            res["tier"] = "verified"
            res["evidence"] = ["pair:" + layout,
                               "joint_rate=%s" % res["joint_rate"]] + \
                              corroboration(n1, d_ord.klass, layout)
            out.append(res)
    return out


# ---------------------------------------------------------------- overlap
def uid_overlap_matrix(classes):
    """Cross-class uid namespace overlap (exact set intersections)."""
    names = sorted(k for k, v in classes.items() if v.get("uid") is not None and v["uid"].size)
    pairs = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            sa, sb = classes[a]["uid"], classes[b]["uid"]
            small, big = (sa, sb) if sa.size <= sb.size else (sb, sa)
            inter = small[in_domain(small, big)]
            if inter.size == 0:
                continue
            pairs.append(dict(a=a, b=b, overlap=int(inter.size),
                              a_count=int(sa.size), b_count=int(sb.size),
                              share_of_a=round(inter.size / sa.size, 6),
                              share_of_b=round(inter.size / sb.size, 6),
                              samples=[int(x) for x in inter[:6]]))
    pairs.sort(key=lambda r: (-r["overlap"], r["a"], r["b"]))
    return dict(class_count=len(names), overlapping_pairs=len(pairs), pairs=pairs)


def row_text_fields(name, want_uid):
    """First textual fields of the row whose identity uid matches (evidence)."""
    try:
        if "/" not in name:
            return []
        arch, tid = name.split("/")
        key = (arch, int(tid))
        spec = specs.get(key)
        if spec is None:
            return []
        data = base.Archive(arch).payload(int(tid))
        nrows = struct.unpack_from("<I", data, 8)[0]
        end = len(data) - base.FOOTER_SIZE
        variants = t133.SELECTORS.get(key)
        if spec.kind == "variable" or variants:
            progs = variants if variants else {0: spec.prog}
            fasts = {f: t133.compile_walk(p) for f, p in progs.items()}
            p = base.HEADER_END
            for _ in range(nrows):
                flag = data[p] if variants else 0
                body = p + 1
                q = fasts[flag](data, body, end)
                _, u, _ = struct.unpack_from("<III", data, q - 12)
                if u == want_uid:
                    fields, _ = t133.sample_walk(progs[flag], data, body, q)
                    return [v for _, _, _, k, v in fields if k == "s" and v][:3]
                p = q
            return []
        reader = base.TableReader(spec, l3)
        reader._fixed_setup()
        fmt, fields = reader._fixed_fmt, reader._fixed_fields
        ui = [i for i, f in enumerate(fields) if f[3] == "uid"]
        if not ui:
            return []
        ui = ui[0]
        p = base.HEADER_END
        mv = memoryview(data)
        for _ in range(nrows):
            vals = fmt.unpack_from(mv, p + 1)
            p += 1 + fmt.size
            if int(vals[ui]) != want_uid:
                continue
            out = []
            for v in vals:
                if isinstance(v, bytes) and len(v) >= 3:
                    txt = "".join(chr(c) if 32 <= c < 127 else "\x00" for c in v)
                    txt = txt.strip("\x00 ")
                    if txt:
                        out.append(txt)
            return out[:3]
        return []
    except Exception:
        return []
