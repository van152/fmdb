# ---------------------------------------------------------------- selftest
def selftest(full=False):
    ok = True

    def check(name, cond, detail=""):
        nonlocal ok
        ok = ok and bool(cond)
        print("[%s] %s %s" % ("PASS" if cond else "FAIL", name, detail))

    # ---- 1. pure logic: sentinels, domain stats, specificity guards
    vals = np.array([1, 2, 3, 0xFFFFFFFF, 0xFFFFFFFF], dtype=np.uint64)
    prof = column_profile(vals, 4)
    check("sentinel_excluded", prof["non_sentinel_rows"] == 3 and prof["min"] == 1,
          str(prof["non_sentinel_rows"]))

    enum_col = np.arange(1000, dtype=np.uint64) % 8          # 0..7 enum, 1000 rows
    dom_cont = Domain("continent", "ordinal", np.arange(7, dtype=np.uint64))
    prof_e = column_profile(enum_col, 4)
    cand = dict(target="continent", target_key="ordinal", target_domain_count=7,
                target_large_share=0.0, uniform_chance=7 / 2 ** 32, support_coverage=1.0,
                hits=1000, rows=1000, hit_rate=1.0)
    tier, notes = classify(cand, prof_e, "col_0")
    check("enum_guard_blocks_continent", tier == "ambiguous", str(notes))

    dense_ord_col = (np.arange(5000, dtype=np.uint64) % 251)  # nation-like ordinals
    prof_d = column_profile(dense_ord_col, 4)
    cand_d = dict(target="nation", target_key="ordinal", target_domain_count=251,
                  target_large_share=0.0, uniform_chance=5.8e-08, support_coverage=1.0,
                  hits=5000, rows=5000, hit_rate=1.0)
    tier_d, _ = classify(cand_d, prof_d, "col_4")
    check("dense_ordinal_not_promoted", tier_d == "ambiguous")

    check("name_token_corroborates",
          classify(dict(cand_d, target="nation"), prof_d, "Cnat")[0] == "code_corroborated")

    # statistical promotion of a sparse uid column
    uid_col = np.array([4_315_7326, 200_009_7018, 77_001_234, 43_157_326] * 20,
                       dtype=np.uint64)
    prof_u = column_profile(uid_col, 4)
    cand_u = dict(target="club", target_key="uid", target_domain_count=84259,
                  target_large_share=0.9, uniform_chance=84259 / 2 ** 32,
                  support_coverage=1e-6, hits=80, rows=80, hit_rate=1.0)
    check("sparse_uid_promoted", classify(cand_u, prof_u, "col_9")[0] == "statistical")
    cand_u2 = dict(cand_u, support_coverage=1.0)
    check("uid_coverage_guard", classify(cand_u2, prof_u, "col_9")[0] == "ambiguous")
    cand_u3 = dict(cand_u, hit_rate=0.95)
    check("hit_rate_floor", classify(cand_u3, prof_u, "col_9")[0] == "rejected")

    # ---- 2. real data invariants
    nat = ids_of(("server", 10))
    check("nation_ordinal_dense_0..250",
          nat["ordinal"].size == 251 and int(nat["ordinal"].max()) == 250
          and bool((nat["ordinal"] == np.arange(251, dtype=np.uint64)).all()))
    club = ids_of(("server", 3))
    check("club_uid_unique", np.unique(club["uid"]).size == club["uid"].size)
    team = ids_of(("server", 24))
    inter = np.intersect1d(club["uid"], team["uid"]).size
    check("club_uid_subset_of_team_uid", inter == club["uid"].size,
          "%d/%d" % (inter, club["uid"].size))

    # ---- 3. known edges reproduced from scratch
    cc, _ = decode_club_links()
    club_uid_vals = cc["clublinks|club_uid"]["values"]
    check("club_links.club_uid -> club key",
          domain_hits(club_uid_vals, club["ordinal"]) == club_uid_vals.size
          or domain_hits(club_uid_vals, club["uid"]) == club_uid_vals.size)

    bp, _ = decode_basic_people()
    n_ord, n_uid = bp["basic|nation_ord"], bp["basic|nation_uid"]
    mask = n_ord["present"] & n_uid["present"]
    o, u = n_ord["values"][mask], n_uid["values"][mask]
    joint = (in_domain(o, nat["ordinal"]) & in_domain(u, nat["uid"]))
    check("basic_people.nation_ref pair 100%", int(joint.sum()) == o.size,
          "%d/%d" % (int(joint.sum()), o.size))
    check("basic_people.uid count", bp["basic|uid"]["values"].size == 658011,
          str(bp["basic|uid"]["values"].size))

    nt = decode_name_table(2)[0]
    check("name_table string_ordinal == row index",
          bool((nt["name2|string_ordinal"]["values"] == nt["name2|ordinal"]["values"]).all()))

    # ---- 4. uid 676 collision (t143 finding) reproduced
    stad = ids_of(("server", 21))
    coll = [k for k, arr in (("club", club["uid"]), ("stadium", stad["uid"]))
            if bool((arr == 676).any())]
    check("uid676_in_club_and_stadium", len(coll) == 2, str(coll))

    # ---- 5. artifacts
    if not full and not MASTER.exists():
        print("[SKIP] artifacts not built yet (run the pipeline first)")
    else:
        master = load_json(MASTER)
        check("master_schema", master.get("schema_id") == "fm24.t142.fk_graph_master")
        check("master_has_edges", master["health"]["verified_edges"] > 0,
              str(master["health"]["verified_edges"]))
        check("master_has_pair_proofs", master["health"]["verified_pair_proofs"] > 0)
        check("master_identity_registry_covers_all",
              len(master["identity_registry"]) == 84,
              str(len(master["identity_registry"])))
        check("master_rows_total", master["health"]["rows_decoded"] == 4387917,
              str(master["health"]["rows_decoded"]))
        for d in master["edges_verified"]:
            if d["hit_rate"] < HIT_RATE_MIN or not d.get("verified", True):
                check("edge_threshold_invariant", False, str(d)[:80])
                break
        else:
            check("edge_threshold_invariant", True)
        check("report_written", (OUT / "REPORT.md").is_file())
        check("done_written", (OUT / "DONE.md").is_file())
    print("--- t142 selftest: %s ---" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def ids_of(key):
    """ordinal/uid arrays of one numbered table, decoding it directly."""
    cols, meta = decode_table(key) if not (CACHE / ("%s_%s.json" % key)).is_file() \
        else load_columns(table_key(*key))
    out = {}
    for c in cols.values():
        if c["kind"] in ("ord", "uid"):
            out[c["kind"]] = c["values"]
    return out


# ---------------------------------------------------------------- CLI
def write_artifacts(master):
    dump_json(MASTER, master)
    (OUT / "REPORT.md").write_text(render_report(master), encoding="utf-8")
    (OUT / "DONE.md").write_text(render_done(master), encoding="utf-8")


def print_summary(master):
    h = master["health"]
    print("\n=== t142 FM24 FK graph & referential integrity audit ===")
    print("tables audited          : %d (numbered %d + special %d)"
          % (h["tables_audited"], h["numbered_tables"], h["special_tables"]))
    print("rows decoded            : %s" % f"{h['rows_decoded']:,}")
    print("columns scanned         : %s of %s inventoried"
          % (f"{h['columns_scanned']:,}", f"{h['columns_inventoried']:,}"))
    print("verified FK edges       : %d  (code %d + statistical %d)"
          % (h["verified_edges"], h["verified_code_corroborated"], h["verified_statistical"]))
    print("reference pair proofs   : %d" % h["verified_pair_proofs"])
    print("anonymous col_N FKs     : %d" % h["anonymous_col_edges"])
    print("orphan rows             : %s  (edges with orphans: %d)"
          % (f"{h['orphan_rows_column_edges'] + h['orphan_rows_pair_edges']:,}",
             h["edges_with_orphans"]))
    print("ambiguous candidates    : %s" % f"{h['ambiguous_candidates']:,}")
    print("uid overlap class pairs : %d   shared namespaces: %d"
          % (h["uid_overlapping_class_pairs"], h["shared_key_namespaces"]))
    print("deliverables:")
    for f in ("fk_graph_master.json", "REPORT.md", "DONE.md", "stage1_columns.json",
              "stage2_domains.json", "stage3_edges.json"):
        p = OUT / f
        print("  %-24s %s" % (f, f"{p.stat().st_size:,} B" if p.is_file() else "MISSING"))


def cmd_columns(arch, tid):
    key = (arch, int(tid))
    cols, meta = decode_table(key)
    print(json.dumps(meta, ensure_ascii=False, indent=1))
    rows = []
    for cid, c in cols.items():
        mask = c.get("present")
        vals = c["values"][mask] if mask is not None else c["values"]
        prof = column_profile(vals, c["width"])
        rows.append((c["name"], c["kind"], c["width"], c["off"], prof["non_sentinel_rows"],
                     prof["distinct"], prof["min"], prof["max"]))
    print("%-18s %-6s %-4s %-6s %9s %8s %14s %14s" %
          ("name", "kind", "w", "off", "rows", "distinct", "min", "max"))
    for r in sorted(rows, key=lambda r: (r[3] is None, r[3])):
        print("%-18s %-6s %-4s %-6s %9s %8s %14s %14s" % r)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true", help="run the self test")
    ap.add_argument("--stage", choices=["decode", "domains", "edges", "report", "all"],
                    default="all")
    ap.add_argument("--columns", nargs=2, metavar=("ARCHIVE", "TID"),
                    help="dump decoded column inventory of one table")
    ap.add_argument("--force-decode", action="store_true", help="ignore the column cache")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    if args.columns:
        return cmd_columns(*args.columns)
    if args.selftest:
        return selftest()

    OUT.mkdir(parents=True, exist_ok=True)
    if args.stage in ("decode", "all"):
        print("[stage 1] decoding every table into the column cache")
        build_cache(force=args.force_decode)
    if args.stage in ("domains", "all"):
        print("[stage 2] identity domains")
        build_domains()
    if args.stage in ("edges", "all"):
        print("[stage 3] foreign-key audit")
        _, _, classes = build_domains()
        scan = scan_edges(classes, verbose=not args.quiet)
        dump_json(STAGE3, scan)
    if args.stage in ("report", "all"):
        print("[stage 4] assembly + report")
        registry, _, classes = build_domains()
        scan = load_json(STAGE3)
        master = assemble(registry, classes, scan, l3_fourcc_index(), c_slot_index())
        write_artifacts(master)
        print_summary(master)
    return 0


if __name__ == "__main__":
    sys.exit(main())
