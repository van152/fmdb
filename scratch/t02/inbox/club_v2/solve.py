"""Read-only t02 club table walker. Writes checkpoints only in this directory."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import struct
import sys
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent
SOURCE = Path(r"D:\tmp2b\fm24-db\scripts\t02_club.py")


def load_raw():
    spec = importlib.util.spec_from_file_location("t02_club_source", SOURCE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.load_table()


def try_row(raw: bytes, start: int, ordinal: int, block_width: int):
    p = start
    try:
        a, b, c, d = struct.unpack_from("<4I", raw, p); p += 16
        block = raw[p:p + block_width]
        if len(block) != block_width:
            return None
        p += block_width
        grp = struct.unpack_from("<I", raw, p)[0]; p += 4
        flag1 = raw[p]; p += 1
        n1 = struct.unpack_from("<I", raw, p)[0]; p += 4
        if n1 > 200 or p + n1 > len(raw):
            return None
        full_bytes = raw[p:p + n1]
        full = full_bytes.decode("utf-8"); p += n1
        n2 = struct.unpack_from("<I", raw, p)[0]; p += 4
        if n2 > 200 or p + n2 > len(raw):
            return None
        short_bytes = raw[p:p + n2]
        short = short_bytes.decode("utf-8"); p += n2
        flags = raw[p:p + 3]; p += 3
        o, x, y = struct.unpack_from("<III", raw, p); p += 12
        marker = raw[p]; p += 1
        if o != ordinal or x != y or marker not in (0, 12):
            return None
        return {
            "idx": ordinal, "payload_off": start, "end_off": p,
            "row_len": p - start, "block_width": block_width,
            "db_id": a, "parent_ref": b, "id_dup1": c, "id_dup2": d,
            "id_block_hex": block.hex(), "group": grp, "flag1": flag1,
            "full_name": full, "short_name": short, "flag3_hex": flags.hex(),
            "identity": [o, x, y], "marker": marker,
            "full_len": n1, "short_len": n2,
        }
    except (IndexError, struct.error, UnicodeDecodeError):
        return None


def compact_sample(raw: bytes, row: dict):
    # Hex includes complete row body and boundary marker, supporting independent byte audit.
    return {
        "row": row["idx"], "member_offset": f"0x{row['payload_off']:x}",
        "row_length": row["row_len"], "block_width": row["block_width"],
        "identity_relative_offset": row.get("identity_rel_off"),
        "db_id": row.get("db_id"), "full_name": row.get("full_name"),
        "short_name": row.get("short_name"),
        "bytes_hex": raw[row["payload_off"]:row["end_off"]].hex(" "),
    }


def base_output():
    return {
        "type_id": 3, "entity": "club", "status": "in_progress",
        "variants": [], "row_offset_map": [], "unclosed": [],
    }


def persist(out):
    tmp = OUT / "output.json.tmp"
    tmp.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(OUT / "output.json")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--limit", type=int, help="rows to walk (default: all)")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    raw = load_raw()
    count = struct.unpack_from("<I", raw, 8)[0]
    limit = min(count, args.limit if args.limit is not None else count)
    out = base_output()
    persist(out)
    rows = []
    pos = 14
    width_counts = Counter()
    length_counts = Counter()
    marker_counts = Counter()
    prefix_counts = Counter()
    ambiguous = []
    failed = None
    samples = {"4": [], "5": [], "unparsed_body": []}
    next_checkpoint = 0
    for i in range(limit):
        candidates = [r for w in (4, 5) if (r := try_row(raw, pos, i, w)) is not None]
        if len(candidates) == 2:
            ambiguous.append({"row": i, "member_offset": f"0x{pos:x}", "candidate_widths": [4, 5]})
            failed = {"row": i, "member_offset": f"0x{pos:x}", "reason": "both block widths satisfy row invariants"}
            break
        if len(candidates) == 1:
            row = candidates[0]
            width_key = str(row["block_width"])
            width_counts[width_key] += 1
            end = row["end_off"]
            marker_counts[row["marker"]] += 1
            prefix_counts["standard_fields"] += 1
        else:
            # Preserve framing where the class-specific body is not yet decoded:
            # locate the ordinal|ID|ID suffix and require an exact repeated ID and known trailer byte.
            needle = struct.pack("<I", i)
            stop = min(pos + 8192, len(raw) - 13)
            hits = []
            q = raw.find(needle, pos + 20, stop)
            while q >= 0:
                if q + 13 <= len(raw):
                    ordinal, id1, id2 = struct.unpack_from("<III", raw, q)
                    marker = raw[q + 12]
                    if ordinal == i and id1 == id2 and marker in (0, 12):
                        hits.append((q, marker, id1))
                q = raw.find(needle, q + 1, stop)
            if len(hits) != 1:
                failed = {"row": i, "member_offset": f"0x{pos:x}",
                          "reason": "identity-suffix framing not unique after schema parse failure",
                          "identity_hits": [{"off": f"0x{x:x}", "marker": m} for x, m, _ in hits[:8]],
                          "probe_hex": raw[pos:pos + 80].hex(" ")}
                break
            q, marker, idv = hits[0]
            end = q + 13
            row = {"idx": i, "payload_off": pos, "end_off": end, "row_len": end - pos,
                   "block_width": None, "identity_rel_off": q - pos, "marker": marker,
                   "identity": [i, idv, idv], "full_name": None, "short_name": None}
            width_counts["unparsed_body"] += 1
            marker_counts[marker] += 1
            prefix_counts[str(q - pos)] += 1
        rows.append(row)
        length_counts[row["row_len"]] += 1
        key = str(row["block_width"]) if row["block_width"] is not None else "unparsed_body"
        if len(samples[key]) < 3:
            samples[key].append(compact_sample(raw, row))
        pos = end
        if i + 1 >= next_checkpoint:
            out.update({
                "status": "in_progress", "count": count, "walked_rows": len(rows),
                "next_member_offset": f"0x{pos:x}",
                "partial_width_counts": {str(k): v for k, v in sorted(width_counts.items())},
                "partial_row_length_counts": {str(k): v for k, v in sorted(length_counts.items())},
                "unclosed": ([failed] if failed else []),
            })
            persist(out)
            next_checkpoint += 1000
    if limit == count and not failed:
        footer = raw[-8:]
        end_rows = len(raw) - 8
        footer_ok = pos == end_rows
        out.update({
            "status": "closed" if footer_ok and not ambiguous and not width_counts.get("unparsed_body", 0) else "in_progress",
            "count": count, "walked_rows": len(rows),
            "member_length": len(raw), "member_sha256": hashlib.sha256(raw).hexdigest(),
            "row_body_end_member_offset": f"0x{pos:x}",
            "footer_offset": f"0x{end_rows:x}", "footer_hex": footer.hex(" "),
            "footer_exact": footer_ok,
            "width_counts": {str(k): v for k, v in sorted(width_counts.items())},
            "row_length_distribution": {str(k): v for k, v in sorted(length_counts.items())},
            "marker_counts": {str(k): v for k, v in sorted(marker_counts.items())},
            "identity_prefix_length_counts": {str(k): v for k, v in sorted(prefix_counts.items())},
            "variant_samples": {str(k): v for k, v in samples.items()},
            "ambiguous_rows": ambiguous,
            "unclosed": ([] if footer_ok and not ambiguous and not width_counts.get("unparsed_body", 0) else
                         ([{"reason": f"{width_counts.get('unparsed_body', 0)} row bodies are only identity-framed; semantic layout remains open"}]
                          if footer_ok and not ambiguous else
                          [{"reason": "row/footer boundary mismatch", "parsed_end": f"0x{pos:x}", "expected": f"0x{end_rows:x}"}])), 
        })
    else:
        out.update({
            "status": "in_progress", "count": count, "walked_rows": len(rows),
            "member_length": len(raw), "next_member_offset": f"0x{pos:x}",
            "partial_width_counts": {str(k): v for k, v in sorted(width_counts.items())},
            "partial_row_length_counts": {str(k): v for k, v in sorted(length_counts.items())},
            "partial_marker_counts": {str(k): v for k, v in sorted(marker_counts.items())},
            "variant_samples": {str(k): v for k, v in samples.items()},
            "ambiguous_rows": ambiguous, "unclosed": [failed] if failed else [],
        })
    persist(out)
    print(f"walked_rows={len(rows)}/{count}; widths={dict(width_counts)}; length_classes={len(length_counts)}; failed={failed}")
    print(f"next_offset=0x{pos:x}; footer_exact={out.get('footer_exact', False)}; output={OUT / 'output.json'}")
    if args.selftest:
        assert count == 84259, count
        assert len(rows) > 69705, len(rows)
        assert not failed, failed
        assert out.get("footer_exact") is True, out.get("footer_exact")
        assert sum(width_counts.values()) == count
        print("selftest OK")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
