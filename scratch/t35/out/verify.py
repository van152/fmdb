#!/usr/bin/env python3
"""Independent t35 verifier: source hashes, archive frame, rows, and candidate scan."""
from __future__ import annotations

import hashlib
import json
import os
import runpy
import struct
import sys
from collections import Counter
from pathlib import Path

# Starting from parents[2] keeps the requested in-workspace ancestry; for this
# nested out/ location the repository marker is one directory above scratch.
ROOT = Path(__file__).resolve().parents[2]
if not (ROOT / "AGENTS.md").is_file():
    ROOT = ROOT.parent
OUT = Path(__file__).resolve().parent
DISCOVERY = OUT / "cafl_cvfl_discovery.json"
PROFILE = OUT / "profiles/parent_table3_context.json"
T14 = ROOT / "scratch/t14/out/census.json"
STAGE2 = ROOT / "reports/stage2_table_identity.json"
MASTER = ROOT / "evidence/fm24/reports/editor_schema/master.json"
MANIFEST = ROOT / "evidence/MANIFEST.json"
ZSTD_MAGIC = bytes.fromhex("28 b5 2f fd")
TAD_HEADER = bytes.fromhex("03 01 74 61 64 2e f1 0d")
TERMS = (
    "AFFILIAT", "CLUB_LINK", "LINKED_CLUB", "CLUB_RELATION", "RELATED_CLUB",
    "FEEDER_CLUB", "FARM_CLUB", "SATELLITE_CLUB", "SISTER_CLUB",
    "SUBSIDIARY_CLUB", "PARTNER_CLUB", "AFFILIATE_CLUB",
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def selected_payload(archive: str, tid: int, expected_sha: str) -> bytes:
    os.environ["FM24_DB_DIR"] = str(ROOT / "scratch/data")
    module = runpy.run_path(str(ROOT / "scripts/fm24_dump.py"))
    codec = module["_reader"]()
    path = ROOT / "scratch/data" / f"{archive}_db.dat"
    entries = codec["list_tables"](path, path.name)
    entry = codec["_resolve_table"](tid, entries, path.name)
    packed = path.read_bytes()
    base = int(entry["offset"])
    hits = [off for off in range(base, min(base + 256, len(packed) - 3)) if packed[off:off + 4] == ZSTD_MAGIC]
    valid = []
    for off in hits:
        try:
            raw = codec["_stream_decompress"](packed[off:], 256 * 1024 * 1024)
        except Exception:
            continue
        if raw.startswith(TAD_HEADER) and digest(raw) == expected_sha:
            valid.append(raw)
    if len(valid) != 1:
        raise ValueError(f"{archive} table_{tid}: expected one header/hash-matched frame, got {len(valid)}")
    return valid[0]


def parse_row(raw: bytes, start: int, ordinal: int, width: int):
    p = start
    try:
        lanes = struct.unpack_from("<4I", raw, p)
        p += 16
        block = raw[p:p + width]
        if len(block) != width:
            return None
        p += width
        group = struct.unpack_from("<I", raw, p)[0]
        p += 4
        flag = raw[p]
        p += 1
        full_n = struct.unpack_from("<I", raw, p)[0]
        p += 4
        if full_n > 200 or p + full_n > len(raw):
            return None
        raw[p:p + full_n].decode("utf-8")
        p += full_n
        short_n = struct.unpack_from("<I", raw, p)[0]
        p += 4
        if short_n > 200 or p + short_n > len(raw):
            return None
        raw[p:p + short_n].decode("utf-8")
        p += short_n
        if p + 3 + 13 > len(raw):
            return None
        p += 3
        stored, key_a, key_b = struct.unpack_from("<III", raw, p)
        p += 12
        marker = raw[p]
        p += 1
        if stored != ordinal or key_a != key_b or marker not in (0, 12):
            return None
        return {"ordinal": ordinal, "start": start, "end": p, "length": p - start,
                "block_width": width, "lanes": lanes, "block": block, "group": group,
                "flag": flag, "marker": marker, "identity_key": key_a}
    except (IndexError, struct.error, UnicodeDecodeError):
        return None


def walk(raw: bytes) -> dict:
    if not raw.startswith(TAD_HEADER) or len(raw) < 22:
        raise ValueError("table_3 header invalid")
    n = struct.unpack_from("<I", raw, 8)[0]
    if n != 84259:
        raise ValueError(f"table_3 count changed: {n}")
    pos = 14
    widths, lengths, markers = Counter(), Counter(), Counter()
    lanes = [[], [], [], []]
    bit_set = [[0] * 8 for _ in range(5)]
    compact = []
    samples = {}
    for ordinal in range(n):
        candidates = [r for w in (4, 5) if (r := parse_row(raw, pos, ordinal, w)) is not None]
        if len(candidates) > 1:
            raise ValueError(f"ambiguous row {ordinal}")
        if candidates:
            row = candidates[0]
            widths[str(row["block_width"])] += 1
            for lane, value in zip(lanes, row["lanes"]):
                lane.append(value)
            if row["block_width"] == 5:
                for j, value in enumerate(row["block"]):
                    for bit in range(8):
                        bit_set[j][bit] += (value >> bit) & 1
        else:
            needle = struct.pack("<I", ordinal)
            q = raw.find(needle, pos + 20, min(pos + 8192, len(raw) - 13))
            hits = []
            while q >= 0:
                if q + 13 <= len(raw):
                    stored, a, b = struct.unpack_from("<III", raw, q)
                    mark = raw[q + 12]
                    if stored == ordinal and a == b and mark in (0, 12):
                        hits.append((q, a, mark))
                q = raw.find(needle, q + 1, min(pos + 8192, len(raw) - 13))
            if len(hits) != 1:
                raise ValueError(f"compact row {ordinal}: expected unique identity, got {len(hits)}")
            q, key, mark = hits[0]
            row = {"ordinal": ordinal, "start": pos, "end": q + 13,
                   "length": q + 13 - pos, "block_width": None,
                   "identity_key": key, "marker": mark}
            compact.append(ordinal)
            widths["identity_only"] += 1
        lengths[row["length"]] += 1
        markers[str(row["marker"])] += 1
        if ordinal in (0, 69705, 69706, 69707, 69708, 69709, n - 1):
            samples[str(ordinal)] = {"row_offset": row["start"], "row_length": row["length"],
                                     "block_width": row["block_width"], "identity_key": row["identity_key"],
                                     "marker": row["marker"]}
        pos = row["end"]
    footer = len(raw) - 8
    if pos != footer:
        raise ValueError(f"closure mismatch: rows end {pos}, footer at {footer}")
    bit_profile = []
    standard5 = widths.get("5", 0)
    for byte_index, counts in enumerate(bit_set, start=16):
        bit_profile.append({
            "row_relative_byte_offset": byte_index, "rows": standard5,
            "bits": [{"bit": bit, "set_count": counts[bit], "clear_count": standard5 - counts[bit]} for bit in range(8)],
        })
    return {
        "count": n, "payload_bytes": len(raw), "payload_sha256": digest(raw),
        "row_body_bytes": pos - 14, "closure_equation": f"14 + {pos - 14} + 8 = {len(raw)}",
        "row_width_counts": dict(widths),
        "row_length_distribution": {str(k): v for k, v in sorted(lengths.items())},
        "row_length_min": min(lengths), "row_length_max": max(lengths),
        "distinct_row_lengths": len(lengths), "marker_counts": dict(markers),
        "compact_identity_only_rows": compact,
        "raw_prefix_u32_lanes": [
            {"raw_u32_lane": i, "rows": len(v), "unique_values": len(set(v)),
             "minimum": min(v), "maximum": max(v),
             "values_in_club_ordinal_domain_0_84259": sum(0 <= x < 84259 for x in v),
             "sample_first_12": v[:12]} for i, v in enumerate(lanes)
        ],
        "aggregate5_byte_bit_counts": bit_profile, "row_samples": samples,
    }


def semantic_candidate_count(census: dict, stage2: dict) -> tuple[int, int]:
    stage_types = {row.get("table_type") for row in stage2.get("rows", [])}
    hits = []
    for row in census.get("tables", []):
        classes = [row.get("primary_class") or ""] + [v.get("class", "") for v in row.get("vtables", [])]
        text = " ".join(classes).upper()
        matched = [term for term in TERMS if term in text]
        if matched:
            hits.append((row.get("table_type"), matched))
    return len(hits), len(stage_types)


def main() -> int:
    try:
        discovery = load_json(DISCOVERY)
        context = load_json(PROFILE)
        source_hashes = discovery["provenance"]["sha256"]
        for rel, expected in source_hashes.items():
            path = ROOT / rel
            if not path.is_file() or digest(path.read_bytes()) != expected:
                raise ValueError(f"source hash mismatch: {rel}")
        manifest = load_json(MANIFEST)
        master_entry = next(f for f in manifest["files"] if f["path"] == "evidence/fm24/reports/editor_schema/master.json")
        if master_entry["sha256"] != digest(MASTER.read_bytes()):
            raise ValueError("master.json does not match evidence/MANIFEST.json")
        c = load_json(T14)
        s = load_json(STAGE2)
        if len(c["tables"]) != 74 or len(s["rows"]) != 45:
            raise ValueError("t14/stage2 census size changed")
        candidates, stage_types = semantic_candidate_count(c, s)
        if candidates != 0 or stage_types != 45 or discovery["semantic_candidate_scan"]["candidate_count"] != 0:
            raise ValueError(f"semantic scan mismatch: candidates={candidates}, stage2_types={stage_types}")
        client_meta = context["archives"]["client"]["selected_frame"]
        raw = selected_payload("client", 3, client_meta["payload_sha256"])
        actual = walk(raw)
        expected = context["profiles"]["client"]
        for key in ("count", "payload_bytes", "payload_sha256", "row_body_bytes", "closure_equation",
                    "row_width_counts", "row_length_distribution", "row_length_min", "row_length_max",
                    "distinct_row_lengths", "marker_counts", "compact_identity_only_rows",
                    "raw_prefix_u32_lanes", "aggregate5_byte_bit_counts"):
            if actual[key] != expected[key]:
                raise ValueError(f"profile mismatch in {key}")
        if any(record["item_field_candidates"] for record in discovery["copy_ready"]):
            raise ValueError("unexpected item column candidate was promoted")
        if actual["count"] != 84259 or actual["row_width_counts"] != {"5": 84256, "identity_only": 3}:
            raise ValueError("expected all-row parent profile did not reproduce")
    except Exception as exc:
        print(f"FAIL {type(exc).__name__}: {exc}")
        return 1
    print("PASS: frozen source hashes and master/MANIFEST binding")
    print("PASS: 74 t14 types + 45 stage2 rows; affiliation/link semantic candidates = 0")
    print(f"PASS: client table_3 rows={actual['count']} lengths={actual['distinct_row_lengths']} closure={actual['closure_equation']}")
    print("PASS: row-length, marker, raw lane and per-bit statistics independently reproduced")
    print("PASS: Cafl/Cvfl copy-ready entries remain unknown with no item-column promotions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
