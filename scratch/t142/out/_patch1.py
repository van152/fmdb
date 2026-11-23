import pathlib

p = pathlib.Path('scripts/t142_fk_graph_audit.py')
s = p.read_text(encoding='utf-8')

# 1) name tokens
s = s.replace('    "TEAM": ("team", "tfte", "ttea"),',
              '    "TEAM": ("team", "tfte", "ttea", "otht", "t24"),')
s = s.replace('    "NATIONAL_TEAM": ("ntte", "ntmt"),',
              '    "NATIONAL_TEAM": ("ntte", "ntmt", "natt"),')

# 2) u64 columns: only the low half is an independent reference
old_u64 = '''            elif k == "u" and w == 8:
                v = c["values"]
                test_cols.append((cid + "#lo32", c["name"] + ".lo32", 4,
                                  v & np.uint64(0xFFFFFFFF), mask, c["off"]))
                test_cols.append((cid + "#hi32", c["name"] + ".hi32", 4,
                                  v >> np.uint64(32), mask, c["off"]))'''
new_u64 = '''            elif k == "u" and w == 8:
                # 8-byte references are (uid u32, dbid u32): only the low half is
                # ever an independent reference target.
                v = c["values"]
                test_cols.append((cid + "#lo32", c["name"] + ".lo32", 4,
                                  v & np.uint64(0xFFFFFFFF), mask, c["off"]))'''
assert old_u64 in s
s = s.replace(old_u64, new_u64)

# 3) new test_reference_pair
start = s.index('def test_reference_pair(')
end = s.index('# ---------------------------------------------------------------- overlap')
new_pair = '''def test_reference_pair(src_table, src_class, n1, n2, v1, v2, layout, domains):
    """Reference-pair proof for the two layouts proven empirically.

    ``ordinal_uid``  low u32 = target ``ordinal``, high u32 = target ``uid``
                     (basic_people ``nation_ref`` / ``club_ref``);
    ``uid_dbid``     low u32 = target ``uid``, high u32 is the companion
                     ``dbid`` (== uid for same-database objects, 0 for
                     cross-database person references).
    """
    if v1.size < MIN_ROWS or v2.size != v1.size:
        return []
    keep = sentinel_mask(v1, 4) & sentinel_mask(v2, 4)
    if int(keep.sum()) < MIN_ROWS:
        return []
    a, b = v1[keep], v2[keep]
    out = []
    uids = {d.klass: d for d in domains if d.key == "uid"}
    for d in domains:
        if d.klass == src_class:
            continue
        d_uid = uids.get(d.klass)
        if d_uid is None:
            continue
        if layout == "ordinal_uid":
            if d.key != "ordinal":
                continue
            if int(a.max()) > d.max or int(b.max()) > d_uid.max:
                continue
            h_a = in_domain(a, d.arr)
            h_b = in_domain(b, d_uid.arr)
            key_a, key_b = "ordinal", "uid"
        elif layout == "uid_dbid":
            if d.key != "uid":
                continue
            if int(a.max()) > d_uid.max:
                continue
            h_a = in_domain(a, d_uid.arr)
            h_b = (b == a) | (b == np.uint64(0))
            key_a, key_b = "uid", "dbid"
        else:
            continue
        joint = h_a & h_b
        hits = int(np.count_nonzero(joint))
        if hits < PAIR_RATE_MIN * a.size:
            continue
        bad = a[~joint]
        res = dict(src_table=src_table, src_class=src_class, layout=layout,
                   low_column=n1, high_column=n2, target=d.klass,
                   low_key=key_a, high_field=key_b, rows=int(a.size),
                   low_hit_rate=round(int(np.count_nonzero(h_a)) / a.size, 6),
                   high_hit_rate=round(int(np.count_nonzero(h_b)) / b.size, 6),
                   joint_hits=hits, joint_rate=round(hits / a.size, 6),
                   orphan_rows=int(a.size - hits),
                   orphan_samples=[int(x) for x in np.unique(bad)[:SAMPLE_ORPHANS]],
                   tier="pair_proved", verified=True,
                   evidence=["pair:" + layout, "joint_rate=%s" % round(hits / a.size, 6)]
                   + corroboration(n1, d.klass, layout))
        out.append(res)
    return out


'''
s = s[:start] + new_pair + s[end:]

# 4) pair candidate construction: line based replacement
lines = s.split('\n')
i0 = next(i for i, ln in enumerate(lines) if ln.strip() == 'for off in sorted(by_off):')
i1 = next(i for i, ln in enumerate(lines) if ln.strip() == 'if verbose:')
block = '''        for off in sorted(by_off):
            for c1 in by_off[off]:
                for c2 in by_off.get(off + 4, []):
                    if c2 is not c1:
                        for layout in ("uid_dbid", "ordinal_uid"):
                            pair_cands.append((c1["name"], c2["name"], c1["values"],
                                               c2["values"], layout))
        for cid, c in cols.items():
            if c["kind"] == "u" and c["width"] == 8 and "present" not in c:
                v = c["values"]
                pair_cands.append((c["name"] + ".lo32", c["name"] + ".hi32",
                                   v & np.uint64(0xFFFFFFFF), v >> np.uint64(32),
                                   "uid_dbid"))
        if name == "basic_people":
            for base in ("nation", "club"):
                a, b = cols.get("basic|%s_ord" % base), cols.get("basic|%s_uid" % base)
                if a is None or b is None:
                    continue
                m = a["present"] & b["present"]
                pair_cands.append((base + "_ref.ordinal", base + "_ref.uid",
                                   a["values"][m], b["values"][m], "ordinal_uid"))
        seen_pairs = set()
        for n1, n2, v1, v2, layout in pair_cands:
            for got in test_reference_pair(name, klass, n1, n2, v1, v2, layout, domains):
                sig = (got["src_table"], got["low_column"], got["high_column"],
                       got["target"], got["layout"])
                if sig in seen_pairs:
                    continue
                seen_pairs.add(sig)
                pair_edges.append(got)
'''.rstrip('\n').split('\n')
lines = lines[:i0] + block + lines[i1:]
s = '\n'.join(lines)

p.write_text(s, encoding='utf-8')
print('patched ok')
