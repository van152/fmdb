import pathlib

p = pathlib.Path('scripts/t142_fk_graph_audit.py')
s = p.read_text(encoding='utf-8')

old = '''        if e.get("mask"):
            bits = np.unpackbits(arrays_cache[e["mask"]])[:meta["rows"]].astype(bool)
            if int(bits.sum()) == int(c["values"].size) and bits.size == int(c["values"].size):
                pass                      # redundant mask: column covers every row
            elif int(bits.sum()) != int(c["values"].size):
                raise ValueError("%s: mask/hits mismatch for %s" % (name, e["id"]))
            else:
                c["present"] = bits'''
new = '''        if e.get("mask"):
            bits = np.unpackbits(arrays_cache[e["mask"]])[:meta["rows"]].astype(bool)
            hits = int(bits.sum())
            n = int(c["values"].size)
            if n == meta["rows"] and hits < meta["rows"]:
                # placeholder layout: one value per row, missing rows flagged
                c["present"] = bits
            elif n == hits:
                # already-filtered layout: the mask only records *which* rows
                c["row_mask"] = bits
            else:
                raise ValueError("%s: mask/value mismatch for %s (%d vs %d)"
                                 % (name, e["id"], hits, n))'''
assert old in s
s = s.replace(old, new)

old2 = '''        by_off = {}
        for cid, c in cols.items():
            if c["kind"] == "u" and c["width"] == 4 and "present" not in c:
                by_off.setdefault(c["off"], []).append(c)'''
new2 = '''        by_off = {}
        for cid, c in cols.items():
            if c["kind"] == "u" and c["width"] == 4 and "row_mask" not in c \\
                    and "present" not in c:
                by_off.setdefault(c["off"], []).append(c)'''
assert old2 in s
s = s.replace(old2, new2)

old3 = '''            if c["kind"] == "u" and c["width"] == 8 and "present" not in c:'''
new3 = '''            if c["kind"] == "u" and c["width"] == 8 and "present" not in c \\
                    and "row_mask" not in c:'''
assert old3 in s
s = s.replace(old3, new3)

p.write_text(s, encoding='utf-8')
print('ok')
